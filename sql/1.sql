-- Number of employees hired for each job and department in 2021 divided by quarter. The
-- table must be ordered alphabetically by department and job.

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
