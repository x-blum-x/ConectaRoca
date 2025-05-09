CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    tel TEXT,
    cpf TEXT,
    sexo TEXT,
    idade INTEGER,
    cidade TEXT,
    estado TEXT,
    localidade TEXT,
    last_modified DATETIME,
    last_modifier INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT CHECK(type IN ('income', 'expense')) NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS cropplans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    crop_type TEXT,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cropplan_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    status TEXT CHECK(status IN ('pending', 'done')) DEFAULT 'pending',
    date DATE,
    FOREIGN KEY(cropplan_id) REFERENCES cropplans(id)
);

CREATE TABLE IF NOT EXISTS inventory_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    unit TEXT NOT NULL,
    category TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS inventory_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    type TEXT CHECK(type IN ('entrada', 'saida')) NOT NULL,
    quantity REAL NOT NULL,
    date DATE NOT NULL,
    unit_weight REAL,
    total_weight REAL,
    unit_price REAL,
    total_value REAL,
    responsible TEXT,
    location TEXT,
    note TEXT,
    FOREIGN KEY(item_id) REFERENCES inventory_items(id)
);