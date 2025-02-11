import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('en_GB')  # Use UK locale

def generate_vehicle_data(n_vehicles=20):
    # UK boundary coordinates
    uk_bounds = {
        'lat_min': 50.10319,  # Southern England
        'lat_max': 58.44377,  # Northern Scotland
        'lon_min': -7.64133,  # Western Ireland
        'lon_max': 1.75159    # Eastern England
    }

    # Major UK cities with their coordinates
    uk_cities = [
        {'name': 'London', 'lat': 51.5074, 'lon': -0.1278},
        {'name': 'Manchester', 'lat': 53.4808, 'lon': -2.2426},
        {'name': 'Birmingham', 'lat': 52.4862, 'lon': -1.8904},
        {'name': 'Leeds', 'lat': 53.8008, 'lon': -1.5491},
        {'name': 'Glasgow', 'lat': 55.8642, 'lon': -4.2518},
        {'name': 'Liverpool', 'lat': 53.4084, 'lon': -2.9916},
        {'name': 'Edinburgh', 'lat': 55.9533, 'lon': -3.1883},
        {'name': 'Bristol', 'lat': 51.4545, 'lon': -2.5879}
    ]

    vehicles = []
    for _ in range(n_vehicles):
        # Randomly select a city as starting point
        city = np.random.choice(uk_cities)
        # Add some random offset to spread vehicles around the city
        lat_offset = np.random.uniform(-0.1, 0.1)
        lon_offset = np.random.uniform(-0.1, 0.1)

        vehicle = {
            'vehicle_id': fake.uuid4(),
            'model': fake.random_element(['DAF XF', 'Volvo FH', 'Mercedes Actros', 'Scania R Series']),
            'year': fake.random_int(min=2018, max=2023),
            'status': fake.random_element(['Active', 'Maintenance', 'Idle']),
            'lat': np.clip(city['lat'] + lat_offset, uk_bounds['lat_min'], uk_bounds['lat_max']),
            'lon': np.clip(city['lon'] + lon_offset, uk_bounds['lon_min'], uk_bounds['lon_max']),
            'fuel_level': fake.random_int(min=10, max=100),
            'speed': fake.random_int(min=0, max=120),
            'driver': fake.name(),
            'last_maintenance': fake.date_this_year(),
            'mileage': fake.random_int(min=1000, max=100000),
            'direction': fake.random_int(min=0, max=360),  # Added direction for movement
            'current_city': city['name']  # Add current city information
        }
        vehicles.append(vehicle)
    return pd.DataFrame(vehicles)

def generate_telematics_data(n_records=100):
    data = []
    base_time = datetime.now()
    for i in range(n_records):
        record = {
            'timestamp': base_time - timedelta(minutes=i*5),
            'driver_id': fake.uuid4(),
            'harsh_braking': fake.random_int(min=0, max=5),
            'speeding_events': fake.random_int(min=0, max=10),
            'sharp_turns': fake.random_int(min=0, max=3),
            'safety_score': fake.random_int(min=60, max=100),
            'distance_driven': fake.random_int(min=50, max=500)
        }
        data.append(record)
    return pd.DataFrame(data)

def generate_iot_data(n_devices=50):
    data = []
    for _ in range(n_devices):
        device = {
            'device_id': fake.uuid4(),
            'vehicle_id': fake.uuid4(),
            'temperature': fake.random_int(min=60, max=90),
            'engine_health': fake.random_element(['Good', 'Fair', 'Poor']),
            'battery_level': fake.random_int(min=20, max=100),
            'diagnostic_code': fake.random_element(['P0100', 'P0200', 'P0300', None]),
            'last_ping': fake.date_time_between(start_date='-1h', end_date='now')
        }
        data.append(device)
    return pd.DataFrame(data)

def generate_logistics_data(n_shipments=30):
    uk_cities = ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow', 
                'Liverpool', 'Edinburgh', 'Bristol', 'Cardiff', 'Belfast']

    data = []
    for _ in range(n_shipments):
        origin, destination = np.random.choice(uk_cities, size=2, replace=False)
        data.append({
            'shipment_id': fake.uuid4(),
            'origin': origin,
            'destination': destination,
            'status': fake.random_element(['In Transit', 'Delivered', 'Delayed']),
            'eta': fake.future_date(),
            'temperature': fake.random_int(min=-5, max=25),
            'humidity': fake.random_int(min=30, max=70),
            'vehicle_id': fake.uuid4()
        })
    return pd.DataFrame(data)