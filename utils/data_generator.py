import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def generate_vehicle_data(n_vehicles=20):
    vehicles = []
    for _ in range(n_vehicles):
        vehicle = {
            'vehicle_id': fake.uuid4(),
            'model': fake.random_element(['Toyota Truck', 'Ford F150', 'Volvo FH16', 'Mercedes Actros']),
            'year': fake.random_int(min=2018, max=2023),
            'status': fake.random_element(['Active', 'Maintenance', 'Idle']),
            'lat': fake.latitude(),
            'lon': fake.longitude(),
            'fuel_level': fake.random_int(min=10, max=100),
            'speed': fake.random_int(min=0, max=120),
            'driver': fake.name(),
            'last_maintenance': fake.date_this_year(),
            'mileage': fake.random_int(min=1000, max=100000),
            'direction': fake.random_int(min=0, max=360)  # Added direction for movement
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
    data = []
    for _ in range(n_shipments):
        data.append({
            'shipment_id': fake.uuid4(),
            'origin': fake.city(),
            'destination': fake.city(),
            'status': fake.random_element(['In Transit', 'Delivered', 'Delayed']),
            'eta': fake.future_date(),
            'temperature': fake.random_int(min=-5, max=25),
            'humidity': fake.random_int(min=30, max=70),
            'vehicle_id': fake.uuid4()
        })
    return pd.DataFrame(data)

def generate_construction_data(n_equipment=25):
    data = []
    for _ in range(n_equipment):
        data.append({
            'equipment_id': fake.uuid4(),
            'type': fake.random_element(['Excavator', 'Bulldozer', 'Crane', 'Loader']),
            'utilization_rate': fake.random_int(min=30, max=100),
            'maintenance_due': fake.date_this_month(),
            'fuel_consumption': fake.random_int(min=10, max=50),
            'location': fake.city(),
            'operator': fake.name()
        })
    return pd.DataFrame(data)