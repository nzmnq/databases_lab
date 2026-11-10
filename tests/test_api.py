import pytest
from my_project import create_app, db
from my_project.auth.domain.retail_chain import RetailChain
from my_project.auth.domain.parking_station import ParkingStation

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
        db.session.add_all([station1, station2])
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
    assert len(res.json) == 2

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
    assert res.json['total_stations'] == 1
    assert res.json['parking_stations'][0]['id'] == 1

def test_get_parent_retail_chain_of_station(client):
    res = client.get('/api/parking-stations/2/retail-chain')
    assert res.status_code == 200
    assert res.json['parking_station_id'] == 2
    assert res.json['retail_chain']['id'] == 2
    assert res.json['retail_chain']['name'] == "Victoria Gardens ТРЦ"
