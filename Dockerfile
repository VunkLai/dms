FROM python:3.8-slim

WORKDIR /backend

COPY ./requirements.txt .

# We don't need env in container
RUN pip install -r requirements.txt

COPY . .

RUN python dms/manage.py migrate

ENTRYPOINT [ "python", "/backend/dms/manage.py" ]
CMD [  "runserver", "0.0.0.0:8000" ]
EXPOSE 8000
