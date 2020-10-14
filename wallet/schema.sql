DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS wallet;
DROP TABLE IF EXISTS 'transaction';

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

CREATE TABLE 'transaction' (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    value REAL NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES user (id),
    FOREIGN KEY (receiver_id) REFERENCES user (id)
);


INSERT INTO user (username, password) VALUES
    ('john', 'pbkdf2:sha256:150000$KFsR0SZJ$74d6b151f4a350fd32a6d524d76b17b18115a412e648419912c10f32b1b78b2b'),
    ('sophie', 'pbkdf2:sha256:150000$c731omsC$2ea84b1fcf3b54a8a526d6060696996d6592b801eac40cd1a73d2403cc1d5f0b');

INSERT INTO wallet (user_id, value) VALUES
    (1, 100.0),
    (2, 50.0);

INSERT INTO 'transaction' (sender_id, receiver_id, created, value) VALUES
    (1, 2, DateTime('now'), 50.0);
