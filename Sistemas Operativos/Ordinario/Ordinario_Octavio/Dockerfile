FROM php:8.5-apache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    unzip \
    && docker-php-ext-install mysqli \
    && rm -rf /var/lib/apt/lists/*

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Set working directory to the standard Apache path
WORKDIR /var/www/html

# Copy ONLY the contents of the src directory to the container's web root
COPY src/ .

# Enable Apache mod_rewrite (common for PHP apps)
RUN a2enmod rewrite

# Expose port 80
EXPOSE 80
