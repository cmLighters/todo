drop database if exists todo;
create database todo;
grant select, insert, delete, update on todo.* to 'cm'@'localhost';
set session time_zone="+08:00";

use todo;

drop table if exists entries;
create table entries(
	entry_id	int	 not null	auto_increment,
	content 	varchar(200) 	not null,
	sub_time 	datetime 	not null,
	primary key(entry_id)
)


	

