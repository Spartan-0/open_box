from pyspark.sql import SparkSession

# Create a Spark session
spark = SparkSession.builder.appName("ReadFromHBase").getOrCreate()

# Define the Phoenix configuration
conf = {
    "hbase.zookeeper.quorum": "localhost:2181", # Zookeeper quorum
    "hbase.mapreduce.inputtable": "my_table", # HBase table name
    "phoenix.schema.isNamespaceMappingEnabled": "true" # Namespace mapping
}

# Read the data from HBase using Phoenix
df = spark.read.format("org.apache.phoenix.spark") \
    .options(**conf) \
    .load()

# Create a temporary view so that we can query the data using SQL
df.createOrReplaceTempView("hbase_table")

# Run a SQL query on the data
result = spark.sql("SELECT * FROM hbase_table WHERE column1='value1'")

# Show the query results
result.show()

# Stop the Spark session
spark.stop()
