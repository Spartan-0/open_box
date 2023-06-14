from pyspark.sql.functions import *
from pyspark.sql.window import Window
from pyspark.sql import SparkSession
import os
import configparser
import argparse
from pyspark.storagelevel import StorageLevel

parser = argparse.ArgumentParser(description="pyspark arguments")
parser.add_argument('--input',help="getting inputfile path")
args = parser.parse_args()
input_path = args.input

# Define Spark Session
spark = SparkSession.builder.master("local").appName("Pyspark_app").enableHiveSupport().getOrCreate()
script_path = os.path.realpath(__file__)
config_path = os.path.join(os.path.dirname(script_path), "/config/app_config.cfg")
config = configparser.ConfigParser()
config.red(config_path)
app_name = config.get("DEFAULT","app_name")

# Define the input data
data = [
  (1, 'John', 'Smith', '2021-01-01'),
  (1, 'John', 'Doe', '2022-01-01'),
  (2, 'Jane', 'Doe', '2021-01-01'),
  (2, 'Jane', 'Doe', '2022-01-01')
]

df = spark.createDataFrame(data, ['id', 'first_name', 'last_name', 'effective_date'])
df.persist(StorageLevel.MEMORY_AND_DISK)
df.count()

# Create a window partitioned by id and ordered by effective_date
window = Window.partitionBy('id').orderBy('effective_date')

# Create a new column to represent the current version of the record
df = df.withColumn('is_current', row_number().over(window).desc() == 1)

# Create a new column to represent the end date of the current version of the record
df = df.withColumn('end_date', lead('effective_date', 1).over(window))

# Replace null end dates with a default value
df = df.withColumn('end_date', coalesce('end_date', lit('9999-12-31')))

# Create a unique identifier for each record
df = df.withColumn('version', dense_rank().over(window))

# Create a new column to represent the start date of the record
df = df.withColumn('start_date', when(col('is_current'), col('effective_date')).otherwise(lead('effective_date', 1).over(window)))

# Replace null start dates with a default value
df = df.withColumn('start_date', coalesce('start_date', lit('1900-01-01')))

# Drop the effective date column
df = df.drop('effective_date')

df.show(5,truncate=False)
df.unpersist
df.count()
# Write the dataframe to a table
#df.write.format('delta').mode('overwrite').saveAsTable('slowly_changing_dim')
