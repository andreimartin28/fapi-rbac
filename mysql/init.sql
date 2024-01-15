create database if not exists rbac_fastapi;

use rbac_fastapi;

create table rbac_fastapi.users(
user_id int unsigned not null auto_increment primary key,
user_username varchar(50) not null,
user_password varchar(150) not null,
user_date_created datetime not null default now(),
user_status tinyint unsigned not null default 1
);

