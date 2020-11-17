use securities_master;

create table `data_vendor` (
	`id` int NOT null Auto_Increment,
    `name` varchar(64) Not null,
    `webite_url` varchar(255) null,
    `support_email` varchar(255) null,
    `created_date` datetime NOT null,
    `last_updated_date` datetime NOT null,
	Primary Key (`id`)
) Engine=InnoDB Auto_Increment=1 Default Charset=UTF8MB4;