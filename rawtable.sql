CREATE TABLE City (
    name VARCHAR(150) NOT NULL PRIMARY KEY,
    region VARCHAR(150) NOT NULL
);

CREATE TABLE Address (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(250) NOT NULL,
    complemento VARCHAR(250),
    neighborhood VARCHAR(50),
    city_id VARCHAR(150) NOT NULL,
    FOREIGN KEY (city_id) REFERENCES City(name) ON DELETE CASCADE
);

CREATE TABLE Institute (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    address_id INT NOT NULL,
    FOREIGN KEY (address_id) REFERENCES Address(id) ON DELETE CASCADE
);

CREATE TABLE PreviousSchool (
    name VARCHAR(250) PRIMARY KEY,
    completion_date DATE NOT NULL,
    type VARCHAR(10) NOT NULL,
    address_id INT NOT NULL,
    FOREIGN KEY (address_id) REFERENCES Address(id) ON DELETE CASCADE
);

CREATE TABLE Course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    shifit VARCHAR(10) NOT NULL,
    type VARCHAR(32) NOT NULL,
    time_required INT NOT NULL,
    institute_id INT NOT NULL,
    FOREIGN KEY (institute_id) REFERENCES Institute(id) ON DELETE CASCADE
);

CREATE TABLE CustomUser (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    last_name VARCHAR(150),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150),
    social_name VARCHAR(150),
    mother_name VARCHAR(150) NOT NULL,
    father_name VARCHAR(150),
    birth_date DATE,
    sex VARCHAR(6),
    gender VARCHAR(30),
    disability VARCHAR(50),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE StudentCourse (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    shifit VARCHAR(79) NOT NULL,
    institute_id INT NOT NULL,
    ingressed_semester VARCHAR(10) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (institute_id) REFERENCES Institute(id) ON DELETE CASCADE
);

CREATE TABLE Status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    shifit VARCHAR(11) NOT NULL,
    current_semester VARCHAR(10) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    institute_id INT NOT NULL,
    FOREIGN KEY (institute_id) REFERENCES Institute(id) ON DELETE CASCADE
);
