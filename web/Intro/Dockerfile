# Use a base image with php and nginx installed
FROM nginx:latest

# Copy your web files to the container
COPY ./web-files /usr/share/nginx/html

COPY flag.txt /usr/share/flag_jeannedhack.txt

# # Set the user:group to /flag_jeannedhack.txt to nginx
# RUN chown nginx:nginx /flag_jeannedhack.txt

# # Set the permissions of /flag_jeannedhack.txt to all users
# RUN chmod 444 /flag_jeannedhack.txt

# Expose the default HTTP port
EXPOSE 80

# Start the web server
CMD ["nginx", "-g", "daemon off;"]