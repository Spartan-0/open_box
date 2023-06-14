
from pyspark import SparkContext
from pyspark.sql import SparkSession,SQLContext, HiveContext
from pyspark.sql.functions import *
from pyspark.sql.types import StructField,StructType,StringType,IntegerType,ArrayType,FloatType,DataType
from pyspark.sql.window import Window
import os
import argparse

# Spark context as SC to read RDD
sc = SparkContext.builder().master("local").appName("PysparkRDDApp").getOrCreate()
# Spark context as spark to read spark session or sql context for DataFrames
spark = SparkSession.builder().master("local").appName("PySparkDFApp").getOrCreate().enableHiveSupport()

parser = argparse.ArgumentParser(description="To Read CLI Arguments")
parser.add_argument("--input",help="file input path to process in spark")
args = parser.parse_args()
input_path=args.input

data1 = spark.read.options(header=True, multiline=True, inferSchema=True).formt("csv").load(input_path[0])
data2 = spark.read.options(header=True, multiline=True, inferSchema=True).formt("csv").load(input_path[1])

window_spec = Window.partitionBy("id").orderBy("salary").desc()

# All Joins including Self Join
inner = data1.alias("e").join(data1.alias("m"),col("e.emp_id") == col("m.manager_id"),'inner').withColumn("isCurrent",when(col("e.start_date"),col("current_date")).otherwise(lead("e.start_date",1).over(window_spec)))
