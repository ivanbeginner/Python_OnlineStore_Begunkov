FROM python:3.12
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ENV PYTHONUNBUFFERED=1
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
RUN sh -c python manage.py makemigrations
RUN sh -c python manage.py migrate
RUN sh -c python collectstatic -no-input

EXPOSE 8000


CMD ["python", "[manage.py](http://manage.py/)", "runserver", "0.0.0.0:8000"]
