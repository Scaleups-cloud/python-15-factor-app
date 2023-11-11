FROM python:3.10.13-slim-bullseye
WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./
RUN pip install --no-cache-dir pipenv && \
    pipenv install --deploy --ignore-pipfile

COPY . .

EXPOSE 5000
CMD ["pipenv", "run", "python", "./app/app.py"]
