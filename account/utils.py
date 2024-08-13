
    # Отправка сообщения с указанием времени отправки в формате YYYYMMDDHHMMSS.
    # time = '20240101123000'
    # xml_data = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
    # <message>
    #    <login>{login}</login>
    #    <pwd>{password}</pwd>
    #    <id>{transactionId}</id>
    #    <sender>{sender}</sender>
    #    <text>{text}</text>
    #    <time>{time}</time>
    #    <phones>
    #        <phone>{phone}</phone>
    #    </phones>
    # </message>"""


    # Отправка сообщения на несколько номеров.
    # phones = ['996550403993', '996779377888']
    # phones_xml = ''.join([f'<phone>{phone}</phone>' for phone in phones])
    # xml_data = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
    # <message>
    #    <login>{login}</login>
    #    <pwd>{password}</pwd>
    #    <id>{transactionId}</id>
    #    <sender>{sender}</sender>
    #    <text>{text}</text>
    #    <phones>
    #        <phone>{phones_xml}</phone>
    #    </phones>
    # </message>"""


    # Отправка тестового сообщения, сообщение не будет отправлено фактически и не будет тарифицировано.
    # xml_data = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
    # <message>
    #    <login>{login}</login>
    #    <pwd>{password}</pwd>
    #    <id>{transactionId}</id>
    #    <sender>{sender}</sender>
    #    <text>{text}</text>
    #    <phones>
    #        <phone>{phone}</phone>
    #    </phones>
    #    <test>1</test>
    # </message>"""



import requests
import logging
from decouple import config
import uuid

logger = logging.getLogger(__name__)

def send_sms(phone_number, message):
    
    # Логин для доступа к платформе smspro.nikita.kg.  
    login = config('LOGIN')
    # Пароль для доступа к платформе smspro.nikita.kg. 
    password = config('PASSWORD')
    # Уникальный идентификатор транзакции. Для каждой отправки он должен быть уникальным.
    transactionId = str(uuid.uuid4())
    print(transactionId)
    # Имя отправителя - должно быть согласовано с администратором smspro.nikita.kg
    sender = config('SENDER')
    # Текст СМС-сообщения - текст на русском или латинице любой длины (до 800 знаков). 
    text = message
    # Номер телефона получателя СМС в формате 996ххххххххх. 
    phone = phone_number

    xml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
    <message>
        <login>{login}</login>
        <pwd>{password}</pwd>
        <id>{transactionId}</id>
        <sender>{sender}</sender>
        <text>{text}</text>
        <phones>
            <phone>{phone}</phone>
        </phones>
    </message>"""
    
    url = 'https://smspro.nikita.kg/api/message'
    headers = {'Content-Type': 'application/xml'}

    try:
        response = requests.post(url, data=xml_data, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        
        # Логирование ответа
        logger.info('Ответ сервера: %s', response.text)
        
        return response.text
    except requests.exceptions.RequestException as e:
        # Логирование ошибки
        logger.error('Ошибка при отправке SMS: %s', e)
        return None
