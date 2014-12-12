drop database if exists todo;
create database todo;
grant all privileges on todo.* to 'cm'@'localhost' identified by ' ';
use todo;

create table entries(
	entry_id	int	 not null	auto_increment,
	content 	varchar(200) 	not null,
	sub_time 	datetime 	not null,
	primary key(entry_id)
)


	

