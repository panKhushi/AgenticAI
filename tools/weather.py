import requests
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def execute(arguments: dict):

    city = arguments.get("city")

    if not city:
        return "Weather Error: City not provided."

    try:
        geo_response = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1},
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

        current = weather_response.json()["current_weather"]

        return (
            f"City: {city_name}, Country: {country}\n"
            f"Temperature: {current['temperature']}°C\n"
            f"Wind Speed: {current['windspeed']} km/h\n"
            f"Weather Code: {current['weathercode']}"
        )

    except Exception as e:
        return f"Weather Error: {e}"


if __name__ == "__main__":
    print(execute({"city": "Delhi"}))