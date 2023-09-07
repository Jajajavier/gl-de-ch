from sqlalchemy.sql import text

class ReportingService:

    def __init__(self, db) -> None:
        self.db = db

    def get_employee_hires_by_department_job_quarter_2021(self):
        sql = text("""
            SELECT 
                d.department, 
                j.job,
                SUM(CASE WHEN QUARTER(e.datetime) = 1 THEN 1 ELSE 0 END) AS Q1,
                SUM(CASE WHEN QUARTER(e.datetime) = 2 THEN 1 ELSE 0 END) AS Q2,
                SUM(CASE WHEN QUARTER(e.datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
                SUM(CASE WHEN QUARTER(e.datetime) = 4 THEN 1 ELSE 0 END) AS Q4
            FROM 
                employees e
            JOIN 
                departments d ON e.department_id = d.id
            JOIN 
                jobs j ON e.job_id = j.id
            WHERE 
                YEAR(e.datetime) = 2021
            GROUP BY 
                d.department, j.job
            ORDER BY 
                d.department ASC, j.job ASC;
        """)
        
        result = self.db.execute(sql).fetchall()
        return [row._asdict() for row in result]

    def get_departments_above_mean_hires_2021(self):
        sql = text("""
            SELECT 
                d.id,
                d.department,
                COUNT(e.id) as hired
            FROM 
                departments d
            JOIN 
                employees e ON d.id = e.department_id
            WHERE 
                YEAR(e.datetime) = 2021
            GROUP BY 
                d.id, d.department
            HAVING 
                COUNT(e.id) > (
                    SELECT 
                        AVG(employees_count) 
                    FROM (
                        SELECT 
                            COUNT(*) as employees_count
                        FROM 
                            employees e
                        WHERE 
                            YEAR(e.datetime) = 2021
                        GROUP BY 
                            e.department_id
                    ) AS sub
                )
            ORDER BY 
                COUNT(e.id) DESC;
        """)
        
        result = self.db.execute(sql).fetchall()
        return [row._asdict() for row in result]