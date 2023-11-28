from google.cloud import storage
from pathlib import Path
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from flask import Flask, request

load_dotenv()

app = Flask(__name__)

BUCKET_NAME = 'proyectocloud2023-2'
prefix = 'lr_model/'

storage_client = storage.Client()

bucket = storage_client.get_bucket(BUCKET_NAME)
blobs = bucket.list_blobs(prefix=prefix) 

for blob in blobs:
    if blob.name.endswith("/"):
        continue
    file_split = blob.name.split("/")
    directory = "/".join(file_split[0:-1])
    Path(directory).mkdir(parents=True, exist_ok=True)
    blob.download_to_filename(blob.name)

spark = SparkSession.builder.appName("ModelTraining").getOrCreate()

model = PipelineModel.load("lr_model")

@app.route('/review')
def analyse_review():
    review = request.args.get('review')
    if review:
        single_prediction = spark.createDataFrame([(review,)], ["review_body"])

        single_prediction = model.transform(single_prediction)

        analisis = "Positivo" if single_prediction.select("prediction").first()[0] == 1.0 else "Negativo"
        return {"analisis" : analisis}
    else:
        return {"analisis" : "No se envio un review"}
    

if __name__ == '__main__':
    app.run(port=5000)