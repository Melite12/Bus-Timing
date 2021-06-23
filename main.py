from flask import Flask, redirect, url_for, request, render_template
import requests
import datetime
import json
from pprint import pprint

app = Flask(__name__)
headers = {"AccountKey": "u/cdTkg+Qbu9VsF/1MUVfA== ", "accept": "application/json"}


def get_bus_data(code):
    return requests.get(
        "http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2",
        headers=headers,
        params={"BusStopCode": code},
    ).json()

def parse_data(bus_data):
    bus_dict = {}
    bus_data = bus_data['Services']
    for data in bus_data:
        bus_no = data["ServiceNo"]
        bus_timing = [data["NextBus"]["EstimatedArrival"][11:19], data["NextBus2"]["EstimatedArrival"][11:19],
                      data["NextBus3"]["EstimatedArrival"][11:19]]
        bus_dict[bus_no] = bus_timing

    return bus_dict

def parse_time(bus_dict):
    for times in bus_dict.values():
        for time in times:
            time = time[11:19]

    return bus_dict



@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        code = int(request.form.get("code"))
        return redirect(url_for("bus_timing", code=code))
    return render_template("homepage.html")


@app.route("/bus_stop/<code>")
def bus_timing(code):
    bus_data = get_bus_data(code)
    bus_dict = parse_data(bus_data)
    bus_dict = parse_time(bus_dict)
    pprint(bus_dict)

    return render_template("bus_timing.html", code=code, bus_dict = bus_dict)


if __name__ == "__main__":
    app.run(debug=True)
