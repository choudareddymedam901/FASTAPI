from os import name

from fastapi import FastAPI
from realtime import BaseModel
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def test():
    return {"message": "Hello World"}

@app.get("/name")
def name1():
    return {"name": "My Name is choudareddy, I'm learning FastAPI and Python. I have 2 years of experience in Python and Django. I have worked on multiple projects using Django and FastAPI."}

students = {1:"John", 2:"Alice", 3:"Bob"}
students = {}

class Student(BaseModel):
    student_id: int
    name: str

@app.get("/students")
def get_students():
    return students

@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id in students:
        return {"id": student_id, "name": students[student_id]}
    else:
        return {"error": "Student not found"}

@app.get("/add_students")
def add_student(student_id: int, name: str):
    if student_id in students:
        return {"error": "Student ID already exists"}
    else:
        students[student_id] = name
        return {"message": "Student added successfully", "id": student_id, "name": name}

@app.post("/add_students_post")
def add_student_post(student: Student):
    if student.student_id in students:
        return {"error": "Student ID already exists"}
    else:
        students[student.student_id] = student.name
        return {"message": "Student added successfully", "id": student.student_id, "name": student.name}