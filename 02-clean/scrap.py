# Import
from pyspark.sql import SparkSession
from optimus import Optimus

# SPARK: Session
spark = SparkSession.builder.appName('optimus').getOrCreate()
op = Optimus(spark)
