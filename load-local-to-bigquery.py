import os
from google.cloud import bigquery

KEY_PATH = "/Users/angelina.teneva/Documents/data-geeking-gcp-c710229c3108.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH

# Construct a BigQuery client object.
client = bigquery.Client()

# schema must be specified with schema fields
data_engineer_jobs = [
    bigquery.SchemaField("job_title", "STRING"),
    bigquery.SchemaField("salary_estimate", "STRING"),
    bigquery.SchemaField("job_description", "STRING"),
    bigquery.SchemaField("rating", "FLOAT64"),
    bigquery.SchemaField("company_name", "STRING"),
    bigquery.SchemaField("location", "STRING"),
    bigquery.SchemaField("headquarters", "STRING"),
    bigquery.SchemaField("size", "STRING"),
    bigquery.SchemaField("founded", "INT64"),
    bigquery.SchemaField("type_of_ownership", "STRING"),
    bigquery.SchemaField("industry", "STRING"),
    bigquery.SchemaField("sector", "STRING"),
    bigquery.SchemaField("revenue", "STRING"),
    bigquery.SchemaField("easy_apply", "STRING"),
]


# schema must be specified with schema fields
median_income = [
    bigquery.SchemaField("fifs_code", "STRING"),
    bigquery.SchemaField("state", "STRING"),
    bigquery.SchemaField("area", "STRING"),
    bigquery.SchemaField("median_household_income_2019", "FLOAT64")
]


def load_local_csv_to_bq(table_id, file_path, bq_schema):
    """
    Uploads GCS files to a BigQuery table
    :param table_id: "project.dataset.table"
    :param file_path: "local path/file"
    :param bq_schema: "schema representation of the file to be loaded"
    """

    job_config = bigquery.LoadJobConfig(
        schema=bq_schema,
        autodetect=False,
        source_format="CSV",
        field_delimiter=",",
        encoding="UTF-8",
        allow_quoted_newlines=True,
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        quote_character='"',
        max_bad_records=0,
        ignore_unknown_values=True
    )

    with open(file_path, "rb") as source_file:
        load_job = client.load_table_from_file(
            source_file, table_id, job_config=job_config
        )

    load_job.result()
    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")


if __name__ == '__main__':
    load_local_csv_to_bq(
        "data-geeking-gcp.the_data_challenge.data_engineer_jobs",
        "/Users/angelina.teneva/Downloads/data_engineer.csv",
        data_engineer_jobs
    )

    load_local_csv_to_bq(
        "data-geeking-gcp.the_data_challenge.usa_median_household_income",
        "/Users/angelina.teneva/Downloads/usa_median_household_income_2019.csv",
        median_income
    )