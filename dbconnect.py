import pymssql

# Замените значения на реальные данные подключения
server = '94.158.157.13'
database = 'Одесса'
username = 'asporsql'
password = 'QazXswEdc132'

def search_person_by_phone(phone_number):
    try:
        conn = pymssql.connect(server=server, user=username, password=password, database=database)
        cursor = conn.cursor()

        # Выполнение SQL-запроса с фильтром по номеру телефона
        query = f"SELECT FullName, Adr, CodeNDS, Tel, PriceID FROM Persons WHERE Tel LIKE '%{phone_number}%'"
        cursor.execute(query)

        # Получение результатов запроса
        rows = cursor.fetchall()

        if rows:
            result_data = []
            for row in rows:
                fullname = row[0]  # Фулл имя
                adres = row[1]  # Адрес
                ttn = row[2]  # Циферка перед True
                tel = row[3]  # Номер телефона
                priceid = row[4]  # PriceID
                result_data.append((fullname, adres, ttn, tel, priceid))

            return result_data
        else:
            return False

    except pymssql.Error as e:
        return f"Ошибка: {e}"

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


search_name = "Костенко Олег Олександрович"  # Часть ФИО для поиска

def search_by_fullname(fullname):
    try:
        conn = pymssql.connect(server=server, user=username, password=password, database=database)
        print("Соединение установлено.")

        cursor = conn.cursor()

        # Выполнение SQL-запроса для поиска по части ФИО в Text3 и выборки данных из колонок Text3 и Text5
        query = f"SELECT ID, Text3, Text5, DocDate, DocSum FROM Documents WHERE Text3 LIKE N'%{fullname}%'"
        cursor.execute(query)

        # Получение результатов запроса
        rows = cursor.fetchall()
        result = []

        for row in rows:
            id = row[0]
            ordername = row[1]
            ttn = row[2]
            date = row[3]
            summ = row[4]
            result.append((id, ordername, ttn, date, summ))

        # Закрытие курсора и подключения
        cursor.close()
        conn.close()

        return result

    except pymssql.Error as e:
        print("Соединение не установлено.")
        print("Ошибка:", e)
