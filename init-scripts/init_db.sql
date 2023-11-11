
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
