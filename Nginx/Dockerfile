# Use the official Nginx image from the Docker Hub
FROM nginx:latest

# Install OpenSSL
RUN apt-get update && apt-get install -y openssl

# Generate self-signed certificate and key
RUN mkdir -p /etc/ssl/private /etc/ssl/certs && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/key.pem \
    -out /etc/ssl/certs/cert.pem \
    -subj "/CN=localhost"

# Copy the Nginx configuration file
COPY ./Conf/default.conf /etc/nginx/nginx.conf


# Expose ports 80 and 443
EXPOSE 80 443