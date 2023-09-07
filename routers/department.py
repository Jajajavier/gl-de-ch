import codecs
import csv
from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from schemes.department import Department
from config.database import Session
from config.upload_file import MIN_ROWS, MAX_ROWS
from services.department import DepartmentService

department_router = APIRouter()


@department_router.post(
    '/departments/upload',
    tags=['departments'])
def upload_file(file: UploadFile = File(...)):
    """Create departments from CSV file"""
    csv_reader = csv.DictReader(
        codecs.iterdecode(file.file, 'utf-8'),
        delimiter=",",
        fieldnames=['id', "department"])
    departments = list(csv_reader)
    n_departments = len(departments)
    if n_departments < MIN_ROWS:
        file.file.close()
        return JSONResponse(status_code=409, content={
            "message": "The file needs more rows",
            "min_rows": MIN_ROWS
        })
    elif n_departments > MAX_ROWS:
        file.file.close()
        return JSONResponse(status_code=409, content={
            "message": "The file needs less rows",
            "max_rows": MAX_ROWS
        })
    else:
        db = Session()
        departments = [Department(**department) for department in departments]
        DepartmentService(db).create_departments(departments)
        file.file.close()
        return JSONResponse(status_code=201, content={
            "message": "The file has been uploaded"
        })

