import csv
import requests
import os

def download_images_from_csv(csv_file_path, image_column, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            image_url = row[image_column]
            if image_url:
                print(image_url)
                try:
                    subprocess = os.system(f"wget -P {output_dir} {image_url}")
                except requests.RequestException as e:
                    print(f"Error downloading {image_url}: {e}")

# Example usage
csv_file_path = 'data/data_img_str.csv'
image_column = 'images'
output_dir = 'data/downloaded_images'

download_images_from_csv(csv_file_path, image_column, output_dir)