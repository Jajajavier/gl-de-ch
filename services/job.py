from sqlalchemy import insert
from typing import List
from models.job import JobModel
from schemes.job import Job


class JobService():

    def __init__(self, db) -> None:
        # Bind the database session to the instance
        self.db = db

    def create_jobs(self, jobs: List[Job]):
        try:
            result = self.db.execute(
                insert(JobModel),
                jobs
            )
            self.db.commit()
            return result
        except Exception as e:
            self.db.rollback()
            with self.db.no_autoflush:
                for job in jobs:
                    job.job = job.job.strip()
                    new_job = JobModel(**job.dict())
                    self.db.merge(new_job)
                self.db.commit()
            return e
