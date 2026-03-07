-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: db_srorn
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '81e61c78-d514-11f0-8797-b6a75bcebd3c:1-2948';

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_categories_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Develop',NULL),(2,'Support',NULL);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status_id` int DEFAULT '1',
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `status_id` (`status_id`),
  KEY `ix_departments_id` (`id`),
  CONSTRAINT `departments_ibfk_1` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,'IT',1,'Testing1','2025-12-02 12:53:56'),(2,'Support Team',1,'Testing2','2025-12-02 12:53:56'),(3,'Report',1,'Report','2025-12-12 18:13:47'),(4,'Development',2,'Development','2025-12-12 18:15:51'),(5,'Manager',2,'Manager','2025-12-12 18:18:19'),(6,'Developer',1,'Developer','2025-12-13 18:29:04'),(7,'Testing',1,'','2025-12-31 11:30:24');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ticket_id` int DEFAULT NULL,
  `image_path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `file_path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ticket_id` (`ticket_id`),
  KEY `ix_items_id` (`id`),
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `tickets` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (1,7,'uploads/images/problem1.jpg','uploads/files/log.txt','Boot log file'),(2,7,'uploads/images/problem2.jpg','uploads/files/log.txt','Blue screen photo'),(3,13,'uploads/images/problem1.jpg','uploads/files/log.txt','Boot log file'),(4,13,'uploads/images/problem2.jpg','uploads/files/log.txt','Blue screen photo'),(13,35,'IMG_20251205_173009.jpg',NULL,'Image attachment'),(14,35,NULL,'script1 (2).txt','File attachment'),(15,36,'IMG_20251205_173009.jpg','Schedule_Templat Loan 23-07-2025.xlsx','File attachment'),(16,38,'Screenshot 2025-12-09 144248.png','AIR.xlsx','File attachment'),(17,72,'uploads/tickets/images/d36e09cf-5f96-414d-a77e-bfe60360ba6c.png',NULL,'Image attachment'),(18,73,'uploads/tickets/images/f650bc51-ab64-44cd-9a6b-4f7723738830.png','uploads/tickets/files/9f14d3ab-36f2-49e0-90c1-b54f2a386252.xlsx','File attachment'),(19,74,'app/uploads/tickets/images/6071760a-2533-49cc-a42d-161a7c933be4.png','app/uploads/tickets/files/f1a8ff61-9b35-48bf-add8-0278cc99f62b.sql','File attachment'),(20,75,'app/uploads/tickets/images/adf6daa2-abef-48f2-851d-685fe862bcdb.png','app/uploads/tickets/files/96cba0f2-6102-482d-8f2a-954041643a87.sql','File attachment'),(21,85,'app/uploads/tickets/images/1959f300-dd54-434a-bedc-189978cc8d0e.png',NULL,'Image attachment'),(22,86,'app/uploads/tickets/images/06ac208f-dbef-48a1-b0eb-29859eaffcbf.png','app/uploads/tickets/files/271a1e2d-9783-4f0f-b750-7f56b03f3d56.xlsx','File attachment'),(23,87,'app/uploads/tickets/images/65d5c14b-3fe6-479c-9a75-7e2e8c00e40d.png',NULL,'Image attachment');
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `link` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_notifications_id` (`id`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (1,2,'New Ticket Created','Ticket #52 - testinfg','/ticket/views/52','ticket',1,'2025-12-13 14:53:50'),(2,2,'New Ticket Created','Ticket #53 - drfgdfgdfgdfg','/ticket/views/53','ticket',1,'2025-12-13 14:53:50'),(3,2,'New Ticket Created','Ticket #54 - king','/ticket/views/54','ticket',1,'2025-12-13 16:08:40'),(4,2,'New Ticket Created','Ticket #55 - Srenfgnf','/ticket/views/55','ticket',1,'2025-12-13 18:48:16'),(5,1,'New Ticket Created','Ticket #56 - testinfg','/ticket/views/56','ticket',0,'2025-12-13 19:38:35'),(6,2,'Ticket Updated','Ticket #7 has been updated','/ticket/views/7','ticket',1,'2025-12-14 14:36:24'),(7,3,'Ticket Updated','Ticket #7 has been updated','/ticket/views/7','ticket',0,'2025-12-14 14:39:47'),(8,2,'Ticket Updated','Ticket #7 has been updated','/ticket/views/7','ticket',1,'2025-12-14 14:42:17'),(9,2,'New Ticket Created','Ticket #57 - testinfg','/ticket/views/57','ticket',1,'2025-12-14 15:05:25'),(10,2,'New Ticket Created','Ticket #58 - Srenfgnf','/ticket/views/58','ticket',1,'2025-12-14 17:32:01'),(11,2,'New Ticket Created','Ticket #59 - llll','/ticket/views/59','ticket',1,'2025-12-14 17:35:03'),(12,2,'New Ticket Created','Ticket #60 - Srenfgnf','/ticket/views/60','ticket',1,'2025-12-14 17:41:23'),(13,2,'New Ticket Created','Ticket #61 - king','/ticket/views/61','ticket',1,'2025-12-14 17:41:44'),(14,2,'New Ticket Created','Ticket #62 - Dear i can not open report','/ticket/views/62','ticket',0,'2025-12-15 02:07:45'),(15,2,'New Ticket Created','Ticket #63 - Reject Column Number Of Application មិនត្រឹមត្រូវ','/ticket/views/63','ticket',0,'2025-12-15 02:09:25'),(16,2,'New Ticket Created','Ticket #64 - Loan Account Overview : Make Repayment  ចង់អោយអាច Edit សាច់ប្រាក់បាន','/ticket/views/64','ticket',0,'2025-12-15 02:11:58'),(17,2,'New Ticket Created','Ticket #65 - Loan Account Overview : Make Repayment  ចង់អោយអាច Edit សាច់ប្រាក់បាន','/ticket/views/65','ticket',0,'2025-12-15 02:15:17'),(18,2,'New Ticket Created','Ticket #66 - Loan Account Overview : Make Repayment  ចង់អោយអាច Edit សាច់ប្រាក់បាន','/ticket/views/66','ticket',0,'2025-12-15 02:16:37'),(19,2,'New Ticket Created','Ticket #67 - Dear i can not open report','/ticket/views/67','ticket',0,'2025-12-15 02:22:32'),(20,2,'New Ticket Created','Ticket #68 - Dear i can not open report','/ticket/views/68','ticket',0,'2025-12-15 02:35:09'),(21,2,'New Ticket Created','Ticket #69 - Loan Account Overview : Make Repayment  ចង់អោយអាច Edit សាច់ប្រាក់បាន','/ticket/views/69','ticket',0,'2025-12-15 02:35:52'),(22,2,'New Ticket Created','Ticket #70 - Loan Account Overview : Make Repayment  ចង់អោយអាច Edit សាច់ប្រាក់បាន','/ticket/views/70','ticket',0,'2025-12-15 02:36:23'),(23,2,'New Ticket Created','Ticket #71 - testinfg','/ticket/views/71','ticket',1,'2025-12-15 12:36:40'),(24,1,'Ticket Updated','Ticket #12 has been updated','/ticket/views/12','ticket',0,'2025-12-16 15:56:04'),(25,1,'Ticket Updated','Ticket #16 has been updated','/ticket/views/16','ticket',0,'2025-12-16 15:57:49'),(26,1,'Ticket Updated','Ticket #16 has been updated','/ticket/views/16','ticket',0,'2025-12-16 16:20:45'),(27,2,'Ticket Updated','Ticket #17 has been updated','/ticket/views/17','ticket',0,'2025-12-16 16:30:21'),(28,2,'Ticket Updated','Ticket #37 has been updated','/ticket/views/37','ticket',1,'2025-12-16 16:34:29'),(29,1,'New Ticket Created','Ticket #72 - testinfg','/ticket/views/72','ticket',0,'2025-12-16 17:03:13'),(30,1,'Ticket Updated','Ticket #72 has been updated','/ticket/views/72','ticket',0,'2025-12-16 17:16:39'),(31,1,'Ticket Updated','Ticket #72 has been updated','/ticket/views/72','ticket',0,'2025-12-16 17:16:54'),(32,1,'Ticket Updated','Ticket #72 has been updated','/ticket/views/72','ticket',0,'2025-12-16 17:17:02'),(33,2,'New Ticket Created','Ticket #73 - Srenfgnf','/ticket/views/73','ticket',1,'2025-12-16 17:17:27'),(34,1,'New Ticket Created','Ticket #74 - testinfg','/ticket/views/74','ticket',0,'2025-12-16 17:26:14'),(35,1,'New Ticket Created','Ticket #75 - Srenfgnf','/ticket/views/75','ticket',0,'2025-12-16 17:52:30'),(36,2,'Ticket Updated','Ticket #73 has been updated','/ticket/views/73','ticket',0,'2025-12-17 04:57:46'),(37,2,'Ticket Updated','Ticket #13 has been updated','/ticket/views/13','ticket',1,'2025-12-17 12:38:55'),(38,1,'Ticket Updated','Ticket #16 has been updated','/ticket/views/16','ticket',0,'2025-12-17 12:39:06'),(39,2,'New Ticket Created','Ticket #76 - Srenfgnf','/ticket/views/76','ticket',1,'2025-12-17 12:45:43'),(40,2,'New Ticket Created','Ticket #77 - Srenfgnf','/ticket/views/77','ticket',1,'2025-12-17 12:47:39'),(41,2,'New Ticket Created','Ticket #78 - Srenfgnf','/ticket/views/78','ticket',0,'2025-12-18 12:40:48'),(42,2,'New Ticket Created','Ticket #79 - testinfg','/ticket/views/79','ticket',0,'2025-12-18 12:41:09'),(43,1,'Ticket Updated','Ticket #10 has been updated','/ticket/views/10','ticket',0,'2025-12-22 11:53:34'),(44,1,'Ticket Updated','Ticket #10 has been updated','/ticket/views/10','ticket',0,'2025-12-22 11:54:10'),(45,2,'New Ticket Created','Ticket #80 - Srenfgnf','/ticket/views/80','ticket',0,'2025-12-22 11:55:34'),(46,2,'New Ticket Created','Ticket #81 - testinfg','/ticket/views/81','ticket',0,'2025-12-22 12:38:01'),(47,4,'Ticket Updated','Ticket #17 has been updated','/ticket/views/17','ticket',0,'2025-12-22 12:38:14'),(48,1,'Ticket Updated','Ticket #76 has been updated','/ticket/views/76','ticket',0,'2025-12-22 12:39:38'),(49,2,'Ticket Updated','Ticket #76 has been updated','/ticket/views/76','ticket',1,'2025-12-22 12:41:25'),(50,2,'New Ticket Created','Ticket #82 - Testing','/ticket/views/82','ticket',0,'2025-12-22 12:45:39'),(51,2,'New Ticket Created','Ticket #83 - Testing','/ticket/views/83','ticket',0,'2025-12-22 12:50:48'),(52,1,'Ticket Updated','Ticket #10 has been updated','/ticket/views/10','ticket',0,'2025-12-22 12:51:02'),(53,1,'Ticket Updated','Ticket #10 has been updated','/ticket/views/10','ticket',0,'2025-12-22 12:55:17'),(54,1,'New Ticket Created','Ticket #84 - Srenfgnf','/ticket/views/84','ticket',0,'2025-12-31 04:15:42'),(55,8,'New Ticket Created','Ticket #85 - Testing','/ticket/views/85','ticket',1,'2025-12-31 04:51:00'),(56,1,'Ticket Updated','Ticket #10 has been updated','/ticket/views/10','ticket',0,'2025-12-31 11:26:46'),(57,2,'New Ticket Created','Ticket #86 - Testiing12','/ticket/views/86','ticket',0,'2025-12-31 11:46:53'),(58,8,'New Ticket Created','Ticket #87 - I want to install wimdows on my laptop.','/ticket/views/87','ticket',1,'2025-12-31 12:41:20'),(59,4,'Ticket Updated','Ticket #87 has been updated','/ticket/views/87','ticket',0,'2025-12-31 12:46:22'),(60,4,'Ticket Updated','Ticket #87 has been updated','/ticket/views/87','ticket',0,'2025-12-31 12:47:06'),(61,5,'New Ticket Created','Ticket #88 - Srenfgnf','/ticket/views/88','ticket',0,'2026-02-27 13:48:27'),(62,4,'Ticket Updated','Ticket #36 has been updated','/ticket/views/36','ticket',0,'2026-02-27 15:14:49'),(63,1,'New Ticket Created','Ticket #89 - Srenfgnf','/ticket/views/89','ticket',0,'2026-03-06 08:40:46');
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permissions`
--

