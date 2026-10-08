USE smart_parking_db;

SELECT 
    ps.id AS station_id,
    rc.name AS retail_chain,
    ps.name AS parking_name,
    ps.city,
    ps.address,
    ps.total_spots,
    ps.hourly_rate,
    IF(ps.is_24_7, 'Цілодобово', 'Обмежений графік') AS work_mode
FROM parking_stations ps
JOIN retail_chains rc ON ps.chain_id = rc.id
ORDER BY rc.name, ps.name;


SELECT 
    ps.name AS station_name,
    COUNT(spot.id) AS registered_spots_in_system,
    SUM(CASE WHEN spot.current_status = 'FREE' THEN 1 ELSE 0 END) AS free_spots,
    SUM(CASE WHEN spot.current_status = 'OCCUPIED' THEN 1 ELSE 0 END) AS occupied_spots,
    SUM(CASE WHEN spot.current_status = 'RESERVED' THEN 1 ELSE 0 END) AS reserved_spots,
    SUM(CASE WHEN spot.current_status = 'MAINTENANCE' THEN 1 ELSE 0 END) AS maintenance_spots,
    ROUND(
        (SUM(CASE WHEN spot.current_status = 'OCCUPIED' THEN 1 ELSE 0 END) / COUNT(spot.id)) * 100, 
        1
    ) AS occupancy_rate_percent
FROM parking_stations ps
JOIN parking_zones pz ON ps.id = pz.station_id
JOIN parking_spots spot ON pz.id = spot.zone_id
GROUP BY ps.id, ps.name;

SELECT 
    ps.name AS station_name,
    pz.name AS zone_name,
    spot.spot_number,
    st.type_name AS spot_type,
    sess.license_plate,
    sess.entry_time,
    TIMESTAMPDIFF(MINUTE, sess.entry_time, NOW()) AS current_duration_minutes
FROM parking_spots spot
JOIN parking_zones pz ON spot.zone_id = pz.id
JOIN parking_stations ps ON pz.station_id = ps.id
JOIN spot_types st ON spot.spot_type_id = st.id
LEFT JOIN parking_sessions sess 
    ON spot.id = sess.spot_id 
   AND sess.status = 'ACTIVE'
WHERE spot.current_status = 'OCCUPIED'
ORDER BY ps.name, spot.spot_number;

SELECT 
    sess.id AS session_id,
    ps.name AS parking_station,
    pz.code AS zone_code,
    spot.spot_number,
    sess.license_plate,
    sess.entry_time,
    sess.exit_time,
    sess.duration_minutes,
    ROUND(sess.duration_minutes / 60, 2) AS duration_hours,
    sess.total_cost,
    sess.status AS session_status
FROM parking_sessions sess
JOIN parking_spots spot ON sess.spot_id = spot.id
JOIN parking_zones pz ON spot.zone_id = pz.id
JOIN parking_stations ps ON sess.station_id = ps.id
ORDER BY sess.entry_time DESC;

SELECT 
    tck.ticket_number,
    ps.name AS station_name,
    tck.license_plate,
    tck.issue_time,
    tck.payment_status,
    tck.paid_time,
    tck.paid_amount,
    COALESCE(tck.payment_method, 'НЕ СПЛАЧЕНО') AS payment_method
FROM parking_tickets tck
JOIN parking_stations ps ON tck.station_id = ps.id
ORDER BY tck.issue_time DESC;

SELECT 
    rc.card_number,
    rc.card_type,
    ent.company_name,
    ent.edrpou_code,
    ent.contact_person,
    c.phone AS contact_phone,
    c.email,
    rc.balance,
    rc.discount_percent,
    rc.expiry_date,
    rc.status AS card_status
FROM regular_cards rc
JOIN clients c ON rc.client_id = c.id
JOIN client_enterprises ent ON c.id = ent.client_id
WHERE c.client_type = 'ENTERPRISE'
ORDER BY ent.company_name;

SELECT 
    rc.card_number,
    CONCAT(ind.last_name, ' ', ind.first_name) AS full_name,
    ind.tax_id,
    ind.driver_license,
    c.phone,
    rc.balance,
    rc.discount_percent,
    rc.status AS card_status,
    GROUP_CONCAT(v.license_plate SEPARATOR ', ') AS registered_vehicles
FROM regular_cards rc
JOIN clients c ON rc.client_id = c.id
JOIN client_individuals ind ON c.id = ind.client_id
LEFT JOIN vehicles v ON c.id = v.client_id
WHERE c.client_type = 'INDIVIDUAL'
GROUP BY rc.id, ind.client_id, full_name, ind.tax_id, ind.driver_license, c.phone, rc.balance, rc.discount_percent, rc.status
ORDER BY full_name;

SELECT 
    r.id AS reservation_id,
    ps.name AS station_name,
    pz.code AS zone_code,
    spot.spot_number,
    r.license_plate,
    CASE 
        WHEN c.client_type = 'INDIVIDUAL' THEN CONCAT(ind.last_name, ' ', ind.first_name)
        WHEN c.client_type = 'ENTERPRISE' THEN ent.company_name
    END AS client_name,
    c.phone,
    r.reserved_from,
    r.reserved_to,
    r.booking_fee,
    r.status AS reservation_status
FROM parking_reservations r
JOIN parking_stations ps ON r.station_id = ps.id
JOIN parking_spots spot ON r.spot_id = spot.id
JOIN parking_zones pz ON spot.zone_id = pz.id
JOIN clients c ON r.client_id = c.id
LEFT JOIN client_individuals ind ON c.id = ind.client_id
LEFT JOIN client_enterprises ent ON c.id = ent.client_id
ORDER BY r.reserved_from ASC;

SELECT 
    ps.name AS station_name,
    ps.address,
    pz.name AS zone_name,
    spot.spot_number,
    st.type_name,
    spot.has_ev_charger,
    spot.current_status
FROM parking_spots spot
JOIN parking_zones pz ON spot.zone_id = pz.id
JOIN parking_stations ps ON pz.station_id = ps.id
JOIN spot_types st ON spot.spot_type_id = st.id
WHERE spot.has_ev_charger = TRUE 
  AND spot.current_status = 'FREE';


SELECT 
    ps.name AS station_name,
    rc.name AS retail_chain,
    COUNT(tck.id) AS total_tickets_issued,
    SUM(CASE WHEN tck.payment_status = 'PAID' THEN 1 ELSE 0 END) AS paid_tickets_count,
    COALESCE(SUM(tck.paid_amount), 0.00) AS total_revenue_uah,
    COALESCE(AVG(CASE WHEN tck.payment_status = 'PAID' THEN tck.paid_amount END), 0.00) AS avg_ticket_cost_uah
FROM parking_stations ps
JOIN retail_chains rc ON ps.chain_id = rc.id
LEFT JOIN parking_tickets tck ON ps.id = tck.station_id
GROUP BY ps.id, ps.name, rc.name
ORDER BY total_revenue_uah DESC;
