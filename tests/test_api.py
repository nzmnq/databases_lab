from datetime import datetime
import pytest
from my_project import create_app, db
from my_project.auth.domain.retail_chain import RetailChain
from my_project.auth.domain.parking_station import ParkingStation
from my_project.auth.domain.client import Client
from my_project.auth.domain.parking_spot import ParkingSpot
from my_project.auth.domain.parking_reservation import ParkingReservation
from my_project.auth.domain.station_maintenance import StationMaintenance, ReservationDeleteLog

@pytest.fixture
def client():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }
    app = create_app(test_config=test_config)

    with app.app_context():
        db.create_all()

        chain1 = RetailChain(
            id=1,
            name="Сільпо Рітейл",
            edrpou="32847921",
            website="https://silpo.ua",
            support_phone="+380800301707"
        )
        chain2 = RetailChain(
            id=2,
            name="Victoria Gardens ТРЦ",
            edrpou="40192844",
            website="https://victoriagardens.com.ua",
            support_phone="+380322595959"
        )
        db.session.add_all([chain1, chain2])
        db.session.commit()

        station1 = ParkingStation(
            id=1,
            chain_id=1,
            name="Паркінг супермаркету Сільпо",
            city="Львів",
            address="вул. Наукова, 35А",
            capacity=120,
            hourly_rate=20.00,
            is_24_7=True
        )
        station2 = ParkingStation(
            id=2,
            chain_id=2,
            name="Підземний паркінг Victoria Gardens",
            city="Львів",
            address="вул. Кульпарківська, 226А",
            capacity=1500,
            hourly_rate=30.00,
            is_24_7=True
        )
        station3 = ParkingStation(
            id=3,
            chain_id=1,
            name="Паркінг Сільпо ТЦ Роксолана",
            city="Львів",
            address="пл. Соборна, 14",
            capacity=90,
            hourly_rate=35.00,
            is_24_7=True
        )
        db.session.add_all([station1, station2, station3])

        c1 = Client(id=1, client_type='INDIVIDUAL', phone='+380671112233', email='client1@example.com')
        c2 = Client(id=2, client_type='ENTERPRISE', phone='+380674445566', email='client2@example.com')
        spot2 = ParkingSpot(id=2, zone_id=1, spot_type_id=1, spot_number='A-02', current_status='FREE')
        spot5 = ParkingSpot(id=5, zone_id=1, spot_type_id=1, spot_number='A-05', current_status='RESERVED')
        spot7 = ParkingSpot(id=7, zone_id=2, spot_type_id=2, spot_number='B-01', current_status='FREE')
        db.session.add_all([c1, c2, spot2, spot5, spot7])
        db.session.flush()

        res1 = ParkingReservation(
            id=1,
            client_id=1,
            spot_id=5,
            license_plate='BC1001AA',
            reserved_from=datetime(2026, 9, 25, 10, 0, 0),
            reserved_to=datetime(2026, 9, 25, 12, 0, 0),
            booking_fee=30.00,
            status='CONFIRMED',
        )
        res2 = ParkingReservation(
            id=2,
            client_id=1,
            spot_id=2,
            license_plate='BC1001AA',
            reserved_from=datetime(2026, 9, 26, 10, 0, 0),
            reserved_to=datetime(2026, 9, 26, 12, 0, 0),
            booking_fee=40.00,
            status='CONFIRMED',
        )
        res3 = ParkingReservation(
            id=3,
            client_id=2,
            spot_id=5,
            license_plate='BC2002BB',
            reserved_from=datetime(2026, 9, 27, 14, 0, 0),
            reserved_to=datetime(2026, 9, 27, 16, 0, 0),
            booking_fee=45.00,
            status='CONFIRMED',
        )
        db.session.add_all([res1, res2, res3])

        maint1 = StationMaintenance(
            id=1,
            station_id=1,
            inspector_code='AB-101-12',
            description='Планова перевірка',
            maintenance_cost=1200.00,
        )
        log1 = ReservationDeleteLog(
            id=1,
            reservation_id=99,
            client_id=1,
            spot_id=2,
            license_plate='BC1001AA',
            status='CANCELLED',
        )
        db.session.add_all([maint1, log1])
        db.session.commit()

        yield app.test_client()

        db.session.remove()
        db.drop_all()

def test_health_check(client):
    res = client.get('/api/health')
    assert res.status_code == 200
    assert res.json['status'] == 'healthy'


