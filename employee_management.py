from fastapi import FastAPI
from pydantic import BaseModel

class Employee(BaseModel):
    name : str
    age : int
    department : str
    salary : float

app=FastAPI()

data=[
    {
        "name":"John",
        "age":30,
        "department":"HR",
        "salary":50000.0
    },
    {
        "name":"Alice",
        "age":25,
        "department":"IT",
        "salary":60000.0
    },
    {
        "name":"Bob",
        "age":28,
        "department":"Finance",
        "salary":55000.0
    },{
        "name":"Eve",
        "age":35,
        "department":"IT",
        "salary":70000.0
    },
    {
        "name":"Charlie",
        "age":32,
        "department":"HR",
        "salary":52000.0
    },
    {
        "name":"David",
        "age":29,
        "department":"Finance",
        "salary":58000.0
    }
]

#get all employees
@app.get("/getallemp")
def getAll():
    return{
        "message":"All Employees fetched successfully",
        "data":data
    }

#get by department
@app.get("/getbydept/{department}")
def getByDept(department:str):
    emp_dept=[]
    for index,e in enumerate(data):
        if e["department"]==department:
            emp_dept.append(e)
    return{
        "message":f"Employees with department {department} fetched successfully",
        "data":emp_dept
    }

#get by name
@app.get("/getbyname/{name}")
def getbyname(name:str):
    for emp in data:
        if emp["name"]==name:
            return{
                "message": "Employee fetched successfully",
                "data":emp
            }
    return{
        "message":f"No employee found with name {name}"
    }

#get by id
@app.get("/getbyempid/{id}")
def getbyempid(id:int):
    for index,emp in enumerate(data):
        if index==id:
            return{
                "message":f"Employee with id {id} fetched successfully",
                "data":emp
            }
    return{
        "message":f"No employee found with id {id}"
    }

#add new employee
@app.post("/addEmp")
def addEmp(emp:Employee):
    newEmp={
        "id":len(data)+1,
        **emp.model_dump()
    }
    data.append(newEmp)
    return{
        "message":"Employee added successfully",
        "data":newEmp
    }

#update emp
@app.put("/updateemp/{id}")
def update_emp(id:int,emp:Employee):
    for index,e in enumerate(data):
        if index==id:
            data[index].update(emp.model_dump())
            return{
                "message":f"Employee with id {id} updated successfully",
                "data":data
            }
    return{
        "message":f"No employee found with id {id}"
    }

#delete emp
@app.delete("/deleteemp/{id}")
def delete_emp(id:int):
    for index,e in enumerate(data):
        if index==id:
            deleted_emp=data.pop(index)
            return{
                "message":f"Employee with id {id} deleted successfully",
                "deleted_emp":deleted_emp
            }
    return{
        "message":f"No employee found with id {id}"
    }