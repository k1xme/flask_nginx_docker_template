FROM ubuntu:14.04

RUN apt-get clean && apt-get update
RUN apt-get install -y python2.7 python-pip python-dev
RUN apt-get install -y libssl-dev libffi-dev git
RUN apt-get install -y nginx supervisor

RUN pip install flask
RUN pip install paypalrestsdk
RUN pip install gunicorn

RUN git clone https://github.com/k1xme/flask_nginx_docker_template.git /new_site

ENV PAYMENT_SERVER_PORT 4567
ENV PAYPAL_CLIENT_ID AQkquBDf1zctJOWGKWUEtKXm6qVhueUEMvXO_-MCI4DQQ4-LWvkDLIN2fGsd
ENV PAYPAL_CLIENT_SECRET EL1tVxAjhT7cJimnz5-Nsx9k2reTKSVfErNQF-CmrwJgxRtylkGTKlU4RvrX
ENV PAYPAL_MODE sandbox
ENV PAYMENT_SERVER_SECRET_KEY doushidashabi

ENV GUNICORN_WORKER 4
ENV GUNICORN_ADDRESS 0.0.0.0:$PAYMENT_SERVER_PORT

EXPOSE 80 443

WORKDIR /new_site

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY flask_paypal_com.conf /etc/nginx/sites-enabled/flask_paypal_com.conf

#ENTRYPOINT gunicorn -w $GUNICORN_WORKER -b $GUNICORN_ADDRESS payment_server:app

CMD ["/usr/bin/supervisord"]