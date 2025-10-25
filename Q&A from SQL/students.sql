CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT CHECK(gender IN ('Male','Female')),
    department TEXT,
    gpa REAL
);

INSERT INTO students (name, age, gender, department, gpa) VALUES
('Tanvir Mahamud', 21, 'Male', 'CSE', 3.90),
('Sadia Rahman', 22, 'Female', 'EEE', 3.75),
('Rafiul Islam', 20, 'Male', 'CSE', 3.60),
('Mim Chowdhury', 23, 'Female', 'BBA', 3.88),
('Hasan Karim', 24, 'Male', 'CSE', 3.20),
('Nusrat Jahan', 21, 'Female', 'ECE', 3.70),
('Rafsan Ahmed', 20, 'Male', 'BBA', 3.50),
('Tania Akter', 22, 'Female', 'CSE', 3.85),
('Mehedi Hasan', 23, 'Male', 'EEE', 3.45),
('Sumaiya Islam', 21, 'Female', 'BBA', 3.78),
('Arif Hossain', 24, 'Male', 'CSE', 3.66),
('Sabrina Sultana', 22, 'Female', 'ECE', 3.80),
('Rizwan Rahman', 23, 'Male', 'BBA', 3.59),
('Farhana Akter', 21, 'Female', 'EEE', 3.40),
('Saif Uddin', 22, 'Male', 'CSE', 3.85),
('Tamanna Rahim', 20, 'Female', 'CSE', 3.76),
('Arafat Hossain', 24, 'Male', 'ECE', 3.68),
('Samiha Noor', 23, 'Female', 'BBA', 3.55),
('Fahim Ahamed', 22, 'Male', 'CSE', 3.92),
('Labiba Chowdhury', 21, 'Female', 'EEE', 3.83);
