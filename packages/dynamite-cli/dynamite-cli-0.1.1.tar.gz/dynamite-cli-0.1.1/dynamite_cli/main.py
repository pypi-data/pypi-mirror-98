import typer

from typing import Optional
from .dynamo_copy import copy_dynamo_items

app = typer.Typer()


@app.command()
def copy(
    src_table: str,
    src_region: str,
    src_profile: str,
    dst_table: str,
    dst_region: Optional[str] = typer.Argument(None),
    dst_profile: Optional[str] = typer.Argument(None),
):
    """
    Copy dynamo table items to another table
    """
    typer.echo(f"copy {src_table} in {dst_table}")

    if not dst_region:
        dst_region = src_region
    if not dst_profile:
        dst_profile = src_profile

    if resume(src_table, src_region, src_profile, dst_table, dst_region, dst_profile):
        copy_dynamo_items(src_table, src_region, src_profile, dst_table, dst_region, dst_profile)

    typer.Exit()


def resume(src_table: str,
    src_region: str,
    src_profile: str,
    dst_table: str,
    dst_region: str,
    dst_profile: str,
) -> bool:

    src_table_msg = typer.style(src_table, fg=typer.colors.BLUE,  bold=True)
    dst_table_msg = typer.style(dst_table, fg=typer.colors.BLUE, bold=True)

    dst_region_msg = typer.style(dst_region, fg=typer.colors.BLUE, bold=True)
    dst_profile_msg = typer.style(dst_profile, fg=typer.colors.BLUE, bold=True)

    src_region_msg = typer.style(src_region, fg=typer.colors.BLUE, bold=True)
    src_profile_msg = typer.style(src_profile, fg=typer.colors.BLUE, bold=True)

    typer.secho("#"*40, fg=typer.colors.BLUE)
    typer.echo(f"source table: {src_table_msg}")
    typer.echo(f"source region: {src_region_msg}")
    typer.echo(f"source profile: {src_profile_msg}")

    typer.echo("-"*40)

    typer.echo(f"dest table: {dst_table_msg}")
    typer.echo(f"dest region: {dst_region_msg}")
    typer.echo(f"dest profile: {dst_profile_msg}")

    typer.secho("#"*40, fg=typer.colors.BLUE)

    return typer.confirm("Configurations are correct?")
