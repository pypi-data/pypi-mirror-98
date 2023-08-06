# Postgres Helper

The `postgres-helper` library is build on top of [`psycopg2`](https://github.com/psycopg/psycopg2/). It will be really helpful for running the basic postgresql query in python.

### Installation

For installation of `postgres-helper`, you need to run following command

```shell
pip install postgres-helper
```

### Examples using this library

Please check the official documentation for full documentation.

```python
#Library import
from pg.pg import Pg

# Initialization of library
pg = Db(dbname='postgres', user='postgres', password='admin', host='localhost', port='5432')

# Get the column names of the specific table
pg.get_columns_name(table='pg_table')

# Get values from specific column of table
pg.get_values_from_column(column='pg_table_col', table='pg_table', schema='public')

# Create schema
pg.create_schema(name='schema_name')

# Create column
pg.create_column(column='col_name', table='pg_table', col_datatype='varchar', schema='public')

# Update column
pg.update_column(column='col_name', value='updated_value', table='pg_table', where_column='where_col', where_value="where_val", schema='public')

# Delete table
pg.delete_table(name='pg_table', schema='public')

# Delete values
pg.delete_values(table_name='pg_table', condition='name=value', schema='public')
```
