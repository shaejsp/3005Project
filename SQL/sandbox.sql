-- This file is just queries I wanted to keep track of before implementing the functoinality in the ui

-- when a user signs up - throws error if there's a user with that username already
insert into customer (username, password)
values ('shae', 'password');

-- when a user logs in - if valid login == 1, else 0
select count(*) from customer
where username = 'shae' and password = 'password';

-- user is searching by book title
select * from book
where title like '%Harry%Potter%';

-- searches all books by author - ex JK Rowling
select * from book
where ISBN in (
	select ISBN from writes
	where auth_id in (
		select auth_id from author
		where auth_name LIKE '%Rowling%'));

-- search books by genre
select * from book
where ISBN in (
	select ISBN from book_genre
	where genre_id in (
		select g_id from genre
		where g_name LIKE '%horror%'));

-- add a book to the cart
insert into book_in_cart (ISBN, quantity, cart_id)
values (9780439023481, 1, (
	select cart_id from customer
	where username = 'shae'));

-- add a billing address to a user
insert into postal_area (postal_code, province, country)
values ('K1S5B6', 'Ontario', 'Canada');

insert into address(street_num, street_name, city, postal_code)
values ('1125', 'Colonel By Drive', 'Ottawa', 'K1S5B6');

insert into customer_billing (cust_id, addr_id)
values (
	(select cust_id from customer
	where username = 'shae'),
	(select addr_id from address
	where postal_code = 'K1S5B6' and city = 'Ottawa' and street_name = 'Colonel By Drive' and street_num = '1125'));

-- add a book to the cart where ISBN = 97804..., and username = xx_420_xx
insert into book_in_cart (ISBN, quantity, cart_id)
values (9780439023481, 1, (select cart_id from customer where username = 'xx_420_xx'));

-- add stuff to a purchase and clear the cart
insert into purchase (cust_id, addr_id)
values (
	(select cust_id from customer
	where username = 'shae'),
	(select addr_id from customer_shipping
	where cust_id = (select cust_id from customer
					where username = 'shae')), 00000000001111111111);

insert into book_purchased (ISBN, quantity, order_id)
values (
	(select ISBN from book_in_cart where book_in_cart.cart_id =
	 	(select cust_id from customer where username = 'shae')),
	(select quantity from book_in_cart where book_in_cart.cart_id =
	 	(select cust_id from customer where username = 'shae')),
	 (select order_id from purchase where cust_id = (select cust_id from customer where username = 'shae')));

delete from book_in_cart
where cart_id in (select cart_id from customer where username = 'shae');

-- delete a book
delete from published
where ISBN = '9780143039952';

delete from book_genre
where ISBN = '9780143039952';

delete from writes
where ISBN = '9780143039952';

delete from book
where ISBN = '9780143039952';
