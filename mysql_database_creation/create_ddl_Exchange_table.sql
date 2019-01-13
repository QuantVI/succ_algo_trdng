use securities_master;

create table `exchange` (
	`id` int NOT NULL AUTO_INCREMENT,
    `abbrev` varchar(32) NOT NULL,
    `name` varchar(255) NOT NULL,
    `city` varchar(255) NULL,
    `country` varchar(255) NULL,
    `currency` varchar(64) NULL,
    `timezone_offset` time NULL,
    `created_date` datetime NOT NULL,
    `last_updated_date` datetime NOT NULL,
	PRIMARY KEY(`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=UTF8MB4; 


-- 0 row(s) affected, 1 warning(s): 3719 'utf8' is currently an alias for the character set UTF8MB3, which will be replaced by UTF8MB4 in a future release. Please consider using UTF8MB4 in order to be unambiguous.

