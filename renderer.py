import locale
import dateutil
import logging
import boto3
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from uuid import uuid4
from weasyprint import HTML
from pytz import timezone
from dateutil import tz
from botocore.exceptions import ClientError
from num2words import num2words


locale.setlocale(locale.LC_TIME, "ru_RU.utf8")

env = Environment(
    loader=FileSystemLoader("./templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


def num2words_converter(value):
    return num2words(value, lang="ru", to="currency", currency='RUB')


def russian_date(value):
    """ Принимает строку с датой в ISO формате и превращает в русскую дату """
    return dateutil.parser.parse(value).strftime("%d %B %Y")


def short_date(value):
    """ Принимает строку с датой в ISO формате и превращает в короткую дату """
    return dateutil.parser.parse(value).strftime("%d.%m.%Y")


def russian_price(value: float):
    """
    Преобразует число в строку с разделителями между тысячными
    и округляет до 2 знаков после запятой

    3242321.123    -> 3 242 321.123
    """
    return '{:,.2f}'.format(value).replace(',', ' ')


env.filters["num2words"] = num2words_converter
env.filters["russian_date"] = russian_date
env.filters["russian_price"] = russian_price


def render_pdf(params: dict, out_file):
    template = env.get_template("order-1c.html")
    result = template.render(**params)

    HTML(string=result).write_pdf(out_file)


def _get_current_time_str():
    utcnow = datetime.utcnow()
    moscow_tz = tz.gettz("Europe/Moscow")
    local = utcnow.replace(tzinfo=timezone("UTC")).astimezone(moscow_tz)
    local_str = local.isoformat().split(".")[0]

    return local_str


def upload_file(file_name: str) -> str:
    """ Загрузить файл на амазон, вернуть линк с уникальным именем """
    current_time_str = _get_current_time_str()
    path_name = f"1c-orders/{uuid4()}-{current_time_str}.pdf"

    # Upload the file
    bucket_name = os.environ["AWS_S3_BUCKET_NAME"]
    s3_client = boto3.client("s3")

    try:
        s3_client.upload_file(file_name, bucket_name, path_name)
    except ClientError as e:
        logging.error(e)
        return None

    return f"https://{bucket_name}.s3.amazonaws.com/{path_name}"
