[![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](http://130.193.37.228:9005/item/1/)
[![foodgram workflow](https://github.com/zomini/stripe_api/actions/workflows/main.yml/badge.svg)](https://github.com/zomini/zomini/stripe_api/actions/workflows/main.yml)
# stripe_api
Spripe API. Работа с платежной системой Stripe.<br>


Проект работает: <br>
- Для тестирования использовал REST Client for Visual Studio Code, см. файл requests.http в папке с проектом.
- http://130.193.37.228:9005/admin/ -username = superuser password = password
- http://130.193.37.228:9005/item/1/ api html с кнопкой покупки отдельного товара.
- http://130.193.37.228:9005/item/1/?coupon=sljEVntJ С промиком.
- http://130.193.37.228:9005/buy/1/ api редиректа на stripe
- http://130.193.37.228:9005/item/1/?coupon=sljEVntJ c промиком
- http://130.193.37.228:9005/order_create/ api создания ордера (см. файл requests.http, корень репозитария, дада:) - нужна api документация )
- http://130.193.37.228:9005/order_html/1/ api html с кнопкой покупки по Ордеру 
- http://130.193.37.228:9005/order_buy/1/ api редиректа ордера на stripe

Полезные команды:
```
sudo docker-compose exec web python script.py
sudo docker-compose exec web python manage.py collectstatic --noinput
sudo docker-compose exec web python manage.py migrate --noinput 
```