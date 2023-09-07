# gl-de-ch
Globant Data Engineering Coding Challenge

## How to run the code

### Prerequisites
- Python 3.9
- Docker

### Steps
1. Clone the repository
2. Run `docker-compose up` in the root folder
3. Open a browser and go to `http://127.0.0.1:8000/docs`
4. Click on the `POST` button and then on `Try it out`
5. Select a file to upload and click on `Execute`, you can pick one of the files in the `testdata` folder

## SQL Queries

Number of employees hired for each job and department in 2021 divided by quarter. The
table must be ordered alphabetically by department and job.

```sql
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
```

### Results Sample

|department|job|Q1|Q2|Q3|Q4|
|----------|---|--|--|--|--|
|Accounting|Actuary|0|1|0|0|
|Accounting|Budget/Accounting Analyst III|0|1|0|0|
|Accounting|Desktop Support Technician|0|0|1|0|
|Accounting|Food Chemist|1|0|0|0|
|Accounting|Graphic Designer|0|1|0|0|
|Accounting|Junior Executive|0|0|1|0|
|Accounting|Media Manager III|0|1|0|0|
|Accounting|Programmer Analyst IV|0|0|0|1|
|Accounting|Programmer III|0|0|1|0|
|Accounting|Senior Cost Accountant|0|0|0|1|
|Accounting|Senior Developer|0|0|0|1|
|Accounting|Statistician I|0|0|0|1|
|Accounting|Statistician II|0|0|0|2|
|Accounting|VP Accounting|0|0|1|0|
|Accounting|Web Designer I|0|0|0|1|
|Accounting|Web Designer III|0|0|0|1|
|Accounting|Web Developer I|0|1|0|0|
|Accounting|Web Developer III|0|0|0|1|
|Business Development|Account Executive|0|2|0|0|
|Business Development|Account Representative III|0|1|0|0|
|Business Development|Accountant IV|0|1|0|0|
|Business Development|Accounting Assistant I|0|0|1|0|
|Business Development|Actuary|0|0|1|0|
|Business Development|Administrative Assistant I|1|0|0|0|
|Business Development|Administrative Assistant III|1|0|0|0|
|Business Development|Administrative Officer|0|1|0|0|


List of ids, name and number of employees hired of each department that hired more
employees than the mean of employees hired in 2021 for all the departments, ordered
by the number of employees hired (descending).

```sql
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
```

### Results Sample

|id|department|hired|
|--|----------|-----|
|8|Support|113|
|5|Engineering|108|
|6|Human Resources|103|
|7|Services|102|
|4|Business Development|84|
|9|Marketing|81|
|3|Research and Development|69|
