from datetime import datetime

from jinja2 import Template
from uuid import uuid4
from weasyprint import HTML
from datetime import datetime
from pytz import timezone
from dateutil import tz
import logging
import boto3
from botocore.exceptions import ClientError

import os



def render_pdf(params: dict, out_file):

    with open('./templates/order-1c.html') as f:
        template = Template(f.read())

    result = template.render(**params)

    HTML(string=result).write_pdf(out_file)


def _get_current_time_str():

    utcnow = datetime.utcnow()
    local = utcnow.replace(tzinfo=timezone('UTC')).astimezone(tz.gettz('Europe/Moscow'))
    local_str = local.isoformat().split('.')[0]
    return local_str


def upload_file(file_name: str) -> str:
    """ Загрузить файл на амазон, вернуть линк с уникальным именем """

    current_time_str = _get_current_time_str()
    path_name = f'1c-orders/{uuid4()}-{current_time_str}.pdf'
    # Upload the file
    bucket_name = os.environ['AWS_S3_BUCKET_NAME']
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket_name, path_name)
    except ClientError as e:
        logging.error(e)
        return None

    url = f'https://{bucket_name}.s3.amazonaws.com/{path_name}'
    return url
