# Dynamite-cli

A cli to copy dynamo table items to another table

## Requirements
You need [poetry](https://python-poetry.org/) as a dependency manager

## Installation
`pip install dynamite-cli`

## Usage
You can print an help menu with `dynamite-cli --help`

The **source table**, **source region**, **source profile** and **destination table** are `required` fields  
If you don't specify a destination **region** and/or a destination **profile**, the source one are used.

The `profile` field is used to retrieve the credentials to connect to your AWS account. So you need at least one account configured in your `.aws/credentials` file (*aws_access_key_id*, and *aws_secret_access_key*)


> NOTE: the tables should have the same schema

Example:
`dynamite-cli <SRC_TABLE> <SRC_REGION> <SRC_PROFILE> <DST_TABLE> [DST_REGION] [DST_PROFILE]`
