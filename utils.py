import requests

def get_aqi(city):
    api_key = "b12fa0b558f4349d5edbd5da92d9d7ef"
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    try:
        geo_res = requests.get(geo_url).json()
        if not geo_res: return None
        lat, lon = geo_res[0]['lat'], geo_res[0]['lon']
        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        return requests.get(aqi_url).json()
    except:
        return None