import click

class SQLFileType(click.ParamType):
    name = "sql"

    def convert(self, value, param, ctx):
        
        if value.endswith('.sql'):
            return value
        else:
            self.fail("expected sql files.")