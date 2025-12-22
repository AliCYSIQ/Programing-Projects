import requests as req

API_KEY = "70222fa3697dffa80ae91f83bbf2cc71"
base_url = "http://api.openweathermap.org/data/2.5/weather"
while True:
        
    city = input("\nenter the name of the city('quit' to quit): ").lower()
    if city == "quit":
        break
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric" 
    }

    response = req.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"\nWeather in {city.title()} : {data.get('main').get('temp')}C, {data.get('weather')[0].get('description')}.")
    elif response.status_code == 404:
        print(f"\nthere's no city named '{city}', please write it well")
    elif response.status_code == 401:
        print(f"\n\nthere's error in api key , please wail until we fix it ")

