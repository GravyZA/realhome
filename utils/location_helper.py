import requests

def get_coordinates(location_name):
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": location_name, "format": "json", "limit": 1},
            headers={"User-Agent": "RealHome/1.0 (your-email@example.com)"}
        )
        data = response.json()
        if data:
            lat = float(data[0]["lat"])
            lng = float(data[0]["lon"])
            return lat, lng
    except Exception as e:
        print(f"[Geo Error] {e}")
    return None, None
