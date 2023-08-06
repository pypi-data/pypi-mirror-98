import typer
import boto3


def copy_dynamo_items(
    src_table: str,
    src_region: str,
    src_profile: str,
    dst_table: str,
    dst_region: str,
    dst_profile: str,
):
    src_table_msg = typer.style(src_table, fg=typer.colors.GREEN, bold=True)
    dst_table_msg = typer.style(dst_table, fg=typer.colors.GREEN, bold=True)

    typer.echo(f"DynamoDB: copy items from {src_table_msg} to {dst_table_msg}")

    # create client
    src_client = boto3.Session(profile_name=src_profile).client('dynamodb', region_name=src_region)
    dst_client = src_client
    if dst_region is not None:
        if dst_profile is not None:
            dst_client = boto3.Session(profile_name=dst_profile).client('dynamodb', region_name=dst_region)
        else:
            dst_client = boto3.client('dynamodb', region_name=dst_region)


    # scan
    dynamo_items = []
    api_response = src_client.scan(TableName=src_table, Select='ALL_ATTRIBUTES')
    dynamo_items.extend(api_response['Items'])

    items_len_msg = typer.style(str(len(dynamo_items)), fg=typer.colors.GREEN, bold=True)

    typer.echo(f"Collected {items_len_msg} items from source table {src_table_msg}")

    while 'LastEvaluatedKey' in api_response:
        api_response = src_client.scan(
            TableName=src_table,
            Select='ALL_ATTRIBUTES',
            ExclusiveStartKey=api_response['LastEvaluatedKey']
        )
        dynamo_items.extend(api_response['Items'])
        print("Collected total {0} items from table {1}".format(len(dynamo_items), src_table))

    # split all items into chunks, not very optimal as memory allocation is doubled,
    # though this script not intended for unattented execution, so it should be fine
    chunk_size = 25
    current_chunk = []
    chunks = [current_chunk]
    for item in dynamo_items:
        current_chunk.append(item)
        if len(current_chunk) == chunk_size:
            current_chunk = []
            chunks.append(current_chunk)

    with typer.progressbar(chunks, length=100, label="Copying") as progress:
        for chunk in progress:
            if len(chunk) > 0:
                write_request = {dst_table: list(map(lambda x: {'PutRequest': {'Item': x}}, chunk))}
                dst_client.batch_write_item(RequestItems=write_request)
