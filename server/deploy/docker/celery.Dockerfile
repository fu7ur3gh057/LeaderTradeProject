# PYTHON
FROM python:3.10.9-bullseye
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# create and set workdir
WORKDIR /app/server
# copy local project
COPY .. .

#update pip
# install requirements
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# make our celery-entrypoint.sh executable
RUN chmod +x ./deploy/config/celery-entrypoint.sh
EXPOSE 8200
# execute our celery-entrypoint.sh file
ENTRYPOINT ["./deploy/config/celery-entrypoint.sh"]