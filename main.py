import aiohttp
import asyncio
import csv


async def get_travel_time(api_key, session, origin_coord, destination_coord):
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": f"{origin_coord[0]},{origin_coord[1]}",
        "destinations": f"{destination_coord[0]},{destination_coord[1]}",
        "mode": "driving",
        "key": api_key,
    }

    async with session.get(base_url, params=params) as response:
        data = await response.json()
        print(data)

        try:
            travel_time = data["rows"][0]["elements"][0]["duration"]["text"]
            return travel_time
        except (KeyError, IndexError):
            return "N/A"


def read_coordinates_from_csv(csv_file):
    coordinates = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip the header
        for row in reader:
            kecamatan, kelurahan, xcoord, ycoord = row
            coordinates.append((float(xcoord), float(ycoord), kelurahan))
    return coordinates


async def generate_combination_csv(api_key, coordinates, output_file):
    async with aiohttp.ClientSession() as session:
        with open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            header = ["Kelurahan"] + [coord[2] for coord in coordinates]
            writer.writerow(header)

            for origin_coord in coordinates:
                row = [origin_coord[2]]

                tasks = [get_travel_time(api_key, session, (origin_coord[0], origin_coord[1]),
                                         (dest_coord[0], dest_coord[1])) for dest_coord in coordinates]

                results = await asyncio.gather(*tasks)

                row.extend(results)
                writer.writerow(row)


if __name__ == "__main__":
    api_key = env.API_KEY
    input_csv_file = "source.csv"

    coordinates = read_coordinates_from_csv(input_csv_file)

    output_file = "travel_time_matrix.csv"

    asyncio.run(generate_combination_csv(api_key, coordinates, output_file))
