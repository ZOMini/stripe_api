FROM python:3.9.7-slim
WORKDIR /stripe_api
COPY stripe_api/ .
RUN pip install -r requirements.txt
# RUN python3 script.py
CMD ["gunicorn", "stripe_api.wsgi:application", "--bind", "0:8005" ] 
