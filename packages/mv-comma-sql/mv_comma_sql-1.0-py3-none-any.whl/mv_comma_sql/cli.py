import sys
import click
from mv_comma_sql.type import SQLFileType

@click.group()
def cli():
    click.echo("Hye, thanks for using mv_comma_sql")
    pass


@cli.command()
@click.argument(
    "inputfile", required=1, nargs=1, type=SQLFileType()
)
@click.argument(
    "outputfile",required=0, type=SQLFileType()
)
def mv_comma(inputfile, outputfile):
    """
    move comma from the end to the front
    """

    if not outputfile:
        outputfile = inputfile

    # read the input file
    with open(inputfile, "r") as fi:
        query_string = fi.read()

    query_row_list = query_string.split("\n")
    new_row_list = []

    add_comma_flag = False
    for row in query_row_list:
        
        # deal with comma
        if add_comma_flag:
            # cnt space in the left
            spc = len(row) - len(row.lstrip())
            row = row.strip()
            row = " " * spc + ", " + row
        
        # reset the flag
        add_comma_flag = False
        if row.endswith(","):
            add_comma_flag = True
            row = row.rstrip(",")
        new_row_list.append(row)

    new_query = "\n".join(new_row_list)

    with open(outputfile, "w") as fp:
        fp.write(new_query)
    click.echo(f"{inputfile} is reformatted as {outputfile}")


cli()