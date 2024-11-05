import pandas as pd
from datetime import datetime, timedelta
import requests
import calendar

def getResponseFromCurrentAPI(lat = 21.0245, lon =105.841, apiKey = "89f98790ae72fd8a2da6032ba8e9c7b3"):
    endpoint = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apiKey}"
    print(endpoint)

    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            print("Successful request")
            return response.json()
        
        else:
            print(f"Something wrong:\n\
                    Code: {response.status_code},\n\
                    Message: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def transformResponseCurrentToDataframe(lat = 21.0245, lon =105.841, apiKey = "89f98790ae72fd8a2da6032ba8e9c7b3") -> pd.DataFrame:
    response = getResponseFromCurrentAPI(lat= lat, lon= lon, apiKey= apiKey)
    # listKeys = ["Country", "Name", "TimeStamp", "Temperature", "Feels Like", "Pressure", "Humidity", "Wind Speed", "Cloud", "Weather Description Main", "Rain (1h)"]
    listKeys = ["TimeStamp", "Temperature", "Feels Like", "Pressure", "Humidity", "Wind Speed", "Cloud", "Weather Description Main", "Rain (1h)"]
    dfDict = {f"{key}": None for key in listKeys}

    # Extract needed atribute from Response(JSON)
    # country = response["sys"].get("country")
    # name = response["name"]
    timestamp = datetime.utcfromtimestamp(response['dt']).strftime('%Y-%m-%d %H:%M:%S')
    temperature = response["main"].get("temp")
    feelslike = response["main"].get("feels_like")
    pressure = response["main"].get("pressure")
    humidity = response["main"].get("humidity")
    windspeed = response["wind"].get("speed")
    cloud = response["clouds"].get("all")
    weatherdescriptionmain = response["weather"][0].get("main")
    if response.get("rain"):
        rain1h = response["rain"].get("1h", 0)
    else:
        rain1h = 0

    # listValues = [country, name, timestamp, temperature, feelslike, pressure, humidity, windspeed, cloud, weatherdescriptionmain, rain1h]
    listValues = [timestamp, temperature, feelslike, pressure, humidity, windspeed, cloud, weatherdescriptionmain, rain1h]


    for i in range(9):
        dfDict[listKeys[i]] = listValues[i]

    df = pd.DataFrame(dfDict, index= [0]) # index = [0]: ensure that Pandas treat each value in dfDict as single row
    df = df.applymap(lambda x: pd.to_numeric(x, errors= "ignore"))
    df["TimeStamp"] = pd.to_datetime(df["TimeStamp"])

    return df