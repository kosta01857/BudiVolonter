-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: budivolonter
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `aktivnost`
--

DROP TABLE IF EXISTS `aktivnost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aktivnost` (
  `idOrg` int NOT NULL,
  `idAkt` int NOT NULL AUTO_INCREMENT,
  `naziv` varchar(256) NOT NULL,
  `brMesta` int NOT NULL,
  `datumOd` date NOT NULL,
  `datumDo` date NOT NULL,
  `datumRok` date NOT NULL,
  `mesto` varchar(256) NOT NULL DEFAULT 'nije navedeno',
  `lokacija` int NOT NULL,
  `opis` varchar(3000) DEFAULT NULL,
  PRIMARY KEY (`idAkt`),
  KEY `idx_brakt` (`idAkt`),
  KEY `FK_lokacija_idx` (`lokacija`),
  KEY `FK_korisnik_aktivnost_idx` (`idOrg`),
  CONSTRAINT `FK_korisnik_aktivnost` FOREIGN KEY (`idOrg`) REFERENCES `korisnik` (`idKor`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_lokacija` FOREIGN KEY (`lokacija`) REFERENCES `lokacija` (`idLok`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aktivnost`
--

LOCK TABLES `aktivnost` WRITE;
/*!40000 ALTER TABLE `aktivnost` DISABLE KEYS */;
INSERT INTO `aktivnost` VALUES (1,1,'Volontiranje u bolnici',10,'2024-06-01','2024-06-30','2024-05-31','Beograd',1,'Pomoc osoblju bolnice u svakodnevnim aktivnostima.'),(3,2,'Radionice za decu',20,'2024-07-01','2024-07-15','2024-06-25','Novi Sad',2,'Održavanje kreativnih radionica za decu.'),(1,3,'Sportski kamp',15,'2024-08-01','2024-08-10','2024-07-20','Subotica',3,'Organizacija sportskih aktivnosti za decu i mlade.'),(2,4,'Ekološka akcija',30,'2024-09-01','2024-09-05','2024-08-25','Niš',4,'Čišćenje i uređenje parkova.');
/*!40000 ALTER TABLE `aktivnost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_korisnik_idKor` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_korisnik_idKor` FOREIGN KEY (`user_id`) REFERENCES `korisnik` (`idKor`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'','admin','logentry'),(2,'','contenttypes','contenttype'),(3,'','sessions','session'),(4,'','budivolonter','aktivnost'),(5,'','budivolonter','korisnik'),(6,'','budivolonter','lokacija'),(7,'','budivolonter','oblast'),(8,'','budivolonter','prepiska'),(9,'','budivolonter','prijava'),(10,'','budivolonter','pripada'),(11,'','budivolonter','vestina'),(12,'','budivolonter','zanimaga'),(13,'','budivolonter','poruka');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'sessions','0001_initial','2024-05-14 00:25:32.235804');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2sjfb10t8otlov0c1gs6g8ghhpslp9fh','.eJxVjDkOwjAUBe_iGll4SWxT0ucM1t-CA8iR4qRC3B0ipYD2zcx7qQzbWvLWZMkTq4uy6vS7IdBD6g74DvU2a5rrukyod0UftOlhZnleD_fvoEAr39oH5E5SbxnBpq4P7FMIBsgZISMuEhgkHi2OECEaR9F5hiR0loQhqvcH-aM4yg:1s7129:KKGGwpe7lGTcTPuYR_sZrO2AZsjinkQJ20XRctuMrsg','2024-05-28 22:54:09.821389'),('4hqzdlzg67ar79h8ipwny9rl9mc5d0is','.eJxVjEsOwjAMBe-SNYqCXacxS_acoXJiQwsolfpZIe4OlbqA7ZuZ93KdrEvfrbNN3aDu5NAdfrcs5WF1A3qXeht9GesyDdlvit_p7C-j2vO8u38Hvcz9t26JJCtntJgYGzgGoUJXxgyJAoEaB8WY2ihMBmKATCoFIIXMbePeH8y_NyA:1s8LgK:TAKL2gjV_J2QimsoFteO3nPEuLPW3bVe-tZRjyiWS-4','2024-06-01 15:09:08.398785'),('g7ff79thcsii3x9yfmmsc24l1zzm0goi','.eJxVjEEOwiAQRe_C2hAYEFuX7j0DGWYGqRpISrsy3l2bdKHb_977LxVxXUpcu8xxYnVWVh1-t4T0kLoBvmO9NU2tLvOU9KbonXZ9bSzPy-7-HRTs5VuTYXN0KIRAltjjCXKAgKMXBB5zEmKbXCAvg3hvnRWikGGgYMgAqvcHEss4_g:1sD4qG:FJfCO4NnuDVaezNmKGK2o8aDEOQp-dBaj7VI8SdlxXM','2024-06-14 16:10:56.314173'),('hsftp1fu4djs7bwp5djt0elsd4nu6d3i','.eJxVjDkOwjAUBe_iGll4SWxT0ucM1t-CA8iR4qRC3B0ipYD2zcx7qQzbWvLWZMkTq4uy6vS7IdBD6g74DvU2a5rrukyod0UftOlhZnleD_fvoEAr39oH5E5SbxnBpq4P7FMIBsgZISMuEhgkHi2OECEaR9F5hiR0loQhqvcH-aM4yg:1sCHuH:8n2IluPzUGSE3z4sSoyr2c-rZcuEqxeFqp7dbJQITc0','2024-06-12 11:55:49.499163'),('k39q437q8lh7gyhvy9r3msh74p7iw50o','.eJxVjDkOwjAUBe_iGll4SWxT0ucM1t-CA8iR4qRC3B0ipYD2zcx7qQzbWvLWZMkTq4uy6vS7IdBD6g74DvU2a5rrukyod0UftOlhZnleD_fvoEAr39oH5E5SbxnBpq4P7FMIBsgZISMuEhgkHi2OECEaR9F5hiR0loQhqvcH-aM4yg:1sCHJE:oYUphRNHvYrSlIE_GSJ29Vkli_SZweIa_ZIvW_5GY5s','2024-06-12 11:17:32.285504'),('vukovu1mwfvto7ycklc3ltlve9lcqh26','.eJxVjDkOwjAUBe_iGll4SWxT0ucM1t-CA8iR4qRC3B0ipYD2zcx7qQzbWvLWZMkTq4uy6vS7IdBD6g74DvU2a5rrukyod0UftOlhZnleD_fvoEAr39oH5E5SbxnBpq4P7FMIBsgZISMuEhgkHi2OECEaR9F5hiR0loQhqvcH-aM4yg:1sCMQt:ic_zpPf9HiE1uc90cWqMnTKdxhEc0ilNnlhEv4mWv-A','2024-06-12 16:45:47.474666'),('zrha08zqigif5zxhd982einap8k1goqs','.eJxVjDkOwjAUBe_iGll4SWxT0ucM1t-CA8iR4qRC3B0ipYD2zcx7qQzbWvLWZMkTq4uy6vS7IdBD6g74DvU2a5rrukyod0UftOlhZnleD_fvoEAr39oH5E5SbxnBpq4P7FMIBsgZISMuEhgkHi2OECEaR9F5hiR0loQhqvcH-aM4yg:1s8LaB:UfbgPCAVZJ8HsuZKoOePwnXINQGjCK63Xkp3AO_TYW0','2024-06-01 15:02:47.852192');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `korisnik`
--

DROP TABLE IF EXISTS `korisnik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `korisnik` (
  `idKor` int NOT NULL AUTO_INCREMENT,
  `email` varchar(256) NOT NULL,
  `password` varchar(256) NOT NULL,
  `ime` varchar(256) NOT NULL,
  `prezime` varchar(256) DEFAULT NULL,
  `pib` int DEFAULT NULL,
  `telefon` varchar(14) DEFAULT NULL,
  `tip` char(1) NOT NULL,
  `datumRodj` date DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_active` tinyint DEFAULT NULL,
  PRIMARY KEY (`idKor`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `PIB_UNIQUE` (`pib`),
  UNIQUE KEY `telefon_UNIQUE` (`telefon`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `korisnik`
--

LOCK TABLES `korisnik` WRITE;
/*!40000 ALTER TABLE `korisnik` DISABLE KEYS */;
INSERT INTO `korisnik` VALUES (1,'marko@gmail.com','pbkdf2_sha256$720000$EOmu3yd8YbISsrZrmFRiwy$Id0ELO3cFw2MITGJrNHFDvWGfOVr92KevyLoB7ijGz0=','Marko','Marković',123456789,'0612345678','O','1990-01-01','2024-05-31 16:10:56',1),(2,'ana@gmail.com','pbkdf2_sha256$720000$T0KLSKOigjMdj83KdEAwiG$CR4E0usgWCuQyLJZm30YJ0Hj12gN0yUqUgGBTvibXZc=','Ana','Anić',987654321,'0609876543','V','1992-05-15','2024-05-31 16:03:35',1),(3,'jovan@gmail.com','pbkdf2_sha256$720000$MnH2etfjU8B6V6E4TFRKoM$kamxUT/PepdKccys1kh+ZJtVx0Zc0bhbD0/MAkwlWJs=','Jovan','Jovanović',456123789,'0651234567','O','1985-08-20','2024-05-31 16:03:35',1),(4,'milica@gmail.com','pbkdf2_sha256$720000$YJZliUdQfB7404h7IGMX3d$QaYT77aR9b20VDVDyoyITkacNsrpmt7StI+Lr3RFNqk=','Milica','Milić',321654987,'0626543210','V','1995-12-30','2024-05-31 16:03:35',1),(21,'admin@bv.rs','pbkdf2_sha256$720000$fB91HR8EMIQCYYMDbfJEbR$J5KoRCekeUntUSPXc0zTE7fE+dWohcmOXI9sWxm3Dho=','Admin',NULL,NULL,NULL,'A',NULL,NULL,NULL);
/*!40000 ALTER TABLE `korisnik` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lokacija`
--

DROP TABLE IF EXISTS `lokacija`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lokacija` (
  `drzava` varchar(256) NOT NULL,
  `kontinent` varchar(256) NOT NULL,
  `idLok` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`idLok`),
  KEY `idx_kontinent` (`kontinent`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lokacija`
--

LOCK TABLES `lokacija` WRITE;
/*!40000 ALTER TABLE `lokacija` DISABLE KEYS */;
INSERT INTO `lokacija` VALUES ('Afghanistan','Asia',1),('Srbija','Evropa',2),('Hrvatska','Evropa',3),('Bosna i Hercegovina','Evropa',4),('Crna Gora','Evropa',5);
/*!40000 ALTER TABLE `lokacija` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oblast`
--

DROP TABLE IF EXISTS `oblast`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oblast` (
  `oblast` varchar(256) NOT NULL,
  `idObl` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`idObl`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oblast`
--

LOCK TABLES `oblast` WRITE;
/*!40000 ALTER TABLE `oblast` DISABLE KEYS */;
INSERT INTO `oblast` VALUES ('Zdravstvo',1),('Obrazovanje',2),('Sport',3),('Kultura',4),('Ekologija',5);
/*!40000 ALTER TABLE `oblast` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `poruka`
--

DROP TABLE IF EXISTS `poruka`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `poruka` (
  `idPor` int NOT NULL AUTO_INCREMENT,
  `idPre` int NOT NULL,
  `redBr` varchar(45) NOT NULL,
  `tekst` varchar(2000) NOT NULL,
  `time` timestamp NOT NULL,
  `status` char(1) NOT NULL,
  `idSender` int NOT NULL,
  PRIMARY KEY (`idPor`),
  KEY `FK_Prepiska_Poruka_idx` (`idPre`),
  CONSTRAINT `FK_Prepiska_Poruka` FOREIGN KEY (`idPre`) REFERENCES `prepiska` (`idPre`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `poruka`
--

LOCK TABLES `poruka` WRITE;
/*!40000 ALTER TABLE `poruka` DISABLE KEYS */;
INSERT INTO `poruka` VALUES (95,1,'001','Zdravo, kako si?','2024-05-31 17:38:21','S',2),(96,2,'001','Da li ćemo imati sastanak?','2024-05-31 17:38:21','S',1),(97,3,'001','Koje su sledeće aktivnosti?','2024-05-31 17:38:21','S',3);
/*!40000 ALTER TABLE `poruka` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prepiska`
--

DROP TABLE IF EXISTS `prepiska`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prepiska` (
  `idPre` int NOT NULL AUTO_INCREMENT,
  `idKor1` int NOT NULL,
  `idKor2` int NOT NULL,
  PRIMARY KEY (`idPre`),
  KEY `FK_kor1_prepiska_idx` (`idKor1`),
  KEY `FK_kor2_prepiska_idx` (`idKor2`),
  CONSTRAINT `FK_kor1_prepiska` FOREIGN KEY (`idKor1`) REFERENCES `korisnik` (`idKor`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_kor2_prepiska` FOREIGN KEY (`idKor2`) REFERENCES `korisnik` (`idKor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prepiska`
--

LOCK TABLES `prepiska` WRITE;
/*!40000 ALTER TABLE `prepiska` DISABLE KEYS */;
INSERT INTO `prepiska` VALUES (1,1,2),(2,2,3),(3,1,3);
/*!40000 ALTER TABLE `prepiska` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prijava`
--

DROP TABLE IF EXISTS `prijava`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prijava` (
  `idPri` int NOT NULL AUTO_INCREMENT,
  `idVol` int NOT NULL,
  `idAkt` int NOT NULL,
  `pismo` varchar(2000) NOT NULL,
  `rezime` mediumblob,
  `status` char(1) NOT NULL,
  `preporukaVol` char(1) DEFAULT NULL,
  `preporukaOrg` char(1) DEFAULT NULL,
  `komVol` varchar(1000) DEFAULT NULL,
  `komOrg` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`idPri`),
  KEY `FK_kor_prijava_idx` (`idVol`),
  KEY `FK_akt_prijava_idx` (`idAkt`),
  CONSTRAINT `FK_akt_prijava` FOREIGN KEY (`idAkt`) REFERENCES `aktivnost` (`idAkt`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_kor_prijava` FOREIGN KEY (`idVol`) REFERENCES `korisnik` (`idKor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prijava`
--

LOCK TABLES `prijava` WRITE;
/*!40000 ALTER TABLE `prijava` DISABLE KEYS */;
INSERT INTO `prijava` VALUES (19,2,1,'Želim da pomognem u bolnici.',NULL,'A',NULL,NULL,'Radujem se volontiranju.','Odličan kandidat.'),(20,3,2,'Volela bih da radim sa decom.',NULL,'O',NULL,NULL,'Imam iskustvo u radu sa decom.','Izuzetno posvećena.'),(21,4,3,'Veliki sam ljubitelj sporta.',NULL,'O',NULL,NULL,'Aktivan sportista.','Preporuka za rad sa decom.');
/*!40000 ALTER TABLE `prijava` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pripada`
--

DROP TABLE IF EXISTS `pripada`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pripada` (
  `idAkt` int NOT NULL,
  `idObl` int NOT NULL,
  PRIMARY KEY (`idAkt`,`idObl`),
  KEY `FK_oblast_pripada_idx` (`idObl`),
  CONSTRAINT `FK_akt_pripada` FOREIGN KEY (`idAkt`) REFERENCES `aktivnost` (`idAkt`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_oblast_pripada` FOREIGN KEY (`idObl`) REFERENCES `oblast` (`idObl`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pripada`
--

LOCK TABLES `pripada` WRITE;
/*!40000 ALTER TABLE `pripada` DISABLE KEYS */;
INSERT INTO `pripada` VALUES (1,1),(2,2),(3,3),(4,5);
/*!40000 ALTER TABLE `pripada` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vestina`
--

DROP TABLE IF EXISTS `vestina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vestina` (
  `idAkt` int NOT NULL,
  `idVes` int NOT NULL AUTO_INCREMENT,
  `opis` varchar(256) NOT NULL,
  PRIMARY KEY (`idVes`),
  KEY `FK_aktivnostBrAkt_vestina_idx` (`idAkt`),
  CONSTRAINT `FK_akt_vestina` FOREIGN KEY (`idAkt`) REFERENCES `aktivnost` (`idAkt`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vestina`
--

LOCK TABLES `vestina` WRITE;
/*!40000 ALTER TABLE `vestina` DISABLE KEYS */;
INSERT INTO `vestina` VALUES (1,68,'Rad sa pacijentima'),(2,69,'Organizacija aktivnosti'),(3,70,'Trenerske veštine'),(4,71,'Ekološka svest');
/*!40000 ALTER TABLE `vestina` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zanima_ga`
--

DROP TABLE IF EXISTS `zanima_ga`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zanima_ga` (
  `idKor` int NOT NULL,
  `idObl` int NOT NULL,
  PRIMARY KEY (`idKor`,`idObl`),
  KEY `FK_oblast_zanima_ga_idx` (`idObl`),
  CONSTRAINT `FK_korisnik_zanimga_ga` FOREIGN KEY (`idKor`) REFERENCES `korisnik` (`idKor`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_oblast_zanima_ga` FOREIGN KEY (`idObl`) REFERENCES `oblast` (`idObl`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zanima_ga`
--

LOCK TABLES `zanima_ga` WRITE;
/*!40000 ALTER TABLE `zanima_ga` DISABLE KEYS */;
INSERT INTO `zanima_ga` VALUES (1,1),(2,2),(3,3),(4,4);
/*!40000 ALTER TABLE `zanima_ga` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-31 23:49:34
