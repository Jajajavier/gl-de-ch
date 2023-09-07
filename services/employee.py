from sqlalchemy import insert
from typing import List
from models.employee import EmployeeModel
from schemes.employee import Employee


class EmployeeService():

    def __init__(self, db) -> None:
        # Bind the database session to the instance
        self.db = db

    def create_employees(self, employees: List[Employee]):
        try:
            result = self.db.execute(
                insert(EmployeeModel),
                employees
            )
            self.db.commit()
            return result
        except Exception as e:
            self.db.rollback()
            with self.db.no_autoflush:
                for employee in employees:
                    employee.employee = employee.employee.strip()
                    new_employee = EmployeeModel(**employee.dict())
                    self.db.merge(new_employee)
                self.db.commit()
            return e
