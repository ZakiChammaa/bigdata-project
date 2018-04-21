from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.ml.linalg import Vectors
from pyspark.ml import PipelineModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

PATH_TO_MODEL = 'model/'

def getSparkSessionInstance(sparkConf):
    if ('sparkSessionSingletonInstance' not in globals()):
        globals()['sparkSessionSingletonInstance'] = SparkSession\
            .builder\
            .config(conf=sparkConf)\
            .getOrCreate()
    return globals()['sparkSessionSingletonInstance']

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./virtualenv/bin/spark-submit streaming.py <hostname> <port>", file=sys.stderr)
        sys.exit(-1)
    
    sc = SparkContext(appName="PythonStreaming")

    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel( logger.Level.ERROR )
    logger.LogManager.getLogger("akka").setLevel( logger.Level.ERROR )

    ssc = StreamingContext(sc, 1)

    lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))

    def process(time, rdd):
        print("========= %s =========" % str(time))
        try:
            spark = getSparkSessionInstance(rdd.context.getConf())
            rowRdd = rdd.map(lambda p: Row(label=float(p.split(',')[3]), features=Vectors.dense([float(x) for x in p.split(',')[0:3]] + [float(x) for x in p.split(',')[4:8]])))
            testing_df = spark.createDataFrame(rowRdd)

            model = PipelineModel.load(PATH_TO_MODEL)
            predictions = model.transform(testing_df)

            predictions.select("prediction", "indexedLabel", "features").show(5)

            evaluator = MulticlassClassificationEvaluator(
                labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
            accuracy = evaluator.evaluate(predictions)
            with open("accuracy.txt", "a") as f:
                f.write("%f," % accuracy)
            print("Accuracy = %g " % accuracy)
        except:
            pass

    lines.foreachRDD(process)

    ssc.start()
    ssc.awaitTermination()
