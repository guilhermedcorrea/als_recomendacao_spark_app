from os.path import abspath
import pyspark.sql.functions as f
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark import SparkContext, SparkConf
import os
import pandas as pd
import warnings

2

warnings.filterwarnings('ignore')

warehouse_location = abspath('spark-warehouse')

os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-19"
os.environ["SPARK_HOME"] = r"C:\databases_Etl\venv\Lib\site-packages\pyspark"




if __name__=='__main__':
    conf = SparkConf()
    conf.set("spark.master","local[*]")
    conf.set("spark.executor.memory", "4g")
    conf.set("spark.driver.memory", "4g")
    conf.set("spark.sql.adaptive.enabled","true")
    conf.set("spark.sql.adaptive.localShuffleReader.enabled","true")
    conf.set("spark.dynamicAllocation.enabled", "false")
    conf.set("spark.sql.adaptive.optimizeSkewsInRebalancePartitions.enabled","true")
    conf.set("spark.sql.adaptive.skewJoin.enabled","true")
    conf.set("spark.sql.statistics.size.autoUpdate.enabled","true")
    conf.set("spark.sql.inMemoryColumnarStorage.compressed","true")
    conf.set("hive.exec.dynamic.partition", "true")
    conf.set("hive.exec.dynamic.partition.mode", "nonstrict")
    conf.set("spark.sql.ansi.enabled","true")
    conf.set('spark.driver.extraClassPath', r"\\wsl.localhost\Ubuntu-18.04\home\guilherme\als_recomendacao_spark_app\sqlserverjars\mssql-jdbc-12.2.0.jre11.jar")
    conf.set('spark.executor.extraClassPath', r"\\wsl.localhost\Ubuntu-18.04\home\guilherme\als_recomendacao_spark_app\sqlserverjars\mssql-jdbc-12.2.0.jre11.jar")
    spark = SparkSession.builder\
            .config(conf=conf)\
            .config("spark.sql.warehouse.dir", warehouse_location)\
            .config("spark.sql.catalogImplementation", "hive") \
            .enableHiveSupport() \
            .getOrCreate()
    




  
