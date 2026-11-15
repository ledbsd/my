FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Устанавливаем Apache и Python, включаем CGI
RUN apt-get update && \
    apt-get install -y --no-install-recommends apache2 python3 && \
    a2enmod cgi && \
    rm -rf /var/lib/apt/lists/*

# Копируем конфиг и скрипты
COPY apache-site.conf /etc/apache2/sites-available/
COPY cgi-bin/ /usr/lib/cgi-bin/

# Отключаем стандартный сайт, включаем наш
RUN a2dissite 000-default.conf && \
    a2ensite apache-site.conf && \
    chmod 755 /usr/lib/cgi-bin/*.py && \
    chown -R www-data:www-data /usr/lib/cgi-bin/

EXPOSE 80

# Запуск Apache в foreground режиме
CMD ["apache2ctl", "-D", "FOREGROUND"]
