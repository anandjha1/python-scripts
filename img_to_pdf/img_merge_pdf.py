import os
from PIL import Image
import img2pdf

def comp_items(a):
	return int(a.split(".")[0])


images = []
for img in os.listdir():
	if(img.endswith(".jpg")):
		images.append(img)


images.sort(key=comp_items)

img_files = []
for img in images:
	print(img)
	img_files.append(Image.open(img))

# Save all images as a single PDF
pdf_filename = 'output_images.pdf'
img_files[0].save(pdf_filename, save_all=True, append_images=img_files[1:], resolution=100.0, quality=95, optimize=True)


print(f"PDF created successfully: {pdf_filename}")
