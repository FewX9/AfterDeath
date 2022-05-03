-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 02, 2022 at 11:16 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `afterdeath`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `id` int(11) NOT NULL,
  `username` varchar(254) NOT NULL,
  `password` varchar(254) NOT NULL,
  `f_name` varchar(254) NOT NULL,
  `l_name` varchar(254) NOT NULL,
  `phone` varchar(254) NOT NULL,
  `address` varchar(254) NOT NULL,
  `mail` varchar(254) NOT NULL,
  `img` varchar(254) NOT NULL,
  `permission` varchar(254) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`id`, `username`, `password`, `f_name`, `l_name`, `phone`, `address`, `mail`, `img`, `permission`) VALUES
(1, 'admin', '1234', 'Thanatip', 'Thaowangnai', '0950969999', 'xxx/xxx', 'thanatip.thao@bumail.net', 'avatar.png', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `session` varchar(254) NOT NULL,
  `item` varchar(254) NOT NULL,
  `price` int(11) NOT NULL,
  `unit` int(11) NOT NULL,
  `add_date` varchar(254) NOT NULL,
  `i_id` int(11) NOT NULL,
  `img` varchar(254) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`id`, `session`, `item`, `price`, `unit`, `add_date`, `i_id`, `img`) VALUES
(7, '6qefmu8iSLkq9zVh6JVi', 'โลงศพ1', 5000, 1, '2022-05-03 02:16:17', 12, '2022-05-03_02-01-02_2022-05-01_15-30-41_x.jpg'),
(8, '7Q3wAkEoN7Dbo8SxNvbP', 'SET F606', 25000, 1, '2022-05-03 02:20:05', 5, 'set2.jpg'),
(9, 'Fh1511a2VqkFJLmPPHnw', 'SET F606', 25000, 1, '2022-05-03 02:22:44', 5, 'set2.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `c_order`
--

CREATE TABLE `c_order` (
  `id` int(11) NOT NULL,
  `f_name` varchar(254) NOT NULL,
  `l_name` varchar(254) NOT NULL,
  `phone` varchar(254) NOT NULL,
  `total_price` varchar(254) NOT NULL,
  `time` varchar(254) NOT NULL,
  `status` varchar(254) NOT NULL,
  `s_name` varchar(254) NOT NULL,
  `s_phone` varchar(254) NOT NULL,
  `slip` varchar(254) NOT NULL,
  `session` varchar(254) NOT NULL,
  `address` varchar(254) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `item`
--

CREATE TABLE `item` (
  `id` int(11) NOT NULL,
  `name` varchar(254) NOT NULL,
  `price` int(11) NOT NULL,
  `count` int(11) NOT NULL,
  `img` varchar(254) NOT NULL,
  `collection` varchar(254) NOT NULL,
  `recommend` varchar(254) NOT NULL,
  `stock` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `item`
--

INSERT INTO `item` (`id`, `name`, `price`, `count`, `img`, `collection`, `recommend`, `stock`) VALUES
(4, 'SET F501', 10000, 0, 'set1.jpg', 'set', 'true', 9999),
(5, 'SET F606', 25000, 3, 'set2.jpg', 'set', 'true', 9996),
(6, 'รถขนส่ง', 5000, 0, 'van.jpg', 'service', 'false', 9999),
(7, 'ฉีดยารักษาสภาพศพ', 5000, 1, 'inject.jpg', 'service', 'false', 9999),
(8, 'หีบตู้เย็นให้เช่า', 5000, 0, 'c_box.jpg', 'service', 'false', 9999),
(9, 'ชุดแพ็ค(ถุงแพ็คศพ,ใบชา,จันหอม)', 5000, 0, 'c_bag.jpg', 'service', 'false', 9999),
(10, 'อาบน้ำ แต่งหน้า แต่งตัว ผู้เสียชีวิต', 5000, 0, 'shower.jpg', 'service', 'false', 9999),
(11, 'ถ่ายรูปในงานพิธี', 5000, 0, 't_photo.jpg', 'service', 'false', 9999),
(12, 'โลงศพ1', 5000, 2, '2022-05-03_02-01-02_2022-05-01_15-30-41_x.jpg', 'coffin', 'true', 9997),
(13, 'กรรไกรตัดเล็บแบบยาว', 2000, 0, '2022-05-03_02-01-32_2022-04-26_07-54-33_กรรไกรตัดเล็บแบบยาว.jpg', 'gift', 'false', 9999),
(14, 'กะเพาะปลา', 2000, 0, '2022-05-03_02-02-08_2022-05-01_15-45-49_2022-04-26_07-55-18_กะเพาะปลา.jpg', 'food', 'false', 9999);

-- --------------------------------------------------------

--
-- Table structure for table `report`
--

CREATE TABLE `report` (
  `id` int(11) NOT NULL,
  `date` varchar(254) NOT NULL,
  `income` varchar(254) NOT NULL,
  `expenses` varchar(254) NOT NULL,
  `total` varchar(254) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `c_order`
--
ALTER TABLE `c_order`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `item`
--
ALTER TABLE `item`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `report`
--
ALTER TABLE `report`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account`
--
ALTER TABLE `account`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `c_order`
--
ALTER TABLE `c_order`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `item`
--
ALTER TABLE `item`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `report`
--
ALTER TABLE `report`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
