from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()
#pip install psycopg2-binary
db_url = "postgresql://neondb_owner:npg_i6bKfTIXj3uL@ep-still-sea-ax8k0gx2-pooler.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def get_connection_url():
    conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
    return conn

class Students(BaseModel):
    id: int
    name: str
    age: int

def save_student_to_file(student):
    with open("students.txt", "a") as file:
        file.write(f"{student['id']}, {student['name']}, {student['age']}\n")

@app.post("/students")
def create_student(student: Students):
    final_data = student.model_dump()  # Convert the Pydantic model to a dictionary
    save_student_to_file(final_data)
    return {"message": "Student created successfully", "student": final_data}

@app.post("/students/db/insert")
def store_student_in_db(student: Students):
    conn = get_connection_url()
    cursor = conn.cursor()
    insert_query = "INSERT INTO student (id, name, age) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (student.id, student.name, student.age))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Student stored in database successfully", "student": student.model_dump()}

@app.put("/students/db/update")
def update_student_in_db(student: Students):
    conn = get_connection_url()
    cursor = conn.cursor()
    update_query = "UPDATE student SET name = %s, age = %s WHERE id = %s"
    cursor.execute(update_query, (student.name, student.age, student.id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Student updated in database successfully", "student": student.model_dump()}

@app.delete("/students/db/delete/{student_id}")
def delete_student_from_db(student_id: int):
    conn = get_connection_url()
    cursor = conn.cursor()
    delete_query = "DELETE FROM student WHERE id = %s"
    cursor.execute(delete_query, (student_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Student deleted from database successfully", "student_id": student_id}