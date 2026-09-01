#The gift inside is your function. The wrapping paper adds extra feature (like bows or patterns) around your gift without changing what is inside the box.
#def get_students() is your normal Python function.
    #@app.get("/students") is the decorator.
    #The @ decorator tells FastAPI:
    #"Hey FastAPI! Take this function and attach it to the web server. Whenever someone visits the website at /students using a GET request, run this function!"

from fastapi import FastAPI
#Imports BaseModel from Pydantic, which FastAPI uses to define data schemas, perform automatic data validation, and parse request bodies.
#Pydantic is a popular Python library used for data validation, parsing, and settings management
#In Pydantic, BaseModel is the foundational class used to define schemas, data models, and validation rules
from pydantic import BaseModel

#Defines a custom data class named Student that inherits from Pydantic's BaseModel. This defines the shape of JSON payload data sent in POST requests.
class Student(BaseModel):
    name : str
    age : int
    course : str

app= FastAPI()


#A decorator registering an HTTP GET endpoint at the URL path /queryparam.
#Defines the function to run when /queryparam is called. Because name is declared in the function signature but not in the path string, FastAPI automatically treats it as a URL query parameter (e.g., /queryparam?name=John).
#http://127.0.0.1:8000/queryparam?name=Alice
@app.get("/queryparam")
def get_query(name : str):
    return{
        "name" : name
    }

#Registers an HTTP GET endpoint with a dynamic path parameter denoted by {student_id}.
#http://127.0.0.1:8000/students/1
@app.get("/students/{student_id}")
def get_studentbyid(student_id:int):
    return{
        "student details":student_id
    }

#Initializes an empty Python list named data to act as an in-memory database during server runtime.
data = []


#Defines the function handling requests to fetch all stored records.
#http://127.0.0.1:8000/getall
@app.get("/getall")
def get_all():
    return data


#Registers an HTTP GET endpoint at /getoneoutofall/{name}, where {name} is a dynamic string path parameter.
##http://127.0.0.1:8000/getoneoutofall/Alice
@app.get("/getoneoutofall/{name}")
def get_one(name : str):
    ##Iterates through each dictionary currently stored in the data list.
    for item in data:
        #Checks if the current dictionary's "name" key matches the queried path parameter name
        if item["name"]==name:
            #If matched, immediately returns the matching dictionary as JSON and exits the function.
            return item
    return{
        "data":"not found"
    }


#Registers an HTTP POST endpoint at /adddata used for creating new records.
#http://127.0.0.1:8000/adddata
#body: {"name": "Alice", "age": 20, "course": "CS"}
@app.post("/adddata")
def add_data(student:Student):
    #Starts constructing a new dictionary to store in the list.
    newData = {
        "id":len(data)+1,
        **student.model_dump() 
        #Generates a simple incremental ID based on the current length of the data array.
        #Unpacks the key-value pairs of the Pydantic model dictionary into newData (converts Student(name="Alice", age=20, course="CS") to "name": "Alice", "age": 20, "course": "CS").z
        #}The ** prefix "unpacks" the key-value pairs from the dictionary into the outer newData dictionary.
        #student.model_dump() is a built-in method provided by Pydantic V2. It converts a Pydantic model instance (in your code, the student object) into a standard Python dict.

    }
    data.append(newData)
    return newData


@app.put("/updateStudent/{student_id}")
def update_student(student_id : int, student : Student):
    for s in data :
        if s["id"] == student_id:
            s.update(student.model_dump())
            return s
    return{
        "message" : "Student not found"
    }


@app.delete("/deleteStudent/{student_id}")
def delete_student(student_id : int):
    for index,s in enumerate(data):
        if s["id"] == student_id:
            deleted_student = data.pop(index)
            return{
                "message" : "Student deleted successfully",
                "deleted_student" : deleted_student
            }
    return{
        "message" : "Student not found"
    }