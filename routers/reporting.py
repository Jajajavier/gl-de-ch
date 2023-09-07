from fastapi import APIRouter
from services.reporting import ReportingService
from config.database import Session

reporting_router = APIRouter()

@reporting_router.get("/get-employee-hires-by-department-job-quarter-2021", tags=["reporting"])
def get_employee_hires_by_department_job_quarter_2021():
    db = Session()  # Create a new session instance using the Session object from config/database.py
    try:
        results = ReportingService(db).get_employee_hires_by_department_job_quarter_2021()
        return results
    finally:
        db.close()

@reporting_router.get("/get-departments-above-mean-hires-2021", tags=["reporting"])
def get_departments_above_mean_hires_2021():
    db = Session()  # Create a new session instance using the Session object from config/database.py
    try:
        results = ReportingService(db).get_departments_above_mean_hires_2021()
        return results
    finally:
        db.close()