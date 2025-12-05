-- 1. Table Creations (DDL)

CREATE TABLE Roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id) ON DELETE RESTRICT
);

CREATE TABLE Categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE MenuItems (
    item_id SERIAL PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category_id INT NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE CASCADE
);

CREATE TABLE RestaurantTables (
    table_id SERIAL PRIMARY KEY,
    table_number VARCHAR(10) UNIQUE NOT NULL,
    seat_capacity INT DEFAULT 4
);

CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    table_id INT NOT NULL,
    user_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Pending',
    total_amount DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (table_id) REFERENCES RestaurantTables(table_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE OrderDetails (
    detail_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT DEFAULT 1,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES MenuItems(item_id)
);

-- 2. Initial Data Insertion (DML)

INSERT INTO Roles (role_name, description) VALUES 
('Admin', 'System Administrator'),
('Waiter', 'Staff serving tables'),
('Kitchen', 'Kitchen Staff');

INSERT INTO Users (username, password, full_name, role_id) VALUES 
('admin_user', 'admin123', 'John Doe', 1),
('waiter_jane', 'waiter123', 'Jane Smith', 2),
('chef_mike', 'chef123', 'Mike Ross', 3);

INSERT INTO Categories (category_name) VALUES 
('Main Course'), 
('Beverages'), 
('Desserts');

INSERT INTO MenuItems (item_name, description, price, category_id) VALUES 
('Cheeseburger', 'Beef burger with cheddar cheese', 12.50, 1),
('Grilled Chicken Salad', 'Fresh salad with grilled chicken breast', 10.00, 1),
('Cola', 'Chilled sparkling soft drink', 2.50, 2),
('Orange Juice', 'Freshly squeezed orange juice', 3.00, 2),
('Chocolate Lava Cake', 'Warm cake with molten chocolate center', 6.50, 3);

INSERT INTO RestaurantTables (table_number, seat_capacity) VALUES 
('T-01', 4), 
('T-02', 2), 
('T-03', 6),
('T-04', 4);
