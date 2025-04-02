-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 24, 2025 at 06:35 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 7.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `voltway_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_charging_station_list`
--

CREATE TABLE `admin_charging_station_list` (
  `station_id` int(11) NOT NULL,
  `Station_name` varchar(50) NOT NULL,
  `Address` varchar(100) NOT NULL,
  `City` char(20) NOT NULL,
  `Charger_type` char(20) NOT NULL,
  `Available_ports` varchar(50) NOT NULL,
  `filepath` varchar(255) NOT NULL,
  `Status` enum('active','inactive') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin_charging_station_list`
--

INSERT INTO `admin_charging_station_list` (`station_id`, `Station_name`, `Address`, `City`, `Charger_type`, `Available_ports`, `filepath`, `Status`) VALUES
(2, 'SDASD', 'DSDS', 'thiruvananthapuram', 'AC Level 1 Charging', '4', './static/image/soil.jpg', 'active'),
(3, 'abcd', 'pune', 'thiruvananthapuram', 'AC Level 1 Charging', '3', 'static\\image\\thirustation.jpg', 'active'),
(4, 'bharat petrolium', 'Thiruvananthapuram', 'thiruvananthapuram', 'AC Level 1 Charging', '6', 'static\\image\\thirustation.jpg', 'active'),
(5, 'bharat petrolium', 'DSDS', 'thiruvananthapuram', 'AC Level 2 Charging', '1', 'static\\image\\thirustation.jpg', 'active');

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `booking_id` int(11) NOT NULL,
  `Station_name` varchar(50) NOT NULL,
  `City` varchar(50) NOT NULL,
  `Available_ports` varchar(11) NOT NULL,
  `Booking_date` date NOT NULL,
  `Time_from` time NOT NULL,
  `Time_to` time NOT NULL,
  `Created_id` timestamp NULL DEFAULT current_timestamp(),
  `login_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`booking_id`, `Station_name`, `City`, `Available_ports`, `Booking_date`, `Time_from`, `Time_to`, `Created_id`, `login_id`) VALUES
(5, 'SDASD', 'thiruvananthapuram', '4', '2024-11-23', '16:28:00', '18:28:00', '2024-11-22 12:59:07', 2),
(88, 'SDASD', 'thiruvananthapuram', '4', '2025-03-20', '11:30:00', '15:30:00', '2025-03-21 06:07:23', 3),
(91, 'SDASD', 'thiruvananthapuram', '4', '2025-03-20', '12:15:00', '15:15:00', '2025-03-21 06:45:37', 3),
(93, 'abcd', 'thiruvananthapuram', '3', '2025-03-21', '12:57:00', '15:57:00', '2025-03-21 07:27:18', 3);

-- --------------------------------------------------------

--
-- Table structure for table `contact_us`
--

CREATE TABLE `contact_us` (
  `Sl_no` int(11) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Feedback_date` date NOT NULL,
  `Feedback` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `usertype` enum('admin','user') NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`login_id`, `username`, `email`, `password`, `usertype`) VALUES
(1, 'admin', 'admin@gmail.com', 'admin', 'admin'),
(2, 'user', 'user@gmail.com', 'user', 'user'),
(3, 'kunal', 'kunalproject025@gmail.com', 'kunal', 'user');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_charging_station_list`
--
ALTER TABLE `admin_charging_station_list`
  ADD PRIMARY KEY (`station_id`);

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `login_id` (`login_id`);

--
-- Indexes for table `contact_us`
--
ALTER TABLE `contact_us`
  ADD PRIMARY KEY (`Sl_no`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`login_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin_charging_station_list`
--
ALTER TABLE `admin_charging_station_list`
  MODIFY `station_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `booking`
--
ALTER TABLE `booking`
  MODIFY `booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=94;

--
-- AUTO_INCREMENT for table `contact_us`
--
ALTER TABLE `contact_us`
  MODIFY `Sl_no` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `login`
--
ALTER TABLE `login`
  MODIFY `login_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `booking`
--
ALTER TABLE `booking`
  ADD CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`login_id`) REFERENCES `login` (`login_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
