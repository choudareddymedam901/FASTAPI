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

class CourseInformation(BaseModel):
    course_id: int
    course_name: str
    credits: int
    instructor: str


#create a new post endpoint to create