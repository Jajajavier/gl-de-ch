from sqlalchemy import insert
from typing import List
from models.department import DepartmentModel
from schemes.department import Department


class DepartmentService():

    def __init__(self, db) -> None:
        # Bind the database session to the instance
        self.db = db

    def create_departments(self, departments: List[Department]):
        try:
            result = self.db.execute(
                insert(DepartmentModel),
                departments
            )
            self.db.commit()
            return result
        except Exception as e:
            self.db.rollback()
            with self.db.no_autoflush:
                for department in departments:
                    department.department = department.department.strip()
                    new_department = DepartmentModel(**department.dict())
                    self.db.merge(new_department)
                self.db.commit()
            return e
