#!/bin/bash

db_server='127.0.0.1'
db_port=3306
database='compute'


while [ -z $root_pwd ]
do
    read -p '请输入mysql数据库root密码:[password]'
    root_pwd=$REPLY
    if [ -z $root_pwd ]; then
        continue
    fi

    mysql -h $db_server -P $db_port -uroot -p"$root_pwd" -e "quit"
    if [ $? -ne 0 ]; then
        echo 'mysql数据库无法登陆，请检查数据库状态和密码输入是否正确。'
        unset -v root_pwd
    fi
done


m_user_check=$(mysql -h $db_server -P $db_port -uroot -p"$root_pwd" -e "
               select count(*) from mysql.user where user='cloud'" | tail -n+2)

if [ $m_user_check -eq 0 ]; then
    mysql -h $db_server -P $db_port -uroot -p"$root_pwd" -e "
    create database $database;
    create user 'cloud'@'%' identified by 'cloud';
    grant all privileges ON $database.* to  'cloud'@'%'; "
else
    mysql -h $db_server -P $db_port -uroot -p"$root_pwd" -e "
    CREATE DATABASE IF NOT EXISTS $database;
    grant all privileges ON $database.* to  'cloud'@'%'; "
fi
