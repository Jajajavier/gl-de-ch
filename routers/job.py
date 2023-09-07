import codecs
import csv
from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from schemes.job import Job
from config.database import Session
from config.upload_file import MIN_ROWS, MAX_ROWS
from services.job import JobService

job_router = APIRouter()

@job_router.post(
    '/jobs/upload',
    tags=['jobs'])
def upload_file(file: UploadFile = File(...)):
    """Create jobs from CSV file"""
    csv_reader = csv.DictReader(
        codecs.iterdecode(file.file, 'utf-8'),
        delimiter=",",
        fieldnames=['id', "job"])
    jobs = list(csv_reader)
    n_jobs = len(jobs)
    if n_jobs < MIN_ROWS:
        file.file.close()
        return JSONResponse(status_code=409, content={
            "message": "The file needs more rows",
            "min_rows": MIN_ROWS
        })
    elif n_jobs > MAX_ROWS:
        file.file.close()
        return JSONResponse(status_code=409, content={
            "message": "The file needs less rows",
            "max_rows": MAX_ROWS
        })
    else:
        db = Session()
        jobs = [Job(**job) for job in jobs]
        JobService(db).create_jobs(jobs)
        file.file.close()
        return JSONResponse(status_code=201, content={
            "message": "The file has been uploaded"
        })
