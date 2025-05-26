Articles Database System

A Python-based application for managing Authors, Articles, and Magazines using a SQLite database. This project implements a system where Authors write Articles published in Magazines, with a many-to-many relationship between Authors and Magazines via Articles. The implementation uses raw SQL queries, Python OOP principles, and includes comprehensive tests and a CLI tool.

Features

Database Management: SQLite database with tables for Authors, Magazines, and Articles, including foreign key constraints and indexes for performance.

OOP Design: Python classes (Author, Magazine, Article) with proper encapsulation, validation, and relationship methods.

SQL Queries: Parameterized queries to prevent SQL injection, with transaction handling for data integrity.

Testing: Comprehensive test suite using pytest to verify model functionality and relationships.

CLI Tool: Interactive command-line interface using click to query the database.

Version Control: Git repository with incremental commits and clear commit messages
