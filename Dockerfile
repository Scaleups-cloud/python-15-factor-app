FROM python:3.10
WORKDIR /usr/src/app
COPY . .

RUN pip install pipenv
RUN pipenv install --system --deploy

EXPOSE 5000
ENV FLASK_CONFIG=development

CMD ["python", "app.py"]