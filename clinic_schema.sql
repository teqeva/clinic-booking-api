CREATE DATABASE IF NOT EXISTS clinic_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE clinic_db;

CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('admin','provider','reception') NOT NULL DEFAULT 'reception',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE patients (
  patient_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  dob DATE,
  gender ENUM('male','female','other') DEFAULT 'female',
  phone VARCHAR(20) UNIQUE,
  email VARCHAR(150) UNIQUE,
  address TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE providers (
  provider_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  specialty VARCHAR(100),
  phone VARCHAR(20),
  email VARCHAR(150) UNIQUE,
  license_no VARCHAR(50) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE services (
  service_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  description TEXT,
  duration_minutes INT NOT NULL,
  price DECIMAL(10,2) DEFAULT 0.00,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE provider_services (
  provider_id INT NOT NULL,
  service_id INT NOT NULL,
  PRIMARY KEY (provider_id, service_id),
  FOREIGN KEY (provider_id) REFERENCES providers(provider_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE appointments (
  appointment_id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id INT NOT NULL,
  provider_id INT NOT NULL,
  service_id INT NOT NULL,
  room VARCHAR(50),
  start_datetime DATETIME NOT NULL,
  end_datetime DATETIME NOT NULL,
  status ENUM('scheduled','completed','cancelled') NOT NULL DEFAULT 'scheduled',
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (provider_id) REFERENCES providers(provider_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT chk_end_after_start CHECK (end_datetime > start_datetime)
) ENGINE=InnoDB;

CREATE UNIQUE INDEX uniq_provider_start ON appointments(provider_id, start_datetime);

CREATE TABLE payments (
  payment_id INT AUTO_INCREMENT PRIMARY KEY,
  appointment_id INT NOT NULL UNIQUE,
  amount DECIMAL(10,2) NOT NULL,
  method ENUM('cash','card','mpesa','insurance') DEFAULT 'cash',
  paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;
