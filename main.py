from fastapi import FastAPI
import psycopg2
from dotenv import dotenv_values

config = dotenv_values(".env")

connect = psycopg2.connect(
    host=config["HOST"],
    port=config["PORT"],
    database=config["DBNAME"],
    user=config["USERID"],
    password=config["USERPW"]
)

cursor = connect.cursor()

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}
