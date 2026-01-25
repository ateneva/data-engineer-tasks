# Terraform

## What is Terraform?

Terraform is a tool that allows us to build infrastructure as code

## Why is Infrastrcture as code important?

Building infrastructure in a controlled way makes it:

- possible to version control
- easy to replicate

## Setting up Terraform

- `setup terraform locally`

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

- `verify installation`

```bash
terraform -version
terraform -help
```

**NB** Terraform comes pre-installed in Google Cloud Shell

## What happens if resource already exists

To import an existing Google Cloud Storage (GCS) bucket into your Terraform state, you use the `terraform import` command. This process brings the resource under Terraform's management without recreating it.

There are two primary ways to achieve this: using the **`terraform import` command** (CLI) or using the **`import` block** (HCL, Terraform v1.5+).

-----

## 1\. Using the `terraform import` Command (CLI)

This is the traditional, one-time command approach.

### **Step 1: Define the Resource Block**

First, you must create a `google_storage_bucket` resource block in your `.tf` file that **accurately reflects the existing bucket's configuration**, especially its `name` and `location`.

```hcl
resource "google_storage_bucket" "example_bucket" {
  name     = "my-existing-gcs-bucket-name" # Must match the existing bucket's name exactly
  location = "US-CENTRAL1"                  # Must match the existing bucket's location
  # Include any other configurations like 'storage_class', 'force_destroy', etc.
  # to match the live bucket.
}
```

### **Step 2: Run the Import Command**

Use the `terraform import` command with the resource address and the unique ID of the live resource.

  - **Resource Address:** `google_storage_bucket.example_bucket` (Type and Local Name)
  - **Resource ID:** The unique **bucket name** (`my-existing-gcs-bucket-name`).

<!-- end list -->

```bash
# generic example 
terraform import google_storage_bucket.example_bucket my-existing-gcs-bucket-name

# specific example 
terraform import google_storage_bucket.eu-data-challenge eu-data-challenge
```

### **Step 3: Verify the State**

After a successful import, always run a plan to check for discrepancies between your HCL code and the actual bucket configuration.

```bash
terraform plan
```

If the plan shows **"No changes. Your infrastructure matches the configuration,"** the import was successful. If it shows changes, you must update your HCL code (in Step 1) to match the live resource's current state until `terraform plan` is clean.

-----

## 2\. Using the `import` Block (HCL - Terraform 1.5+)

The `import` block allows you to specify the resource to be imported directly in your HCL code, and the import is executed when you run `terraform plan` or `terraform apply`.

### **Step 1: Define the Resource and the Import Block**

Add both the resource configuration block and the separate `import` block to your `.tf` file.

```hcl
resource "google_storage_bucket" "example_bucket" {
  name     = "my-existing-gcs-bucket-name"
  location = "US-CENTRAL1"
  # ... other configurations
}

import {
  to = google_storage_bucket.example_bucket
  id = "my-existing-gcs-bucket-name"
}
```

### **Step 2: Run `terraform apply`**

Run a standard `apply`. Terraform will detect the `import` block, perform the import first, and then check the resource against your configuration.

```bash
terraform apply
```

If the HCL configuration perfectly matches the existing bucket, the output will show the resource was imported with no further changes. If there are differences, it will propose an update (a change-in-place) after the import.

The video below explains how to import existing infrastructure to Terraform.

[Import Existing infrastructure using terraform](https://www.youtube.com/watch?v=7lJ9jOKZKyA) discusses the process of importing existing cloud resources, like storage buckets, into a Terraform state file.
<http://googleusercontent.com/youtube_content/0>

## USEFUL CLI

 - `download and install any provider binary for the providers to use within the configuration`

```bash
terraform init
```

- `reformat your configuration in the standard style`

```bash
# check if file format is according to standard style
terraform fmt -check

# apply standard style of formatting
terraform fmt

#Display diffs of formatting changes
terraform fmt -diff
```

- `create an execution plan`

```bash
terraform plan

# only plan changes referring to specific resource
terraform plan -target="resource_type.resource.name"

# e.g.
terraform plan -target="google_bigquery_dataset.the-look-data-quality"

# save an execution plan to apply later
terraform plan -out "my-bucket-config"
```

- `apply the execution plan`

```bash
terraform apply

# apply exectuion plan that has been saved
terraform apply "my-bucket-config"
```

- `show the current state of infrastructure config`

```bash
terraform show
```

- `Mark a resource instance as not fully functional and to be destroyed and recreated on next apply`

```bash
terraform taint
```

- `destroy infrastructure`

```bash
terraform destroy
```
