# Use a lightweight nginx image
FROM nginx:alpine

# Copy the static website files to the nginx html directory
COPY site/ /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# The default nginx command will start the server
CMD ["nginx", "-g", "daemon off;"]
