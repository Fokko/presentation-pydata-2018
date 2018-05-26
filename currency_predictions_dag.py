# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import airflow
from builtins import range
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.lineage.datasets import File
from airflow.models import DAG
from datetime import timedelta

# for now to make it work
Table = File

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}

dag = DAG(
    dag_id='build_currency_preditions', default_args=args,
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(minutes=60))

# Download currency data from coindesk
inlet = File(name="https://api.coindesk.com/v1/bpi/historical"
             "/close.json?start={{ ds }}"
             "&end={{ ds }}")
outlet = File(name="s3a://bucket/currency_rates.{{ ds }}"
              ".0", max_versions=5)
op1 = DummyOperator(dag=dag, task_id="get_currency",
                    inlets={"datasets": [inlet,]},
                    outlets={"datasets": [outlet,]})

# Run machine learning model
outlet = File(name="s3a://bucket/prediction.{{ ds }}."
              "0", max_versions=5)
op2 = DummyOperator(dag=dag, task_id="create_predictions",
                    inlets={"auto": True},
                    outlets={"datasets": [outlet,]})
op2.set_upstream(op1)

# Drop data into Druid
outlet = Table(name="invest_predictions.0", max_versions=5)
op3 = DummyOperator(dag=dag, task_id="load_into_druid",
                    inlets={"auto": True},
                    outlets={"datasets": [outlet,]})
op3.set_upstream(op2)


if __name__ == "__main__":
    dag.cli()
