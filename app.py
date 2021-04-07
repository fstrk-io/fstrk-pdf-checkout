import json
import os

from datetime import datetime
from flask import Flask, render_template, request, send_file, redirect

from detect_image_size import detect
from renderer import render_pdf, upload_file
from flask_basicauth import BasicAuth


app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = os.getenv("BASIC_AUTH_USERNAME")
app.config['BASIC_AUTH_PASSWORD'] = os.getenv("BASIC_AUTH_PASSWORD")
app.config['BASIC_AUTH_FORCE'] = True

BasicAuth(app)


sample_payload_obj = {
    "customer": {
        "name": "ООО \"Рога и копыта\"",
        "inn": "78000000",
        "kpp": "41000000",
        "address": "Ярославль, ул. Строителей, д. 9",
        "phone": "+7 (900) 123-4567",
        "email": "mail@customer.ru",
        "contract": {
            "number": "Р16-12/18",
            "from_date": "2020-04-03T10:15:35.597939",
        },
    },
    "shure": {
        "name": "Общество с ограниченной ответственностью \"Шур Ар-И-И\"",
        "inn": "77123456",
        "kpp": "40001234",
        "address": "Москва, ул. Ленина, д. 1",
        "phone": "+7 (900) 765-4321",
        "email": "mail@shure.ru",
        "bank": {
            "name": "ПАО СБЕРБАНК",
            "bik": "7700000",
            "payment_account": "4212300004450",
            "correspondent_account": "3001000001000",
        },
        "director": {
            "name": "Иванов И.И.",
            "proxy": "Доверенность № 123 от 20.02.2020",
        },
        "accountant": {
            "name": "Иванов И.И.",
            "proxy": "Доверенность № 123 от 20.02.2020",
        },
        "manager": {
            "name": "Иванов И.И.",
            "proxy": None,
        },
    },
    "order": {"number": "123", "created": "2020-04-03T10:15:35.597939"},
    "products": [
        {
            "key": "dd35f031-5861-4d4d-9f13-6420afcfdb7e",
            "price": 76024.2,
            "detail": {
                "name": "AD2/K9B=-G56",
                "rate": "78,72",
                "image": "https://flex.ftrcdn.com/tickets/ad2-k9b-g56-vg1lb1y-dfv7sqs_oMancyf.png",
                "detail": "Ручной передатчик с капсюлем KSM9, цвет чёрный",
            },
            "quantity": 3,
        },
        {
            "key": "5fd5f040-1c75-4a84-abea-ba0c89f74e10",
            "price": 10291.3,
            "detail": {"name": "BETA 52A"},
            "quantity": 1,
        },
    ],
}


@app.route("/", methods=["GET", 'POST'])
def help():
    """
    Форма генерации счета для дебага. Принимает POST-запрос с пейлоадом, отдает PDF
    """
    if request.method == 'GET':
        payload_str = json.dumps(
            sample_payload_obj, indent=4, ensure_ascii=False
        )
        return render_template('sample_payload.html', sample_payload_obj=payload_str)

    payload = json.loads(request.form['payload'])
    render_pdf(payload, './output.pdf')
    response_url = upload_file('./output.pdf')

    return redirect(response_url)


@app.route("/pdf/", methods=["GET"])
def pdf():
    """
    Демо-версия PDF отчеа, открывается прямо в браузере,
    это удобнее, чем каждый раз скачивать
    """
    render_pdf(sample_payload_obj, './output.pdf')
    upload_file('./output.pdf')

    return send_file('./output.pdf', attachment_filename='output.pdf')


@app.route("/api/generate/", methods=["POST"])
def api():
    """ Продакшен-ручка. Принимает данные в JSON, возвращает ссылку в JSON """
    payload = request.json
    try:
        render_pdf(payload, './output.pdf')
        response_url = upload_file('./output.pdf')
    except Exception as e:
        app.log_exception(exc_info=e)
        return {'error': str(e)}, 500

    return {'url': response_url}


@app.route("/api/detect_image_size/", methods=["POST"])
def detect_image_size_handler():
    """Ручка не для Shure, а для МЫВМЕСТЕ: определяет ширину и высоту картинки по URL"""
    try:
        size = detect(request.json['url'])
    except Exception as e:
        return {'error': str(e)}, 500

    return {
        'width': size.width,
        'height': size.height,
    }
