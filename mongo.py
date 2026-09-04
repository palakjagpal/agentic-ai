from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
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
    MONGO_URL, tlsCAFIle=certifi.where()
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