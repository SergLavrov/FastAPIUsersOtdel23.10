from fastapi import FastAPI
import psycopg2
from dotenv import dotenv_values
from pydantic import BaseModel
import traceback

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
    return {"message": "Start Server"}


class vm_get_workers(BaseModel):
    id: int
    firstName: str
    position: str
    phone: str


class vm_get_worker(BaseModel):
    id: int
    firstName: str
    surName: str
    email: str
    phone: str
    address: str
    position: str
    salary: float
    departmentName: str


@app.get("/get-workers")
def get_workers():
    try:
        cursor.execute("""
            SELECT id, firstName, position, phone
            FROM worker;
        """)
        result = cursor.fetchall()
        list_workers = []
        for worker in result:
            list_workers.append(vm_get_workers(
                id=worker[0],
                firstName=worker[1],
                position=worker[2],
                phone=worker[3]
            ))

        return {"workers": list_workers}
    except:
        return {"error": traceback.format_exc()}
