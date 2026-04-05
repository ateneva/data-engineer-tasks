CREATE TABLE IF NOT EXISTS store (
  store_id                              TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  manager_staff_id                      TINYINT UNSIGNED NOT NULL,
  address_id                            SMALLINT UNSIGNED NOT NULL,
  last_update                           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY                           (store_id),
  UNIQUE KEY idx_unique_manager         (manager_staff_id),
  KEY idx_fk_address_id                 (address_id),

  CONSTRAINT fk_store_address FOREIGN KEY (address_id)
    REFERENCES address (address_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO store VALUES (1,1,1,'2006-02-15 04:57:12'),
(2,2,2,'2006-02-15 04:57:12');
COMMIT;
