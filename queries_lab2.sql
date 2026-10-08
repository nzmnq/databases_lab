SELECT 
    name AS 'Назва_корабля', 
    class AS 'Клас_корабля'
FROM Ships 
WHERE name = class 
ORDER BY name ASC;

SELECT DISTINCT 
    SUBSTRING_INDEX(SUBSTRING_INDEX(TRIM(name), ' ', 2), ' ', -1) AS 'Прізвище_пасажира_на_С'
FROM Passenger 
WHERE SUBSTRING_INDEX(SUBSTRING_INDEX(TRIM(name), ' ', 2), ' ', -1) LIKE 'C%';

SELECT DISTINCT 
    L1.model AS 'Модель_ноутбука_1', 
    L2.model AS 'Модель_ноутбука_2', 
    L1.hd AS 'Спільний_обєм_диску', 
    L1.ram AS 'Спільний_обєм_RAM'
FROM Laptop L1 
JOIN Laptop L2 ON L1.hd = L2.hd AND L1.ram = L2.ram AND L1.model > L2.model;

SELECT DISTINCT 
    maker AS 'Виробник_тільки_ПК'
FROM Product 
WHERE type = 'PC' 
  AND NOT (maker = ANY (SELECT maker FROM Product WHERE type = 'Laptop'));

SELECT DISTINCT 
    Product.maker AS 'Виробник_Принтерів_та_ПК_з_мін_RAM'
FROM Product 
JOIN PC ON Product.model = PC.model 
WHERE PC.ram = (SELECT MIN(ram) FROM PC) 
  AND Product.maker IN (SELECT maker FROM Product WHERE type = 'Printer');

SELECT 
    trip_no AS 'Номер_рейсу', 
    ID_comp AS 'Код_компанії', 
    plane AS 'Тип_літака', 
    CONCAT('from ', TRIM(town_from), ' to ', TRIM(town_to)) AS 'Опис_маршруту', 
    time_out AS 'Час_вильоту', 
    time_in AS 'Час_прильоту'
FROM Trip;

SELECT DISTINCT 
    model AS 'Модель_ПК', 
    price AS 'Ціна_ПК'
FROM PC 
WHERE price > (SELECT MIN(price) FROM Laptop);

SELECT * FROM (
    SELECT DISTINCT 
        P1.maker AS 'Виробник', 
        (SELECT MIN(speed) 
         FROM PC 
         JOIN Product P2 ON PC.model = P2.model 
         WHERE P2.maker = P1.maker
        ) AS 'Мінімальна_швидкість'
    FROM Product P1 
    WHERE P1.type = 'PC'
) AS SubQuery
WHERE `Мінімальна_швидкість` >= 500;

SELECT 
    IFNULL(O.point, O_o.point) AS 'Номер_пункту', 
    DATE(IFNULL(O.date, O_o.date)) AS 'Дата_прийому',
    CASE
        WHEN O.out_sum IS NULL THEN 'once a day'
        WHEN O_o.out_sum IS NULL THEN 'more than once a day'
        WHEN O_o.out_sum > O.out_sum THEN 'once a day'
        WHEN O.out_sum > O_o.out_sum THEN 'more than once a day'
        ELSE 'both'
    END AS 'Статус_лідера'
FROM (
    SELECT point, date, SUM(`out`) AS out_sum 
    FROM Outcome 
    GROUP BY point, date
) O
LEFT JOIN (
    SELECT point, date, SUM(`out`) AS out_sum 
    FROM Outcome_o 
    GROUP BY point, date
) O_o ON O.point = O_o.point AND O.date = O_o.date
UNION
SELECT 
    IFNULL(O.point, O_o.point) AS 'Номер_пункту', 
    DATE(IFNULL(O.date, O_o.date)) AS 'Дата_прийому',
    CASE
        WHEN O.out_sum IS NULL THEN 'once a day'
        WHEN O_o.out_sum IS NULL THEN 'more than once a day'
        WHEN O_o.out_sum > O.out_sum THEN 'once a day'
        WHEN O.out_sum > O_o.out_sum THEN 'more than once a day'
        ELSE 'both'
    END AS 'Статус_лідера'
FROM (
    SELECT point, date, SUM(`out`) AS out_sum 
    FROM Outcome 
    GROUP BY point, date
) O
RIGHT JOIN (
    SELECT point, date, SUM(`out`) AS out_sum 
    FROM Outcome_o 
    GROUP BY point, date
) O_o ON O.point = O_o.point AND O.date = O_o.date
ORDER BY 1, 2;

SELECT 
    P.type AS 'Тип_продукції', 
    U.model AS 'Модель_продукції', 
    ROUND(AVG(U.price), 2) AS 'Середня_ціна'
FROM (
    SELECT model, price FROM PC
    UNION ALL
    SELECT model, price FROM Laptop
    UNION ALL
    SELECT model, price FROM Printer
) U
JOIN Product P ON U.model = P.model
GROUP BY P.type, U.model
ORDER BY P.type, U.model;