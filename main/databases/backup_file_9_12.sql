-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: dados_tcc
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `anotacoes`
--

DROP TABLE IF EXISTS `anotacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anotacoes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `placa` varchar(20) NOT NULL,
  `titulo` varchar(100) NOT NULL,
  `descricao` text NOT NULL,
  `data_anotacao` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `placa` (`placa`),
  CONSTRAINT `anotacoes_ibfk_1` FOREIGN KEY (`placa`) REFERENCES `carros` (`placa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anotacoes`
--

LOCK TABLES `anotacoes` WRITE;
/*!40000 ALTER TABLE `anotacoes` DISABLE KEYS */;
/*!40000 ALTER TABLE `anotacoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carros`
--

DROP TABLE IF EXISTS `carros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carros` (
  `chassi` varchar(50) NOT NULL,
  `modelo` varchar(50) NOT NULL,
  `ano` int NOT NULL,
  `placa` varchar(20) NOT NULL,
  `empresa_id` int NOT NULL,
  `ultima_troca_pneus` date NOT NULL,
  `ultima_troca_oleo` date NOT NULL,
  `ultima_revisao` date NOT NULL,
  `ultima_troca_vela` date NOT NULL,
  `ultima_troca_caixa_cambio` date NOT NULL,
  `ultima_troca_suspensao` date NOT NULL,
  `ultima_troca_bateria` date NOT NULL,
  `validade_bateria` date NOT NULL,
  `ultima_troca_correia_dentada` date NOT NULL,
  `proxima_revisao` date NOT NULL,
  `scanner_instalado` tinyint(1) NOT NULL,
  `data_cadastro` date DEFAULT NULL,
  PRIMARY KEY (`chassi`),
  UNIQUE KEY `placa` (`placa`),
  KEY `empresa_id` (`empresa_id`),
  CONSTRAINT `carros_ibfk_1` FOREIGN KEY (`empresa_id`) REFERENCES `empresas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carros`
--

LOCK TABLES `carros` WRITE;
/*!40000 ALTER TABLE `carros` DISABLE KEYS */;
INSERT INTO `carros` VALUES ('1HGBH41JXMN109186','Modelo A1',2020,'ABC1A23',1,'2023-01-01','2023-02-01','2023-03-01','2023-04-01','2023-05-01','2023-06-01','2023-07-01','2024-07-01','2023-08-01','2023-09-01',1,'2023-05-03'),('1HGBH41JXMN109187','Modelo A2',2021,'ABC1B23',1,'2023-01-02','2023-02-02','2023-03-02','2023-04-02','2023-05-02','2023-06-02','2023-07-02','2024-07-02','2023-08-02','2023-09-02',0,'2023-03-28'),('1HGBH41JXMN109188','Modelo A3',2022,'ABC1C23',1,'2023-01-03','2023-02-03','2023-03-03','2023-04-03','2023-05-03','2023-06-03','2023-07-03','2024-07-03','2023-08-03','2023-09-03',1,'2023-03-05'),('1HGBH41JXMN109189','Modelo A4',2023,'ABC1D23',1,'2023-01-04','2023-02-04','2023-03-04','2023-04-04','2023-05-04','2023-06-04','2023-07-04','2024-07-04','2023-08-04','2023-09-04',0,'2023-02-28'),('1HGBH41JXMN109190','Modelo A5',2020,'ABC1E23',1,'2023-01-05','2023-02-05','2023-03-05','2023-04-05','2023-05-05','2023-06-05','2023-07-05','2024-07-05','2023-08-05','2023-09-05',1,'2023-04-12'),('1HGBH41JXMN109191','Modelo A6',2021,'ABC1F23',1,'2023-01-06','2023-02-06','2023-03-06','2023-04-06','2023-05-06','2023-06-06','2023-07-06','2024-07-06','2023-08-06','2023-09-06',0,'2023-11-29'),('1HGBH41JXMN109192','Modelo A7',2022,'ABC1G23',1,'2023-01-07','2023-02-07','2023-03-07','2023-04-07','2023-05-07','2023-06-07','2023-07-07','2024-07-07','2023-08-07','2023-09-07',1,'2024-09-18'),('1HGBH41JXMN109193','Modelo A8',2023,'ABC1H23',1,'2023-01-08','2023-02-08','2023-03-08','2023-04-08','2023-05-08','2023-06-08','2023-07-08','2024-07-08','2023-08-08','2023-09-08',0,'2024-11-06'),('1HGBH41JXMN109194','Modelo A9',2020,'ABC1I23',1,'2023-01-09','2023-02-09','2023-03-09','2023-04-09','2023-05-09','2023-06-09','2023-07-09','2024-07-09','2023-08-09','2023-09-09',1,'2023-02-09'),('1HGBH41JXMN109195','Modelo A10',2021,'ABC1J23',1,'2023-01-10','2023-02-10','2023-03-10','2023-04-10','2023-05-10','2023-06-10','2023-07-10','2024-07-10','2023-08-10','2023-09-10',0,'2023-12-28'),('1HGBH41JXMN109196','Modelo D1',2020,'JKL1A24',4,'2023-01-01','2023-02-01','2023-03-01','2023-04-01','2023-05-01','2023-06-01','2023-07-01','2024-07-01','2023-08-01','2023-09-01',1,'2023-08-17'),('1HGBH41JXMN109197','Modelo D2',2021,'JKL1B24',4,'2023-01-02','2023-02-02','2023-03-02','2023-04-02','2023-05-02','2023-06-02','2023-07-02','2024-07-02','2023-08-02','2023-09-02',0,'2023-02-28'),('1HGBH41JXMN109198','Modelo D3',2022,'JKL1C24',4,'2023-01-03','2023-02-03','2023-03-03','2023-04-03','2023-05-03','2023-06-03','2023-07-03','2024-07-03','2023-08-03','2023-09-03',1,'2023-12-05'),('1HGBH41JXMN109199','Modelo D4',2023,'JKL1D24',4,'2023-01-04','2023-02-04','2023-03-04','2023-04-04','2023-05-04','2023-06-04','2023-07-04','2024-07-04','2023-08-04','2023-09-04',0,'2023-02-25'),('1HGBH41JXMN109200','Modelo D5',2020,'JKL1E24',4,'2023-01-05','2023-02-05','2023-03-05','2023-04-05','2023-05-05','2023-06-05','2023-07-05','2024-07-05','2023-08-05','2023-09-05',1,'2024-12-23'),('1HGBH41JXMN109201','Modelo D6',2021,'JKL1F24',4,'2023-01-06','2023-02-06','2023-03-06','2023-04-06','2023-05-06','2023-06-06','2023-07-06','2024-07-06','2023-08-06','2023-09-06',0,'2024-06-10'),('1HGBH41JXMN109202','Modelo D7',2022,'JKL1G24',4,'2023-01-07','2023-02-07','2023-03-07','2023-04-07','2023-05-07','2023-06-07','2023-07-07','2024-07-07','2023-08-07','2023-09-07',1,'2024-04-08'),('1HGBH41JXMN109203','Modelo D8',2023,'JKL1H24',4,'2023-01-08','2023-02-08','2023-03-08','2023-04-08','2023-05-08','2023-06-08','2023-07-08','2024-07-08','2023-08-08','2023-09-08',0,'2023-01-10'),('1HGBH41JXMN109204','Modelo D9',2020,'JKL1I24',4,'2023-01-09','2023-02-09','2023-03-09','2023-04-09','2023-05-09','2023-06-09','2023-07-09','2024-07-09','2023-08-09','2023-09-09',1,'2023-04-27'),('1HGBH41JXMN109205','Modelo D10',2021,'JKL1J24',4,'2023-01-10','2023-02-10','2023-03-10','2023-04-10','2023-05-10','2023-06-10','2023-07-10','2024-07-10','2023-08-10','2023-09-10',0,'2024-07-08'),('1HGBH41JXMN109206','Modelo E1',2020,'MNO1A24',5,'2023-01-01','2023-02-01','2023-03-01','2023-04-01','2023-05-01','2023-06-01','2023-07-01','2024-07-01','2023-08-01','2023-09-01',1,'2023-08-19'),('1HGBH41JXMN109207','Modelo E2',2021,'MNO1B24',5,'2023-01-02','2023-02-02','2023-03-02','2023-04-02','2023-05-02','2023-06-02','2023-07-02','2024-07-02','2023-08-02','2023-09-02',0,'2023-08-10'),('1HGBH41JXMN109208','Modelo E3',2022,'MNO1C24',5,'2023-01-03','2023-02-03','2023-03-03','2023-04-03','2023-05-03','2023-06-03','2023-07-03','2024-07-03','2023-08-03','2023-09-03',1,'2024-02-20'),('1HGBH41JXMN109209','Modelo E4',2023,'MNO1D24',5,'2023-01-04','2023-02-04','2023-03-04','2023-04-04','2023-05-04','2023-06-04','2023-07-04','2024-07-04','2023-08-04','2023-09-04',0,'2024-11-14'),('1HGBH41JXMN109210','Modelo E5',2020,'MNO1E24',5,'2023-01-05','2023-02-05','2023-03-05','2023-04-05','2023-05-05','2023-06-05','2023-07-05','2024-07-05','2023-08-05','2023-09-05',1,'2024-12-12'),('1HGBH41JXMN109211','Modelo E6',2021,'MNO1F24',5,'2023-01-06','2023-02-06','2023-03-06','2023-04-06','2023-05-06','2023-06-06','2023-07-06','2024-07-06','2023-08-06','2023-09-06',0,'2023-02-14'),('1HGBH41JXMN109212','Modelo E7',2022,'MNO1G24',5,'2023-01-07','2023-02-07','2023-03-07','2023-04-07','2023-05-07','2023-06-07','2023-07-07','2024-07-07','2023-08-07','2023-09-07',1,'2023-10-07'),('1HGBH41JXMN109213','Modelo E8',2023,'MNO1H24',5,'2023-01-08','2023-02-08','2023-03-08','2023-04-08','2023-05-08','2023-06-08','2023-07-08','2024-07-08','2023-08-08','2023-09-08',0,'2024-06-17'),('1HGBH41JXMN109214','Modelo E9',2020,'MNO1I24',5,'2023-01-09','2023-02-09','2023-03-09','2023-04-09','2023-05-09','2023-06-09','2023-07-09','2024-07-09','2023-08-09','2023-09-09',1,'2024-01-04'),('1HGBH41JXMN109215','Modelo E10',2021,'MNO1J24',5,'2023-01-10','2023-02-10','2023-03-10','2023-04-10','2023-05-10','2023-06-10','2023-07-10','2024-07-10','2023-08-10','2023-09-10',0,'2023-08-31'),('2HGBH41JXMN109186','Modelo B1',2020,'DEF1A23',2,'2023-01-01','2023-02-01','2023-03-01','2023-04-01','2023-05-01','2023-06-01','2023-07-01','2024-07-01','2023-08-01','2023-09-01',1,'2023-04-18'),('2HGBH41JXMN109187','Modelo B2',2021,'DEF1B23',2,'2023-01-02','2023-02-02','2023-03-02','2023-04-02','2023-05-02','2023-06-02','2023-07-02','2024-07-02','2023-08-02','2023-09-02',0,'2024-06-24'),('2HGBH41JXMN109188','Modelo B3',2022,'DEF1C23',2,'2023-01-03','2023-02-03','2023-03-03','2023-04-03','2023-05-03','2023-06-03','2023-07-03','2024-07-03','2023-08-03','2023-09-03',1,'2023-07-08'),('2HGBH41JXMN109189','Modelo B4',2023,'DEF1D23',2,'2023-01-04','2023-02-04','2023-03-04','2023-04-04','2023-05-04','2023-06-04','2023-07-04','2024-07-04','2023-08-04','2023-09-04',0,'2023-02-21'),('2HGBH41JXMN109190','Modelo B5',2020,'DEF1E23',2,'2023-01-05','2023-02-05','2023-03-05','2023-04-05','2023-05-05','2023-06-05','2023-07-05','2024-07-05','2023-08-05','2023-09-05',1,'2024-02-28'),('2HGBH41JXMN109191','Modelo B6',2021,'DEF1F23',2,'2023-01-06','2023-02-06','2023-03-06','2023-04-06','2023-05-06','2023-06-06','2023-07-06','2024-07-06','2023-08-06','2023-09-06',0,'2024-05-17'),('2HGBH41JXMN109192','Modelo B7',2022,'DEF1G23',2,'2023-01-07','2023-02-07','2023-03-07','2023-04-07','2023-05-07','2023-06-07','2023-07-07','2024-07-07','2023-08-07','2023-09-07',1,'2024-05-28'),('2HGBH41JXMN109193','Modelo B8',2023,'DEF1H23',2,'2023-01-08','2023-02-08','2023-03-08','2023-04-08','2023-05-08','2023-06-08','2023-07-08','2024-07-08','2023-08-08','2023-09-08',0,'2023-11-24'),('2HGBH41JXMN109194','Modelo B9',2020,'DEF1I23',2,'2023-01-09','2023-02-09','2023-03-09','2023-04-09','2023-05-09','2023-06-09','2023-07-09','2024-07-09','2023-08-09','2023-09-09',1,'2023-04-08'),('2HGBH41JXMN109195','Modelo B10',2021,'DEF1J23',2,'2023-01-10','2023-02-10','2023-03-10','2023-04-10','2023-05-10','2023-06-10','2023-07-10','2024-07-10','2023-08-10','2023-09-10',0,'2023-08-24'),('3HGBH41JXMN109186','Modelo C1',2020,'GHI1A23',3,'2023-01-01','2023-02-01','2023-03-01','2023-04-01','2023-05-01','2023-06-01','2023-07-01','2024-07-01','2023-08-01','2023-09-01',1,'2023-06-05'),('3HGBH41JXMN109187','Modelo C2',2021,'GHI1B23',3,'2023-01-02','2023-02-02','2023-03-02','2023-04-02','2023-05-02','2023-06-02','2023-07-02','2024-07-02','2023-08-02','2023-09-02',0,'2023-03-13'),('3HGBH41JXMN109188','Modelo C3',2022,'GHI1C23',3,'2023-01-03','2023-02-03','2023-03-03','2023-04-03','2023-05-03','2023-06-03','2023-07-03','2024-07-03','2023-08-03','2023-09-03',1,'2024-09-12'),('3HGBH41JXMN109189','Modelo C4',2023,'GHI1D23',3,'2023-01-04','2023-02-04','2023-03-04','2023-04-04','2023-05-04','2023-06-04','2023-07-04','2024-07-04','2023-08-04','2023-09-04',0,'2024-11-28'),('3HGBH41JXMN109190','Modelo C5',2020,'GHI1E23',3,'2023-01-05','2023-02-05','2023-03-05','2023-04-05','2023-05-05','2023-06-05','2023-07-05','2024-07-05','2023-08-05','2023-09-05',1,'2023-06-16'),('3HGBH41JXMN109191','Modelo C6',2021,'GHI1F23',3,'2023-01-06','2023-02-06','2023-03-06','2023-04-06','2023-05-06','2023-06-06','2023-07-06','2024-07-06','2023-08-06','2023-09-06',0,'2023-07-17'),('3HGBH41JXMN109192','Modelo C7',2022,'GHI1G23',3,'2023-01-07','2023-02-07','2023-03-07','2023-04-07','2023-05-07','2023-06-07','2023-07-07','2024-07-07','2023-08-07','2023-09-07',1,'2024-05-05'),('3HGBH41JXMN109193','Modelo C8',2023,'GHI1H23',3,'2023-01-08','2023-02-08','2023-03-08','2023-04-08','2023-05-08','2023-06-08','2023-07-08','2024-07-08','2023-08-08','2023-09-08',0,'2024-02-06'),('3HGBH41JXMN109194','Modelo C9',2020,'GHI1I23',3,'2023-01-09','2023-02-09','2023-03-09','2023-04-09','2023-05-09','2023-06-09','2023-07-09','2024-07-09','2023-08-09','2023-09-09',1,'2024-06-17'),('3HGBH41JXMN109195','Modelo C10',2021,'GHI1J23',3,'2023-01-10','2023-02-10','2023-03-10','2023-04-10','2023-05-10','2023-06-10','2023-07-10','2024-07-10','2023-08-10','2023-09-10',0,'2023-01-04');
/*!40000 ALTER TABLE `carros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `credenciais`
--

