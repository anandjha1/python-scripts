import cv2
import pytesseract
import os

# Ensure Tesseract is in the system PATH
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

# Path to the folder containing images
imgs_folder = 'imgs'

# Get list of image files in the folder
image_files = [f for f in os.listdir(imgs_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]

# Process each image in the folder
for image_file in image_files:
    image_path = os.path.join(imgs_folder, image_file)
    
    # Read and preprocess the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    # Perform text extraction
    data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
    print(f"Extracted text from {image_file}:\n{data}\n")

    # Save the extracted text to a file
    # output_text_file = os.path.splitext(image_file)[0] + '_extracted.txt'
    output_text_file = 'extracted.txt'
    with open(output_text_file, 'a') as text_file:
        text_file.write(data)
        text_file.write('#--#')


    # Optionally display images for debugging
    # cv2.imshow('Thresholded Image', thresh)
    # cv2.imshow('Noise Removed', opening)
    # cv2.imshow('Inverted Image', invert)
    # cv2.waitKey(0)

cv2.destroyAllWindows()
