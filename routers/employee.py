import codecs
import csv
from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from schemes.employee import Employee
from config.database import Session
from config.upload_file import MIN_ROWS, MAX_ROWS
from services.employee import EmployeeService

employee_router = APIRouter()

@employee_router.post(
    '/employees/upload',
    tags=['employees'])
def upload_file(file: UploadFile = File(...)):
    """Create employees from CSV file"""
    csv_reader = csv.DictReader(
        codecs.iterdecode(file.file, 'utf-8'),
        delimiter=",",
        fieldnames=[
            'id',
            "name",
            "datetime",
            "department_id",
            "job_id"])
    employees = list(csv_reader)
    n_employees = len(employees)
    if n_employees < MIN_ROWS:
        file.file.close()
        return JSONResponse(status_code=409, content={
            "message": "The file needs more rows",
            "min_rows": MIN_ROWS
        })
    elif n_employees > MAX_ROWS:
        file.file.close()
        return JSONResponse(status_code=409, content={
            "message": "The file needs less rows",
            "max_rows": MAX_ROWS
        })
    else:
        db = Session()
        employees = [Employee(**employee) for employee in employees
                     if (employee['name'] and employee['datetime'] and employee['department_id'] and employee['job_id'])]
        EmployeeService(db).create_employees(employees)
        file.file.close()
        return JSONResponse(status_code=201, content={
            "message": "The file has been uploaded"
        })