DROP TABLE IF EXISTS `credenciais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `credenciais` (
  `idcredenciais` varchar(36) NOT NULL,
  `username` varchar(50) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `sobrenome` varchar(50) NOT NULL,
  `data_nasc` date NOT NULL,
  `funcao` varchar(50) NOT NULL,
  `empresa_id` int DEFAULT NULL,
  `is_admin` tinyint(1) NOT NULL,
  PRIMARY KEY (`idcredenciais`),
  UNIQUE KEY `username` (`username`),
  KEY `empresa_id` (`empresa_id`),
  CONSTRAINT `credenciais_ibfk_1` FOREIGN KEY (`empresa_id`) REFERENCES `empresas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credenciais`
--

LOCK TABLES `credenciais` WRITE;
/*!40000 ALTER TABLE `credenciais` DISABLE KEYS */;
INSERT INTO `credenciais` VALUES ('8a3d03e6-39ca-4216-aa8d-a7bb489db8aa','empresa','scrypt:32768:8:1$TFMFo3BRaaqM3AJo$b7864092999fdfbed31c0e7b8249316e66d7a84979504aefa2e8e2dd0bd324c23d6cbd303e6cd6b2eac4ebf591fe5be313fe70f6fe9595db7024e7862a190f70','empresa','empresa','2000-12-06','Empresa',1,0),('b2dad3bb-efa0-4870-8567-4cbf08afe45b','admin','scrypt:32768:8:1$5y6R8GWqB89QltKk$4fbdd7da2dca7b1930c2c71636a53b6c034f8c19d424b764b79860b2c7ad1304eb980eef484bf2485426ade26104cab2e8480f9f5dd65ebe2b2dfae7939044cc','admin','admin','1998-11-19','Administrador',NULL,1);
/*!40000 ALTER TABLE `credenciais` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empresas`
--

