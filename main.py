from flask import Flask, jsonify
import os
import requests
import sys
from flask import Flask, render_template, url_for, request, jsonify, render_template_string
import socket
import http.client
import json
import sys

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
    print(data)
    api_token = json.loads(data.decode("utf-8"))['api_token']
    print(api_token)
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

def get_tovar(category_id):
    api_token = get_api_token()
    conn = http.client.HTTPSConnection("test.aspor.ua")
    category_id = f'{category_id}'  # Замените на фактический ID категории
    print(category_id)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'api_token': api_token,
        'Cookie': 'OCSESSID=7b754a323d4b291f2e83e96b29; PHPSESSID=1e058a954dcd2e6a85ab59940f1fdc8c; currency=USD; display=grid; language=uk-ua'
    }

    # Измененный конечный пункт API для получения продуктов по категории
    conn.request("GET",
                 f"/index.php?route=api/catalog/productsByCategory&category_id={category_id}&api_token={api_token}",
                 headers=headers)
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

@app.route('/uacategory_id', methods=['GET'])
def categ():
    try:
        # Получаем значение параметра uacategory_id из запроса
        category_id = request.args.get('uacategory_id')
        print(category_id)
        category_id = str(category_id)
        tovar_list = get_tovar(category_id)
        if not tovar_list["categories"]:  # Если категории пусты
            return render_template('products.html', products=tovar_list["products"])

        # Если категории не пустые
        return render_template('categories.html', categories=tovar_list["categories"])
    except:
        return "Нет товаров в данной категории!"
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
