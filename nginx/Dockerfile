FROM nginx:1.27.2-alpine

COPY ./my_nginx.conf /etc/nginx/my_nginx.conf

COPY ./blue.conf /etc/nginx/conf.d/blue.conf
COPY ./green.conf /etc/nginx/conf.d/green.conf

RUN rm /etc/nginx/conf.d/default.conf

RUN ln -sf /etc/nginx/conf.d/blue.conf /etc/nginx/conf.d/active_env.conf

EXPOSE 80

CMD ["nginx", "-g", "deamon off;"]