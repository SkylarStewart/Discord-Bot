import configparser
import requests

config = configparser.ConfigParser()
config.read('config.ini')

weather_api_key = config['APIdata']['weather_api_key']
discord_api_key = config['APIdata']['discord_api_key']
empty_url = "http://api.openweathermap.org/data/2.5/weather?"


#returns an array in the form [ temperature, pressure, humidity, description, name, country, emoji]
def get_weather(cityName):
    cityNameCaps = cityName.upper()
    fullURL = empty_url + "appid=" + weather_api_key + "&q=" + cityName
    response = requests.get(fullURL)

    #convert into JSON
    weatherData = response.json()

    #throws an error if the city could not be found in the query
    if weatherData["cod"] == "404":
        raise ValueError("error: city was not located")
    else:
        tph = weatherData["main"]
        countrydetails = weatherData["sys"]
        country = countrydetails["country"]
        weatherDesc = weatherData["weather"]
        weatherBase = weatherDesc[0]["main"]

        #a key that maps every single weather description to an emoji for text display
        weather_key = {
            "Thunderstorm": ":thunder_cloud_rain:",
            "Drizzle": ":cloud_rain:",
            "Rain": ":cloud_rain:",
            "Snow": ":snowflake:",
            "Mist": ":fog:",
            "Smoke": ":fog:",
            "Haze": ":fog:",
            "Dust": ":fog:",
            "Fog": ":fog:",
            "Sand": ":fog:",
            "Ash": ":fog:",
            "Squall": ":dash:",
            "Tornado": ":cloud_tornado:",
            "Clear": ":sunny:",
            "Clouds": ":white_sun_cloud:"
        }

        #if it is currently nighttime, the weatherEmoji is overridden with a crescent moon
        weatherEmoji = weather_key[weatherBase]
        if weatherDesc[0]["icon"][2] == 'n':
            weatherEmoji = ":crescent_moon:"

        # convert temperature from kelvin to fahrenheit
        temp = float(tph["temp"])
        temp = round((((temp - 273.15) * 1.8) + 32), 1)
        tempString = str(temp)

        weatherArray = []
        weatherArray.append(tempString)
        weatherArray.append(str(tph["pressure"]))
        weatherArray.append(str(tph["humidity"]))
        weatherArray.append(weatherDesc[0]["description"])
        weatherArray.append(weatherData["name"])
        weatherArray.append(country)
        weatherArray.append(weatherEmoji)

        return weatherArray

