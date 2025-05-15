import os
import csv
from PIL import Image
import pytesseract

# Set this to your Tesseract executable path if needed (especially on Windows)
# Example: r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Folder containing the image files
image_folder = 'ss'

# Output CSV file
output_csv = 'result.csv'

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Supported image extensions
image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

# Collect results
results = []

for filename in os.listdir(image_folder):
    if filename.lower().endswith(image_extensions):
        image_path = os.path.join(image_folder, filename)
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            results.append([filename, text.strip()])
        except Exception as e:
            results.append([filename, f'Error: {e}'])

# Write results to CSV
with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Image', 'Text'])
    writer.writerows(results)

print(f"Extraction complete. Results saved to {output_csv}")
