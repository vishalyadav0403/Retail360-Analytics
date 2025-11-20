-- connect as root
CREATE DATABASE IF NOT EXISTS retail360;
CREATE USER IF NOT EXISTS 'retail_user'@'%' IDENTIFIED BY 'retail_pass';
GRANT ALL PRIVILEGES ON retail360.* TO 'retail_user'@'%';
FLUSH PRIVILEGES;
