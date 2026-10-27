# Open Break Studio OS — Production Multi-Stage Container Image
FROM nginx:1.27-alpine-slim

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy hardened nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy compiled OpenBreak static distribution
COPY . /usr/share/nginx/html/

# Clean non-runtime repository files from container web root
RUN rm -rf /usr/share/nginx/html/.git \
           /usr/share/nginx/html/tests \
           /usr/share/nginx/html/scripts \
           /usr/share/nginx/html/Dockerfile \
           /usr/share/nginx/html/nginx.conf

# Set unprivileged security context
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

EXPOSE 8080

USER nginx

STOPSIGNAL SIGQUIT

CMD ["nginx", "-g", "daemon off;"]
