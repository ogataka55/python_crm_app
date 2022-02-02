CREATE TABLE IF NOT EXISTS users (
-- UNIQUE(ユニーク制約)…他の行の値と重複をNG
    name TEXT UNIQUE,
    age INTEGER
);