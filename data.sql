CREATE DATABASE IF NOT EXISTS smart_parking_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE smart_parking_db;

DROP TABLE IF EXISTS parking_tickets;
DROP TABLE IF EXISTS parking_sessions;
DROP TABLE IF EXISTS parking_reservations;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS regular_cards;
DROP TABLE IF EXISTS client_enterprises;
DROP TABLE IF EXISTS client_individuals;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS parking_spots;
DROP TABLE IF EXISTS spot_types;
DROP TABLE IF EXISTS parking_zones;
DROP TABLE IF EXISTS parking_stations;
DROP TABLE IF EXISTS retail_chains;

CREATE TABLE retail_chains (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    edrpou VARCHAR(10) NOT NULL UNIQUE,
    website VARCHAR(150),
    support_phone VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE parking_stations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chain_id INT NOT NULL,
    name VARCHAR(120) NOT NULL,
    city VARCHAR(50) NOT NULL,
    address VARCHAR(200) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    capacity INT NOT NULL DEFAULT 0,
    hourly_rate DECIMAL(8, 2) NOT NULL DEFAULT 30.00,
    is_24_7 BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE parking_zones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    station_id INT NOT NULL,
    code VARCHAR(20) NOT NULL,
    name VARCHAR(80) NOT NULL,
    floor_level INT NOT NULL DEFAULT 0,
    UNIQUE KEY uq_station_zone_code (station_id, code)
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE spot_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255),
    tariff_multiplier DECIMAL(4, 2) NOT NULL DEFAULT 1.00
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE parking_spots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    zone_id INT NOT NULL,
    spot_type_id INT NOT NULL,
    spot_number VARCHAR(20) NOT NULL,
    current_status ENUM('FREE', 'OCCUPIED', 'RESERVED', 'MAINTENANCE') NOT NULL DEFAULT 'FREE',
    UNIQUE KEY uq_zone_spot_number (zone_id, spot_number)
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_type ENUM('INDIVIDUAL', 'ENTERPRISE') NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    registration_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE client_individuals (
    client_id INT PRIMARY KEY,
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    tax_id VARCHAR(12) NOT NULL UNIQUE,
    driver_license VARCHAR(20) NOT NULL UNIQUE
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE client_enterprises (
    client_id INT PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    edrpou_code VARCHAR(10) NOT NULL UNIQUE,
    contact_person VARCHAR(120) NOT NULL,
    legal_address VARCHAR(250) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE regular_cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    card_number VARCHAR(32) NOT NULL UNIQUE,
    card_type ENUM('PREPAID', 'POSTPAID', 'CORPORATE_VIP') NOT NULL,
    issue_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    discount_percent DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    status ENUM('ACTIVE', 'BLOCKED', 'EXPIRED') NOT NULL DEFAULT 'ACTIVE'
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NULL,
    license_plate VARCHAR(16) NOT NULL UNIQUE,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    color VARCHAR(30)
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE parking_reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    spot_id INT NOT NULL,
    client_id INT NOT NULL,
    license_plate VARCHAR(16) NOT NULL,
    reserved_from DATETIME NOT NULL,
    reserved_to DATETIME NOT NULL,
    booking_fee DECIMAL(8, 2) NOT NULL DEFAULT 0.00,
    status ENUM('PENDING', 'CONFIRMED', 'CANCELLED', 'COMPLETED', 'NO_SHOW') NOT NULL DEFAULT 'CONFIRMED',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE parking_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    spot_id INT NOT NULL,
    card_id INT NULL,
    license_plate VARCHAR(16) NOT NULL,
    entry_time DATETIME NOT NULL,
    exit_time DATETIME NULL,
    duration_minutes INT GENERATED ALWAYS AS (
        CASE WHEN exit_time IS NOT NULL THEN TIMESTAMPDIFF(MINUTE, entry_time, exit_time) ELSE NULL END
    ) VIRTUAL,
    total_cost DECIMAL(10, 2) DEFAULT 0.00,
    status ENUM('ACTIVE', 'COMPLETED', 'OVERDUE') NOT NULL DEFAULT 'ACTIVE'
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE parking_tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL UNIQUE,
    ticket_number VARCHAR(32) NOT NULL UNIQUE,
    issue_time DATETIME NOT NULL,
    payment_status ENUM('UNPAID', 'PAID', 'EXEMPT') NOT NULL DEFAULT 'UNPAID',
    paid_time DATETIME NULL,
    paid_amount DECIMAL(10, 2) DEFAULT 0.00,
    payment_method ENUM('CASH', 'CARD', 'MOBILE_APP', 'SUBSCRIPTION') NULL
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE parking_stations
    ADD CONSTRAINT FK_stations_retail_chains
    FOREIGN KEY (chain_id) REFERENCES retail_chains(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE parking_zones
    ADD CONSTRAINT FK_zones_parking_stations
    FOREIGN KEY (station_id) REFERENCES parking_stations(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE parking_spots
    ADD CONSTRAINT FK_spots_parking_zones
    FOREIGN KEY (zone_id) REFERENCES parking_zones(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    ADD CONSTRAINT FK_spots_spot_types
    FOREIGN KEY (spot_type_id) REFERENCES spot_types(id)
    ON UPDATE CASCADE;

ALTER TABLE client_individuals
    ADD CONSTRAINT FK_client_individuals_clients
    FOREIGN KEY (client_id) REFERENCES clients(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE client_enterprises
    ADD CONSTRAINT FK_client_enterprises_clients
    FOREIGN KEY (client_id) REFERENCES clients(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE regular_cards
    ADD CONSTRAINT FK_regular_cards_clients
    FOREIGN KEY (client_id) REFERENCES clients(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE vehicles
    ADD CONSTRAINT FK_vehicles_clients
    FOREIGN KEY (client_id) REFERENCES clients(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE parking_reservations
    ADD CONSTRAINT FK_reservations_parking_spots
    FOREIGN KEY (spot_id) REFERENCES parking_spots(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    ADD CONSTRAINT FK_reservations_clients
    FOREIGN KEY (client_id) REFERENCES clients(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE parking_sessions
    ADD CONSTRAINT FK_sessions_parking_spots
    FOREIGN KEY (spot_id) REFERENCES parking_spots(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    ADD CONSTRAINT FK_sessions_regular_cards
    FOREIGN KEY (card_id) REFERENCES regular_cards(id)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE parking_tickets
    ADD CONSTRAINT FK_tickets_parking_sessions
    FOREIGN KEY (session_id) REFERENCES parking_sessions(id)
    ON DELETE CASCADE ON UPDATE CASCADE;

CREATE INDEX idx_tickets_barcode ON parking_tickets(ticket_number, payment_status);
CREATE INDEX idx_sessions_license_plate ON parking_sessions(license_plate, status);
CREATE INDEX idx_reservations_period ON parking_reservations(spot_id, reserved_from, reserved_to);
CREATE INDEX idx_spots_zone_status ON parking_spots(zone_id, current_status);
CREATE INDEX idx_clients_phone ON clients(phone);

INSERT INTO retail_chains (id, name, edrpou, website, support_phone) VALUES
(1, 'Сільпо Рітейл', '32847921', 'https://silpo.ua', '+380800301707'),
(2, 'Епіцентр К', '32490244', 'https://epicentrk.ua', '+380800202727'),
(3, 'Ашан Україна', '35443413', 'https://auchan.ua', '+380800500428'),
(4, 'Victoria Gardens ТРЦ', '40192844', 'https://victoriagardens.com.ua', '+380322595959'),
(5, 'King Cross Leopolis', '36781290', 'https://kingcross.com.ua', '+380322421999'),
(6, 'Форум Львів (Multi Ukraine)', '38901234', 'https://forum-lviv.com.ua', '+380322956999'),
(7, 'АТБ-Маркет', '30487219', 'https://atbmarket.com', '+380800500415'),
(8, 'ТРЦ Спартак', '41209384', 'https://spartak.lviv.ua', '+380322971100'),
(9, 'Метро Кеш енд Кері', '32049199', 'https://metro.ua', '+380800501401'),
(10, 'ТВК Південний', '20823490', 'https://pivdennij.com', '+380322951111');

INSERT INTO parking_stations (id, chain_id, name, city, address, latitude, longitude, capacity, hourly_rate, is_24_7) VALUES
(1, 4, 'Підземний паркінг ТРЦ Victoria Gardens', 'Львів', 'вул. Кульпарківська, 226А', 49.807185, 23.978254, 1500, 30.00, TRUE),
(2, 5, 'Паркінг King Cross Leopolis', 'Сокільники', 'вул. Стрийська, 30', 49.771210, 24.010150, 1800, 25.00, TRUE),
(3, 2, 'Автопаркінг Епіцентр Південний', 'Львів', 'вул. Городоцька, 302', 49.824510, 23.941290, 800, 20.00, FALSE),
(4, 1, 'Паркінг супермаркету Сільпо', 'Львів', 'вул. Наукова, 35А', 49.799200, 23.998410, 120, 20.00, TRUE),
(5, 3, 'Відкритий паркінг Ашан Сокільники', 'Сокільники', 'вул. Стрийська, 30', 49.772500, 24.011800, 600, 25.00, TRUE),
(6, 6, 'Критий паркінг Forum Lviv', 'Львів', 'вул. Під Дубом, 7Б', 49.850120, 24.023410, 600, 40.00, TRUE),
(7, 7, 'Паркувальний майданчик АТБ №12', 'Львів', 'вул. Шевченка, 60', 49.849200, 23.991200, 80, 15.00, TRUE),
(8, 8, 'Паркінг спортивного ТРЦ Спартак', 'Львів', 'вул. Мазепи, 1Б', 49.871100, 24.029800, 550, 30.00, TRUE),
(9, 9, 'Торговельний паркінг Metro Cash&Carry', 'Львів', 'вул. Дж. Вашингтона, 8', 49.818400, 24.075600, 450, 20.00, FALSE),
(10, 10, 'Багаторівневий паркінг ТВК Південний', 'Львів', 'вул. Щирецька, 36', 49.812300, 23.974500, 900, 25.00, TRUE);

INSERT INTO parking_zones (id, station_id, code, name, floor_level) VALUES
(1, 1, 'VG-P1', 'Підземний рівень -1', -1),
(2, 1, 'VG-P2', 'Підземний рівень -2', -2),
(3, 1, 'VG-EV', 'Секція електромобілів VG', -1),
(4, 2, 'KC-OPEN', 'Відкрита площадка King Cross', 0),
(5, 2, 'KC-GROUNF', 'Підземний паркінг King Cross', -1),
(6, 3, 'EP-A', 'Зона будівельних матеріалів', 0),
(7, 4, 'SL-1', 'Зона відвідувачів Сільпо', 0),
(8, 6, 'FL-L1', 'Рівень паркування L1', 1),
(9, 6, 'FL-L2', 'Рівень паркування L2', 2),
(10, 8, 'SP-A', 'Секція фасаду ТРЦ Спартак', 0),
(11, 9, 'MT-1', 'Зона великогабаритних авто Metro', 0),
(12, 10, 'PV-ROOF', 'Даховий відкритий майданчик Південний', 3);

INSERT INTO spot_types (id, type_name, description, tariff_multiplier) VALUES
(1, 'Стандартне', 'Звичайне паркомісце для легкового автомобіля', 1.00),
(2, 'Інклюзивне', 'Місце для водіїв з інвалідністю біля входу', 0.00),
(3, 'EV Зарядка', 'Місце обладнане швидкісною зарядною станцією', 1.50),
(4, 'Сімейне', 'Розширене паркомісце для авто з дитячими візками', 1.00),
(5, 'VIP / Службове', 'Особливе місце з можливістю тривалого резервування', 1.75),
(6, 'Мотоциклетне', 'Компактне місце для мотоциклів та скутерів', 0.50),
(7, 'Вантажне / Бус', 'Збільшене місце для комерційних фургонів', 1.80),
(8, 'Каршерінг', 'Спеціальне паркомісце партнерського каршерінгу', 0.90),
(9, 'Нічний абонемент', 'Паркомісце за спеціальним нічним тарифом', 0.80),
(10, 'Експрес Drop-Off', 'Місце короткочасної висадки (до 15 хв)', 0.00);

INSERT INTO parking_spots (id, zone_id, spot_type_id, spot_number, current_status) VALUES
(1, 1, 1, 'A-101', 'OCCUPIED'),
(2, 1, 1, 'A-102', 'FREE'),
(3, 1, 2, 'A-103', 'FREE'),
(4, 3, 3, 'EV-01', 'OCCUPIED'),
(5, 3, 3, 'EV-02', 'RESERVED'),
(6, 2, 1, 'B-201', 'FREE'),
(7, 4, 1, 'K-015', 'OCCUPIED'),
(8, 4, 4, 'K-016', 'FREE'),
(9, 6, 7, 'EP-50', 'MAINTENANCE'),
(10, 8, 5, 'FL-V1', 'RESERVED'),
(11, 8, 8, 'FL-CS1', 'FREE'),
(12, 5, 6, 'KC-M01', 'FREE'),
(13, 10, 1, 'SP-10', 'OCCUPIED'),
(14, 11, 7, 'MT-B01', 'FREE'),
(15, 12, 9, 'PV-R05', 'FREE'),
(16, 3, 3, 'EV-03', 'FREE'),
(17, 3, 3, 'EV-04', 'FREE');

INSERT INTO clients (id, client_type, phone, email, registration_date) VALUES
(1, 'INDIVIDUAL', '+380671112233', 'oleg.petrenko@gmail.com', '2024-01-15 10:20:00'),
(2, 'INDIVIDUAL', '+380502223344', 'iryna.koval@ukr.net', '2024-02-10 14:15:00'),
(3, 'INDIVIDUAL', '+380633334455', 'taras.melnyk@gmail.com', '2024-03-05 09:00:00'),
(4, 'INDIVIDUAL', '+380974445566', 'oksana.k@gmail.com', '2024-04-18 16:40:00'),
(5, 'INDIVIDUAL', '+380685556677', 'andriy.shev@ukr.net', '2024-05-20 11:30:00'),
(6, 'INDIVIDUAL', '+380931234567', 'mykhailo.boyko@gmail.com', '2024-06-01 10:00:00'),
(7, 'INDIVIDUAL', '+380962345678', 'natalia.moroz@ukr.net', '2024-06-15 12:45:00'),
(8, 'INDIVIDUAL', '+380993456789', 'yuriy.kozak@gmail.com', '2024-07-04 15:20:00'),
(9, 'INDIVIDUAL', '+380674567890', 'olena.lysenko@ukr.net', '2024-07-22 09:10:00'),
(10, 'INDIVIDUAL', '+380505678901', 'vasyl.hrynkiv@gmail.com', '2024-08-05 17:30:00'),
(11, 'INDIVIDUAL', '+380636789012', 'roman.dub@gmail.com', '2024-08-18 11:15:00'),
(12, 'INDIVIDUAL', '+380987890123', 'sofiya.yaremchuk@ukr.net', '2024-09-02 14:00:00'),
(13, 'ENTERPRISE', '+380322401000', 'office@softserveinc.com', '2023-11-01 09:00:00'),
(14, 'ENTERPRISE', '+380322902000', 'logistics@novaposhta.ua', '2023-12-12 12:00:00'),
(15, 'ENTERPRISE', '+380442303000', 'transport@uberdrive.ua', '2024-01-20 15:00:00'),
(16, 'ENTERPRISE', '+380322504000', 'fleet@galych-trans.lviv.ua', '2024-02-28 08:30:00'),
(17, 'ENTERPRISE', '+380322705000', 'corp@lion-delivery.com', '2024-03-15 13:45:00'),
(18, 'ENTERPRISE', '+380322986000', 'info@eleks.com', '2024-04-10 10:30:00'),
(19, 'ENTERPRISE', '+380322997000', 'logistics@carpathian-cargo.ua', '2024-05-14 11:20:00'),
(20, 'ENTERPRISE', '+380322338000', 'office@west-autotrade.lviv.ua', '2024-06-02 16:10:00'),
(21, 'ENTERPRISE', '+380322449000', 'support@zahid-service.ua', '2024-06-25 09:40:00'),
(22, 'ENTERPRISE', '+380322551000', 'supply@pharma-west.lviv.ua', '2024-07-12 14:50:00');

INSERT INTO client_individuals (client_id, first_name, last_name, tax_id, driver_license) VALUES
(1, 'Олег', 'Петренко', '3124567890', 'BXT123456'),
(2, 'Ірина', 'Коваль', '3298765431', 'BXT654321'),
(3, 'Тарас', 'Мельник', '3045678912', 'CXA987654'),
(4, 'Оксана', 'Кравчук', '3312345678', 'CXA112233'),
(5, 'Андрій', 'Шевченко', '2987654321', 'DXB445566'),
(6, 'Михайло', 'Бойко', '3156789012', 'DXB778899'),
(7, 'Наталія', 'Мороз', '3423456789', 'EXC121212'),
(8, 'Юрій', 'Козак', '2890123456', 'EXC343434'),
(9, 'Олена', 'Лисенко', '3512345670', 'FXD565656'),
(10, 'Василь', 'Гриньків', '3012345678', 'FXD787878'),
(11, 'Роман', 'Дуб', '3198765432', 'GXA909090'),
(12, 'Софія', 'Яремчук', '3345678901', 'GXA123789');

INSERT INTO client_enterprises (client_id, company_name, edrpou_code, contact_person, legal_address) VALUES
(13, 'ТОВ СофтСерв Холдинг', '36245199', 'Данило Садовий', 'м. Львів, вул. Садова, 2А'),
(14, 'ТОВ Нова Пошта Логістик', '37890123', 'Микола Григорчук', 'м. Львів, вул. Городоцька, 357'),
(15, 'ПП Убер Таксі Захід', '41234567', 'Сергій Бондар', 'м. Львів, пр. Чорновола, 67'),
(16, 'ТОВ Галич Транс Експрес', '39876543', 'Орест Воробець', 'м. Львів, вул. Шевченка, 311'),
(17, 'ПП Ліон Делівері Груп', '42345678', 'Віталій Кміть', 'м. Львів, вул. Зелена, 149'),
(18, 'ТОВ Елекс Девелопмент', '34871234', 'Ольга Павлюк', 'м. Львів, вул. Наукова, 7Д'),
(19, 'ПрАТ Карпатська Логістика', '21567890', 'Іван Романюк', 'м. Львів, вул. Стрийська, 202'),
(20, 'ТОВ Вест Авто Трейд', '43120987', 'Маркіян Баран', 'м. Львів, вул. Кульпарківська, 93'),
(21, 'ПП Захід Сервіс Плюс', '40981234', 'Ростислав Гнатюк', 'м. Львів, вул. Липинського, 36'),
(22, 'ТОВ Фарма Захід Дистрибюція', '38291045', 'Галина Сенчишин', 'м. Львів, вул. Пасічна, 129');

INSERT INTO regular_cards (id, client_id, card_number, card_type, issue_date, expiry_date, balance, discount_percent, status) VALUES
(1, 1, 'CARD-IND-10001', 'PREPAID', '2024-01-16', '2025-01-16', 500.00, 10.00, 'ACTIVE'),
(2, 2, 'CARD-IND-10002', 'POSTPAID', '2024-02-11', '2025-02-11', 0.00, 5.00, 'ACTIVE'),
(3, 3, 'CARD-IND-10003', 'PREPAID', '2024-03-06', '2024-09-06', 20.00, 10.00, 'EXPIRED'),
(4, 4, 'CARD-IND-10004', 'PREPAID', '2024-04-19', '2025-04-19', 150.00, 5.00, 'ACTIVE'),
(5, 5, 'CARD-IND-10005', 'PREPAID', '2024-05-22', '2025-05-22', 300.00, 5.00, 'ACTIVE'),
(6, 13, 'CARD-CORP-90001', 'CORPORATE_VIP', '2023-11-02', '2025-11-02', 15000.00, 20.00, 'ACTIVE'),
(7, 13, 'CARD-CORP-90002', 'CORPORATE_VIP', '2023-11-02', '2025-11-02', 12000.00, 20.00, 'ACTIVE'),
(8, 14, 'CARD-CORP-90003', 'POSTPAID', '2023-12-15', '2024-12-15', 0.00, 15.00, 'ACTIVE'),
(9, 15, 'CARD-CORP-90004', 'PREPAID', '2024-01-22', '2025-01-22', 4500.00, 12.00, 'ACTIVE'),
(10, 16, 'CARD-CORP-90005', 'POSTPAID', '2024-03-01', '2025-03-01', 0.00, 10.00, 'ACTIVE'),
(11, 18, 'CARD-CORP-90006', 'CORPORATE_VIP', '2024-04-10', '2025-04-10', 8000.00, 18.00, 'ACTIVE'),
(12, 19, 'CARD-CORP-90007', 'PREPAID', '2024-02-15', '2024-08-15', 0.00, 10.00, 'BLOCKED');

INSERT INTO vehicles (id, client_id, license_plate, make, model, color) VALUES
(1, 1, 'BC1234AA', 'Toyota', 'RAV4', 'Білий'),
(2, 2, 'BC5678BB', 'Nissan', 'Leaf', 'Синій'),
(3, 3, 'BC9012CC', 'Volkswagen', 'Golf', 'Сірий'),
(4, 4, 'BC3456DD', 'Renault', 'Megane', 'Червоний'),
(5, 5, 'BC7890EE', 'Skoda', 'Octavia', 'Чорний'),
(6, 6, 'BC1122FF', 'Hyundai', 'Tucson', 'Сріблястий'),
(7, 7, 'BC3344GG', 'Kia', 'Sportage', 'Коричневий'),
(8, 8, 'BC5566HH', 'Mazda', 'CX-5', 'Червоний'),
(9, 13, 'BC0001TT', 'Tesla', 'Model Y', 'Білий'),
(10, 13, 'BC0002TT', 'Tesla', 'Model 3', 'Сріблястий'),
(11, 14, 'BC5555NP', 'Mercedes-Benz', 'Sprinter', 'Білий'),
(12, 15, 'BC7777UB', 'Hyundai', 'Ioniq 5', 'Сірий'),
(13, 16, 'BC8888GT', 'MAN', 'TGL', 'Синій'),
(14, NULL, 'AA4488KX', 'BMW', 'X5', 'Чорний'),
(15, NULL, 'KA9900MP', 'Audi', 'A6', 'Сірий');

INSERT INTO parking_reservations (id, spot_id, client_id, license_plate, reserved_from, reserved_to, booking_fee, status, created_at) VALUES
(1, 5, 1, 'BC1234AA', '2026-09-22 16:00:00', '2026-09-22 19:00:00', 50.00, 'CONFIRMED', '2026-09-22 10:00:00'),
(2, 4, 2, 'BC5678BB', '2026-09-22 12:00:00', '2026-09-22 15:00:00', 45.00, 'COMPLETED', '2026-09-21 18:30:00'),
(3, 10, 13, 'BC0001TT', '2026-09-22 14:00:00', '2026-09-22 20:00:00', 100.00, 'CONFIRMED', '2026-09-22 09:15:00'),
(4, 7, 3, 'BC9012CC', '2026-09-23 09:00:00', '2026-09-23 18:00:00', 60.00, 'CONFIRMED', '2026-09-22 11:40:00'),
(5, 9, 15, 'BC7777UB', '2026-09-20 10:00:00', '2026-09-20 12:00:00', 30.00, 'CANCELLED', '2026-09-19 14:00:00'),
(6, 2, 4, 'BC3456DD', '2026-09-21 11:00:00', '2026-09-21 14:00:00', 40.00, 'COMPLETED', '2026-09-21 08:00:00'),
(7, 8, 5, 'BC7890EE', '2026-09-22 18:00:00', '2026-09-22 21:00:00', 30.00, 'PENDING', '2026-09-22 14:50:00'),
(8, 1, 6, 'BC1122FF', '2026-09-24 10:00:00', '2026-09-24 14:00:00', 50.00, 'CONFIRMED', '2026-09-23 16:00:00'),
(9, 3, 7, 'BC3344GG', '2026-09-25 09:00:00', '2026-09-25 12:00:00', 0.00, 'CONFIRMED', '2026-09-24 11:20:00'),
(10, 6, 8, 'BC5566HH', '2026-09-25 13:00:00', '2026-09-25 17:00:00', 40.00, 'PENDING', '2026-09-24 15:10:00'),
(11, 13, 14, 'BC5555NP', '2026-09-26 08:00:00', '2026-09-26 18:00:00', 80.00, 'CONFIRMED', '2026-09-25 10:00:00'),
(12, 15, 18, 'BC0002TT', '2026-09-26 12:00:00', '2026-09-26 16:00:00', 50.00, 'CONFIRMED', '2026-09-25 14:30:00');

INSERT INTO parking_sessions (id, spot_id, card_id, license_plate, entry_time, exit_time, total_cost, status) VALUES
(1, 1, 1, 'BC1234AA', '2026-09-22 13:10:00', NULL, 0.00, 'ACTIVE'),
(2, 4, 6, 'BC0001TT', '2026-09-22 12:00:00', NULL, 0.00, 'ACTIVE'), 
(3, 7, 8, 'BC5555NP', '2026-09-22 11:30:00', NULL, 0.00, 'ACTIVE'), 
(4, 2, NULL, 'AA4488KX', '2026-09-22 10:00:00', '2026-09-22 12:45:00', 90.00, 'COMPLETED'), 
(5, 1, 2, 'BC5678BB', '2026-09-21 14:00:00', '2026-09-21 16:30:00', 71.25, 'COMPLETED'),
(6, 7, NULL, 'BC9012CC', '2026-09-21 09:15:00', '2026-09-21 11:15:00', 50.00, 'COMPLETED'),
(7, 9, 9, 'BC7777UB', '2026-09-21 15:20:00', '2026-09-21 18:20:00', 52.80, 'COMPLETED'),
(8, 8, 4, 'BC3456DD', '2026-09-20 18:00:00', '2026-09-20 19:30:00', 28.50, 'COMPLETED'),
(9, 10, 7, 'BC0002TT', '2026-09-20 10:00:00', '2026-09-20 14:00:00', 128.00, 'COMPLETED'),
(10, 3, NULL, 'BC7890EE', '2026-09-19 13:00:00', '2026-09-19 15:00:00', 0.00, 'COMPLETED'),
(11, 13, 5, 'BC1122FF', '2026-09-22 08:30:00', '2026-09-22 10:30:00', 60.00, 'COMPLETED'),
(12, 14, 10, 'BC8888GT', '2026-09-22 07:00:00', '2026-09-22 11:00:00', 144.00, 'COMPLETED');

INSERT INTO parking_tickets (id, session_id, ticket_number, issue_time, payment_status, paid_time, paid_amount, payment_method) VALUES
(1, 1, 'TCK-20260922-0001', '2026-09-22 13:10:00', 'UNPAID', NULL, 0.00, NULL),
(2, 2, 'TCK-20260922-0002', '2026-09-22 12:00:00', 'UNPAID', NULL, 0.00, NULL),
(3, 3, 'TCK-20260922-0003', '2026-09-22 11:30:00', 'UNPAID', NULL, 0.00, NULL),
(4, 4, 'TCK-20260922-0004', '2026-09-22 10:00:00', 'PAID', '2026-09-22 12:40:00', 90.00, 'CARD'),
(5, 5, 'TCK-20260921-0005', '2026-09-21 14:00:00', 'PAID', '2026-09-21 16:25:00', 71.25, 'SUBSCRIPTION'),
(6, 6, 'TCK-20260921-0006', '2026-09-21 09:15:00', 'PAID', '2026-09-21 11:10:00', 50.00, 'CASH'),
(7, 7, 'TCK-20260921-0007', '2026-09-21 15:20:00', 'PAID', '2026-09-21 18:15:00', 52.80, 'SUBSCRIPTION'),
(8, 8, 'TCK-20260920-0008', '2026-09-20 18:00:00', 'PAID', '2026-09-20 19:25:00', 28.50, 'MOBILE_APP'),
(9, 9, 'TCK-20260920-0009', '2026-09-20 10:00:00', 'PAID', '2026-09-20 13:55:00', 128.00, 'SUBSCRIPTION'),
(10, 10, 'TCK-20260919-0010', '2026-09-19 13:00:00', 'EXEMPT', '2026-09-19 15:00:00', 0.00, 'SUBSCRIPTION'),
(11, 11, 'TCK-20260922-0011', '2026-09-22 08:30:00', 'PAID', '2026-09-22 10:25:00', 60.00, 'CARD'),
(12, 12, 'TCK-20260922-0012', '2026-09-22 07:00:00', 'PAID', '2026-09-22 10:50:00', 144.00, 'SUBSCRIPTION');
