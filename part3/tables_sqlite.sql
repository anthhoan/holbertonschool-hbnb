-- SQLite Database Schema for HBnB Application
-- Note: SQLite doesn't support CREATE DATABASE, databases are files

-- Enable foreign key constraints (important for SQLite)
PRAGMA foreign_keys = ON;

-- Drop tables in reverse order to avoid foreign key constraint issues
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Create places table
CREATE TABLE places (
    id CHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create reviews table
CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    place_id CHAR(36) NOT NULL,
    user_id CHAR(36) NOT NULL,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, place_id)
);

-- Create amenities table
CREATE TABLE amenities (
    id CHAR(36) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Create place_amenity junction table
CREATE TABLE place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_places_owner_id ON places(owner_id);
CREATE INDEX idx_reviews_place_id ON reviews(place_id);
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_place_amenity_amenity_id ON place_amenity(amenity_id);

-- ========================================
-- INITIAL DATA INSERTION
-- ========================================

-- Insert Administrator User
-- Password: admin1234 (hashed using bcrypt)
INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin,
    created_at,
    updated_at
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$CmBltn4A3L4gzUbAGT21S.pfX0KtkktvgQKnKNvMfQ/9TQsre8WAK',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert Initial Amenities
INSERT INTO amenities (id, name, created_at, updated_at) VALUES
    ('b9b8259e-58a0-422c-9fd8-1fa1b60e737c', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('34461184-a42f-4bd0-8efb-2111cc1d8349', 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('c28fcc71-dfa1-41c8-81a2-f2cd4dff3d02', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- ========================================
-- SAMPLE CRUD OPERATIONS FOR TESTING
-- ========================================

-- Test SELECT operations
-- Verify admin user creation
SELECT id, first_name, last_name, email, is_admin FROM users WHERE is_admin = TRUE;

-- Verify amenities insertion
SELECT id, name FROM amenities ORDER BY name;

-- Test INSERT operations
-- Example: Insert a regular user
-- INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES
--     ('test-user-uuid', 'John', 'Doe', 'john.doe@example.com', 'hashed_password', FALSE);

-- Example: Insert a place
-- INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
--     ('test-place-uuid', 'Cozy Apartment', 'A nice place to stay', 100.00, 37.7749, -122.4194, 'test-user-uuid');

-- Example: Insert a review (with rating constraint test)
-- INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES
--     ('test-review-uuid', 'Great place!', 5, 'test-user-uuid', 'test-place-uuid');

-- Test UPDATE operations
-- Example: Update user information
-- UPDATE users SET first_name = 'Jane', updated_at = CURRENT_TIMESTAMP WHERE id = 'test-user-uuid';

-- Test DELETE operations
-- Example: Delete a review
-- DELETE FROM reviews WHERE id = 'test-review-uuid';

-- Test constraint violations
-- Example: Try to insert duplicate email (should fail)
-- INSERT INTO users (id, first_name, last_name, email, password) VALUES
--     ('another-uuid', 'Test', 'User', 'admin@hbnb.io', 'password');

-- Example: Try to insert invalid rating (should fail)
-- INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES
--     ('bad-review-uuid', 'Bad rating test', 6, 'test-user-uuid', 'test-place-uuid');

-- Example: Try to insert duplicate review from same user for same place (should fail)
-- INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES
--     ('duplicate-review-uuid', 'Another review', 4, 'test-user-uuid', 'test-place-uuid');
