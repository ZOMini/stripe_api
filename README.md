[![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](http://130.193.37.228:9005/item/1/)
[![foodgram workflow](https://github.com/zomini/stripe_api/actions/workflows/main.yml/badge.svg)](https://github.com/zomini/zomini/stripe_api/actions/workflows/main.yml)
# stripe_api
Spripe API. Работа с платежной системой Stripe. Тестовое задание.<br>
Текст задания - [Test Task](https://github.com/ZOMini/stripe_api/blob/main/Testwork%20Python%20Developer.pdf)

### Проект работает:
- Для тестирования использовал REST Client for Visual Studio Code, см. файл requests.http в папке с проектом.
- http://130.193.37.228:9005/redoc/ - API documentation
- http://130.193.37.228:9005/admin/ - username = superuser / password = password
- http://130.193.37.228:9005/item/1/ api html с кнопкой покупки отдельного товара.
- http://130.193.37.228:9005/item/1/?coupon=sljEVntJ С промиком.
- http://130.193.37.228:9005/buy/1/ api редиректа на stripe
- http://130.193.37.228:9005/buy/1/?coupon=sljEVntJ С промиком.
- http://130.193.37.228:9005/order_create/ api создания ордера (см. файл requests.http, корень репозитария).
- http://130.193.37.228:9005/order_html/1/ api html с кнопкой покупки по Ордеру.
- http://130.193.37.228:9005/order_buy/1/ api редиректа ордера на stripe.

### Инструкции для деплоя проекта на сервере:
- https://docs.docker.com/engine/install/ - Устанавливаем докер
- В 'Actions secrets' в настройках вашего проекта на GitHub внесите необходимые параметры сервера:
(некоторые переменные задал по умолчанию, для ускорения деплоя и тестирования)
```
DOCKER_PASSWORD - Пароль от DockerHub (для обновления образа на DockerHub)
DOCKER_USERNAME - Логин от DockerHub (для обновления образа на DockerHub)
HOST - Публичный ip адрес сервера
USER - Пользователь сервера
PASSPHRASE - Если ssh-ключ защищен фразой-паролем
SSH_KEY - Приватный ssh-ключ
SECRET_KEY
DEBUG
```
- После деплоя запускаем скрипт, из папки ~/stripe_api, там лежит docker-compose.yaml - (Миграции, статика, создание суперпользователя - username = superuser password = password):
```
sudo docker-compose exec web python script.py
```


### Полезные команды:
```
sudo docker-compose exec web python script.py
sudo docker-compose exec web python manage.py collectstatic --noinput
sudo docker-compose exec web python manage.py migrate --noinput
sudo docker-compose down
sudo docker image prune
```