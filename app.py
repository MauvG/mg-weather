import datetime as dt
from datetime import datetime, timedelta
import requests
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


hour = int(datetime.now().strftime("%H"))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city")
        country_code = request.form.get("country")
        url = 'http://api.openweathermap.org/data/2.5/weather?q={},{}&appid=b79e96b76aa08a992f19c2b461333618&units=metric'.format(city, country_code)
        city = city.lower().capitalize()
        data = requests.get(url).json()

        if data['cod'] == '404':
            print("Not Found")
            return redirect("/error")
        else:
            print("Found")

        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        wind_speed = (data['wind']['speed']) * 3.6
        wind_speed = "{:.2f}".format(wind_speed)
        humidity = data['main']['humidity']
        timezone = data['timezone']
        current_time = (datetime.now() + timedelta(seconds=timezone)).strftime("%H:%M")
        description = (data['weather'][0]['description']).capitalize()
        sun_rise_time = dt.datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone']).strftime("%H:%M")
        sun_set_time = dt.datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone']).strftime("%H:%M")
        country = data['sys']['country']
        icon = data['weather'][0]['icon']
        image = "http://openweathermap.org/img/wn/{}@2x.png".format(icon)

        if 'd' in icon:
            background = "day"
        else:
            background = "night"

        return render_template("layout.html", city=city, temp=temp, feels_like=feels_like, wind_speed=wind_speed, humidity=humidity, description=description,
        sun_rise_time=sun_rise_time, sun_set_time=sun_set_time, country=country, image=image, background=background, current_time=current_time)
    else:
        if hour > 6 and hour < 18:
            background = "day"
        else:
            background = "night"

        return render_template("form.html", background=background)

@app.route("/error")
def error():
    if hour > 6 and hour < 18:
        background = "day"
    else:
        background = "night"

    return render_template("error.html", background=background)