def test_get_all_retail_chains(client):
    res = client.get('/api/retail-chains')
    assert res.status_code == 200
    assert isinstance(res.json, list)
    assert len(res.json) == 2

def test_get_retail_chain_by_id(client):
    res = client.get('/api/retail-chains/1')
    assert res.status_code == 200
    assert res.json['id'] == 1
    assert res.json['name'] == "Сільпо Рітейл"

def test_get_retail_chain_not_found(client):
    res = client.get('/api/retail-chains/999')
    assert res.status_code == 404

def test_create_retail_chain(client):
    payload = {
        "name": "Епіцентр К",
        "edrpou": "32490244",
        "website": "https://epicentrk.ua",
        "support_phone": "+380800202727"
    }
    res = client.post('/api/retail-chains', json=payload)
    assert res.status_code == 201
    assert res.json['id'] is not None
    assert res.json['name'] == payload['name']
    assert res.json['edrpou'] == payload['edrpou']

def test_create_retail_chain_validation(client):
    res = client.post('/api/retail-chains', json={"name": "Only Name"})
    assert res.status_code == 400
    res = client.post('/api/retail-chains', json={
        "name": "Different Name",
        "edrpou": "32847921",
        "support_phone": "+380501234567"
    })
    assert res.status_code == 409

def test_update_retail_chain(client):
    payload = {"support_phone": "+380441112233", "website": "https://new-silpo.ua"}
    res = client.put('/api/retail-chains/1', json=payload)
    assert res.status_code == 200
    assert res.json['support_phone'] == "+380441112233"
    assert res.json['website'] == "https://new-silpo.ua"

def test_delete_retail_chain(client):
    res = client.delete('/api/retail-chains/1')
    assert res.status_code == 200

    res = client.get('/api/retail-chains/1')
    assert res.status_code == 404

def test_get_all_parking_stations(client):
    res = client.get('/api/parking-stations')
    assert res.status_code == 200
    assert len(res.json) == 3

def test_get_parking_station_by_id(client):
    res = client.get('/api/parking-stations/1')
    assert res.status_code == 200
    assert res.json['id'] == 1
    assert res.json['city'] == 'Львів'

def test_create_parking_station(client):
    payload = {
        "chain_id": 1,
        "name": "Новий паркінг Сільпо",
        "city": "Львів",
        "address": "вул. Шевченка, 100",
        "capacity": 50,
        "hourly_rate": 25.0,
        "is_24_7": True
    }
    res = client.post('/api/parking-stations', json=payload)
    assert res.status_code == 201
    assert res.json['id'] is not None
    assert res.json['name'] == payload['name']

def test_create_parking_station_invalid_parent(client):
    payload = {
        "chain_id": 9999,
        "name": "Паркінг з неіснуючою мережею",
        "city": "Львів",
        "address": "вул. Тестова, 1"
    }
    res = client.post('/api/parking-stations', json=payload)
    assert res.status_code == 400

def test_update_parking_station(client):
    payload = {"hourly_rate": 45.0, "capacity": 2000}
    res = client.put('/api/parking-stations/2', json=payload)
    assert res.status_code == 200
    assert res.json['hourly_rate'] == 45.0
    assert res.json['capacity'] == 2000

def test_delete_parking_station(client):
    res = client.delete('/api/parking-stations/1')
    assert res.status_code == 200

    res = client.get('/api/parking-stations/1')
    assert res.status_code == 404

def test_get_parking_stations_of_retail_chain(client):
    res = client.get('/api/retail-chains/1/parking-stations')
    assert res.status_code == 200
    assert res.json['retail_chain_id'] == 1
    assert res.json['total_stations'] == 2
    assert len(res.json['parking_stations']) == 2
    assert res.json['parking_stations'][0]['id'] == 1
    assert res.json['parking_stations'][1]['id'] == 3

def test_get_parent_retail_chain_of_station(client):
    res = client.get('/api/parking-stations/2/retail-chain')
    assert res.status_code == 200
    assert res.json['parking_station_id'] == 2
    assert res.json['retail_chain']['id'] == 2
    assert res.json['retail_chain']['name'] == "Victoria Gardens ТРЦ"


def test_get_all_reservations(client):
    res = client.get('/api/reservations')
    assert res.status_code == 200
    assert len(res.json) == 3
    assert res.json[0]['client_phone'] == '+380671112233'
    assert res.json[0]['spot_number'] == 'A-05'


