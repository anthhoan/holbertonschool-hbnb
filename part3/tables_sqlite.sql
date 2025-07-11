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
    id TEXT PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT 0
);

-- Create places table
CREATE TABLE places (
    id TEXT PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    owner_id TEXT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- Create reviews table
CREATE TABLE reviews (
    id TEXT PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    text TEXT NOT NULL,
    rating INTEGER NOT NULL,
    place_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create amenities table
CREATE TABLE amenities (
    id TEXT PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL
);

-- Create place_amenity junction table
CREATE TABLE place_amenity (
    place_id TEXT NOT NULL,
    amenity_id TEXT NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);

-- Create indexes for better performance
CREATE INDEX idx_places_owner_id ON places(owner_id);
CREATE INDEX idx_reviews_place_id ON reviews(place_id);
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_place_amenity_amenity_id ON place_amenity(amenity_id);
