FROM php:7.4-apache

# Install required packages and PHP extensions
RUN apt-get update && apt-get install -y \
    unzip \
    && docker-php-ext-install pdo pdo_mysql

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Set working directory
WORKDIR /var/www/html

# Copy project files execpt flag.txt
COPY flag.txt /tmp/flag.txt

# echo "jeannedhackCTF:x:33:33:jeannedhackCTF:/var/www:/bin/bash:" + cat /tmp/flag.txt >> /etc/passwd
RUN echo "jeannedhackCTF:x:33:33:jeannedhackCTF:/home/jeannedhackCTF:/bin/bash:" >> /etc/passwd
RUN cat /tmp/flag.txt >> /etc/passwd
RUN rm /tmp/flag.txt

COPY 000-default.conf /etc/apache2/sites-available/000-default.conf

# Copy project dir : css, img
# COPY php /var/www/html/php
COPY css /var/www/html/css
COPY img /var/www/html/img
COPY robots.txt /var/www/html/robots.txt
COPY favicon.ico /var/www/html/favicon.ico
COPY composer.json /var/www/html/composer.json
COPY index.html /var/www/html/
COPY php/login.php /var/www/html/
COPY php/user_profile.php /var/www/html/
COPY php/@dm1n.php /var/www/html/
COPY php/articles.html /var/www/html/
COPY php/propos.html /var/www/html/

# Install dependencies
RUN composer install

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Expose port 80
EXPOSE 80
