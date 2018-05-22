
from __future__ import print_function
from builtins import range
from airflow.operators import BashOperator
from airflow.models import DAG
from datetime import datetime, timedelta

import time
from pprint import pprint

seven_days_ago = datetime.combine(
        datetime.today() - timedelta(7), datetime.min.time()
)

args = {
    'owner': 'airflow',
    'start_date': seven_days_ago,
}

dag = DAG(
    dag_id='example_pydata_dag',
    default_args=args,
    schedule_interval='@daily'
)

download_currency_cmd = '''
curl -s 'https://api.coindesk.com/v1/bpi/historical/close.json?start={{ ds }}&end={{ ds }}' > /tmp/{{ ds }}.json
'''
# Returns
# {
# 	"bpi": {
# 		"2018-01-01": 13412.44
# 	},
# 	"disclaimer": "This data was produced from the CoinDesk Bitcoin Price Index. BPI value data returned as USD.",
# 	"time": {
# 		"updated": "Jan 2, 2018 00:03:00 UTC",
# 		"updatedISO": "2018-01-02T00:03:00+00:00"
# 	}
# }

download_currency = BashOperator(
    task_id='download_currency',
    bash_command=download_currency_cmd,
    dag=dag
)

extract_data = BashOperator(
    task_id='extract_data',
    bash_command="cat /tmp/{{ ds }}.json | jq '.bpi[]' ",
    dag=dag
)

download_currency >> extract_data
