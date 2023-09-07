-- List of ids, name and number of employees hired of each department that hired more
-- employees than the mean of employees hired in 2021 for all the departments, ordered
-- by the number of employees hired (descending).

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
