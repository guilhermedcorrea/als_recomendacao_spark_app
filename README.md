#Iniciando o Projeto



#https://realpython.com/build-recommendation-engine-collaborative-filtering/


#Tutorial Base
#https://spark.apache.org/docs/2.2.0/ml-collaborative-filtering.html

#https://medium.com/camilawaltrick/sistema-de-recomendacao-filtragem-colaborativa-als-spark-f5a4a7ccf8cf





Criar modelo ALS

Alternating Least Square é um algoritmo de fatoração de matriz implementado no Apache Spark ML e construído para problemas de filtragem colaborativa em larga escala.

Fatoração de matrizes (ou decomposição)
A ideia básica é decompor uma matriz em partes menores da mesma forma que podemos fazer para um número


- numBlocks é o número de blocos nos quais os atendentes e e atendimentos serão particionados para paralelizar a computação (o padrão é 10).
- classificação é o número de fatores latentes no modelo (o padrão é 10).
- maxIter é o número máximo de iterações a serem executadas (o padrão é 10).
- regParam especifica o parâmetro de regularização em ALS (o padrão é 1.0).
- implicitPrefs especifica se deve usar a variante ALS de feedback explícito ou uma adaptada para dados de feedback implícito (o padrão é falso, o que significa usar feedback explícito).
- alfaé um parâmetro aplicável à variante de feedback implícito do ALS que governa a confiança da linha de base nas observações de preferência (o padrão é 1,0).
- nonnegative especifica se deve ou não usar restrições não negativas para mínimos quadrados (o padrão é false).


```Python

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
conf.set('spark.driver.extraClassPath', r"/home/guilherme/als_recomendacao_spark_app/sqlserverjars/mssql-jdbc-12.2.0.jre11.jar")
conf.set('spark.executor.extraClassPath', r"/home/guilherme/als_recomendacao_spark_app/sqlserverjars/mssql-jdbc-12.2.0.jre11.jar")
spark = SparkSession.builder\
        .config(conf=conf)\
        .config("spark.sql.warehouse.dir", warehouse_location)\
        .config("spark.sql.catalogImplementation", "hive") \
        .enableHiveSupport() \
        .getOrCreate()
```


<b>Iniciando o spark Session e os Serviços do HIVE - SQL</b>



```Python
df_business = spark.read.option("inferSchema",True) \
                 .options(header='True', inferSchema='True', delimiter=';') \
                .csv(r"/home/guilherme/als_recomendacao_spark_app/app/csvteste/tabela_teste.csv")

df_business = df_business.select("ID_AGENTE", "HORA", 
                                 "CAMPANHA_ID",  
                                 "ESTADO", "PLANO"
                                 ,"TIPO_PLANO"
                                 ,"OPERADORA","FORMA_PAGTO"
                                 ,"VENDA","ID_AUDITOR","ID_VENDA","CAMPANHA"
        ,"ID_TICKET")


df_business = df_business.filter((df_business['VENDA'] == 'Sim'))
```
<b>Faz a Leitura do Arquivo CSV filtrando as colunas a serem usadas, condição VENDA = 'Sim'</b>



```Python
driver = "com.microsoft.sqlserver.jdbc.SQLServerDriver"

database_host = "BIGDATA"
database_port = "1433" 
database_name = "BIGDATA"
table = "comercial.ranking_atendimento_tim"
user = "sa"
password = "123"

url = f"jdbc:sqlserver://{database_host}:{database_port};database={database_name}"

remote_table = (spark.read
  .format("jdbc")
  .option("driver", driver)
  .option("url", url)
  .option("dbtable", table)
  .option("user", user)
  .option("password", password)
  .load()
)
```

<b>Consultando Tabela SQL Server</b>