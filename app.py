from flask import Flask, render_template, jsonify
import logging
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

# List of device IPs
device_info = {
    "CARGO DOMESTIC SW1:IP:231": "192.168.1.231",
    "CARGO DOMESTIC SW2:IP:232": "192.168.1.232",
    "CARGO INTERNATIONAL SW1:IP:234": "192.168.1.234",
    "CARGO SERVER ROOM SW1:IP:235": "192.168.1.235"
}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": "Basic c3VwZXI6YWRtaW4=",
    "Connection": "keep-alive",
    "Referer": "http://192.168.1.235/fn_tree.htm",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"
}

# Create a logger
logging.basicConfig(filename='temperature_log.txt', level=logging.INFO)


def get_temperature(device_ip):
    url = f"http://{device_ip}/device.htm"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        temperature_element = None

        if device_ip == "192.168.1.235":
            temperature_element = soup.find("font", {"color": "green"})
        else:
            temperature_ele = soup.find("font", {"color": "green"})
            if temperature_ele:
                temperature_element = temperature_ele.find("font")

        if temperature_element:
            temperature = temperature_element.text
            return temperature
        else:
            return "Temperature information not found"
    else:
        return f"Request failed with status code: {response.status_code}"

@app.route('/')
def index():
    temperatures = []
    for location, device_ip in device_info.items():
        temperature = get_temperature(device_ip)
        temperatures.append({"location": location, "temperature": temperature})
    return render_template('index.html', temperatures=temperatures)

#updated 
@app.route('/temperature')
def temperature():
    temperatures = []
    for location, device_ip in device_info.items():
        temperature = get_temperature(device_ip)
        temperatures.append({"location": location, "temperature": temperature})
        # Append the temperature data to the log
        logging.info(f"Device IP: {device_ip}, Temperature: {temperature}")
    return jsonify(temperatures)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

