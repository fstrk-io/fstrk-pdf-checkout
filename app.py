import json
import os

from datetime import datetime
from flask import Flask, render_template, request, send_file, redirect

from detect_image_size import detect
from renderer import render_pdf, upload_file
from flask_basicauth import BasicAuth

app = Flask(__name__)

app.config["BASIC_AUTH_USERNAME"] = os.getenv("BASIC_AUTH_USERNAME")
app.config["BASIC_AUTH_PASSWORD"] = os.getenv("BASIC_AUTH_PASSWORD")
app.config["BASIC_AUTH_FORCE"] = True

BasicAuth(app)

sample_payload_obj = {
    "customer": {
        "inn": "___________",
        "kpp": "___________",
        "name": "___________",
        "email": "test@test.ru",
        "phone": "+79312980954",
        "address": "Ленина, 1",
        "contract": {
            "number": "___________",
            "from_date": "2020-04-03T21:44:38.135914",
        },
    },
    "shure": {
        "inn": "123",
        "kpp": "456",
        "bank": {
            "bik": "044030790",
            "name": "ПАО «БАНК «САНКТ-ПЕТЕРБУРГ»",
            "payment_account": "123",
            "correspondent_account": "456",
        },
        "name": "ООО «ЕвроКомпозит» (EuroComposite LLC)",
        "email": "info@shure.ru",
        "phone": "тел.(812) 981-48-31",
        "address": "191024, Россия, Санкт-Петербург, Невский проспект, д. 170",
        "manager": {"name": "Сосновский Илья Сергеевич", "proxy": None},
        "director": {
            "name": "Сосновский Илья Сергеевич",
            "proxy": "На основании Устава",
        },
        "accountant": {
            "name": "Сосновский Илья Сергеевич",
            "proxy": "На основании Приказа №1 от 02.08.2017 г.",
        },
    },
    "products": [
        {
            "code": 3530,
            "guid": "e59cc7bd-f193-4131-b4db-24e7637981ee",
            "image": "https://flex.ftrcdn.com/tickets/blx14re-sm35-m17-0sdr6a0.png",
            "price": 41930,
            "title": "BLX14RE/SM35-M17",
            "category": "66ca4151-f81b-4dc8-8b64-ab708a6f8adf",
            "quantity": 1,
            "description": "Головной кардиоидный микрофон с рэковым аналоговым приёмником.",
            "field_html_2": "",
            "product_type": "f0abe3eb-e29f-4db8-8273-9ed655d1acb3",
            "price_comment": None,
            "discount_price": 41930,
            "field_string_3": "4-5 недель",
            "field_multichoice": [],
            "field_multichoice_5": ["Вокальный"],
            "field_multichoice_6": [],
        }
    ],
    "order": {"number": "348ш", "created": "2021-04-19T10:27:01.444955"},
    "discount_price": 41930,
}


@app.route("/", methods=["GET", "POST"])
def help():
    """
    Форма генерации счета для дебага. Принимает POST-запрос с пейлоадом, отдает PDF
    """
    if request.method == "GET":
        payload_str = json.dumps(sample_payload_obj, indent=4, ensure_ascii=False)
        return render_template("sample_payload.html", sample_payload_obj=payload_str)

    payload = json.loads(request.form["payload"])
    render_pdf(payload, "./output.pdf")
    response_url = upload_file("./output.pdf")

    return redirect(response_url)


@app.route("/pdf/", methods=["GET"])
def pdf():
    """
    Демо-версия PDF отчеа, открывается прямо в браузере,
    это удобнее, чем каждый раз скачивать
    """
    render_pdf(sample_payload_obj, "./output.pdf")
    upload_file("./output.pdf")

    return send_file("./output.pdf", attachment_filename="output.pdf")


@app.route("/api/generate/", methods=["POST"])
def api():
    """ Продакшен-ручка. Принимает данные в JSON, возвращает ссылку в JSON """
    payload = request.json
    try:
        render_pdf(payload, "./output.pdf")
        response_url = upload_file("./output.pdf")
    except Exception as e:
        app.log_exception(exc_info=e)
        return {"error": str(e)}, 500

    return {"url": response_url}


@app.route("/api/detect_image_size/", methods=["POST"])
def detect_image_size_handler():
    """Ручка не для Shure, а для МЫВМЕСТЕ: определяет ширину и высоту картинки по URL"""
    try:
        size = detect(request.json["url"])
    except Exception as e:
        return {"error": str(e)}, 500

    return {
        "width": size.width,
        "height": size.height,
    }
