from jinja2 import Template

from weasyprint import HTML


def render_pdf(params: dict, out_file):

    with open('./templates/order-1c.html') as f:
        template = Template(f.read())

    result = template.render(**params)

    HTML(string=result).write_pdf(out_file)