def test_get_reservations_grouped_by_clients(client):
    res = client.get('/api/reservations/grouped-by-clients')
    assert res.status_code == 200
    assert len(res.json) == 2
    assert res.json[0]['id'] == 1
    assert len(res.json[0]['reserved_spots']) == 2
    assert res.json[1]['id'] == 2
    assert len(res.json[1]['reserved_spots']) == 1


def test_get_spots_by_client_m2m(client):
    res = client.get('/api/reservations/clients/1/spots')
    assert res.status_code == 200
    assert res.json['client']['id'] == 1
    spot_ids = {s['id'] for s in res.json['reserved_spots']}
    assert spot_ids == {2, 5}


def test_get_clients_by_spot_m2m(client):
    res = client.get('/api/reservations/spots/5/clients')
    assert res.status_code == 200
    assert res.json['parking_spot']['id'] == 5
    client_ids = {c['id'] for c in res.json['reserving_clients']}
    assert client_ids == {1, 2}


def test_create_and_delete_reservation_m2m(client):
    res = client.post('/api/reservations', json={
        'client_id': 2,
        'spot_id': 7,
        'license_plate': 'BC7777KK',
        'booking_fee': 25.00,
    })
    assert res.status_code == 201
    created_id = res.json['id']
    assert res.json['client_id'] == 2
    assert res.json['spot_id'] == 7
    assert res.json['spot_number'] == 'B-01'

    res_del = client.delete(f'/api/reservations/{created_id}')
    assert res_del.status_code == 200

    res_get = client.get(f'/api/reservations/{created_id}')
    assert res_get.status_code == 404


def test_create_reservation_invalid_fk(client):
    res = client.post('/api/reservations', json={
        'client_id': 9999,
        'spot_id': 5,
    })
    assert res.status_code == 400

    res2 = client.post('/api/reservations', json={
        'client_id': 1,
        'spot_id': 9999,
    })
    assert res2.status_code == 400


def test_station_maintenances_crud(client):
    res_all = client.get('/api/station-maintenances')
    assert res_all.status_code == 200
    assert len(res_all.json) == 1

    res_by_station = client.get('/api/station-maintenances/station/1')
    assert res_by_station.status_code == 200
    assert res_by_station.json['total_maintenances'] == 1

    res_create = client.post('/api/station-maintenances', json={
        'station_id': 2,
        'inspector_code': 'CD-202-33',
        'description': 'Перевірка шлагбауму',
        'maintenance_cost': 950.0,
    })
    assert res_create.status_code == 201
    created_id = res_create.json['id']
    assert res_create.json['inspector_code'] == 'CD-202-33'

    res_upd = client.put(f'/api/station-maintenances/{created_id}', json={
        'maintenance_cost': 1100.0,
    })
    assert res_upd.status_code == 200
    assert res_upd.json['maintenance_cost'] == 1100.0

    res_del = client.delete(f'/api/station-maintenances/{created_id}')
    assert res_del.status_code == 200


def test_stored_programs_audit_logs_and_validation(client):
    res_logs = client.get('/api/stored-programs/audit-logs')
    assert res_logs.status_code == 200
    assert res_logs.json['total_logs'] == 1
    assert res_logs.json['logs'][0]['reservation_id'] == 99

    res_bad_stat = client.get('/api/stored-programs/station-stats?stat=INVALID')
    assert res_bad_stat.status_code == 400

    res_bad_m2m = client.post('/api/stored-programs/reservations-m2m', json={'client_email': 'a@b.com'})
    assert res_bad_m2m.status_code == 400

    res_bad_maint = client.post('/api/stored-programs/station-maintenances', json={'station_id': 1})
    assert res_bad_maint.status_code == 400


