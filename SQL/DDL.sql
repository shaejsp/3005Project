
create table book
  (title			   varchar(50),
   ISBN				   varchar(13),
   num_pages		 numeric(4,0),
   price			   numeric(4,2),
   quantity			 numeric(4,0),
   pub_percent	 numeric(2,2),
   year				   numeric(4,0),
   summary			 varchar(1000),
   primary key (ISBN)
  );

create table author
  (auth_id				numeric(6, 0),
   auth_name			varchar(50),
   primary key (auth_id)
  );

create table writes
  (ISBN           varchar(13),
   auth_id				numeric(6, 0),
   primary key (auth_id, ISBN),
   foreign key (auth_id) references author,
   foreign key (ISBN) references book
  );

create table genre
  (g_id				numeric(6, 0),
   g_name			varchar(15),
   primary key (g_id)
  );

create table book_genre
  (genre_id     numeric(6,0),
   ISBN         varchar(13),
   primary key (genre_id, ISBN),
   foreign key (genre_id) references genre,
   foreign key (ISBN) references book
 );

create table postal_area
 (postal_code  varchar(6),
  province     varchar(20),
  country      varchar(20),
  primary key (postal_code)
);

create table address
(addr_id			numeric(6, 0),
 city				varchar(20),
 postal_code			varchar(6),
 street_name			varchar(20),
 street_num			varchar(5),
 primary key (addr_id),
 foreign key (postal_code) references postal_area
);

create table customer
 (cust_id				numeric(6, 0),
  username			varchar(20),
  password		  varchar(20),
  primary key (cust_id)
 );

create table customer_billing
  (cust_id    numeric(6,0),
   addr_id    numeric(6,0),
   primary key (cust_id),
   foreign key (cust_id) references customer,
   foreign key (addr_id) references address
 );

 create table customer_shipping
   (cust_id    numeric(6,0),
    addr_id    numeric(6,0),
    primary key (cust_id),
    foreign key (cust_id) references customer,
    foreign key (addr_id) references address
  );

create table purchase
 (order_id				numeric(6,0),
  tracking_num		varchar(20),
  cust_id	  			numeric(6,0),
  addr_id         numeric(6,0),
  primary key (order_id),
  foreign key (cust_id) references customer,
  foreign key (addr_id) references address
 );

create table book_in_cart
  (ISBN     varchar(13),
   cart_id  numeric(6,0),
   quantity numeric(3,0),
   primary key (ISBN, cart_id),
   foreign key (ISBN) references book,
   foreign key (cart_id) references customer
 );

create table publisher
  (pub_id   numeric(6,0),
   pub_name varchar(50),
   email    varchar(320),
   phone    varchar(12),
   addr_id  numeric(6,0),
   primary key (pub_id),
   foreign key (addr_id) references address
 );

create table book_purchased
  (order_id			numeric(6,0),
   ISBN				 varchar(13),
   quantity			numeric(4,0),
   primary key (order_id, ISBN),
   foreign key (order_id) references purchase,
   foreign key (ISBN) references book
  );

create table published
  (pub_id   numeric(6,0),
   ISBN     varchar(13),
   primary key (pub_id, ISBN),
   foreign key (pub_id) references publisher,
   foreign key (ISBN) references book
 );
