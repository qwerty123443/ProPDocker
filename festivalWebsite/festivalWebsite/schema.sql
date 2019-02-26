DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS shop;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS camping;
DROP TABLE IF EXISTS reservation;
DROP TABLE IF EXISTS order_details;

CREATE TABLE IF NOT EXISTS camping (
  spotID integer NOT NULL
,  userID integer NOT NULL
,  PRIMARY KEY (spotID, userID)
,  FOREIGN KEY (userID) REFERENCES user (id)
,  FOREIGN KEY (spotID) REFERENCES reservation (spotID)
);
CREATE TABLE IF NOT EXISTS order_details (
  orderID integer NOT NULL
,  productID integer NOT NULL
,  amount integer NULL DEFAULT NULL
,  PRIMARY KEY (orderID, productID)
,  FOREIGN KEY (orderID) REFERENCES orders (orderID)
,  FOREIGN KEY (productID) REFERENCES product (productID)
);

CREATE TABLE IF NOT EXISTS orders (
  orderID integer NOT NULL
,  userID integer NOT NULL
,  orderDate TIMESTAMP NULL DEFAULT current_timestamp
,  PRIMARY KEY (orderID, userID)
,  FOREIGN KEY (userID) REFERENCES user (userID)
);

CREATE TABLE IF NOT EXISTS post (
  id integer PRIMARY KEY AUTOINCREMENT
,  author_id integer NOT NULL
,  created TIMESTAMP NOT NULL DEFAULT current_timestamp
,  title TEXT NULL DEFAULT NULL
,  body TEXT NULL DEFAULT NULL
,  FOREIGN KEY (author_id) REFERENCES user (userID)
);

CREATE TABLE IF NOT EXISTS product (
  productID integer NOT NULL PRIMARY KEY AUTOINCREMENT
,  shopID integer NOT NULL
,  name TEXT NULL DEFAULT NULL
,  description TEXT NULL DEFAULT NULL
,  price integer NULL DEFAULT NULL
,  barcode TEXT NULL DEFAULT NULL
,  isRentable TEXT NULL
,  FOREIGN KEY (shopID) REFERENCES shop (shopID)
);

CREATE TABLE IF NOT EXISTS reservation (
  reservationID integer NOT NULL
,  spotID integer NOT NULL
,  reservationTime TIMESTAMP NULL DEFAULT current_timestamp
,  PRIMARY KEY (reservationID, spotID)
,  FOREIGN KEY (spotID) REFERENCES camping (spotID)
);

CREATE TABLE IF NOT EXISTS shop (
  shopID integer NULL DEFAULT NULL
,  shopName TEXT NULL DEFAULT NULL
,  ownerID integer NULL DEFAULT NULL
,  PRIMARY KEY (shopID)
,  FOREIGN KEY (ownerID) REFERENCES user (id)
);

CREATE TABLE IF NOT EXISTS user (
  id integer NULL PRIMARY KEY AUTOINCREMENT
,  username TEXT NOT NULL
,  firstname TEXT NOT NULL
,  lastname TEXT NOT NULL
,  birthdate DATE NOT NULL
,  street TEXT NOT NULL
,  housenumber integer NOT NULL
,  housenumberaddition TEXT NULL DEFAULT ''
,  city TEXT NOT NULL
,  province TEXT NOT NULL
,  email TEXT NOT NULL
,  password TEXT NOT NULL
,  balance integer NOT NULL DEFAULT 0
,  userType integer NOT NULL DEFAULT 1
,  festivalCheckintime TIMESTAMP NULL DEFAULT NULL
,  campingCheckintime TIMESTAMP NULL DEFAULT NULL
,  isLateBuyer TEXT NOT NULL DEFAULT 'False'
,  isValid TEXT NOT NULL DEFAULT 'True'
,  IBAN TEXT NULL
);
