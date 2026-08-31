from fastapi import FastAPI

app=FastAPI()

@app.get("/students/{studentID}")
def get_student(studentID:int):
    return{
        "studentID":studentID
    }
