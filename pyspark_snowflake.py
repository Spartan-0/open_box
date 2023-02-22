from pyspark.sql import SparkSession

# create SparkSession
spark = SparkSession.builder \
    .appName("HiveToSnowflake") \
    .config("spark.sql.sources.partitionOverwriteMode", "dynamic") \
    .enableHiveSupport() \
    .getOrCreate()

# read data from Hive table
hive_database = "your_hive_database"
hive_table = "your_hive_table"
df = spark.table(f"{hive_database}.{hive_table}")

# write data to Snowflake
snowflake_options = {
    "sfUrl": "your_snowflake_url",
    "sfUser": "your_snowflake_user",
    "sfPassword": "your_snowflake_password",
    "sfDatabase": "your_snowflake_database",
    "sfSchema": "your_snowflake_schema",
    "sfWarehouse": "your_snowflake_warehouse",
    "sfRole": "your_snowflake_role",
    "dbtable": "your_snowflake_table"
}

df.write \
    .format("snowflake") \
    .options(**snowflake_options) \
    .mode("append") \
    .save()
