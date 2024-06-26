-- Database: Final

-- DROP DATABASE IF EXISTS "Final";

CREATE DATABASE "Final"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_Canada.1252'
    LC_CTYPE = 'English_Canada.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- Table creation for 'Employee'
CREATE TABLE employee (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

-- Table creation for 'Admin'
CREATE TABLE admin (
    admin_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- Table creation for 'Trainer'
CREATE TABLE trainer (
    trainer_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- Table creation for 'Available TIme'
CREATE TABLE available_time (
    available_time_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    trainer_id INT NOT NULL,
    FOREIGN KEY (trainer_id) REFERENCES trainer(trainer_id)
);

-- Table creation for 'Subscription'
CREATE TABLE subscription (
    subscription_id SERIAL PRIMARY KEY,
    tier_name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL
);

-- Table creation for 'Member' with foreign key to 'Subscription'
CREATE TABLE member (
    member_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    subscription_id INT NOT NULL, -- Assuming the foreign key field is named 'subscription_id'
    FOREIGN KEY (subscription_id) REFERENCES subscription(subscription_id)
);

CREATE TABLE exercise_routine (
    exercise_routine_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    description TEXT,
    FOREIGN KEY (member_id) REFERENCES member(member_id)
);

CREATE TABLE goal (
    goal_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    description TEXT,
    date_completed DATE,
    FOREIGN KEY (member_id) REFERENCES member(member_id)
);

-- Table creation for 'Class'
CREATE TABLE class (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(255) NOT NULL,
    start_time TIME,
    end_time TIME,
    date DATE,
    purpose TEXT,
    description TEXT,
    trainer_id INT NOT NULL,
    max_attendance INT, 
    current_num_attendees INT, 
    FOREIGN KEY (trainer_id) REFERENCES trainer(trainer_id)
);
CREATE TABLE takes (
    member_id INT NOT NULL,
    class_id INT NOT NULL,
    PRIMARY KEY (member_id, class_id),
    FOREIGN KEY (member_id) REFERENCES member(member_id),
    FOREIGN KEY (class_id) REFERENCES class(class_id)
);

-- Table creation for 'Room'
CREATE TABLE room (
    room_id SERIAL PRIMARY KEY,
    room_number INT UNIQUE NOT NULL,
    name TEXT UNIQUE,
    description TEXT
);

-- Table creation for 'Booking'
CREATE TABLE booking (
    booking_id SERIAL PRIMARY KEY,
    class_id INT NOT NULL,
    room_id INT NOT NULL,
    FOREIGN KEY (class_id) REFERENCES class(class_id),
    FOREIGN KEY (room_id) REFERENCES room(room_id)
);

-- Table creation for 'Equipment'
CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    room_id INT NOT NULL,
    description TEXT,
    last_serviced DATE NOT NULL,
    FOREIGN KEY (room_id) REFERENCES room(room_id)
);

CREATE TABLE metrics (
    metrics_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    weight INT NOT NULL,
    height INT NOT NULL,
    age INT NOT NULL,
    FOREIGN KEY (member_id) REFERENCES member(member_id)
);

CREATE TABLE billing (
    billing_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    date_billed DATE NOT NULL,
    payed BOOLEAN NOT NULL,
    FOREIGN KEY (member_id) REFERENCES member(member_id)
);

-- Indexes for Employee Table
CREATE INDEX idx_employee_name ON employee (name);

-- Indexes for Trainer Table
CREATE INDEX idx_trainer_employee_id ON trainer (employee_id);

-- Indexes for Admin Table
CREATE INDEX idx_admin_employee_id ON admin (employee_id);

-- Indexes for Available Time Table
CREATE INDEX idx_available_time_trainer_id ON available_time (trainer_id);
CREATE INDEX idx_available_time_date ON available_time (date);

-- Indexes for Member Table
CREATE INDEX idx_member_subscription_id ON member (subscription_id);

-- Indexes for Subscription Table
CREATE INDEX idx_subscription_tier_name ON subscription (tier_name);

-- Indexes for Class Table
CREATE INDEX idx_class_trainer_id ON class (trainer_id);
CREATE INDEX idx_class_date ON class (date);

-- Indexes for Booking Table
CREATE INDEX idx_booking_class_id ON booking (class_id);
CREATE INDEX idx_booking_room_id ON booking (room_id);

-- Indexes for Equipment Table
CREATE INDEX idx_equipment_room_id ON equipment (room_id);

-- Indexes for Metrics Table
CREATE INDEX idx_metrics_member_id ON metrics (member_id);

-- Indexes for Billing Table
CREATE INDEX idx_billing_member_id ON billing (member_id);
CREATE INDEX idx_billing_date_billed ON billing (date_billed);
