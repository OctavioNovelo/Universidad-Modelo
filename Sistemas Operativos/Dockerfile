FROM php:8.2-apache

# Cambiar el puerto de Apache de 80 a 85
RUN sed -i 's/Listen 80/Listen 85/' /etc/apache2/ports.conf
RUN sed -i 's/:80/:85/' /etc/apache2/sites-available/000-default.conf

COPY phpapp/index.php /var/www/html/

EXPOSE 85
