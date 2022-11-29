create database fib;
use fib;

create table Adminis (
admin_id int primary key auto_increment,
admin_name varchar(255),
email varchar(255),
ad_password varchar(255)
);


create table donor (
donor_id int primary key auto_increment,
name varchar(255),
d_location varchar(255),
d_contact_number int(10),
email varchar(255),
dn_password varchar(255)
);



create table volunteer (
volunteer_id int primary key auto_increment,
v_name varchar(255),
v_location varchar(255),
v_contact_number int(10),
email varchar(255),
vl_password varchar(255)
);


create table reciever (
reciever_id int primary key auto_increment,
r_address varchar(255),
r_contact_number int(10)
);


create table food_added (
foodid int primary key auto_increment,
food_qty int,
food_cat varchar(255),
f_status varchar(255),
pickup_location varchar(255),
created_time datetime,
duration_time datetime,
d_id int 
);



create table food_del (
fd_id int primary key,
fd_qty int,
fd_cat varchar(255),
fd_status varchar(255),
fd_pickUp datetime,
fd_duration datetime,
d_id int,
foreign key (d_id) references donor(donor_id)
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


