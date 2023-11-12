-- Create the 'books' table
CREATE TABLE IF NOT EXISTS books (
                                     id SERIAL PRIMARY KEY,
                                     title VARCHAR(128) NOT NULL,
    author VARCHAR(128) NOT NULL,
    year_published INT,
    isbn VARCHAR(13) NOT NULL UNIQUE
    );

-- Insert some initial data into the 'books' table
INSERT INTO books (title, author, year_published, isbn) VALUES
                                                            ('To Kill a Mockingbird', 'Harper Lee', 1960, '9780061120084'),
                                                            ('1984', 'George Orwell', 1949, '9780451524935'),
                                                            ('The Great Gatsby', 'F. Scott Fitzgerald', 1925, '9780743273565');

-- Create the 'users' table
CREATE TABLE IF NOT EXISTS users (
                                     id SERIAL PRIMARY KEY,
                                     username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
    );

-- Create the 'token_blacklist' table
CREATE TABLE IF NOT EXISTS token_blacklist (
                                               id SERIAL PRIMARY KEY,
                                               token VARCHAR(500) UNIQUE NOT NULL,
    blacklisted_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

-- Insert an admin user
-- Note: admin pwd is 'admin@123'
INSERT INTO users (username, password, is_admin) VALUES
    ('admin', 'sha256$AcEb5wUCNoECYvIw$a7a47222758fb19b009e5e9add18ac8a94029fadedf88e1cf59d15ba730ecc57', TRUE);
