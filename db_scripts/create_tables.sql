CREATE TABLE `providers` (
  `id` varchar(45) NOT NULL,
  `code` varchar(15) DEFAULT NULL,
  `icon` varchar(15) DEFAULT NULL,
  `name` varchar(25) DEFAULT NULL,
  `description` text,
  `created_by` varchar(45) DEFAULT NULL,
  `created_date` varchar(45) DEFAULT NULL,
  `enable` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `deployments` (
  `id` varchar(45) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `description` text,
  `state` varchar(45) DEFAULT NULL,
  `provider_id` varchar(45) DEFAULT NULL,
  `created_by` varchar(15) DEFAULT NULL,
  `created_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `deployment_provider_fk_idx` (`provider_id`),
  CONSTRAINT `deployment_provider_fk` FOREIGN KEY (`provider_id`) REFERENCES `providers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;