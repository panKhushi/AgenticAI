import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)


from config import GEOCODING_URL, WEATHER_URL
import requests



def execute(arguments: dict):

    city = arguments.get("city")

    if not city:
        return "Weather Error: City not provided."

    try:
        # Get coordinates
        geo_response = requests.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 1
            },
            timeout=10
        )

        geo_response.raise_for_status()

        geo_data = geo_response.json()

        if "results" not in geo_data:
            return f"City '{city}' not found."

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]
        city_name = location["name"]
        country = location.get("country", "")

        # Get weather
        weather_response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": True
            },
            timeout=10
        )

        weather_response.raise_for_status()

        weather_data = weather_response.json()

        current = weather_data["current_weather"]

        temperature = current["temperature"]
        windspeed = current["windspeed"]
        weather_code = current["weathercode"]

        return (
            f"City: {city_name}, Country: {country}\n"
            f"Temperature: {temperature}°C\n"
            f"Wind Speed: {windspeed} km/h\n"
            f"Weather Code: {weather_code}"
        )

    except Exception as e:
        return f"Weather Error: {e}"
if __name__ == "__main__":
    print("Weather tool \n")
    print(
        execute({"city": "New York"})
    )