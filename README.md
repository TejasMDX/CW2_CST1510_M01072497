# Project for the module CST1510

Student Name: Tejasvin Jeddedu
Student ID: M01072497
Course: CST1510 -CW2 - Multi-Domain Intelligence Platform

# Week 7: Secure Authentication System

## Project Description
A command-line authentication system implementing secure password hashing
This system allows users to register accounts and log in with proper password

## Features
- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence

## Technical Implementation
- Hashing Algorithm: bcrypt with automatic salting
- Data Storage: Plain text file (`users.txt`) with comma-separated values
- Password Security: One-way hashing, no plaintext storage
- Validation: Username (3-20 alphanumeric characters), Password (6-50 characters)

# Week 8: Data Pipeline & CRUD (SQL)

## Project Description
Created database tables for all three domains and implemented full CRUD (Create, Read, Update, Delete) operations

## Features
- Creating the .db database file
- Verifying that CSV files and user.txt data are correctly loaded into the database
- Testing the proper setup and integrity of the database
- Validating the functionality of CRUD operations (Create, Read, Update, Delete)

## Technical Implementation
- Creating database tables for the three domains and the user login system
- Writing SQL queries to implement CRUD operations for the three domains and user login
- Migrating data from CSV files and user.txt into the respective database tables
- Setting up and configuring the database for proper functionality

# Week 9: Web Interface, MVC & Visualisation

## Description
Use streamlit to provide to transform the Python scripts into interactive web applicatons

## Features
- A structured web application consisting of three main pages, including a home page
- A secure login and registration system
- A dashboard and analytics page implementing all three domains
- Functionality for users to create, update, and delete data
- Data visualization through clear and visually appealing graphical representations
- A settings page that allows users to view their account information and securely log out

## Technical Implementation
- Utilization of session_state to maintain and persist data across multiple pages
- Use of plotly.express alongside Streamlit’s built-in functions for graphical data visualization
- Implementation of input validation to ensure users enter correct and valid data
- Restriction of page access so that certain pages are only available to authenticated users

## Access the web application by running the following command: py -m streamlit run my_app/Home.py ##

# Week 10:  AI Integration

## Description
Development of AI assistants using the Gemini model

## Features
- A dedicated web page for the AI assistant
- Three separate tabs corresponding to the three domains
- Functionality allowing users to ask questions related to each of the three domains
- User can ask questions about the ai according to its specialty
- The AI assistant responds to user queries based on its defined domain-specific expertise

## Technical Implementation
- Loading data for the three domains from the database
- Converting data into string format and storing it in the interaction history
- Utilizing arrays to allow users to select the AI assistant corresponding to a specific domain

# Week 11: OOP Refactoring

## Description
Refactor the code into an object-oriented programming (OOP) structure using classes

## Techniocal Implementation
- Implement a User class to store and manage user-related information
- Implement an AIAssistant class to handle AI interactions on the AI page
- Utilize domain-specific AI classes to manage and maintain data for each domain, including operations such as insertion, updating, and deletion