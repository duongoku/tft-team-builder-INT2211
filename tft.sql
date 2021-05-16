-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: tft
-- ------------------------------------------------------
-- Server version	8.0.21

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

--
-- Table structure for table `authentication_system`
--

DROP TABLE IF EXISTS `authentication_system`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authentication_system` (
  `System_ID` int NOT NULL,
  PRIMARY KEY (`System_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `board`
--

DROP TABLE IF EXISTS `board`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `board` (
  `Board_ID` int NOT NULL,
  `Username` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Board_ID`),
  KEY `Username` (`Username`),
  CONSTRAINT `board_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `user` (`Username`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `champion`
--

DROP TABLE IF EXISTS `champion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `champion` (
  `Board_ID` int NOT NULL,
  `Slot_ID` int NOT NULL,
  `Champion_ID` int NOT NULL,
  PRIMARY KEY (`Champion_ID`,`Slot_ID`,`Board_ID`),
  KEY `Board_ID` (`Board_ID`),
  CONSTRAINT `champion_ibfk_1` FOREIGN KEY (`Champion_ID`) REFERENCES `champion_details` (`Champion_ID`) ON UPDATE CASCADE,
  CONSTRAINT `champion_ibfk_2` FOREIGN KEY (`Board_ID`) REFERENCES `board` (`Board_ID`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `champion_details`
--

DROP TABLE IF EXISTS `champion_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `champion_details` (
  `Champion_ID` int NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Skill_Description` varchar(1500) DEFAULT NULL,
  PRIMARY KEY (`Champion_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `item` (
  `Item_ID` int NOT NULL,
  `Board_ID` int NOT NULL,
  `Slot_ID` int NOT NULL,
  `Champion_ID` int NOT NULL,
  PRIMARY KEY (`Item_ID`,`Champion_ID`,`Slot_ID`,`Board_ID`),
  KEY `Champion_ID` (`Champion_ID`,`Slot_ID`,`Board_ID`),
  CONSTRAINT `item_ibfk_1` FOREIGN KEY (`Item_ID`) REFERENCES `item_details` (`Item_ID`) ON UPDATE CASCADE,
  CONSTRAINT `item_ibfk_2` FOREIGN KEY (`Champion_ID`, `Slot_ID`, `Board_ID`) REFERENCES `champion` (`Champion_ID`, `Slot_ID`, `Board_ID`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `item_details`
--

DROP TABLE IF EXISTS `item_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `item_details` (
  `Item_ID` int NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Description` varchar(1500) DEFAULT NULL,
  PRIMARY KEY (`Item_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trait`
--

DROP TABLE IF EXISTS `trait`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trait` (
  `Trait_ID` int NOT NULL,
  `Champion_ID` int NOT NULL,
  PRIMARY KEY (`Trait_ID`,`Champion_ID`),
  KEY `Champion_ID` (`Champion_ID`),
  CONSTRAINT `trait_ibfk_1` FOREIGN KEY (`Champion_ID`) REFERENCES `champion_details` (`Champion_ID`) ON UPDATE CASCADE,
  CONSTRAINT `trait_ibfk_2` FOREIGN KEY (`Trait_ID`) REFERENCES `trait_details` (`Trait_ID`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `trait_details`
--

DROP TABLE IF EXISTS `trait_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trait_details` (
  `Trait_ID` int NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Description` varchar(1500) DEFAULT NULL,
  `Activation` varchar(1500) DEFAULT NULL,
  PRIMARY KEY (`Trait_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `Username` varchar(50) NOT NULL,
  `System_ID` int DEFAULT NULL,
  `Encrypted_Password` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`Username`),
  KEY `System_ID` (`System_ID`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`System_ID`) REFERENCES `authentication_system` (`System_ID`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-16 11:51:28
