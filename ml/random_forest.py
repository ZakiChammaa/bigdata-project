from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import StringIndexer, VectorIndexer
from pyspark.ml.classification import RandomForestClassifier

PATH_TO_MODEL = 'model/'

spark = SparkSession\
    .builder\
    .appName("random_forest")\
    .getOrCreate()

lines = spark.read.csv("data/training.csv", header=True, mode="DROPMALFORMED").rdd
data_rdd = lines.map(lambda p: Row(label=float(p[3]), features=Vectors.dense([float(p[0]), float(p[1]), float(p[2]), float(p[4]), float(p[5]), float(p[6]), float(p[7])])))
trainingData = spark.createDataFrame(data_rdd)

labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(trainingData)

featureIndexer =\
    VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=31).fit(trainingData)

dt = RandomForestClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures")

pipeline = Pipeline(stages=[labelIndexer, featureIndexer, dt])

model = pipeline.fit(trainingData)

# save decision tree model
model.save(PATH_TO_MODEL)