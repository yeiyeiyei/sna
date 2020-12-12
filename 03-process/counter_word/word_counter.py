#!/usr/bin/env python3

#
# Imports
#
import sys

from operator import add
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
import pyspark.sql.functions as f

#
# Spark + Cache
#
#@lru_cache(maxsize=None)
#def get_spark():
#    return (SparkSession.builder
#                .master("local")
#                .appName("gill")
#                .getOrCreate())

#
# Spark
#
spark = SparkSession\
  .builder \
  .appName("PythonWordCount") \
  .getOrCreate()




#
# Read CSV
#
#data = spark.read.options(mode='FAILFAST', header=True, multiLine=True, escape='"', delimiter=',').csv('tweets_2019_07_len_235.csv')
data = spark.read.options(mode='FAILFAST', header=True, multiLine=True, escape='"', delimiter=',').csv('tweets_2020_10_len_6688.csv')

print('############ CSV extract:')
data.show()

# Count and group word frequencies on the column Lyrics, when splitted by space comma
data.withColumn('word', f.explode(f.split(f.col('text'), ' '))).groupBy('word').count().sort('count', ascending=False).show()




# To remove stop words (like "I", "The", ...), we need to provide arrays of words, not strings. Here we use APache Spark Tokenizer to do so.
# We create a new column to push our arrays of words
tokenizer = Tokenizer(inputCol="text", outputCol="words_token")
tokenized = tokenizer.transform(data).select('id','words_token')

print('############ Tokenized data extract:')
tokenized.show()



remover = StopWordsRemover(stopWords=StopWordsRemover.loadDefaultStopWords("spanish"), inputCol="words_token", outputCol="words_clean")
data_clean = remover.transform(tokenized).select('id', 'words_clean')

print('############ Data Cleaning extract:')
data_clean.show()


# Final step : like in the beginning, we can group again words and sort them by the most used
result = data_clean.withColumn('word', f.explode(f.col('words_clean'))) \
  .groupBy('word') \
  .count().sort('count', ascending=False) \

print('############ TOP20 Most used words in Billboard songs are:')
result.show()







# Stop Spark Process
spark.stop()
