import re
import urllib.request
from xml.dom import minidom
import requests
import csv
import json


def remove_tags(string: str) -> str:
    """
    Убирает из строки html-теги
    :param string: входящая строка с html-тегами
    :return str_without_tags: "чистая" строка без тегов
    """
    str_without_tags = re.sub(r"<[^>]+>", " ", string, flags=re.S).replace('\n', ' ')
    return str_without_tags


def convert_currency(currency_code, amount):
    currency_code = currency_code.upper()
    # Ежедневные курсы валют ЦБ РФ
    # url = "http://www.cbr.ru/scripts/XML_daily.asp"

    # Чтение URL
    # webFile = urllib.request.urlopen(url)
    # if requests.get(url).status_code != 200:
    currencies = {'AUD': 60.5738, 'AZN': 56.4149, 'GBP': 116.4578, 'AMD': 23.8891, 'BYN': 29.3918, 'BGN': 51.7707,
                      'BRL': 18.9772, 'HUF': 26.4617, 'VND': 39.7782, 'HKD': 12.2814, 'GEL': 35.5732, 'DKK': 13.5688,
                      'AED': 26.1109, 'USD': 95.9053, 'EUR': 101.4257, 'EGP': 31.0441, 'INR': 11.5191, 'IDR': 60.5539,
                      'KZT': 20.0053, 'CAD': 69.9273, 'QAR': 26.3476, 'KGS': 10.7373, 'CNY': 13.0688, 'MDL': 52.6645,
                      'NZD': 55.932, 'NOK': 86.8078, 'PLN': 22.7248, 'RON': 20.4136, 'RUR': 1,  'RUB': 1, 'XDR': 125.6609,
                      'SGD': 69.8611, 'TJS': 87.5056, 'THB': 26.3111, 'TRY': 34.264, 'TMT': 27.4015, 'UZS': 78.4116,
                      'UAH': 26.2114, 'CZK': 41.0677, 'SEK': 87.1415, 'CHF': 107.5895, 'RSD': 86.5675, 'ZAR': 50.1972,
                      'KRW': 70.9149, 'JPY': 64.0009}
#     else:
#         data = webFile.read()
#         # Имя файла
#         UrlSplit = url.split("/")[-1]
#         ExtSplit = UrlSplit.split(".")[1]
#         FileName = UrlSplit.replace(ExtSplit, "xml")
#
#         with open(FileName, "wb") as localFile:
#             localFile.write(data)
#
#         webFile.close()
#
#         # Парсинг xml и запись данных в файл
#         doc = minidom.parse(FileName)
#
#         # Извлечение данных по валютам
#         currency = doc.getElementsByTagName("Valute")
#         currencies = {}
#         currencies['RUB'] = 1
#         currencies['RUR'] = 1
#         with open("exchange.txt", "w", encoding='utf-8') as out:
#             for rate in currency:
#                 charcode = rate.getElementsByTagName("CharCode")[0]
#                 value = rate.getElementsByTagName("Value")[0]
#                 # nominal = rate.getElementsByTagName("Nominal")[0]
#                 currencies[charcode.firstChild.data] = float('.'.join(value.firstChild.data.split(',')))
    return currencies[currency_code] * amount


def save_to_csv(file_name, object_list):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # получаем список всех атрибутов из первого объекта
        attributes = vars(object_list[0]).keys()
        writer.writerow(attributes)
        for obj in object_list:
            # получаем значения атрибутов в том же порядке, что и заголовки
            values = [getattr(obj, attr) for attr in attributes]
            writer.writerow(values)


def save_to_json(file_name, object_list):
    with open(file_name, mode='w', encoding='utf-8') as file:
        json.dump([vars(obj) for obj in object_list], file, ensure_ascii=False)
