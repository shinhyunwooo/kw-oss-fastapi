from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

FILE_NAME = "courses.json"


class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str


def read_courses():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []


def write_courses(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.get("/")
def root():
    return {"msg": "FastAPI 강좌 기록 API 입니다."}


@app.get("/courses")
def get_courses():
    return read_courses()


@app.post("/courses")
def add_course(course: Course):
    data = read_courses()
    new_course = course.model_dump()
    data.append(new_course)
    write_courses(data)
    return {
        "msg": "강좌가 성공적으로 추가되었습니다.",
        "course": new_course
    }