FROM python:3.9

WORKDIR /code

COPY ./src/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]