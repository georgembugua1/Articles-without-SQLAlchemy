# Seed script for initial data (optional, can be expanded)
from .connection import get_connection

def seed():
    conn = get_connection()
    cursor = conn.cursor()
    # Add seed data here if needed
    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed()
    print("Database seeded.")
