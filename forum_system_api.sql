-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: final_forum_system
-- ------------------------------------------------------
-- Server version	5.5.5-10.9.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(1000) CHARACTER SET utf8mb3 DEFAULT NULL,
  `description` varchar(10000) CHARACTER SET utf8mb3 DEFAULT NULL,
  `is_private` tinyint(4) NOT NULL,
  `is_locked` tinyint(4) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Problems','Public category for all our problems',0,0),(2,'A40 Python','Група на тигрите от питоня за взаимопомощ.',1,0),(3,'Общи приказки','Категория за различни off-topic теми.',0,0),(4,'A40 Final Projects','Следете тук за всички особености покрай финалните проекти.',1,0);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conversations`
--

DROP TABLE IF EXISTS `conversations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `conversations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject` varchar(10000) CHARACTER SET utf8mb3 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conversations`
--

LOCK TABLES `conversations` WRITE;
/*!40000 ALTER TABLE `conversations` DISABLE KEYS */;
INSERT INTO `conversations` VALUES (1,'Относно Judge Task II'),(2,'Да те питам нещо, брат'),(4,'Джаф-джаф!');
/*!40000 ALTER TABLE `conversations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conversations_messages`
--

DROP TABLE IF EXISTS `conversations_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `conversations_messages` (
  `conversation_id` int(11) NOT NULL,
  `message_id` int(11) NOT NULL,
  PRIMARY KEY (`conversation_id`,`message_id`),
  KEY `fk_conversations_has_messages_messages1_idx` (`message_id`),
  KEY `fk_conversations_has_messages_conversations1_idx` (`conversation_id`),
  CONSTRAINT `fk_conversations_has_messages_conversations1` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_conversations_has_messages_messages1` FOREIGN KEY (`message_id`) REFERENCES `messages` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conversations_messages`
--

LOCK TABLES `conversations_messages` WRITE;
/*!40000 ALTER TABLE `conversations_messages` DISABLE KEYS */;
INSERT INTO `conversations_messages` VALUES (1,1),(1,2),(2,3),(4,5),(4,6),(4,7);
/*!40000 ALTER TABLE `conversations_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(10000) CHARACTER SET utf8mb3 DEFAULT NULL,
  `created_on` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_messages_users1_idx` (`user_id`),
  CONSTRAINT `fk_messages_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,'Здрасти, Митак! Ще ти пратя решението след малко.','2022-10-10 18:44:14',3),(2,'Много мерси, брат!','2022-10-10 18:47:31',4),(3,'Здрасти! Относно последния ни проект, да те питам, колко кила си?','2022-10-13 15:38:53',5),(4,'Здрасти! Относно последния ни проект, да те питам, колко кила си?','2022-10-13 15:44:38',5),(5,'Пробвам да видя дали ще ми отговориш хаха!','2022-10-17 15:26:16',5),(6,'Пробвам да видя дали ще ми отговориш хаха!','2022-10-17 15:37:06',11),(7,'Опа, копирах ти съобщението. Извинявай. Иначе те разбирам, де! :)','2022-10-17 15:46:41',11);
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `replies`
--

DROP TABLE IF EXISTS `replies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `replies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(10000) CHARACTER SET utf8mb3 DEFAULT NULL,
  `created_on` datetime NOT NULL,
  `is_best` tinyint(4) DEFAULT 0,
  `user_id` int(11) NOT NULL,
  `topic_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_replies_users1_idx` (`user_id`),
  KEY `fk_replies_topics1_idx` (`topic_id`),
  CONSTRAINT `fk_replies_topics1` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `replies`
--

LOCK TABLES `replies` WRITE;
/*!40000 ALTER TABLE `replies` DISABLE KEYS */;
INSERT INTO `replies` VALUES (1,'Здрасти! Ще ти пиша на лично!','2022-10-10 15:18:51',0,3,1),(2,'Мерси много, брат!','2022-10-10 17:26:13',0,4,1),(3,'Здравейте! Подгответе си въпросите свързани с ДСА модула. Ще отговаряме на всичко - LLists, Recursions, BST, etc.','2022-10-13 14:24:33',0,1,2),(4,'Привет! Аз мога ли да помоля да отделим време за разликите между QUEUE и STACK. Мерси предварително!','2022-10-16 22:51:36',0,8,2),(5,'Здравейте! Можете да се логнете в learn и да видите какви финални проекти са ви разпределени.','2022-10-17 14:16:20',0,1,3),(6,'Здравейте! В тази тема ще споделяме всякакви допълнителни четива за курса.','2022-10-17 14:20:41',0,1,4),(7,'Здравейте! В тази тема ще обсъждаме всичко свързано със софт скилс','2022-10-17 14:24:38',0,1,5),(8,'Cohort-wide announcements','2022-10-17 14:29:46',0,1,6),(9,'Здравейте, тигри! Вижте новата категория направена специално за финалните ви проекти. Поздрави!','2022-10-17 15:07:53',1,10,6);
/*!40000 ALTER TABLE `replies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topics`
--

DROP TABLE IF EXISTS `topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `topics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(10000) CHARACTER SET utf8mb3 DEFAULT NULL,
  `views` int(11) DEFAULT 0,
  `activity` datetime DEFAULT NULL,
  `is_locked` tinyint(4) DEFAULT 0,
  `user_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_topics_users_idx` (`user_id`),
  KEY `fk_topics_categories1_idx` (`category_id`),
  CONSTRAINT `fk_topics_categories1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topics`
--

LOCK TABLES `topics` WRITE;
/*!40000 ALTER TABLE `topics` DISABLE KEYS */;
INSERT INTO `topics` VALUES (1,'Judge Task II - Не мога да реша втората!',2,'2022-10-10 17:26:13',0,4,2),(2,'DSA - Q&A',16,'2022-10-16 22:51:36',0,1,1),(3,'ВАЖНО! Информация за финалния проект!',0,'2022-10-17 14:16:20',0,1,4),(4,'Further Reading',0,'2022-10-17 14:20:41',0,1,2),(5,'Soft skills',0,'2022-10-17 14:24:38',0,1,2),(6,'Important',1,'2022-10-17 15:07:53',0,1,2);
/*!40000 ALTER TABLE `topics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) NOT NULL,
  `password` varchar(1000) NOT NULL,
  `role` varchar(16) NOT NULL,
  `registered_on` date NOT NULL,
  `email` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_name_UNIQUE` (`user_name`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','8c3a6e43e8078ded91fb6faf8006d05988133e10ab72324c7a5c0a16eb6e4f61','admin','2022-10-10','admin@admin.com'),(2,'yaskata','fe284f834781c8cb2edee6f5c8a74949aa96a008a049eb08674d7eb074ada71f','regular','2022-10-10','yasen.h.taha@gmail.com'),(3,'krasi','361467cbd5464afe43c3a8be462e5e8f83320bcc40b643e1d0cef6f9d8baf29b','regular','2022-10-10','krasi@abv.bg'),(4,'mitaka_batko','18e9950511ecab08ed4bd2ae81fcd24c2156e4afedd7a0194b016264d8b54ddb','regular','2022-10-10','mitaka@batko.org'),(5,'pesho','4d6db9b9d208c617b479ca7b7527788b55aab0a4aebb129dd99a64c0adde4f15','regular','2022-10-11','pesho@yahoo.com'),(6,'alice','caa56151f70e20c0b39f343542123edd679bc8acbff9a180f45fc2dd38fa9ba5','regular','2022-10-11','alice@wikipedia.org'),(7,'marry_jane','caa56151f70e20c0b39f343542123edd679bc8acbff9a180f45fc2dd38fa9ba5','regular','2022-10-11','legalize@abv.bg'),(8,'ico_hazarta','8c3a6e43e8078ded91fb6faf8006d05988133e10ab72324c7a5c0a16eb6e4f61','regular','2022-10-11','deputat@parliament.bg'),(9,'sto_kila','caa56151f70e20c0b39f343542123edd679bc8acbff9a180f45fc2dd38fa9ba5','regular','2022-10-11','qvor@bnt.bg'),(10,'edo_trainer','029043336e62785117a9c9164ed2f980d852eff11b5fba6048ced4fe310ebfa4','regular','2022-10-13','tigara@telerikacademy.com'),(11,'troyan_kuche','128753898f9e56f7f94ad60ff117f0633acdc20864f3e342831ed30c2784a427','regular','2022-10-17','troyan_pablo@abv.bg');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_categories`
--

DROP TABLE IF EXISTS `users_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `users_categories` (
  `user_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `access` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`category_id`),
  KEY `fk_users_has_categories_categories1_idx` (`category_id`),
  KEY `fk_users_has_categories_users1_idx` (`user_id`),
  CONSTRAINT `fk_users_has_categories_categories1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_categories_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_categories`
--

LOCK TABLES `users_categories` WRITE;
/*!40000 ALTER TABLE `users_categories` DISABLE KEYS */;
INSERT INTO `users_categories` VALUES (5,2,2),(5,4,2),(8,2,2),(10,2,2),(10,4,2),(11,2,2);
/*!40000 ALTER TABLE `users_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_conversations`
--

DROP TABLE IF EXISTS `users_conversations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `users_conversations` (
  `user_id` int(11) NOT NULL,
  `conversation_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`conversation_id`),
  KEY `fk_users_has_conversations_conversations1_idx` (`conversation_id`),
  KEY `fk_users_has_conversations_users1_idx` (`user_id`),
  CONSTRAINT `fk_users_has_conversations_conversations1` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_conversations_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_conversations`
--

LOCK TABLES `users_conversations` WRITE;
/*!40000 ALTER TABLE `users_conversations` DISABLE KEYS */;
INSERT INTO `users_conversations` VALUES (3,1),(4,1),(5,2),(5,4),(8,2),(11,4);
/*!40000 ALTER TABLE `users_conversations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_replies`
--

DROP TABLE IF EXISTS `users_replies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `users_replies` (
  `user_id` int(11) NOT NULL,
  `reply_id` int(11) NOT NULL,
  `upvote_downvote` int(11) DEFAULT 0,
  PRIMARY KEY (`user_id`,`reply_id`),
  KEY `fk_users_has_replies_replies1_idx` (`reply_id`),
  KEY `fk_users_has_replies_users1_idx` (`user_id`),
  CONSTRAINT `fk_users_has_replies_replies1` FOREIGN KEY (`reply_id`) REFERENCES `replies` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_replies_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_replies`
--

LOCK TABLES `users_replies` WRITE;
/*!40000 ALTER TABLE `users_replies` DISABLE KEYS */;
INSERT INTO `users_replies` VALUES (1,9,1),(8,3,1),(8,9,1);
/*!40000 ALTER TABLE `users_replies` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-17 17:47:43
