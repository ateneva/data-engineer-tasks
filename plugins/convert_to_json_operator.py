from typing import Sequence
import json
import logging
import os
import tempfile
import uuid

from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.hooks.base_hook import BaseHook
from airflow.models import BaseOperator

from partner_webshop_categories import PartnerWebshopCategories
from partner_webshop_channels import PartnerWebshopChannels
from partner_webshop_customer_groups import PartnerWebshopCustomerGroups
from partner_webshop_customers import PartnerWebshopCustomers
from partner_webshop_discount_codes import PartnerWebshopDiscountCodes
from partner_webshop_orders import PartnerWebshopOrders
from partner_webshop_product_discounts import PartnerWebshopProductDiscounts
from partner_webshop_product_types import PartnerWebshopProductTypes
from partner_webshop_products import PartnerWebshopProducts

API_OBJECTS = [
        'customers',
        'customer_groups',
        'channels',
        'orders',
        'discount_codes',
        'categories',
        'product_discounts',
        'product_types',
        'products'
    ]

class PartnerWebshopToGCSOperator(BaseOperator):
    template_fields: Sequence[str] = ("last_ingested_date", "ingestion_end_date", "gcs_prefix")
    def __init__(
            self,
            last_ingested_date: str,
            ingestion_end_date: str,
            api_conn_id: str,
            gcp_conn_id: str,
            gcs_bucket: str,
            gcs_prefix: str,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.last_ingested_date=last_ingested_date
        self.ingestion_end_date=ingestion_end_date
        self.api_conn_id=api_conn_id
        self.gcp_conn_id=gcp_conn_id
        self.gcs_bucket=gcs_bucket
        self.gcs_prefix=gcs_prefix

    def setup_api_client(self):
        from commercetools import Client
        """
            Authenticates to the API; Each arg is a tuple reprsenting element of the needed credentials
        """
        connection_details = BaseHook.get_connection(self.api_conn_id)
        api_url = connection_details.host
        
        connection_extra = json.loads(connection_details.extra)
        
        project_key = connection_extra["project_key"]
        client_id = connection_extra["client_id"]
        client_secret = connection_extra["client_secret"]
        scope = connection_extra["scope"]
        token_url = connection_extra["token_url"]
        
        client = Client(
            project_key=project_key,
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            url=api_url,
            token_url=token_url
        )
        return client

    def write_to_gcs_file(self, api_data,file_name):
        """
            Writes the data retrieved through the API library call to new line delimitted json and uploads to gcs
        Args:
            Returns a list of dicts with the columns to be retrieved
        """

        unique_file_name = f'{file_name}_{uuid.uuid4()}.json'
        temp_file_name = f'{tempfile.mkdtemp()}/{unique_file_name}'

        with open(temp_file_name, mode="w") as f:
            api_data = "\n".join([json.dumps(record, ensure_ascii=False) for record in api_data])
            f.write(api_data)

        logging.info(f"Uploading {temp_file_name} to GCS to {self.gcs_bucket}/{self.gcs_prefix}")
        hook = GCSHook(gcp_conn_id=self.gcp_conn_id)
        hook.upload(
            bucket_name=self.gcs_bucket,
            object_name=f"{self.gcs_prefix}/{unique_file_name}",
            filename=os.path.abspath(temp_file_name)
        )

    def execute(self, context):
        """
            Loops through all API objects and writes the processed data to a `json.gz` in gcs
        """
        client = self.setup_api_client()
        for obj in API_OBJECTS:
            fetch_data = getattr(client, obj).query(
                sort="id asc",
                where=[f'lastModifiedAt > "{self.last_ingested_date}"', f'lastModifiedAt < "{self.ingestion_end_date}"']
            )
            # check if there are any new records per object and save them to a file
            if fetch_data.total != 0:

                # the API has a limit of retrieval of 500; ensure ALL records are retrieved even if they exceed that number
                iterations = int(fetch_data.total/500) + 1

                for num_i in range(iterations):
                    get_all_records = getattr(client, obj).query(
                        limit=500,
                        offset=num_i * 500,
                        sort="id asc",
                        where=[f'lastModifiedAt > "{self.last_ingested_date}"',
                            f'lastModifiedAt < "{self.ingestion_end_date}"']
                    )

                    # hitting the objects and products API classes needs to result in 2 separate file objects
                    if obj == 'orders':   
                        if self.gcs_prefix.find('orders') != -1:
                            logging.info(f'{obj}-->{fetch_data.total} records')
                            logging.info(f'{iterations} needed for {obj}')
                            
                            process_orders_data = PartnerWebshopOrders.process_orders(self=get_all_records)
                            logging.info(f'{len(process_orders_data)} records were written to {obj}.json')
                            self.write_to_gcs_file(process_orders_data, obj)

                        elif self.gcs_prefix.find('order_discounts') != -1: 
                            logging.info(f'{obj}_discounts-->{fetch_data.total} records')
                            logging.info(f'{iterations} needed for {obj}_discounts.json')              
                            
                            process_order_discounts_data = PartnerWebshopOrders.process_order_discounts(self=get_all_records)
                            logging.info(f'{len(process_order_discounts_data)} records were written to {obj}_discounts.json')
                            self.write_to_gcs_file(process_order_discounts_data, f'{obj}_discounts')

                    elif obj == 'products':
                        if self.gcs_prefix.find('products') != -1:
                            logging.info(f'{obj}-->{fetch_data.total} records')
                            logging.info(f'{iterations} needed for {obj}')
                            
                            process_products_data = PartnerWebshopProducts.process_products(self=get_all_records)
                            logging.info(f'{len(process_products_data)} records were written to {obj}.json')
                            self.write_to_gcs_file(process_products_data, obj)
                        
                        elif self.gcs_prefix.find('attributes') != -1:
                            logging.info(f'{obj}_attributes-->{fetch_data.total} records')
                            logging.info(f'{iterations} needed for {obj}_attributes.json')
                        
                            process_product_attributes_data = PartnerWebshopProducts.process_product_attributes(self=get_all_records)
                            
                            logging.info(f'{len(process_product_attributes_data)} records were written to {obj}_attributes.json')
                            self.write_to_gcs_file(process_product_attributes_data, f'{obj}_attributes')

                    # hitting the API classes below results in one file per class
                    elif obj != 'orders' and obj != 'products':
                        process_data = []
                        if obj == 'customers':
                            process_data = PartnerWebshopCustomers.process_customers(self=get_all_records)

                        elif obj == 'customer_groups':
                            process_data = PartnerWebshopCustomerGroups.process_customer_groups(self=get_all_records)

                        elif obj == 'channels':
                            process_data = PartnerWebshopChannels.process_channels(self=get_all_records)

                        elif obj == 'discount_codes':
                            process_data = PartnerWebshopDiscountCodes.process_discount_codes(self=get_all_records)

                        elif obj == 'product_discounts':
                            process_data = PartnerWebshopProductDiscounts.process_product_discounts(self=get_all_records)

                        elif obj == 'product_types':
                            process_data = PartnerWebshopProductTypes.process_product_types(self=get_all_records)

                        elif obj == 'categories':
                            process_data = PartnerWebshopCategories.process_categories(self=get_all_records)
                        
                        if self.gcs_prefix.find(obj) != -1:
                            logging.info(f'{obj}-->{fetch_data.total} records')
                            logging.info(f'{iterations} needed for {obj}')
                            logging.info(f'{len(process_data)} records were written to {obj}.json')
                            self.write_to_gcs_file(process_data, obj)

            # if no new records, highlight in the logging
            else:
                logging.info(f'{fetch_data.total} new records in {obj} object')