DROP TABLE IF EXISTS `permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `group` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_permissions_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissions`
--

LOCK TABLES `permissions` WRITE;
/*!40000 ALTER TABLE `permissions` DISABLE KEYS */;
INSERT INTO `permissions` VALUES (1,'VIEW_USER','User'),(2,'CREATE_USER','User'),(3,'DELETE_USER','User'),(4,'UPDATE_USER','User'),(5,'VIEW_DASHBOARD','Configuretion'),(6,'VIEW_TICKET','Ticket'),(7,'CREATE_TICKET','Ticket'),(8,'UPDATE_TICKET','Ticket'),(9,'DELETE_TICKET','Ticket'),(10,'VIEW_REPORTS','Reports'),(12,'VIEW_SETTING','Configuretion'),(13,'UPDATE_PERMISSIONS','Configuretion'),(14,'VIEW_ROLES','Configuretion'),(15,'CREATE_ROLES','Configuretion'),(16,'ASSIGN_TO_STAFF','Organization'),(17,'MANAGE_EMPLOYEE','Organization'),(18,'MANAGE_ROLE','Configuretion'),(20,'MANAGE_DEPARTMENT','Organization'),(21,'MANAGE_TELEGRAM','Configuretion'),(22,'MANAGE_POSITION','Organization'),(23,'MAKER_CHECKER','Configuretion'),(24,'APPROVE_CHEKER','Configuretion'),(25,'REJECT_CHEKER','Configuretion'),(26,'DELETE_CHEKER','Configuretion'),(27,'DELETE_STAFF','Organization'),(28,'UPDATE_STAFF','Organization'),(29,'VIEW_STAFF','Organization'),(30,'CREATE_STAFF','Organization'),(31,'DISABLE_ROLES','Configuretion'),(32,'CREATE_DEPARTMENT','Organization'),(33,'VIEW_DEPARTMENT','Organization'),(34,'VIEW_ORGANIZATION','Organization'),(35,'CHANGE_USER_PASSWORD','User'),(36,'CHANGE_OWN_PASSWORD','User');
/*!40000 ALTER TABLE `permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `positions`
--

DROP TABLE IF EXISTS `positions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `positions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `level` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `min_salary` decimal(10,2) DEFAULT NULL,
  `max_salary` decimal(10,2) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  KEY `ix_positions_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `positions`
--

LOCK TABLES `positions` WRITE;
/*!40000 ALTER TABLE `positions` DISABLE KEYS */;
INSERT INTO `positions` VALUES (2,'Report Team','Junior',700.00,800.00,1,'2025-12-16 12:32:28'),(3,'Developer','Senior',800.00,1000.00,1,'2025-12-16 12:33:30'),(4,'Project Manger','Manger',1000.00,2000.00,1,'2025-12-31 11:24:47');
/*!40000 ALTER TABLE `positions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `priorities`
--

DROP TABLE IF EXISTS `priorities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `priorities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_priorities_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `priorities`
--

LOCK TABLES `priorities` WRITE;
/*!40000 ALTER TABLE `priorities` DISABLE KEYS */;
INSERT INTO `priorities` VALUES (1,'Hight',NULL),(2,'Low',NULL);
/*!40000 ALTER TABLE `priorities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_permissions`
--

DROP TABLE IF EXISTS `role_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_permissions` (
  `role_id` int DEFAULT NULL,
  `permission_id` int DEFAULT NULL,
  KEY `role_id` (`role_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `role_permissions_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`),
  CONSTRAINT `role_permissions_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_permissions`
--

LOCK TABLES `role_permissions` WRITE;
/*!40000 ALTER TABLE `role_permissions` DISABLE KEYS */;
INSERT INTO `role_permissions` VALUES (1,5),(1,12),(1,10),(1,7),(1,8),(1,9),(1,13),(1,14),(1,15),(2,7),(2,8),(2,9),(2,10),(2,5),(2,6),(3,6),(3,8),(3,1),(3,2),(3,15),(3,10),(3,4),(3,12),(3,3),(3,13),(3,14),(3,5),(3,9),(3,7),(1,6),(1,18),(1,20),(1,21),(1,17),(1,22),(1,16),(1,23),(1,3),(1,2),(1,4),(1,1),(1,24),(1,25),(1,26),(1,30),(1,27),(1,29),(1,28),(1,31),(1,32),(1,33),(4,27),(4,3),(4,13),(4,21),(4,28),(4,5),(4,14),(4,22),(4,29),(4,6),(4,15),(4,23),(4,30),(4,7),(4,16),(4,24),(4,31),(4,8),(4,17),(4,25),(4,1),(4,32),(4,2),(4,9),(4,18),(4,26),(4,33),(4,12),(4,20),(1,34);
/*!40000 ALTER TABLE `role_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_roles_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Admin','Testing',1),(2,'Customer','123',1),(3,'Support','Support',1),(4,'Testing','',1);
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `id` int NOT NULL AUTO_INCREMENT,
  `external_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `firstname` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lastname` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `display_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mobile_no` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `join_on_date` date DEFAULT NULL,
  `position_id` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `position_id` (`position_id`),
  KEY `ix_staff_id` (`id`),
  CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`position_id`) REFERENCES `positions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (2,'EMP-001','John','Doe','John Doe','012345678','2025-12-16',2,1,'2025-12-16 13:37:49'),(3,'EMP-002','Anna','Smith','Anna Smith','098765432','2025-12-16',2,1,'2025-12-16 13:38:05'),(5,'EMP-1102','Hun','Sreng','Hun Sreng','086997981','2025-12-17',3,1,'2025-12-16 14:08:34'),(11,'EMP-1102','Rorn','Panhavatey','Rorn Panhavatey','098765433','2025-12-31',4,1,'2025-12-31 11:10:03'),(13,'','Hun','Sreng','Hun Sreng','0864354334','2025-12-31',2,1,'2025-12-31 11:16:53'),(15,'','Srin','Sombath','Srin Sombath','0864354334','2026-01-09',3,1,'2025-12-31 11:23:51');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_status_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
INSERT INTO `status` VALUES (1,'Active'),(7,'Close'),(10,'Delect'),(4,'Doing'),(2,'InActive'),(3,'Open'),(9,'Reject'),(6,'Resolved'),(5,'UAT'),(8,'Wating Approve');
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `display_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `khmer_first_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `khmer_last_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `createdondate` datetime DEFAULT NULL,
  `updateondate` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `first_name` (`first_name`),
  UNIQUE KEY `last_name` (`last_name`),
  UNIQUE KEY `khmer_first_name` (`khmer_first_name`),
  UNIQUE KEY `khmer_last_name` (`khmer_last_name`),
  KEY `ix_student_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `firstname` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lastname` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `display_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `khmer_firstname` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `khmer_lastname` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `position_id` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT (now()),
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `position_id` (`position_id`),
  KEY `ix_students_id` (`id`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`position_id`) REFERENCES `positions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `telegram_configs`
--

DROP TABLE IF EXISTS `telegram_configs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `telegram_configs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bot_token` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `chat_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_telegram_configs_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `telegram_configs`
--

LOCK TABLES `telegram_configs` WRITE;
/*!40000 ALTER TABLE `telegram_configs` DISABLE KEYS */;
INSERT INTO `telegram_configs` VALUES (1,'6817976775:AAFXGmtHtwrvpp5KBaYPJc4QkVeT6aiYIec','1599791024',0,'2025-12-13 13:18:54','2025-12-31 04:15:13'),(3,'6817976775:AAFXGmtHtwrvpp5KBaYPJc4QkVeT6aiYIec','-1002785449211',1,'2025-12-31 04:14:59','2025-12-31 04:15:13');
/*!40000 ALTER TABLE `telegram_configs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tickets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status_id` int NOT NULL,
  `priority_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  `assigned_to_id` int DEFAULT NULL,
  `assigned_to_department_id` int DEFAULT NULL,
  `assigned_by_id` int DEFAULT NULL,
  `requester_id` int NOT NULL,
  `approved_by_id` int DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `create_date` datetime NOT NULL,
  `approved_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `status_id` (`status_id`),
  KEY `priority_id` (`priority_id`),
  KEY `category_id` (`category_id`),
  KEY `assigned_to_id` (`assigned_to_id`),
  KEY `assigned_to_department_id` (`assigned_to_department_id`),
  KEY `assigned_by_id` (`assigned_by_id`),
  KEY `requester_id` (`requester_id`),
  KEY `approved_by_id` (`approved_by_id`),
  KEY `ix_tickets_id` (`id`),
  CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`status_id`) REFERENCES `status` (`id`),
  CONSTRAINT `tickets_ibfk_2` FOREIGN KEY (`priority_id`) REFERENCES `priorities` (`id`),
  CONSTRAINT `tickets_ibfk_3` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `tickets_ibfk_4` FOREIGN KEY (`assigned_to_id`) REFERENCES `users` (`id`),
  CONSTRAINT `tickets_ibfk_5` FOREIGN KEY (`assigned_to_department_id`) REFERENCES `departments` (`id`),
  CONSTRAINT `tickets_ibfk_6` FOREIGN KEY (`assigned_by_id`) REFERENCES `users` (`id`),
  CONSTRAINT `tickets_ibfk_7` FOREIGN KEY (`requester_id`) REFERENCES `users` (`id`),
  CONSTRAINT `tickets_ibfk_8` FOREIGN KEY (`approved_by_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
INSERT INTO `tickets` VALUES (7,'Computer not booting','sdgdsfgdfg dfgdfgdff',6,1,2,2,NULL,2,1,2,'2024-12-23 18:00:00','2025-03-21 02:00:00','2025-12-10 02:57:37','2025-12-12 19:27:52'),(10,'Email service down','Device stuck on loading screen',7,2,1,1,NULL,2,1,2,'2024-12-30 09:00:00','2025-01-03 17:00:00','2025-12-13 08:16:23','2025-12-13 17:37:29'),(11,'Email service down',NULL,9,NULL,NULL,NULL,NULL,NULL,1,2,NULL,NULL,'2025-12-13 08:17:04','2025-12-13 17:43:03'),(12,'Email service down',NULL,3,NULL,NULL,1,NULL,1,1,2,NULL,NULL,'2025-12-13 08:18:03','2025-12-13 15:33:49'),(13,'Computer not ','Device stuck on loading screen',7,2,1,2,1,2,1,2,'2025-01-01 03:00:00','2025-01-05 11:00:00','2025-12-13 08:32:58','2025-12-13 15:33:43'),(14,'Computer Testing ',NULL,10,NULL,NULL,NULL,NULL,NULL,1,2,NULL,NULL,'2025-12-13 08:35:11','2025-12-13 17:46:47'),(15,'Computer Testing ',NULL,10,NULL,NULL,NULL,NULL,NULL,1,2,NULL,NULL,'2025-12-13 08:35:41','2025-12-13 18:08:49'),(16,'Email service down','Users cannot send emails',4,1,NULL,1,NULL,2,2,2,NULL,NULL,'2025-12-13 08:51:25','2025-12-13 15:51:47'),(17,'All Client Due to pay','Testing',5,1,NULL,4,NULL,2,2,2,NULL,NULL,'2025-12-13 08:53:18','2025-12-13 15:53:32'),(35,'Dear i can not open report','Testing',3,1,2,NULL,3,NULL,2,2,NULL,NULL,'2025-12-13 09:06:27','2025-12-13 16:06:36'),(36,'Reject Column Number Of Application មិនត្រឹមត្រូវ',NULL,3,1,1,4,1,2,2,2,'2026-02-27 15:14:00','2026-03-05 15:14:00','2025-12-13 09:09:40','2025-12-13 16:09:57'),(37,'Srenfgnf',NULL,6,2,1,2,1,1,2,2,NULL,NULL,'2025-12-13 11:11:15','2025-12-13 18:11:26'),(38,'Testing','Please do on this now',6,1,2,2,1,NULL,2,2,'2025-12-13 00:00:00','2025-12-24 00:00:00','2025-12-13 11:13:25','2025-12-13 18:20:28'),(39,'Testing',NULL,6,1,1,1,NULL,NULL,2,2,NULL,NULL,'2025-12-13 13:32:09','2025-12-13 22:02:03'),(40,'Testing',NULL,3,1,1,1,NULL,NULL,2,2,NULL,NULL,'2025-12-13 13:34:03','2025-12-13 22:02:03'),(41,'Testing',NULL,3,1,1,1,NULL,NULL,2,2,NULL,NULL,'2025-12-13 13:39:49','2025-12-13 22:02:03'),(42,'king',NULL,3,2,2,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-13 13:44:42','2025-12-13 22:02:03'),(43,'Srenfgnf',NULL,3,1,1,2,1,NULL,2,2,NULL,NULL,'2025-12-13 13:52:06','2025-12-13 22:02:03'),(44,'Srenfgnf',NULL,3,1,1,2,1,NULL,2,2,NULL,NULL,'2025-12-13 13:57:14','2025-12-13 22:02:03'),(45,'testinfg',NULL,3,2,NULL,1,1,NULL,2,2,NULL,NULL,'2025-12-13 14:04:29','2025-12-13 22:02:03'),(46,'testinfg',NULL,3,2,NULL,1,1,NULL,2,2,NULL,NULL,'2025-12-13 14:06:06','2025-12-13 22:02:03'),(47,'testinfg',NULL,3,1,NULL,NULL,1,NULL,2,2,NULL,NULL,'2025-12-13 14:11:51','2025-12-13 22:02:03'),(48,'the besing','the besing',3,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-13 14:17:48','2025-12-13 22:02:03'),(49,'Srenfgnf',NULL,3,2,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-13 14:22:04','2025-12-13 22:02:03'),(50,'testinfg',NULL,3,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-13 14:26:32','2025-12-13 22:02:03'),(51,'Kesiduf','Kesiduf',3,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-13 14:34:09','2025-12-13 22:02:03'),(52,'testinfg',NULL,3,2,1,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-13 14:49:05','2025-12-13 22:02:03'),(53,'drfgdfgdfgdfg',NULL,3,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-13 14:53:53','2025-12-13 22:02:03'),(54,'king',NULL,3,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-13 16:08:43','2025-12-14 01:47:26'),(55,'Srenfgnf',NULL,3,1,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-13 18:48:19','2025-12-14 21:59:07'),(56,'testinfg',NULL,3,2,NULL,NULL,NULL,2,2,2,'2025-12-23 17:00:00','2025-12-10 17:00:00','2025-12-13 19:38:36','2025-12-14 02:39:08'),(57,'testinfg',NULL,10,2,2,2,1,NULL,2,1,NULL,NULL,'2025-12-14 15:05:29','2025-12-14 22:17:33'),(58,'Srenfgnf',NULL,3,1,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-14 17:32:03','2025-12-15 00:34:14'),(59,'llll',NULL,9,2,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-14 17:35:06','2025-12-15 00:39:47'),(60,'Srenfgnf',NULL,10,NULL,2,2,NULL,NULL,2,2,NULL,NULL,'2025-12-14 17:41:26','2025-12-15 00:41:32'),(61,'king',NULL,3,NULL,2,2,NULL,NULL,2,2,NULL,NULL,'2025-12-14 17:41:48','2025-12-17 19:44:21'),(62,'Dear i can not open report',NULL,3,1,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-15 02:07:45','2025-12-17 19:45:21'),(63,'Reject Column Number Of Application មិនត្រឹមត្រូវ',NULL,3,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-15 02:09:25','2025-12-31 18:06:21'),(64,'Loan Account Overview : Make Repayment  ចង់អោយអាច Edit សាច់ប្រាក់បាន',NULL,3,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-15 02:11:58','2025-12-31 18:27:58'),(65,'Loan Account Overview : Make Repayment  ចង់អោយអាច Edit សាច់ប្រាក់បាន',NULL,9,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-15 02:15:17','2025-12-31 18:28:16'),(66,'Loan Account Overview : Make Repayment  ចង់អោយអាច Edit សាច់ប្រាក់បាន',NULL,9,1,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-15 02:16:38','2025-12-31 18:28:16'),(67,'Dear i can not open report',NULL,9,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-15 02:22:32','2025-12-31 18:28:16'),(68,'Dear i can not open report',NULL,3,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-15 02:35:09','2025-12-31 18:42:06'),(69,'Loan Account Overview : Make Repayment  ចង់អោយអាច Edit សាច់ប្រាក់បាន',NULL,3,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-15 02:35:52','2026-02-27 20:28:46'),(70,'Loan Account Overview : Make Repayment  ចង់អោយអាច Edit សាច់ប្រាក់បាន',NULL,3,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-15 02:36:24','2026-02-27 20:28:46'),(71,'testinfg',NULL,8,1,2,NULL,NULL,NULL,2,NULL,NULL,NULL,'2025-12-15 12:36:40',NULL),(72,'testinfg',NULL,3,1,1,1,NULL,1,1,1,'2025-12-16 10:16:00','2025-12-19 10:16:00','2025-12-16 17:03:14','2025-12-17 00:04:10'),(73,'Srenfgnf',NULL,6,1,1,2,NULL,2,1,1,NULL,NULL,'2025-12-16 17:17:27','2025-12-17 00:17:42'),(74,'testinfg',NULL,3,NULL,NULL,NULL,NULL,NULL,1,1,NULL,NULL,'2025-12-16 17:26:14','2025-12-17 00:26:30'),(75,'Srenfgnf',NULL,3,NULL,NULL,NULL,NULL,NULL,1,1,NULL,NULL,'2025-12-16 17:52:31','2025-12-17 00:52:46'),(76,'Srenfgnf',NULL,4,1,NULL,2,NULL,2,2,2,NULL,NULL,'2025-12-17 12:45:44','2025-12-22 19:39:17'),(77,'Srenfgnf',NULL,10,1,NULL,2,NULL,NULL,2,2,NULL,NULL,'2025-12-17 12:47:39','2025-12-22 19:38:52'),(78,'Srenfgnf',NULL,9,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-18 12:40:48','2025-12-22 19:38:48'),(79,'testinfg',NULL,3,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-18 12:41:09','2025-12-22 19:38:42'),(80,'Srenfgnf',NULL,3,1,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-22 11:55:34','2025-12-22 19:38:34'),(81,'testinfg',NULL,3,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-22 12:38:01','2025-12-22 19:38:29'),(82,'Testing',NULL,8,NULL,NULL,NULL,NULL,NULL,2,NULL,NULL,NULL,'2025-12-22 12:45:39',NULL),(83,'Testing',NULL,8,NULL,NULL,NULL,NULL,NULL,2,NULL,NULL,NULL,'2025-12-22 12:50:48',NULL),(84,'Srenfgnf',NULL,8,2,2,1,NULL,NULL,2,NULL,NULL,NULL,'2025-12-31 04:15:45',NULL),(85,'Testing','Testing',3,1,2,NULL,2,NULL,8,2,NULL,NULL,'2025-12-31 04:51:02','2025-12-31 13:12:30'),(86,'Testiing12',NULL,3,NULL,NULL,NULL,NULL,NULL,2,2,NULL,NULL,'2025-12-31 11:46:54','2025-12-31 18:47:39'),(87,'I want to install wimdows on my laptop.',NULL,4,2,2,4,2,4,8,2,'2025-12-30 10:00:00','2026-01-07 05:45:00','2025-12-31 12:41:21','2025-12-31 19:43:56'),(88,'Srenfgnf',NULL,3,1,1,5,1,NULL,2,2,'2026-02-27 00:00:00','2026-02-27 00:00:00','2026-02-27 13:48:46','2026-02-27 22:14:03'),(89,'Srenfgnf',NULL,8,NULL,NULL,1,NULL,NULL,2,NULL,NULL,NULL,'2026-03-06 08:40:47',NULL);
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `is_delete` int DEFAULT NULL,
  `username` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_locked` int DEFAULT NULL,
  `create_date` datetime NOT NULL,
  `role_id` int NOT NULL,
  `department_id` int DEFAULT NULL,
  `staff_id` int DEFAULT NULL,
  `failed_attempts` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `role_id` (`role_id`),
  KEY `department_id` (`department_id`),
  KEY `ix_users_id` (`id`),
  KEY `fk_users_staff` (`staff_id`),
  CONSTRAINT `fk_users_staff` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`id`) ON DELETE SET NULL,
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`),
  CONSTRAINT `users_ibfk_2` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,0,'Admin','hunsreng2022@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$SqmV0tq7l1IKgfDeO8c4xw$YifEYybHPFgUVevi1ShUti4R8foG3NaAECavjqpAEmI',0,'2025-12-10 01:38:30',1,1,2,0),(2,0,'Sremg','hunsreng2021@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$43xvrbWWUoqx9v4fI8RYqw$ZFZq793dCqv1ChuB7mce7AmFg3qGi/zHplRFSe8Km7E',0,'2025-12-10 02:23:29',1,1,5,0),(3,0,'chealyly','meaksreyeam.vivat@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$Sam19n5vDUHoPUdo7R3jHA$DVp4woXpv32H8WDLXboMyZzo+C2/cA8clfZGTm+03Nc',0,'2025-12-10 10:14:34',1,1,NULL,0),(4,0,'Sombath','Sombath2021@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$a63VuvdeKwUAACDkPOccAw$M48DsIqXO81g9D8TKa3kSJE6rJw4o+FhLFC5L/RHIoc',0,'2025-12-14 15:44:24',3,2,NULL,0),(5,0,'HunSreng','Admin@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$6j2HsLYWYswZg9Aa47xXag$PN9jEsHTM1u2niem6+PDRyC6VnNCvJZz3P+rzaXyyw4',0,'2025-12-16 14:54:28',1,1,5,1),(6,0,'King','King2021@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$Wcs5R4jxPsdYa43RuhfiPA$rgJ04fzl/kHLgWv6wjMy/I3bQdrQ2u/hRDL69qJTDyg',0,'2025-12-16 16:35:05',2,6,3,0),(7,0,'devsolver','teysdhfg@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$SQmBsJaSUgrhPAfgfM95jw$mJXmyqQkezF+0QBliPnLy6F3wYoFP/3sj4hevstWG+E',0,'2025-12-17 12:46:34',1,6,5,0),(8,0,'Customer1','Customer1@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$9/5/j/GeM0YIIWTsvVeKUQ$N5Qv0vHGIlcGHoLzs/Xna0Byb1FiCI1zayJPVbaVBXs',0,'2025-12-31 04:48:14',2,7,NULL,0),(9,0,'Customer2','Customer2@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$GINwrlVK6Z2T8t67F0KIsQ$vfM+0SSBAqHZ7qxEv3OYhiv6TE8Cpm1JEUsAeCTJJzI',0,'2025-12-31 05:03:10',2,NULL,NULL,0),(10,0,'Votey','votey21@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$QEjp3RsDwDiHsDbGGEOI8Q$oLDz9i8FPm41ReArI3mvIDVJcW4IUUYR/nPENZv7eVM',0,'2025-12-31 12:51:45',4,NULL,11,0),(11,0,'TheKing','hunsreng2029@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$kTIGIMQYw7i3tvb+X4tx7g$ElS9MTNPCae7uZJqrGGLzY98hC8osuuxgTAaK7467lE',0,'2026-02-27 15:31:05',2,NULL,NULL,0),(12,0,'the king','hunsreng202ds1@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$cE6pFcKYc64VIqSU0vp/7w$5YcEhMQuLIwpzMyYg4TvKGkNNOFAhMbYehdICztjW9c',0,'2026-03-03 07:36:20',2,NULL,NULL,0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `v_ticket_reports`
--

DROP TABLE IF EXISTS `v_ticket_reports`;
/*!50001 DROP VIEW IF EXISTS `v_ticket_reports`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_ticket_reports` AS SELECT 
 1 AS `id`,
 1 AS `title`,
 1 AS `status`,
 1 AS `category`,
 1 AS `priority`,
 1 AS `department`,
 1 AS `assigned_to`,
 1 AS `assigned_by`,
 1 AS `created_by`,
 1 AS `approved_by`,
 1 AS `create_date`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping routines for database 'db_srorn'
--

--
-- Final view structure for view `v_ticket_reports`
--

/*!50001 DROP VIEW IF EXISTS `v_ticket_reports`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `v_ticket_reports` AS select `t`.`id` AS `id`,`t`.`title` AS `title`,`s`.`name` AS `status`,`c`.`name` AS `category`,`p`.`name` AS `priority`,`d`.`name` AS `department`,`u_assign`.`username` AS `assigned_to`,`u_assignby`.`username` AS `assigned_by`,`u_createby`.`username` AS `created_by`,`u_approve`.`username` AS `approved_by`,`t`.`create_date` AS `create_date` from ((((((((`tickets` `t` left join `departments` `d` on((`t`.`assigned_to_department_id` = `d`.`id`))) left join `users` `u_approve` on((`t`.`approved_by_id` = `u_approve`.`id`))) left join `users` `u_assign` on((`t`.`assigned_to_id` = `u_assign`.`id`))) left join `users` `u_assignby` on((`t`.`assigned_by_id` = `u_assignby`.`id`))) left join `users` `u_createby` on((`t`.`requester_id` = `u_createby`.`id`))) left join `status` `s` on((`t`.`status_id` = `s`.`id`))) left join `categories` `c` on((`t`.`category_id` = `c`.`id`))) left join `priorities` `p` on((`t`.`priority_id` = `p`.`id`))) where (`t`.`status_id` not in (9,10)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-08  0:54:47
