import json

from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
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
    customer=customer, shure=shure,
    # summa_text=summa_text, # TODO write converter
    products=products,
    # TODO change to API point
    order={"number": "123", "created": "27 мая 2020"},
)

# Generate PDF from HTML file
HTML(string=template).write_pdf("order.pdf")
