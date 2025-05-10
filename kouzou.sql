CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    role VARCHAR(32)
);



CREATE TABLE chat_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    user_input TEXT,
    gpt_response TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



INSERT INTO users (username, password, role)
VALUES ('taku', '2933', 'user');