def test_all_15_tables_crud_endpoints(client):
    res_z = client.post('/api/parking-zones', json={'station_id': 1, 'code': 'Z-1', 'name': 'Zone 1', 'floor_level': 1})
    assert res_z.status_code == 201
    zid = res_z.json['id']
    assert client.get(f'/api/parking-zones/{zid}').status_code == 200
    assert client.put(f'/api/parking-zones/{zid}', json={'name': 'Zone 1 Updated'}).json['name'] == 'Zone 1 Updated'

    res_st = client.post('/api/spot-types', json={'type_name': 'EV Fast', 'tariff_multiplier': 1.5})
    assert res_st.status_code == 201
    stid = res_st.json['id']
    assert client.get(f'/api/spot-types/{stid}').status_code == 200

    res_ps = client.post('/api/parking-spots', json={'zone_id': zid, 'spot_type_id': stid, 'spot_number': 'Z-101'})
    assert res_ps.status_code == 201
    psid = res_ps.json['id']
    assert client.get('/api/parking-spots').status_code == 200

    res_c1 = client.post('/api/clients', json={'client_type': 'INDIVIDUAL', 'phone': '+380991112233', 'email': 'ind@example.com'})
    assert res_c1.status_code == 201
    c1_id = res_c1.json['id']
    res_ci = client.post('/api/client-individuals', json={
        'client_id': c1_id, 'first_name': 'Ivan', 'last_name': 'Franko', 'tax_id': '9998887771', 'driver_license': 'DL999111'
    })
    assert res_ci.status_code == 201
    assert client.get(f'/api/client-individuals/{c1_id}').status_code == 200
    assert client.put(f'/api/client-individuals/{c1_id}', json={'first_name': 'Ivan Updated'}).json['first_name'] == 'Ivan Updated'

    res_c2 = client.post('/api/clients', json={'client_type': 'ENTERPRISE', 'phone': '+380994445566', 'email': 'ent@example.com'})
    assert res_c2.status_code == 201
    c2_id = res_c2.json['id']
    res_ce = client.post('/api/client-enterprises', json={
        'client_id': c2_id, 'company_name': 'ACME LLC', 'edrpou_code': '88776655', 'contact_person': 'John', 'legal_address': 'Lviv'
    })
    assert res_ce.status_code == 201
    assert client.get(f'/api/client-enterprises/{c2_id}').status_code == 200

    res_rc = client.post('/api/regular-cards', json={
        'client_id': c1_id, 'card_number': 'CARD-999', 'card_type': 'PREPAID', 'issue_date': '2026-01-01', 'expiry_date': '2027-01-01', 'balance': 250.0
    })
    assert res_rc.status_code == 201
    rc_id = res_rc.json['id']
    assert client.put(f'/api/regular-cards/{rc_id}', json={'expiry_date': '2028-01-01', 'balance': 300.0}).json['balance'] == 300.0

    res_v = client.post('/api/vehicles', json={'client_id': c1_id, 'license_plate': 'BC9999XX', 'make': 'Toyota', 'model': 'Camry', 'color': 'Black'})
    assert res_v.status_code == 201
    assert client.get('/api/vehicles').status_code == 200

    res_sess = client.post('/api/parking-sessions', json={
        'spot_id': psid, 'card_id': rc_id, 'license_plate': 'BC9999XX', 'entry_time': '2026-10-01 10:00:00', 'exit_time': '2026-10-01 12:30:00', 'total_cost': 75.0, 'status': 'COMPLETED'
    })
    assert res_sess.status_code == 201
    assert res_sess.json['duration_minutes'] == 150
    sess_id = res_sess.json['id']

    res_tck = client.post('/api/parking-tickets', json={
        'session_id': sess_id, 'ticket_number': 'TCK-999', 'issue_time': '2026-10-01 10:00:00', 'payment_status': 'PAID', 'paid_amount': 75.0, 'payment_method': 'CARD'
    })
    assert res_tck.status_code == 201
    tck_id = res_tck.json['id']
    assert client.get(f'/api/parking-tickets/{tck_id}').status_code == 200

    assert client.get('/api/reservation-delete-logs').status_code == 200
    assert len(client.get('/api/reservation-delete-logs').json) == 1

    assert client.delete(f'/api/parking-tickets/{tck_id}').status_code == 200
    assert client.delete(f'/api/parking-sessions/{sess_id}').status_code == 200
    assert client.delete(f'/api/vehicles/{res_v.json["id"]}').status_code == 200
    assert client.delete(f'/api/regular-cards/{rc_id}').status_code == 200
    assert client.delete(f'/api/client-individuals/{c1_id}').status_code == 200
    assert client.delete(f'/api/client-enterprises/{c2_id}').status_code == 200
    assert client.delete(f'/api/parking-spots/{psid}').status_code == 200
    assert client.delete(f'/api/spot-types/{stid}').status_code == 200
    assert client.delete(f'/api/parking-zones/{zid}').status_code == 200
