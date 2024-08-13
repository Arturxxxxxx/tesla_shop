import requests

# Логин для доступа к платформе smspro.nikita.kg.  
login = 'koreacenter'
# Пароль для доступа к платформе smspro.nikita.kg. 
password = 'yR70vDbg'
# Уникальный идентификатор транзакции. Для каждой отправки он должен быть уникальным.
# Используя этот ID можно получить отчет о доставке сообщения.
transactionId = 'U4B4m1za1'
# Имя отправителя - должно быть согласовано с администратором smspro.nikita.kg
sender = 'Koreacenter'
# Текст СМС-сообщения - текст на русском или латинице любой длины (до 800 знаков). 
# В случае необходимости платформа smspro.nikita.kg автоматически разделит текст на несколько сообщений. 
text = 'fjkgsjdsljdfjgld;gdg'
# Номер телефона получателя СМС в формате 996ххххххххх. 
# В одной транзакции отправки может быть указано и более 1го телефона.
phone = '996220073654'

xml_data = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
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


url = 'https://smspro.nikita.kg/api/message'
headers = {'Content-Type': 'application/xml'}

response = requests.post(url, data=xml_data, headers=headers)
if response.status_code == 200:
    print('Ответ сервера:', response.text)
