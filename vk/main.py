from flask import Flask
from flask import request
import requests
import json
app = Flask(__name__)
TOKEN = 'a765d57739043c986889dac1608d9157b6784518c6368b04fa0cbcee91a1c580c44a107aa1930cec4b066'
confirmation_token = ''

def method(name, params, token):
    response = requests.get('https://api.vk.com/method/' + name, params={**params, 'access_token' : token})
    print(response.url)
    print(response.text)

@app.route('/', methods=['POST'])
def process():
    # Распаковываем json из пришедшего GET-запроса
    data = json.loads(request.data)
    # Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        if data['object']['body'].lower == 'расписание':
            ''
            try:
                user = json.loads(method('users.get', {'user_ids': data['object']['body'], 'fields': 'domain'}, TOKEN))
                domain = user['response']['domain']
                print(domain)
                contests = requests.get('http://dev.olymplan.ru/api/schedule/vk/' + domain,
                                        timeout=2).text
                method('message.send', {'user_id': data['object']['user_id'],
                                        'message': contests.text}, TOKEN)
            except requests.exceptions.Timeout as e:
                print('No user {} in api'.format(domain))
                method('message.send', {'user_id': data['object']['user_id'],
                                        'message': 'Упс! Что-то пошло не так. Вы точно зарегестрированы на сайте с ником "{}"?'.format(domain)}, TOKEN)
                return
        else:
            method('message.send', {'user_id' : data['object']['user_id'], 'message': 'Привет, это Олимплан! Чтобы посомтреть своё расписание напишите "Расписание"'}, TOKEN)
        return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)