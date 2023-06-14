import pandas as pd
import matplotlib.pyplot as plt
from pyspark.sql.functions import *
from pyspark.sql import SparkSession

# Create Spark Context
spark = SparkSession.builder.appName("testApp").master("local").getOrCreate()

# Create a PySpark DataFrame
df = spark.createDataFrame([(1, 2), (3, 4), (5, 6)], ["col1", "col2"])

# Convert PySpark DataFrame to Pandas DataFrame
pandas_df = df.toPandas()

# Generate a bar chart
pandas_df.plot(kind="bar", x="col1", y="col2")
plt.show()

# Generate a scatter plot
pandas_df.plot(kind="scatter", x="col1", y="col2")
plt.show()
