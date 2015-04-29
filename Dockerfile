FROM ubuntu:14.04

RUN apt-get clean && apt-get update
RUN apt-get install -y python2.7 python-pip python-dev
RUN apt-get install -y libssl-dev libffi-dev
#RUN apt-get install -y nginx

RUN pip install flask
RUN pip install paypalrestsdk
RUN pip install gunicorn

ENV PAYMENT_SERVER_PORT 4567
ENV PAYPAL_CLIENT_ID AQkquBDf1zctJOWGKWUEtKXm6qVhueUEMvXO_-MCI4DQQ4-LWvkDLIN2fGsd
ENV PAYPAL_CLIENT_SECRET EL1tVxAjhT7cJimnz5-Nsx9k2reTKSVfErNQF-CmrwJgxRtylkGTKlU4RvrX
ENV PAYPAL_MODE sandbox
ENV PAYMENT_SERVER_SECRET_KEY doushidashabi

ENV GUNICORN_WORKER 4
ENV GUNICORN_ADDRESS 0.0.0.0:$PAYMENT_SERVER_PORT


WORKDIR /new_site

#ADD . /new_site

ENTRYPOINT gunicorn -w GUNICORN_WORKER -b GUNICORN_BIND payment_server:app