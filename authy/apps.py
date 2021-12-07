from django.apps import AppConfig


class AuthyConfig(AppConfig):
    name = 'authy'


import psycopg2

try:
    db = psycopg2.connect(
        "dbname='postgres' user='abhishek@socialite-db' host='socialite-db.postgres.database.azure.com' password='Aadarsh@123'")
    print("connection established")
except Exception as e:
    print(e)
    print("not done")
