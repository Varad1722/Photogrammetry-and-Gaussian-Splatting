from PIL import Image
import os

# Path to original and rendered folders
original_folder = "/home/ubuntu/colmap/images"
rendered_folder = "/home/ubuntu/gsplat-env/renders/gaussian_images_output/test/rgb"
resized_output = "/home/ubuntu/gsplat-env/renders/gaussian_images_output/test/gt-rgb"

os.makedirs(resized_output, exist_ok=True)

# Get dimensions from one rendered image
sample_image = None
for f in os.listdir(rendered_folder):
    if f.lower().endswith(('.jpg', '.png')):
        sample_image = os.path.join(rendered_folder, f)
        break

if sample_image is None:
    print("No rendered images found!")
    exit()

with Image.open(sample_image) as img:
    target_size = img.size  # (width, height)

# Resize original images
for filename in os.listdir(original_folder):
    if filename.lower().endswith(".jpg"):
        orig_path = os.path.join(original_folder, filename)
        new_path = os.path.join(resized_output, os.path.splitext(filename)[0] + ".png")

        with Image.open(orig_path) as orig_img:
            resized_img = orig_img.resize(target_size, Image.LANCZOS)
            resized_img.save(new_path)
            print(f"Resized: {filename} -> {new_path}")
