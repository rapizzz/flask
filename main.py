import os
import requests
import sys
from flask import Flask, render_template, url_for, request, jsonify, render_template_string
import socket
import http.client
from urllib.parse import unquote
import json
import sys
from dbconnect import *
from dbconnect import search_person_by_phone

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
        'Cookie': 'OCSESSID=7b754a323d4b291f2e83e96b29; PHPSESSID=1e058a954dcd2e6a85ab59940f1fdc8c; currency=UAH; display=grid; language=uk-ua'
    }

    # Измененный конечный пункт API для получения продуктов по категории
    conn.request("GET",
                 f"/index.php?route=api/catalog/productsByCategory&category_id={category_id}&api_token={api_token}",
                 headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))


@app.route("/post_order", methods=['GET', 'POST'])
def post_order():
    user_id = request.args.get('id')  # используйте метод get для безопасного извлечения параметров
    naklad = request.args.get('ttn')  # также используйте метод get для безопасного извлечения параметров
    # Токен вашего телеграм-бота
    telegram_bot_token = "6181658362:AAFUajDdi79ztTxgIjN-OZCFboe01QVhmq8"

    # ID вашего чата в Телеграм
    telegram_chat_id = f"{user_id}"

    # Составление сообщения
    message = f"📦 ТТН Вашого замовлення:\n\n<code>{naklad}</code>"

    # Отправка сообщения в Телеграм
    telegram_api_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    params = {'chat_id': telegram_chat_id, 'parse_mode': 'HTML', 'text': message}
    requests.post(telegram_api_url, params=params)
    return "Order posted successfully"

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/rega", methods=['POST', 'GET'])
def rega():
    print(1)
    currency = request.form.get('currency')
    language = request.form.get('language')
    phoneNumber = request.form.get('phoneNumber')
    userType = request.form.get('userType')
    lang = "uk-ua"
    print(f"Currency: {currency}, Language: {language}, PhoneNumber: {phoneNumber}, UserType: {userType}")
    if userType == "guest":
        api_token = get_api_token()
        lang = "uk-ua"
        categories = get_categories(api_token, lang)
        print(categories)
        user_name = "Your User Name"  # Replace with the actual user name
        return render_template("index_ua.html", user_name=user_name, categories=categories)

    if phoneNumber:
        print(2)
        print(phoneNumber)
        result = search_person_by_phone(phoneNumber)
        #НУЖНО РЕШИТЬ ВОПРОС С ПОДКЛЮЧЕНИЕМ К БАЗЕ
        print(result)
        if result == False:
            print("не партнер")
        else:
            if language == "UA":
                lang = "uk-ua"
            else:
                lang = "ru-ru"
            for data in result:
                fullname, adres, ttn, tel, priceid = data
                if priceid == 1:
                    print(f'Опт')
                if priceid == 2:
                    print(f'Дропшипиинг')
                if priceid == 4:
                    print(f'Диллер')

            api_token = get_api_token()
            categories = get_categories(api_token, lang)
            print(categories)
            user_name = "Your User Name"  # Replace with the actual user name
            return render_template("index_ua.html", user_name=user_name, categories=categories)

    else:
        api_token = get_api_token()
        lang = "uk-ua"
        categories = get_categories(api_token, lang)
        print(categories)
        user_name = "Your User Name"  # Replace with the actual user name
        return render_template("index_ua.html", user_name=user_name, categories=categories)

@app.route('/novapost/divisions', methods=['GET'])
def proxy_novapost():
    query = request.args.get('query', '')
    limit = request.args.get('limit', 5)

    novapost_url = 'https://api.novaposhta.ua/v2.0/json/Address/searchSettlements'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
    }

    api_key = '574fbab8b16065351da4de2c094b7088'  # Замените YOUR_API_KEY на ваш ключ API новой почты

    params = {
        'modelName': 'Address',
        'calledMethod': 'searchSettlements',
        'apiKey': api_key,
        'methodProperties': {
            'CityName': query,
            'Limit': limit,
        },
    }

    try:
        response = requests.post(novapost_url, json=params, headers=headers)
        response.raise_for_status()

        data = response.json()

        if 'data' in data and 'Addresses' in data['data'][0]:
            addresses_list = []
            for item in data['data']:
                if 'Addresses' in item and item['Addresses']:
                    addresses = [address_info.get('Present', '') for address_info in item['Addresses'] if
                                 'Present' in address_info]
                    addresses_list.extend(addresses)

            print(addresses_list)
            addresses_list = json.dumps(addresses_list)
            print(addresses_list)
            return addresses_list

            # return json.
        else:
            # В противном случае возвращаем сообщение об ошибке
            return {'error': 'No data found'}, 404

    except requests.exceptions.RequestException as e:
        error_message = f"Request to {novapost_url} failed: {str(e)}"
        print(error_message)
        return {'error': error_message}, 500

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

@app.route('/submit_order', methods=['POST'])
def submit_order():
    print(1)
    order_data = request.get_json()
    print(order_data)
    url = "https://test.aspor.ua/index.php?route=api/catalog/sendOrder"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(order_data), headers=headers)
    print(response.text)

    jsonfile = json.dumps(order_data)
    data = json.loads(jsonfile)

    # Получение значения user_id
    user_id = data["user_id"]
    print(user_id)

    # Токен вашего телеграм-бота
    telegram_bot_token = "6181658362:AAFUajDdi79ztTxgIjN-OZCFboe01QVhmq8"

    # ID вашего чата в Телеграм
    telegram_chat_id = f"{user_id}"

    # Составление сообщения
    message = f"📦 Ваше замовлення відправлено на обробку! Очікуйте ТТН."

    # Отправка сообщения в Телеграм
    telegram_api_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    params = {'chat_id': telegram_chat_id, 'parse_mode': 'HTML', 'text': message}
    requests.post(telegram_api_url, params=params)
    return render_template("login.html")
    # Process order_data as needed, e.g., store it in a database





def get_public_ip():
    try:
        # Используем сторонний сервис для получения внешнего IP
        response = requests.get('https://api64.ipify.org?format=json')
        ip_data = response.json()
        return ip_data.get('ip')
    except Exception as e:
        print(f"Error getting public IP: {e}")
        return None

@app.route('/test')
def test():
    # Получаем внешний IP
    public_ip = get_public_ip()
    if public_ip:
        return f"{public_ip}"

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
