from fastapi import FastAPI, HTTPException
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

@app.get("/students/db/{student_id}")
def get_student_details_from_db(student_id: int):
    conn = None
    cursor = None
    try:
        conn = get_connection_url()
        cursor = conn.cursor()
        select_query = "SELECT * FROM student WHERE id = %s"
        cursor.execute(select_query, (student_id,))
        student = cursor.fetchone()
        if student is None:
            raise HTTPException(
                status_code=404,
                detail=f"Student with ID {student_id} not found"
            )
        return {"status": "success", "student": student}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching student details: {str(e)}"
        )
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()