from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'..', 'scripts'))
from weather_etl import Weather

default_args = {
    'owner': 'name',
    'depends_on_past': False,
    'start_date': datetime(2026, 8, 28),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
dag = DAG(
    'weather_etl_pipeline',
    default_args=default_args,
    schedule_interval='0 11 * * *',
    catchup=False,
    tags=['weather', 'etl']
)

def run_weather_etl():
    cities = ['Moscow', 'Saint Petersburg', 'Krasnodar']

    for city in cities:
        print(f"Запуск для {city}")
        weather = Weather(city)
        weather.run()

    print("Запрос выполнен")

run_etl_task = PythonOperator(
    task_id='run_weather_etl',
    python_callable=run_weather_etl,
    dag=dag
)
run_etl_task