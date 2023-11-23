from flask import Flask, jsonify
import os
import requests
from flask import Flask, render_template, url_for, request, jsonify, render_template_string
import http.client
import json
import socket

def get_internal_ip():
    try:
        # Используем внешний сервер для определения внутреннего IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # IP-адрес Google DNS
        internal_ip = s.getsockname()[0]
        s.close()
        return internal_ip
    except Exception as e:
        print(f"Ошибка при получении внутреннего IP: {e}")
        return None

# Вызываем функцию и выводим результат
ip_address = get_internal_ip()
if ip_address:
    print(f"Ваш внутренний IP-адрес: {ip_address}")

app = Flask(__name__)

def get_api_token():
    conn = http.client.HTTPSConnection("test.aspor.ua")
    payload = 'username=aspor32&key=VqWUxWnOH223DPB1TR1sqnj6wLJofsHQvxjYmr8lJ7FS3torc51Nj0b2msAK3doaNbCXB8GQtuK2Fr31kbVX7BBtkyC68EoSzCb78Z80jZkABuKHAUtHKNL44yFSUwSmRuzYKG4K8pCFXzStRyuHxTteaw4ggpqUcPEOXjNasNUqp6NxLoTsoNFsfKkc3BOKVsRO5Ip8hNPUFquklnCZrDMKxFyKSWVRSBU48Q0PZ7dB7OnzCzYGN82AuBZOcDsq'
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': 'OCSESSID=a92fa0f6708c451de0ef84aa84; PHPSESSID=df998928fca4c46d1c446b5adcbd2dd0; currency=USD; display=grid; language=uk-ua'
    }
    conn.request("POST", "/index.php?route=api/login", payload, headers)
    res = conn.getresponse()
    data = res.read()
    api_token = (json.loads(data.decode("utf-8")))
    api_token = dict(api_token)
    api_token = api_token['api_token']
    return api_token

def get_categories(api_token, lang):
    conn = http.client.HTTPSConnection("test.aspor.ua")
    headers = {
        'Cookie': f'OCSESSID=a92fa0f6708c451de0ef84aa84; PHPSESSID=df998928fca4c46d1c446b5adcbd2dd0; language={lang}',
        'Content-type': 'application/x-www-form-urlencoded'
    }
    conn.request("GET", f"/index.php?route=api/catalog/categories&api_token={api_token}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

@app.route("/")
def index():
    api_token = get_api_token()
    lang = "uk-ua"
    categories = get_categories(api_token, lang)
    print(categories)
    user_name = "Your User Name"  # Replace with the actual user name
    return render_template("index_ua.html", user_name=user_name, categories=categories)


@app.route('/ru')
def home_ru():
    api_token = get_api_token()
    lang = "ru-ru"
    categories = get_categories(api_token, lang)
    user_name = "Your User Name"  # Replace with the actual user name
    return render_template("index_ru.html", user_name=user_name, categories=categories)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
