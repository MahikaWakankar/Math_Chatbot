CREATE DATABASE math_chatbot;
USE math_chatbot;

-- User Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL,
    username VARCHAR(80) NOT NULL,
    password VARCHAR(120) NOT NULL,  -- Storing passwords in plaintext
    age INT,
    gender VARCHAR(10),
    UNIQUE(email),
    UNIQUE(username)
);

-- Chat History Table
CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Add this line
    FOREIGN KEY(user_id) REFERENCES users(id)
);