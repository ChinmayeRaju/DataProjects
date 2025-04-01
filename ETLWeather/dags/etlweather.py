from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago

#latitude and longitude
LATITUDE = "51.5074"
LONGITUDE = "-0.1278"
POSTGRES_CONN_ID="postgres_default"
API_CONN_ID="open_meteo_api"

default_args={
    "owner":"airflow",
    "start_date": days_ago(1)
}

#DAG
with DAG(dag_id="weather_etl_pipeline",
         default_args=default_args,
         schedule_interval="@daily",
         catchup=False) as dags:
    
    @task()
    def extract_weather_data():
        """Extract weather data from open-meteo API using Airflow Connection."""

        #3 Use Http hook to connection details from Airflow conn
        http_hook = HttpHook(http_conn_id=API_CONN_ID,method="GET")

        ##Build Api endpoint
        # https://api.open-meteo.com
        endpoint = "/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true"

        #make the request via http hook
        response = http_hook.run(endpoint)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"failed to fetched weather data:{response.status_code}")
        
    @task()
    def transform_weather_data(weather_data):
        """Transform the extracted weather data."""
        current_weather = weather_data["current_weather"]
        transformed_data = {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "temperature": current_weather["temperature"],
            "windspeed": current_weather["windspeed"],
            "winddirection":current_weather["winddirection"],
            "weathercode": current_weather["weathercode"]
        }

        return transformed_data
    
    @task()
    def load_weather_data(transformed_data):
        """Load transformed data into postgreSQL"""
        pg_hook = PostgresHook(postgres_conn_id = POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        #create table if it doesnt exist
        cursor.execute(""""
        CREATE TABLE IF NOT EXISTS weather_data (
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            windspeed FLOAT,
            weathercode INT,
            winddirection FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        #Insert transformed data into the table
        cursor.execute("""
        INSERT INTO weather_data (latitude, longitude, temperature,windspeed,winddirection)
        VALUES (%s,%s,%s,%s,%s)
        """, (
            transformed_data['latitude'],
            transformed_data['longitude'],
            transformed_data['temperature'],
            transformed_data['windspeed'],
            transformed_data['winddirection'],
            transformed_data['weathercode']
        ))

        conn.commit()
        cursor.close()

    #Dag Workflow - ETL Pipeline
    weather_data = extract_weather_data()
    transformed_data = transform_weather_data(weather_data)
    load_weather_data(transformed_data)
