# Store Sales Report project

Airflow project based on Udemy's course "Apache Airflow | A Real-Time & Hands-On Course on Airflow"

# Run it

First install docker and docker-compose.

Input the right value at the variable ```AIRFLOW__SMTP__SMTP_PASSWORD``` in the docker-compose-LocalExecutor.yml file.

Then run the command:

```
$ sudo docker-compose -f docker-compose-LocalExecutor.yml up -d
```
