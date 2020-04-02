import json

# from weasyprint import HTML, CSS
# from weasyprint.fonts import FontConfiguration
from jinja2 import Template, Environment, DictLoader

# from num2words import num2words # TODO write converter

# Files
template_file = open("order-1c.html", "r").read()
products_file = open("products.json", "r").read()  # TODO change to API point
customer_file = open("customer.json", "r").read()  # TODO change to API point
shure_file = open("shure.json", "r").read()  # TODO change to API point

# Setup
env = Environment(loader=DictLoader({"template.html": template_file}))
products = json.loads(products_file)
customer = json.loads(customer_file)
shure = json.loads(shure_file)

# Numbers to words converter
# summa_text = num2words(123456789123, lang='ru') # TODO write converter

# Pack 'em all to template
template = env.get_template("template.html").render(
    customer={
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
    shure={
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
    # summa_text=summa_text, # TODO write converter
    products=[
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
    # TODO change to API point
    order={"number": "123", "created": "27 мая 2020"},
    # order=json.load,
)

with open("t.html", "w") as f:
    f.write(template)

# # Generate PDF from HTML file
# HTML(string=template).write_pdf("order.pdf")
