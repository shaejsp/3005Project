create table author
  (a_id				numeric(6, 0),
   a_name			varchar(50),
   primary key (a_id)
  );

create table genre
  (g_id				numeric(6, 0),
   g_name			varchar(15),
   primary key (g_id)
  );

create table publisher
  (p_id				numeric(6, 0),
   p_name			varchar(50),
   addr_id			numeric(6, 0),
   p_email			varchar(320),
   p_phone			varchar(12),
   p_bank_acct			numeric(12),
   p_bank_routing		numeric(9),
   primary key (p_id)
  );

create table customer
  (c_id				numeric(6, 0),
   username			varchar(20),
   pass				varchar(20),
   bill_id			numeric(6, 0),
   ship_id			numeric(6,0),
   primary key (c_id)
  );

create table address
  (addr_id			numeric(6, 0),
   country			varchar(20),
   province			varchar(20),
   city				varchar(20),
   postal_code			varchar(6),
   street_name			varchar(20),
   street_num			varchar(5),
   primary key (addr_id, street_num, street_name, city, postal_code)
  );


create table book
  (b_title			varchar(50),
   ISBN				varchar(17),
   p_id				numeric(6, 0),
   num_pages			numeric(4,0),
   price			numeric(4,2),
   quantity			numeric(4,0),
   pub_percent			numeric(2,2),
   year				numeric(4,0),
   summary			varchar(1000),
   primary key (ISBN),
   foreign key (p_id) references publisher
  );

create table purchase
  (o_id				numeric(6,0),
   tracking_num			varchar(20),
   c_id				numeric(6,0),
   primary key (o_id),
   foreign key (c_id) references customer
  );

create table book_ordered
  (o_id				numeric(6,0),
   ISBN				varchar(17),
   quantity			numeric(4,0),
   primary key (o_id, ISBN),
   foreign key (o_id) references purchase,
   foreign key (ISBN) references book
  );

create table book_genre
  (ISBN				varchar(17),
   g_id				numeric(6, 0),
   primary key (ISBN, g_id),
   foreign key (g_id) references genre,
   foreign key (ISBN) references book
  );

create table writes
  (ISBN				varchar(17),
   a_id				numeric(6, 0),
   primary key (a_id, ISBN),
   foreign key (a_id) references author,
   foreign key (ISBN) references book
  );
