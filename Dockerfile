FROM python:latest
ARG settings
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install npm ruby-dev rubygems supervisor -y
RUN npm install -g bower
RUN gem update --system
RUN gem install compass
RUN ln -s `which nodejs` /usr/bin/node

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
RUN python manage.py bower_install -- --allow-root
RUN python manage.py collectstatic --settings=$settings --noinput
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd /var/log/supervisor
COPY docker-build/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ONBUILD COPY requirements.txt /usr/src/app/
ONBUILD RUN pip install --no-cache-dir -r requirements.txt
ONBUILD COPY . /usr/src/app
ONBUILD RUN python manage.py bower_install -- --allow-root
ONBUILD RUN python manage.py collectstatic --settings=$settings --noinput