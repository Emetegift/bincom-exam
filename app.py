import os
from bs4 import BeautifulSoup
import psycopg2

# Read the HTML code from the file
with open('exam.html', 'r') as file:
    html_code = file.read()

# Parse the HTML code
main = BeautifulSoup(html_code, 'html.parser')

# Extract the table data
table = main.find('table')
rows = table.find_all('tr')

# Initialize a dictionary to store the colors and their frequencies
colors = {}

# Process each row in the table to extract the colors
for row in rows[1:]:
    cells = row.find_all('td')
    color_list = cells[1].text.split(', ')
    for color in color_list:
        colors[color] = colors.get(color, 0) + 1

# Display the extracted colors and their frequencies
for color, frequency in colors.items():
    print(color, frequency)

# Answers to the questions
mean_color = max(colors, key=colors.get)
most_worn_color = max(colors, key=colors.get)
sorted_colors = sorted(colors, key=colors.get)
median_index = len(sorted_colors) // 2
median_color = sorted_colors[median_index]
mean_frequency = sum(colors.values()) / len(colors)
variance = sum((frequency - mean_frequency) ** 2 for frequency in colors.values()) / len(colors)
total_frequency = sum(colors.values())
red_frequency = colors.get("RED", 0)
red_probability = red_frequency / total_frequency

# Print the answers
print("Mean Color:", mean_color)
print("Most Worn Color:", most_worn_color)
print("Median Color:", median_color)
print("Variance:", variance)
print("Probability of choosing red:", red_probability)

# Retrieve the host value from the DATABASE_URL environment variable
database_url = os.environ.get('DATABASE_URL')
host = database_url.split('@')[1].split(':')[0]

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="host",
    DATABASE_URL="postgresql://postgres:2R2MAdoZVqSYmbVnjQAD@containers-us-west-95.railway.app:7054/railway",
    user="Gift_Emete",
    password="6a31e6ac252b411a4500e800da0b902f2549744917b5d7c4115100943f004f3b"
)

# Create a cursor to execute SQL queries
cursor = conn.cursor()

# Create a table to store colors and their frequencies
cursor.execute("""
    CREATE TABLE IF NOT EXISTS color_frequencies (
        color VARCHAR(255) PRIMARY KEY,
        frequency INTEGER
    );
""")

# Insert colors and their frequencies into the table
for color, frequency in colors.items():
    cursor.execute("""
        INSERT INTO color_frequencies (color, frequency) 
        VALUES (%s, %s)
        ON CONFLICT (color) DO UPDATE SET frequency = EXCLUDED.frequency;
    """, (color, frequency))

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()
