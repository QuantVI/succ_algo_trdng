create table `symbol` (
	`id` int not NULL AUTO_INCREMENT,
    `exchange_id` int NULL,
    `ticker` varchar(32) not NULL,
    `instrument` varchar(64) not null,
    `name` varchar(255) null,
    `sector` varchar(255) null,
    `currency` varchar(32) null,
    `created_date` datetime not NULL,
    `last_updated_date` datetime not NULL,
    PRIMARY Key (`id`),
    KEY `index_exchange_id` (`exchange_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 Default Charset=UTF8MB4;
