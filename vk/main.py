from flask import Flask
from flask import request
import requests
import json
import sys
import os
import datetime
app = Flask(__name__)
TOKEN = os.environ['OLYMPLAN_VK_TOKEN']
CONFIRMATION_TOKEN = os.environ['OLYMPLAN_VK_CTOKEN']

def log(string):
    print('[{}] {}'.format(str(datetime.datetime.now()), string), file=sys.stderr)

def method(name, params, token):
    response = requests.get('https://api.vk.com/method/' + name, params={**params, 'access_token' : token})
    return response.text

@app.route('/', methods=['POST'])
def process():
    # Распаковываем json из пришедшего GET-запроса
    log(request.data)
    data = json.loads(request.data.decode('utf-8'))
    # Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return CONFIRMATION_TOKEN
    elif data['type'] == 'message_new':
        if data['object']['body'].lower() == 'расписание':
            ''
            try:
                user = json.loads(method('users.get', {'user_ids': data['object']['user_id'], 'fields': 'domain'}, TOKEN))
                domain = user['response'][0]['domain']
                contests = requests.get('http://dev.olymplan.ru/api/schedule/vk/' + domain,
                                        timeout=2).text
                method('messages.send', {'user_id': data['object']['user_id'],
                                        'message': contests}, TOKEN)
            except requests.exceptions.Timeout as e:
                log('No user {} in api'.format(domain))
                method('messages.send', {'user_id': data['object']['user_id'],
                                        'message': 'Упс! Что-то пошло не так. Вы точно зарегестрированы на сайте с ником "{}"?'.format(domain)}, TOKEN)
        else:
            method('messages.send', {'user_id' : data['object']['user_id'], 'message': 'Привет, это Олимплан! Чтобы посмотреть своё расписание напишите "Расписание"'}, TOKEN)
        return 'ok'

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=1337)

if __name__ == "__main__":
    reactor_args = {}
    
    def run_twisted_wsgi():
        from twisted.internet import reactor
        from twisted.web.server import Site
        from twisted.web.wsgi import WSGIResource

        resource = WSGIResource(reactor, reactor.getThreadPool(), app)
        site = Site(resource)
        reactor.listenTCP(1337, site, interface='0.0.0.0')
        reactor.run(**reactor_args)
        
    run_twisted_wsgi()
