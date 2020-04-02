import json

from flask import Flask, render_template, request, send_file

from renderer import render_pdf

app = Flask(__name__)


sample_payload_obj = {
    "customer": {
        "bank": {
            "name": "ПАО СБЕРБАНК",
            "bik": "7700000",
            "kor_schet": "3001000001000",
        },
        "inn": "77123456",
        "kpp": "41000000",
        "rasch_schet": "4212300004450",
        "address": "Москва, ул. Строителей, 9",
    },
    "shure": {
        "rukovoditel": {
            "name": "Иванов И.И.",
            "doverennost": "доверенность № 123 от 20.02.2020",
        },
        "buhgalter": {
            "name": "Иванов И.И.",
            "doverennost": "доверенность № 123 от 20.02.2020",
        },
        "manager": {"name": "Иванов И.И.", "doverennost": None},
    },
    "products": [
        {
            "key": "dd35f031-5861-4d4d-9f13-6420afcfdb7e",
            "price": 76024,
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
            "price": 10291,
            "detail": {"name": "BETA 52A"},
            "quantity": 1,
        },
    ],
    "order": {"number": "123", "created": "27 мая 2020"},
}



@app.route("/", methods=["GET"])
def help():

    payload_str = json.dumps(sample_payload_obj, indent=4, ensure_ascii=False)
    return render_template('sample_payload.html', sample_payload_obj=payload_str)


@app.route("/pdf/", methods=["POST", "GET"])
def pdf():

    if request.method == 'GET':
        render_pdf(sample_payload_obj, './output.pdf')
    return send_file('./output.pdf', attachment_filename='output.pdf')


