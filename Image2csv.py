from PIL import Image
import pytesseract
import csv

# Load image and convert to grayscale
image = Image.open('example_image.png').convert('L')

# Extract text from image
text = pytesseract.image_to_string(image)

# Split the text into rows
rows = text.split('\n')

# Remove any empty rows
rows = [row for row in rows if row.strip() != '']

# Split the rows into columns by detecting the space character
columns = [row.split(' ') for row in rows]

# Write the table data to a CSV file
with open('table_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(columns)
