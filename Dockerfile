FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python collectstatic -no-input
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=OnlineStore.settings.production
CMD ["python", "[manage.py](http://manage.py/)", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["top", "-b"]