import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

SOURCE = "<FILL_TABLE_NAME>"
TARGET = "<FILL_S3_PATH>"

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


## @type: DataSource
## @args: [database = "air-quality", table_name = SOURCE, transformation_ctx = "DataSource0"]
## @return: DataSource0
## @inputs: []
DataSource0 = glueContext.create_dynamic_frame.from_catalog(
    database = "airquality",
    table_name = SOURCE,
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
## @args: [connection_type = "s3", format = "parquet", connection_options = {"path": TARGET", "partitionKeys": ["year" ,"month" ,"day" ,"hour"]}, transformation_ctx = "DataSink0"]
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