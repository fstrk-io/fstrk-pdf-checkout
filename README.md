# PDF generator for Fstrk.io

Python libs:

- Poetry
- weasyprint
- jinja2
- num2words

## Запуск веб-сервера в Docker

```bash
docker build . -t fstrk-pdf-checkout
docker run --rm -v $PWD:/app -p 5000:5000 -e FLASK_DEBUG=1 -e FLASK_APP=app.py fstrk-pdf-checkout:latest flask run --host=0.0.0.0
```

И потом открыть [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Деплой на Heroku

```bash
# Установка Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Вход в учетку
heroku login

# Добавить деплой-ветку
git remote add heroku https://git.heroku.com/fasttrack-pdf-checkout.git
```

Далее, просто делаем `git push` при любом изменении вот так:

```bash
git push heroku master
```

Heroku сам поймет, что пришли правки и нужно делать их деплой.