docker build . -t fstrk-pdf-checkout
docker run --rm -v $PWD:/app -p 5000:5000 -e FLASK_DEBUG=1 -e FLASK_APP=app.py fstrk-pdf-checkout:latest flask run --host=0.0.0.0