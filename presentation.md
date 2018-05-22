![](airflow.png)

# PyData 2018

# Amsterdam

## Elegant data pipelining with Apache Airflow

---

Imagine you are using machine learning models that need conversion rates for currencies. This you then use for advice to your customers.

For your business it is important that you are able to explain to your customer how you got to a certain decision.

In your data pipelines this means even more emphasis on reproducibility and replicability which require idempotency of your tasks

---

# Apache Airflow (incubating)

- Programmatically task based workflow scheduling
- Developed by Airbnb in 2015, moved to Apache in 2016
- {ETL, Machine Learning, Predictive, General} pipeline
- Used by 120+ companies, including Airbnb, ING, Lyft, LinkedIn, Paypal, Reddit and more
- 462 contributors and growing
- We love open source

---

# Why is this important

- ETL consists of a complex network of dependencies
- Analytics and batch processing is mission critical
- Too much time is spend on monitoring and troubleshooting jobs

---

![fit](job.png)

---

# What does elegant mean?

- Reproducible
- Future proof
- Robust against changes
- Lineage

---

## Functional Programming

Learnings:

- Model transformations a functions
- Repeateable, idempotent functions
- Eliminate side effects

---

# Transformations as a function

Model the operation an a mathematical function:

$$
f(x) \rightarrow y
$$

- No changing of state
- No mutable data
- Easier to reason about and test

^ By setting up a contract of the function, the output can be easily asserted based on a given input. Avoid external state and mutable data so it can be tested and reasoned about in isolation. This should give a determinstic and idempotent building block for your DAG. A specific version of the code, should give the same result.

---

# Avoid external state

Good:
```python
get_currencyrrency = SimpleHttpOperator(
    task_id='get_currency',
    endpoint='https://api.coindesk.com/v1/bpi/historical/close.json?start={{ ds }}&end={{ ds }}',
    dag=dag
)
```
Bad:
```python
get_currencyrrency = SimpleHttpOperator(
    task_id='get_currency',
    endpoint='https://api.coindesk.com/v1/bpi/currentprice.json',
    dag=dag
)
```

---

# Write idempotent tasks

- Never append, but overwrite the partition
- Easier to paralleize

```sql
INSERT OVERWRITE TABLE crypto
    PARTITION(day='{{ ds }}')
SELECT
    w.address    address,
    w.currency   currency
    w.btc        btc,
    r.usd        usd
FROM wallet w
JOIN currency_exchange_rates r USING(currency)
WHERE day = '{{ ds }}'
```

---

# Changing the code over time

- Previously DAG runs can be repeated with new code
- Data can be repaired by rerunning the new code, either by clearing tasks or doing backfills.

---

# Lineage

Answers the question for a developer
- What is the latest version of the data I need?
- Where did I get the data from?

---

# Examples

---

## Beginner
- How do you start well

---

## Intermediate
- Dynamic DAGs

---

## Expert
- Automatic Metadata extraction and Lineage

```python
inlet = File("https://api.coindesk.com/v1/bpi/historical
             /close.json?start={{ ds }}&end={{ ds }}")
outlet = File("s3a://bucketx/currency_rates")
op1 = SimpleHttpOperator(task_id="get_currency",
                         endpoint=inlet.fs_path,
                         inlets={"datasets": [inlet,]},
                         outlet={"datasets": [outlets,]})

outlet = File("s3a://bucketx/sparkified/")
op2 = SparkSubmitOperator(task_id="load_into_table",
                          inlets={"auto": True},
                          outlets={"datasets": [outlet,]},
                          sql=sql)
op2.set_upstream(op1)

outlet = Table()
op3 = DruidOperator(inlets={"auto": True},
                   outlets={"datasets": [outlet,])
```
---

## Enterprise ;-)
- Save it is somewhere
