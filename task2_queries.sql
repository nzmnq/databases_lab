SELECT 
    ps.id AS station_id,
    ps.name AS station_name,
    ps.city,
    ps.address,
    (
        SELECT COUNT(*) 
        FROM parking_spots spot
        JOIN parking_zones pz ON spot.zone_id = pz.id
        WHERE pz.station_id = ps.id AND spot.current_status = 'FREE'
    ) AS free_spots_count
FROM parking_stations ps
WHERE ps.city = 'Львів'
  AND (
      SELECT COUNT(*) 
      FROM parking_spots spot
      JOIN parking_zones pz ON spot.zone_id = pz.id
      WHERE pz.station_id = ps.id AND spot.current_status = 'FREE'
  ) > 10;

SELECT 
    station_id AS parking_id,
    ROUND(AVG(duration_minutes), 2) AS avg_duration_minutes,
    ROUND(AVG(duration_minutes) / 60, 2) AS avg_duration_hours
FROM parking_sessions
WHERE station_id = 5 
  AND status = 'COMPLETED'
  AND entry_time >= NOW() - INTERVAL 7 DAY;

SELECT 
    c.id AS client_id,
    c.phone,
    c.email,
    CASE 
        WHEN c.client_type = 'INDIVIDUAL' THEN CONCAT(ind.last_name, ' ', ind.first_name)
        WHEN c.client_type = 'ENTERPRISE' THEN ent.company_name
    END AS client_name,
    COUNT(pr.id) AS reservations_count
FROM clients c
JOIN regular_cards rc ON c.id = rc.client_id
JOIN parking_reservations pr ON c.id = pr.client_id
LEFT JOIN client_individuals ind ON c.id = ind.client_id
LEFT JOIN client_enterprises ent ON c.id = ent.client_id
WHERE pr.created_at >= NOW() - INTERVAL 1 MONTH
GROUP BY c.id, c.phone, c.email, client_name
HAVING COUNT(pr.id) > 3;

SELECT 
    tck.ticket_number,
    tck.license_plate,
    ps.name AS station_name,
    ps.address AS station_address,
    COALESCE(
        CASE 
            WHEN c.client_type = 'INDIVIDUAL' THEN CONCAT(ind.last_name, ' ', ind.first_name)
            WHEN c.client_type = 'ENTERPRISE' THEN ent.company_name
        END,
        'Разовий відвідувач'
    ) AS user_name,
    tck.payment_status
FROM parking_tickets tck
JOIN parking_stations ps ON tck.station_id = ps.id
JOIN parking_sessions sess ON tck.session_id = sess.id
LEFT JOIN regular_cards rc ON sess.card_id = rc.id
LEFT JOIN clients c ON rc.client_id = c.id
LEFT JOIN client_individuals ind ON c.id = ind.client_id
LEFT JOIN client_enterprises ent ON c.id = ent.client_id
ORDER BY tck.id ASC;

SELECT 
    ps.id AS station_id,
    ps.name AS station_name,
    ps.city,
    ps.address,
    COUNT(sess.id) AS occupied_spots_count
FROM parking_stations ps
JOIN parking_sessions sess ON ps.id = sess.station_id
WHERE sess.entry_time >= NOW() - INTERVAL 1 HOUR
GROUP BY ps.id, ps.name, ps.city, ps.address
HAVING COUNT(sess.id) = (
    SELECT MAX(cnt)
    FROM (
        SELECT COUNT(s2.id) AS cnt
        FROM parking_sessions s2
        WHERE s2.entry_time >= NOW() - INTERVAL 1 HOUR
        GROUP BY s2.station_id
    ) AS max_counts
);
