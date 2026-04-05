-- Sakila Sample Database Schema
-- Version 1.3

USE dvd;

--
-- Table structure for table `actor`
--

ALTER TABLE actor DROP PRIMARY KEY;

--
-- Table structure for table `address`
--

ALTER TABLE address DROP PRIMARY KEY;
ALTER TABLE address DROP FOREIGN KEY;

--
-- Table structure for table `category`
--

ALTER TABLE category DROP PRIMARY KEY;

--
-- Table structure for table `city`
--

ALTER TABLE city DROP PRIMARY KEY;
ALTER TABLE city DROP FOREIGN KEY;

--
-- Table structure for table `country`
--

ALTER TABLE country DROP PRIMARY KEY;

--
-- Table structure for table `customer`
--



--
-- Table structure for table `film`
--

--
-- Table structure for table `film_actor`
--


--
-- Table structure for table `film_category`
--



--
-- Table structure for table `language`
--

--
-- Table structure for table `store`
--

ALTER TABLE store DROP PRIMARY KEY;
ALTER TABLE store DROP FOREIGN KEY;

--
-- Table structure for table `inventory`
--



--
-- Table structure for table `staff`
--


--
-- Table structure for table `rental`
--


--
-- Table structure for table `payment`
--

