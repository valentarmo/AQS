import sys
import datetime
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME',
                                     'source_database'
                                     'source_table_name',
                                     'data_target'])

DATABASE = args['source_database']
SOURCE_TABLE = args['source_table_name']
TARGET = args['data_target']

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

current_date = datetime.datetime.utcnow()
filter_date = current_date - datetime.timedelta(hours = 1)

_year, _month, _day, _hour = filter_date.year, filter_date.month, filter_date.day, filter_date.hour

## @type: DataSource
## @args: [database = DATABASE, push_down_predicate = "(year == '{_year}' and  month == '{_month}' and day == '{_day}' and hour == '{_hour}')", table_name = SOURCE_TABLE, transformation_ctx = "DataSource0"]
## @return: DataSource0
## @inputs: []
DataSource0 = glueContext.create_dynamic_frame.from_catalog(
    database = DATABASE,
    push_down_predicate = f"(year == '{_year}' and  month == '{_month}' and day == '{_day}' and hour == '{_hour}')",
    table_name = SOURCE_TABLE,
    transformation_ctx = "DataSource0"
)

## @type: ApplyMapping
## @args: [mappings = [("location", "string", "location", "string"), ("value", "double", "value", "double"), ("unit", "string", "unit", "string"), ("particle", "string", "particle", "string"), ("country_code", "string", "country_code", "string"), ("date_utc", "string", "date_utc", "string"), ("entity", "string", "entity", "string"), ("latitude", "double", "latitude", "double"), ("longitude", "double", "longitude", "double"), ("year", "string", "year", "string"), ("month", "string", "month", "string"), ("day", "string", "day", "string"), ("hour", "string", "hour", "string")], transformation_ctx = "Transform0"]
## @return: Transform0
## @inputs: [frame = DataSource0]
Transform0 = ApplyMapping.apply(
    frame = DataSource0,
    mappings = [
        ("location", "string", "location", "string"),
        ("value", "double", "value", "double"),
        ("unit", "string", "unit", "string"),
        ("particle", "string", "particle", "string"),
        ("country_code", "string", "country_code", "string"),
        ("date_utc", "string", "date_utc", "string"),
        ("entity", "string", "entity", "string"),
        ("latitude", "double", "latitude", "double"),
        ("longitude", "double", "longitude", "double"),
        ("year", "string", "year", "string"),
        ("month", "string", "month", "string"),
        ("day", "string", "day", "string"),
        ("hour", "string", "hour", "string")
    ],
    transformation_ctx = "Transform0"
)

## @type: DataSink
## @args: [connection_type = "s3", format = "parquet", connection_options = {"path": TARGET, "partitionKeys": ["year" ,"month" ,"day" ,"hour"]}, transformation_ctx = "DataSink0"]
## @return: DataSink0
## @inputs: [frame = Transform0]
DataSink0 = glueContext.write_dynamic_frame.from_options(
    frame = Transform0,
    connection_type = "s3",
    format = "parquet",
    connection_options = {
        "path": TARGET,
        "partitionKeys": ["year" ,"month" ,"day" ,"hour"]
    },
    transformation_ctx = "DataSink0"
)

job.commit()