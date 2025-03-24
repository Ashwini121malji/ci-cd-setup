from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

# Define default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 24),
    'retries': 1,
}

# Define DAG
with DAG(
    'dummy_table_dag',
    default_args=default_args,
    schedule_interval= none
    catchup=False,
) as dag:

    create_table = PostgresOperator(
        task_id='create_dummy_table',
        postgres_conn_id='postgres_default',  # Change if using a different connection ID
        sql="""
        CREATE TABLE IF NOT EXISTS dummy_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            age INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    insert_data = PostgresOperator(
        task_id='insert_dummy_data',
        postgres_conn_id='postgres_default',
        sql="""
        INSERT INTO dummy_table (name, age) VALUES 
        ('Alice', 25),
        ('Bob', 30),
        ('Charlie', 35);
        """
    )

    # Define task dependencies
    create_table >> insert_data
