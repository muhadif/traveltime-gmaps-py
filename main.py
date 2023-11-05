import asyncio
import csv
import os
from datetime import datetime
from time import sleep

import dotenv
from dotenv import load_dotenv, dotenv_values
import gmaps
import googlemaps

load_dotenv()
# Replace 'YOUR_GOOGLE_MAPS_API_KEY' with your actual Google Maps API key
gmaps.configure(api_key=os.getenv('API_KEY'))
gmaps_client = googlemaps.Client(key=os.getenv('API_KEY'))


def calculate_travel_time(origin, destination):
    now = datetime.now()
    directions_result = gmaps_client.directions(origin,
                                                destination,
                                                mode="driving",
                                                departure_time=now)
    if len(directions_result) == 0:
        return 0, 0, 0
    distance = directions_result[0]['legs'][0]['distance']['value']
    duration = directions_result[0]['legs'][0]['duration']['value']

    # distance_value = float(data['routes'][0]['legs'][0]['distance']['value'])
    speed = 0.0 if distance == 0 else distance / duration

    return distance, duration, speed * 3.6


async def process_combinations(writer, origin_data, destination_data):
    origin = f"{origin_data[2]},{origin_data[3]}"
    destination = f"{destination_data[2]},{destination_data[3]}"

    distance, travel_time, speed = calculate_travel_time(origin, destination)

    writer.writerow({
        'Kelurahan Origin': origin_data[1],
        'Kelurahan Destination': destination_data[1],
        'Distance (meter)': distance,
        'Duration in  Traffic (second)': travel_time,
        'Speed (km/h)': speed
    })
async def main():
    # Read data from CSV file
    with open('source.csv', 'r') as csvfile:
        data = csv.DictReader(csvfile)
        coordinates = [tuple(row.values()) for row in data]

    # Initialize the output CSV file
    with open('output_result.csv', 'w', newline='') as csvfile:
        fieldnames = ['Kelurahan Origin', 'Kelurahan Destination', 'Distance (meter)', 'Duration in  Traffic (second)',
                      'Speed (km/h)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for origin_data in coordinates:
            process = []
            for destination_data in coordinates:
                print(f"procees {origin_data[1]} - {destination_data[1]}")
                process_async = process_combinations(writer, origin_data, destination_data)
                process.append(process_async)
            await asyncio.gather(*process)
            print(f"done {origin_data[1]}")


if __name__ == "__main__":
    asyncio.run(main())