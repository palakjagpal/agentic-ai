from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os
import certifi

app=FastAPI()

load_dotenv()

mongo_uri=os.getenv("MONGO_URI")

MONGO_URL=mongo_uri

#tlsCAFile tells MongoClient : Here is the file containing trusted Certificate Authorities that should be used to verify the server's TLS/SSL certificate.
#certifi provides a bundle of trusted CA certificates.
#certifi.where() : "ell me where the trusted CA certificate file is located.
client = MongoClient(
    MONGO_URL, tlsCAFile=certifi.where()
)

#db represents your MongoDB database.
db=client["employee_management"]

#employee_collection represents your MongoDB collection.
employee_collection=db["employees"]

class Employee(BaseModel):
    name : str
    age : int
    department : str
    salary : float

@app.get("/getallemp")
def getAll():
    employees = list(employee_collection.find())
    for e in employees:
        e["_id"]=str(e["_id"])
    return{
        "message":"All Employees fetched successfully",
        "data":employees
    }

@app.get("/getbydept/{department}")
def getBydept(department:str):
    employees = list(employee_collection.find({"department":department}))
    for e in employees:
        e["_id"]=str(e["_id"])
    return{
        "message":f"Employees from {department} department fetched successfully",
        "data":employees
    }

@app.get("/getbyname/{name}")
def getbyname(name :str):
    employee = employee_collection.find_one({"name":name})
    if employee:
        employee["_id"]=str(employee["_id"])
        return{
            "message":"Employee fetched successfully",
            "data":employee
        }
    else:
        return{
            "message":f"No employee found with name {name}"
        }


@app.get("/getbyid/{id}")
def getbyid(id:str):
    employee = employee_collection.find_one({"_id":ObjectId(id)})
    if employee:
        employee["_id"]=str(employee["_id"])
        return{
            "message":f"Employee with id {id} fetched successfully",
            "data":employee
        }
    else:
        return{
            "message":f"No employee found with id {id}"
        }


@app.post("/addemp")
def app_emp(employee : Employee):

    #This converts the Pydantic model object into a Python dictionary.
    new_emp = employee.model_dump()

    #MongoDB returns information about the insertion.
    result = employee_collection.insert_one(new_emp)

    #result.inserted_id : This is the unique ID MongoDB generated for the newly inserted document.
    #new_emp["_id"] : This adds the MongoDB ID to our Python dictionary.
    #str() : MongoDB's _id is usually an ObjectId, not a normal Python string.This makes it easier for FastAPI to return the value as JSON.
    new_emp["_id"]=str(result.inserted_id) 
    return{
        "message":"Employee added successfully",
        "data":new_emp
    }

@app.put("/updateEmp/{emp_id}")
def updateEmp(emp_id:str, employee:Employee):
    updated_emp = employee.model_dump()
    result = employee_collection.update_one(
        {"_id":ObjectId(emp_id)},
        {"$set":updated_emp})
    if result.modified_count==1:
        return{
            "message":"Employee updated successfully",
            "data":updated_emp
        }
    else:
        return{
            "message":"No employee found with the given ID"
        }

@app.delete("/delEmp/{emp_id}")
def delEmp(emp_id : str):
    result = employee_collection.delete_one(
        {"_id":ObjectId(emp_id)}
    )
    if result.deleted_count==1:
        return{
            "message":"Employee deleted successfully",
            "data":emp_id
        }
    else:
        return{
            "message":"No employee found with the given ID"
        }