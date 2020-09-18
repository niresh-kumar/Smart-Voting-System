/*
SQLyog Community Edition- MySQL GUI v6.07
Host - 5.0.27-community-nt : Database - votingsystem
*********************************************************************
Server version : 5.0.27-community-nt
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

create database if not exists `votingsystem`;

USE `votingsystem`;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

/*Table structure for table `facerec` */

DROP TABLE IF EXISTS `facerec`;

CREATE TABLE `facerec` (
  `usernames` varchar(50) default NULL,
  `password` varchar(20) default NULL,
  `passwords` varchar(50) default NULL,
  `Userids` varchar(50) default NULL,
  `Votercardnos` varchar(50) default NULL,
  `emails` varchar(50) default NULL,
  `phonenos` varchar(11) default NULL,
  `Adresess` varchar(50) default NULL,
  `LoginAuth` varchar(5) default NULL,
  `FaceAuth` varchar(5) default NULL,
  `VoteAuth` varchar(5) default NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `facerec` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
