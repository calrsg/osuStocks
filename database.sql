CREATE DATABASE `osustocks` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

CREATE TABLE `users` (
  `userID` bigint NOT NULL,
  `balance` int NOT NULL,
  PRIMARY KEY (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `players` (
  `playerID` int NOT NULL,
  `player_name` varchar(45) NOT NULL,
  `country` varchar(45) NOT NULL,
  `rank` int NOT NULL,
  `rank_country` int NOT NULL,
  `pp` int NOT NULL,
  `accuracy` float NOT NULL,
  `val` double NOT NULL,
  PRIMARY KEY (`playerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `holdings` (
  `holdingID` int NOT NULL AUTO_INCREMENT,
  `userID` bigint DEFAULT NULL,
  `stockID` int DEFAULT NULL,
  `amount` int DEFAULT NULL,
  PRIMARY KEY (`holdingID`),
  UNIQUE KEY `holdingID_UNIQUE` (`holdingID`),
  KEY `userID_idx` (`userID`),
  KEY `stockID_idx` (`stockID`),
  CONSTRAINT `stockID` FOREIGN KEY (`stockID`) REFERENCES `players` (`playerID`),
  CONSTRAINT `userID` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
