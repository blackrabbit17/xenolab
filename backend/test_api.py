import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xenolab.settings')
django.setup()

from django.test import Client
import json

client = Client()

# Test wind endpoint
print("Testing /wind/ endpoint:")
response = client.get('/wind/')
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    print("Success!")
else:
    print("Failed to get wind data")

# Test sunlight endpoint
print("\nTesting /sunlight/ endpoint:")
response = client.get('/sunlight/')
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    print("Success!")
else:
    print("Failed to get sunlight data")

# Test temphumidity endpoint
print("\nTesting /temphumidity/ endpoint:")
response = client.get('/temphumidity/')
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    print("Success!")
else:
    print("Failed to get temperature/humidity data")

# Test lifeform endpoint with different types
print("\nTesting /lifeform/ endpoint with venus type:")
response = client.get('/lifeform/?type=venus')
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    print(f"Success! Data: {response.json()}")
else:
    print("Failed to get venus lifeform data")

print("\nTesting /lifeform/ endpoint with pitcher type:")
response = client.get('/lifeform/?type=pitcher')
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    print(f"Success! Data: {response.json()}")
else:
    print("Failed to get pitcher lifeform data")

print("\nTesting /lifeform/ endpoint with sundew type:")
response = client.get('/lifeform/?type=sundew')
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    print(f"Success! Data: {response.json()}")
else:
    print("Failed to get sundew lifeform data")

# Test map endpoint with different types
print("\nTesting /map/ endpoint with venus type:")
response = client.get('/map/?type=venus')
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    print(f"Success! Got image data, size: {len(response.content)} bytes")
else:
    print("Failed to get venus map data")

# Test atmospherics endpoint
print("\nTesting /atmospherics/ endpoint:")
response = client.get('/atmospherics/')
print(f"Status code: {response.status_code}")
if response.status_code == 200:
    print(f"Success! Data: {response.json()}")
else:
    print("Failed to get atmospherics data")