create table `daily_price` (
	`id` int NOT null Auto_Increment,
    `data_vendor_id` int NOT null,
    `symbol_id` int NOT null,
    `price_date` datetime not null,
    `created_date` datetime not null,
    `last_updated_date` datetime not null,
    `open_price` decimal(19,4) null,
    `high_price` decimal(19,4) null,
    `low_price` decimal(19,4) null,
    `close_price` decimal(19,4) null,
    `adj_close_price` decimal(19,4) null,
    `volume` bigint null,
    Primary Key (`id`),
    Key `index_data_vendor_id` (`data_vendor_id`),
    Key `index_symbol_id` (`symbol_id`)
) Engine=InnoDB Auto_Increment=1 Default Charset=UTF8MB4;

-- using UTF8MB4 insead of utf8 to be more specific, as noted by MySQL warning output