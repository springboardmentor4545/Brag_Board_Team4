-- =========================================
-- psql -U postgres -d project_db -f db_setup.sql
-- 🗃️ DATABASE: project_db (for BragBoard FastAPI)
-- PostgreSQL Schema + Dummy Data
-- =========================================

-- Drop existing tables (in correct order for dependencies)
DROP TABLE IF EXISTS reports, reactions, comments, items, users CASCADE;

-- =========================================
-- 📦 TABLE CREATION SECTION
-- =========================================

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    item_id INT NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    owner_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE reactions (
    id SERIAL PRIMARY KEY,
    reaction_type VARCHAR(50) NOT NULL, -- e.g., 'like', 'clap', 'star'
    item_id INT NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    owner_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    reason TEXT NOT NULL,
    item_id INT REFERENCES items(id) ON DELETE CASCADE,
    comment_id INT REFERENCES comments(id) ON DELETE CASCADE,
    reporter_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =========================================
-- 📈 INDEX CREATION SECTION
-- =========================================

CREATE INDEX ON items (owner_id);
CREATE INDEX ON comments (item_id);
CREATE INDEX ON comments (owner_id);
CREATE INDEX ON reactions (item_id);
CREATE INDEX ON reactions (owner_id);
CREATE INDEX ON reports (item_id);
CREATE INDEX ON reports (comment_id);
CREATE INDEX ON reports (reporter_id);

-- =========================================
-- 🧩 DUMMY DATA SECTION
-- =========================================

-- 👥 Users
-- Passwords are 'password123' hashed with bcrypt. 
-- You can log in with these users via the API.
INSERT INTO users (email, hashed_password, is_admin) VALUES
('alice@company.com', '$2b$12$DRW.g45N0iA4bO/3O5C7a.8sD5Y.xJt2/Wk5/Y5/F/Y5/F/Y5/F.Y', FALSE),
('bob@company.com', '$2b$12$DRW.g45N0iA4bO/3O5C7a.8sD5Y.xJt2/Wk5/Y5/F/Y5/F/Y5/F.Y', FALSE),
('carol@company.com', '$2b$12$DRW.g45N0iA4bO/3O5C7a.8sD5Y.xJt2/Wk5/Y5/F/Y5/F/Y5/F.Y', FALSE),
('admin@company.com', '$2b$12$DRW.g45N0iA4bO/3O5C7a.8sD5Y.xJt2/Wk5/Y5/F/Y5/F/Y5/F.Y', TRUE);

-- 🏆 Items (formerly ShoutOuts)
INSERT INTO items (title, description, owner_id) VALUES
('Kudos to Bob!', 'He fixed the production bug in record time!', 1),
('Creative Campaign Idea', 'Appreciation for Carol''s latest marketing campaign concept.', 2),
('Deployment Hero', 'David was a huge help with the latest deployment.', 3);

-- 💖 Reactions
INSERT INTO reactions (item_id, owner_id, reaction_type) VALUES
(1, 2, 'clap'),
(1, 3, 'like'),
(2, 1, 'star'),
(3, 2, 'clap');

-- 💭 Comments
INSERT INTO comments (item_id, owner_id, content) VALUES
(1, 3, 'Well deserved, Bob!'),
(2, 1, 'Great teamwork everyone!'),
(3, 3, 'Happy to contribute!');

-- 🚩 Reports
INSERT INTO reports (item_id, reporter_id, reason) VALUES
(2, 4, 'This seems like a duplicate of another item.');

-- =========================================
-- 🔍 TEST QUERIES
-- =========================================

-- 1️⃣ All items with their owner
SELECT i.id AS item_id, i.title, i.description, u.email AS owner_email, i.created_at
FROM items i
JOIN users u ON i.owner_id = u.id
ORDER BY i.created_at DESC;

-- 2️⃣ All comments for a specific item (e.g., item_id = 1)
SELECT c.id, c.content, u.email AS author
FROM comments c
JOIN users u ON c.owner_id = u.id
WHERE c.item_id = 1
ORDER BY c.created_at ASC;
