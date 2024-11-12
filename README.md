Установка зависимостей
pip install -r requirements.txt
Запуск программы
python manage.py runserver

Пароль от админ панели:
name: admin
password: admin
name: admin1
password: qwertyuiop


Команда для подключения к mysql 
mysql -u avnadmin -P 20839 -pAVNS_qs4OyVdu1pCCsV6yaIj -h whispr-whispr.i.aivencloud.com defaultdb
user: avnadmin
port: 20839
password: AVNS_qs4OyVdu1pCCsV6yaIj
host: whispr-whispr.i.aivencloud.com
name database: defaultdb

Чтобы работало websocket НЕ ОТКЛЮЧАТЬ daphne из INSTALLED_APP.
Требуется docker
Команда для запуска канального слоя docker run -p 6379:6379 -d redis:5 
http://127.0.0.1/chat