DROP TABLE IF EXISTS `empresas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empresas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `responsavel` varchar(100) NOT NULL,
  `estado` varchar(2) NOT NULL,
  `cnpj` varchar(18) NOT NULL,
  `telefone` varchar(15) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empresas`
--

LOCK TABLES `empresas` WRITE;
/*!40000 ALTER TABLE `empresas` DISABLE KEYS */;
INSERT INTO `empresas` VALUES (1,'Empresa A','Responsável A','SP','00.000.000/0001-01','(11) 1111-1111'),(2,'Empresa B','Responsável B','RJ','00.000.000/0001-02','(21) 2222-2222'),(3,'Empresa C','Responsável C','MG','00.000.000/0001-03','(31) 3333-3333'),(4,'Empresa D','Responsável D','RS','00.000.000/0001-04','(51) 4444-4444'),(5,'Empresa E','Responsável E','BA','00.000.000/0001-05','(71) 5555-5555'),(6,'EMPRESA USJ','GABRIEL LOPES','RJ','00.000.000/0001-25','21964808618');
/*!40000 ALTER TABLE `empresas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solicitacoes_modificacao`
--

DROP TABLE IF EXISTS `solicitacoes_modificacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solicitacoes_modificacao` (
  `id` int NOT NULL AUTO_INCREMENT,
  `chassi` varchar(50) NOT NULL,
  `campo` varchar(50) NOT NULL,
  `novo_valor` varchar(255) NOT NULL,
  `data_solicitacao` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chassi` (`chassi`),
  CONSTRAINT `solicitacoes_modificacao_ibfk_1` FOREIGN KEY (`chassi`) REFERENCES `carros` (`chassi`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitacoes_modificacao`
--

LOCK TABLES `solicitacoes_modificacao` WRITE;
/*!40000 ALTER TABLE `solicitacoes_modificacao` DISABLE KEYS */;
/*!40000 ALTER TABLE `solicitacoes_modificacao` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-09  8:24:15
