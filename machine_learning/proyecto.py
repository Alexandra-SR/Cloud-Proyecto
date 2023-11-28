import os
import json
#import paramiko
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer, IDF
from pyspark.ml.classification import LinearSVC, LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


def preprocess_text(text):
    import re
    import string
    text = re.sub('[' + string.punctuation + ']', '', text)
    text = text.lower()
    text = ' '.join(text.split())
    return text

def train_model(pipeline, trainDF, name, model_dir):
    paramGrid = ParamGridBuilder().build()  
    crossval = CrossValidator(estimator=pipeline,
                              estimatorParamMaps=paramGrid,
                              evaluator=MulticlassClassificationEvaluator(labelCol='label', predictionCol='prediction', metricName='accuracy'),
                              numFolds=5)
    cvModel = crossval.fit(trainDF)
    model_path = os.path.join(model_dir, name)
    cvModel.bestModel.save(model_path)
    return cvModel, model_path

def train():

    MODEL_DIR = './content/model' 
    METADATA_FILE = 'metadata.json'
    METADATA_PATH = os.path.join(MODEL_DIR, METADATA_FILE)

    spark = SparkSession.builder.appName("ModelTraining").getOrCreate()

    # Load training data with Spark
    df = spark.read.parquet('./amazon_us_reviews-train-00000-of-00005.parquet')
    df = df.withColumn('star_rating', df['star_rating'].cast('string'))
    df = df.withColumn('review_body', df['review_body'].cast('string'))
    df = df.withColumn('label', (df['star_rating'] > '3').cast('integer'))

    preprocess_udf = udf(preprocess_text)
    df = df.withColumn('review_body', preprocess_udf('review_body'))
    df = df.select('review_body', 'label')

    # Split the data
    trainDF, testDF = df.randomSplit([0.7, 0.3], seed=42)

    # Common pipeline stages
    tokenizer = Tokenizer(inputCol='review_body', outputCol='mytokens')
    stopwords_remover = StopWordsRemover(inputCol='mytokens', outputCol='filtered_tokens')
    vectorizer = CountVectorizer(inputCol='filtered_tokens', outputCol='rawFeatures')
    idf = IDF(inputCol='rawFeatures', outputCol='vectorizedFeatures')

    # SVM pipeline
    svm = LinearSVC(featuresCol='vectorizedFeatures', labelCol='label')
    svm_pipeline = Pipeline(stages=[tokenizer, stopwords_remover, vectorizer, idf, svm])
    svm_cvModel, svm_model_path = train_model(svm_pipeline, trainDF, "svm_model", MODEL_DIR)

    # Logistic Regression pipeline
    lr = LogisticRegression(featuresCol='vectorizedFeatures', labelCol='label')
    lr_pipeline = Pipeline(stages=[tokenizer, stopwords_remover, vectorizer, idf, lr])
    lr_cvModel, lr_model_path = train_model(lr_pipeline, trainDF, "logistic_regression_model", MODEL_DIR)

    # Save metadata
    metadata = {
        "svm_train_accuracy": MulticlassClassificationEvaluator(labelCol='label', predictionCol='prediction', metricName='accuracy').evaluate(svm_cvModel.transform(testDF)),
        "logistic_regression_train_accuracy": MulticlassClassificationEvaluator(labelCol='label', predictionCol='prediction', metricName='accuracy').evaluate(lr_cvModel.transform(testDF))
    }
    with open(METADATA_PATH, 'w') as outfile:
        json.dump(metadata, outfile)

    print("Metadata saved successfully.")

"""

    # File Transfer with Paramiko
    print("Moving files to remote server")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    k = paramiko.RSAKey.from_private_key_file('path/to/id_rsa')
    client.connect("192.168.1.11", username="xavi", pkey=k)
    sftp = client.open_sftp()
    try:
        sftp.put(svm_model_path, "/remote/path/" + os.path.basename(svm_model_path))
        sftp.put(lr_model_path, "/remote/path/" + os.path.basename(lr_model_path))
        sftp.put(METADATA_PATH, "/remote/path/" + METADATA_FILE)
    finally:
        sftp.close()
        client.close()

    print("Files transferred successfully.")


"""

if __name__ == '__main__':
    train()