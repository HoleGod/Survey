FROM python:3.13
WORKDIR /app1

COPY surveyy /app1
COPY requirements.txt /app1

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]