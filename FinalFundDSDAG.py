import sys

sys.path.append("./FinalFundDSResources")

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from ModelPredict import predict_temperature
from CurrentData import transformResponseCurrentToDataframe

def updateData():
    df = transformResponseCurrentToDataframe()

    pathToHistoricalData = "FinalFundDSResources/history.csv"

    df.to_csv(pathToHistoricalData, mode= 'a', header= False, index= False)

def callModel():
    print(predict_temperature())

default_args = {
    "owner": "nbv2704", 
    "retries": 5,
    "retry_delay": timedelta(minutes= 5)   
} 

with DAG(
    dag_id = "FinalFundDSDAG",
    default_args = default_args,
    description = "This is DAG used for Fundamental of Data Science Project",
    start_date = datetime(2024, 11, 5, 0, 0, 0),
    schedule_interval = "@hourly"
) as dag:
    Data = PythonOperator(
        task_id = "Update Data",
        python_callable = updateData
    )

    Model = PythonOperator(
        task_id = "Re-train and predict",
        python_callable = callModel
    )

    Data >> Model