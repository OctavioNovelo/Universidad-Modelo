SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `characters`;

CREATE TABLE `characters` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(250) DEFAULT NULL,
  `race` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `characters` WRITE;

INSERT INTO `characters` (`id`, `name`, `race`)
VALUES
	(1,'Frodo Baggins','Hobbit'),
	(2,'Gandalf the Grey','Mago'),
	(3,'Aragorn','Hombre'),
	(4,'Legolas','Elfo'),
	(5,'Gimli','Enano'),
	(6,'Galadriel','Elfo'),
	(7,'Sauron','Malo malote'),
	(8,'Samwise Gamgee','Hobbit');

UNLOCK TABLES;
