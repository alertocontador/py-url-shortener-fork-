-- Add your database schema and indexes here
-- URL shortener database schema

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS url_shortener;
USE url_shortener;

-- URLs table to store original URLs and their short keys
CREATE TABLE IF NOT EXISTS urls (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    short_key VARCHAR(255) NOT NULL UNIQUE,
    original_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_short_key (short_key),
    INDEX idx_created_at (created_at)
);
