DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS wallet;
DROP TABLE IF EXISTS transaction;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE wallet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    value REAL NOT NULL DEFAULT 0.0,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE transaction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    value REAL NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES user (id),
    FOREIGN KEY (receiver_id) REFERENCES user (id)
);


