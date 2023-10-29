
# Сущности:
# 1.	Работники
# 	a.	Имя
# 	b.	Фамилия
# 	c.	Электронная почта
# 	d.	Телефон
# 	e.	Адрес
# 	f.	Должность
# 	g.      Зарплата
#
# 2.	Отдел
# 	a.	Название
# 	b.	Средняя зарплата
# 	c.	Количество сотрудников
#
# В отделе может работать несколько сотрудников, один сотрудник может работать только в одном отделе.
#
# Написать endpoints:
# 1.	Вывод всех сотрудников в виде (Имя, должность, телефон)
# 2.	Получение полной информации о сотруднике
# 3.	Добавление сотрудника
# 4.	Удаление сотрудника
# 5.	Вывод сотрудников определённого отдела (Имя, Фамилия, Должность)
# 6.	Получение информации об отделах (Название, количество сотрудников)
# 7.	Добавление отдела
# 8.	Добавление/изменение у сотрудника отдела
# 9.	Удаление отдела (Если есть сотрудники, выдать информацию: удаление невозможно)



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

# Для проверки связи с локальным сервером
@app.get("/")
def root():
    return {"message": "Start Server"}

# 1.	Вывод всех сотрудников в виде (Имя, должность, телефон)
class vm_get_workers(BaseModel):
    id: int
    firstName: str
    position: str
    phone: str

# 2.	Получение полной информации о сотруднике
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

# 3.	Добавление сотрудника
class vm_add_worker(BaseModel):
    firstName: str
    surName: str
    email: str
    phone: str
    address: str
    position: str
    salary: float
    department_id: int


# 4. Удаление сотрудника
class vm_delete_worker(BaseModel):
    id: int


# 5.	Вывод сотрудников определённого отдела (Имя, Фамилия, Должность)
class vm_get_department_workers(BaseModel):
    id: int
    departmentName: str
    firstName: str
    surName: str
    position: str


# 6.	Получение информации об отделах (Название, количество сотрудников)
class vm_info_department(BaseModel):
    id: int
    departmentName: str
    quantityWorkers: int


# 7.	Добавление отдела
class vm_add_department(BaseModel):
    id: int
    name: str
    averageSalary: float
    countWorker: int


# 9.	Удаление отдела (Если есть сотрудники, выдать информацию: удаление невозможно)
class vm_delete_department(BaseModel):
    id: int
    count_worker: int





# 1.	Вывод всех сотрудников в виде (Имя, должность, телефон)
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


# 2.	Получение полной информации о сотруднике
@app.get("/get-worker/{worker_id}")
def get_worker(worker_id: int):
    try:
        cursor.execute(f"""
            SELECT w.id, w.firstName, w.surName, w.email, w.phone, w.address, w.position, w.salary, d.name
            FROM worker w
            LEFT JOIN department d ON w.department_id = d.id
            WHERE w.id = {worker_id};
        """)
        result = cursor.fetchone()
        worker = vm_get_worker(
            id=result[0],
            firstName=result[1],
            surName=result[2],
            email=result[3],
            phone=result[4],
            address=result[5],
            position=result[6],
            salary=result[7],
            departmentName=result[8]
        )
        return {"worker": worker}
    except:
        return {"error": traceback.format_exc()}


# 3.	Добавление сотрудника
@app.post("/add-worker")
def add_worker(worker: vm_add_worker):
    try:
        cursor.execute(f"""
            INSERT INTO worker (firstName, surName, email, phone, address, position, salary, department_id)
            VALUES ('{worker.firstName}', '{worker.surName}', '{worker.email}', '{worker.phone}', '{worker.address}', '{worker.position}', {worker.salary}, {worker.department_id});
        """)
        connect.commit()

        return {"message": "Success"}
    except:
        return {"error": traceback.format_exc()}


# 4. Удаление сотрудника
@app.delete("/delete-worker/{worker_id}")
def delete_worker(worker_id: int):
    try:
        cursor.execute(f"DELETE FROM worker WHERE id = {worker_id}")

        connect.commit()
        return {"message": "Success"}
    except:
        return {"error": traceback.format_exc()}



# 5.	Вывод сотрудников определённого отдела (Имя, Фамилия, Должность)
@app.get("/get-department-workers/{depart_id}")
def get_department_workers(depart_id: int):
    try:
        cursor.execute(f"""
            SELECT d.id, d.name, w.firstName, w.surName, w.position
            FROM department d
            LEFT JOIN worker w ON d.id = w.department_id
            WHERE d.id = {depart_id};
        """)

        result = cursor.fetchall()

        return {"workers of department": result}
    except:
        return {"error": traceback.format_exc()}



# 6.	Получение информации об отделах (Название, количество сотрудников)
@app.get("/info-department/{depart_id}")
def info_department(depart_id: int):
    try:
        cursor.execute(f"""
            SELECT d.id, d.name, d.count_worker
            FROM department d
            WHERE d.id = {depart_id};
        """)
        result = cursor.fetchone()
        d = vm_info_department(
            id=result[0],
            departmentName=result[1],
            quantityWorkers=result[2]
        )
        return {"department info": d}
    except:
        return {"error": traceback.format_exc()}


# 7.	Добавление отдела
@app.post("/add-department")
def add_department(department: vm_add_department):
    try:
        cursor.execute(f"""
            INSERT INTO department (id, name, average_salary, count_worker)
            VALUES ('{id}', '{department.name}', '{department.averageSalary}', '{department.countWorker}')
        """)

        connect.commit()
        return {"message": "Success"}
    except:
        return {"error": traceback.format_exc()}


# 9.	Удаление отдела (Если есть сотрудники, выдать информацию: удаление невозможно)
@app.delete("/delete-department/{department_id}")
def delete_department(department_id, count_worker: int):
    try:
        # cursor.execute(f"DELETE FROM department WHERE id = {department_id} AND {count_worker} IS NULL")

        # cursor.execute(f"DELETE FROM department WHERE id = {department_id} IN (SELECT {count_worker} FROM department WHERE {count_worker} IS NULL)")

        connect.commit()
        return {"message": "Success"}

    except:
        return {"error": traceback.format_exc()}


