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
CREATE TABLE `deploymanager`.`deployments` (
  `id` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NULL,
  `description` TEXT NULL,
  `deploymentscol` VARCHAR(45) NULL,
  `state` VARCHAR(45) NULL,
  `provider_id` VARCHAR(45) NULL,
  `deploymentscol1` VARCHAR(45) NULL,
  `created_by` VARCHAR(15) NULL,
  `created_date` TIMESTAMP NULL,
  PRIMARY KEY (`id`),
  INDEX `deployment_provider_fk_idx` (`provider_id` ASC) VISIBLE,
  CONSTRAINT `deployment_provider_fk`
    FOREIGN KEY (`provider_id`)
    REFERENCES `deploymanager`.`providers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);