DROP SCHEMA IF EXISTS fib;
create database fib;
use fib;

create table admins (
admin_id int primary key auto_increment,
admin_name varchar(255),
email varchar(255),
ad_password varchar(255)
);


create table donor (
donor_id int primary key auto_increment,
name varchar(255),
d_location varchar(255),
d_contact_number bigint(10),
email varchar(255),
dn_password varchar(255)
);



create table volunteer (
volunteer_id int primary key auto_increment,
v_name varchar(255),
v_location varchar(255),
v_contact_number bigint(10),
email varchar(255),
vl_password varchar(255)
);


create table reciever (
reciever_id int primary key auto_increment,
r_address varchar(255),
r_contact_number bigint(10)
);


create table food_added (
foodid int primary key auto_increment,
food_qty int,
food_cat varchar(255),
f_status varchar(255),
pickup_location varchar(255),
created_time datetime,
duration_time datetime,
d_id int,
foreign key (d_id) references donor(donor_id) 
);



create table food_del (
fd_id int primary key,
fd_qty int,
fd_cat varchar(255),
fd_status varchar(255),
fd_pickUp datetime,
fd_duration datetime,
d_id int
);



CREATE TABLE Volunteer_Request
(
requestId int PRIMARY KEY auto_increment,
status varchar(255),
foodId int ,
donorId int ,
recieverId int ,
volunteerId int ,
FOREIGN KEY (foodId) REFERENCES food_added(foodid),
FOREIGN KEY (donorId) REFERENCES donor(donor_id),
FOREIGN KEY (recieverId) REFERENCES reciever(reciever_id),
FOREIGN KEY (volunteerId) REFERENCES volunteer(volunteer_id)
);


create table users(
Username varchar(255),
email varchar(255),
passwd varchar(255),
userType varchar(255));

delimiter //
create trigger donorUser after insert on donor
for each row 
 insert users values(new.name,new.email,new.dn_password,'donor');//
delimiter ;

delimiter //
create trigger volUser after insert on volunteer
for each row 
 insert users values(new.v_name,new.email,new.vl_password,'volunteer');//
delimiter ;

delimiter //
create trigger admUser after insert on admins
for each row 
 insert users values(new.admin_name,new.email,new.ad_password,'admin');//
delimiter ;

delimiter //
create trigger bckFoodDel before delete on food_added
for each row 
 insert food_del values(old.foodid,old.food_qty,old.food_cat,old.f_status,old.pickup_location,old.created_time,old.duration_time,old.d_id);//
delimiter ;

delimiter //
create trigger updatestatus after update on Volunteer_Request
for each row 
 update food_added set f_status=new.status where foodid=old.foodId;//
delimiter ;

insert into admins values (1,'admin 1','admin@test.com','admin@1234');
