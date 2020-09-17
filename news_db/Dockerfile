# ベースとなるイメージを指定
FROM mysql:5.7

#COPY init/* /docker-entrypoint-initdb.d/

# MySQLのルートユーザー用のパスワードを設定
ENV MYSQL_ROOT_PASSWORD=password

CMD ["mysqld"]