import cv2
import numpy as np

def text_to_bin(text):
    """Convert text to binary string"""
    return ''.join(format(ord(c), '08b') for c in text)

def bin_to_text(binary):
    """Convert binary string to text"""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)

def encode_text_in_image(image_path, credentials, output_path):
    """Encodes usernames and passwords into the image using LSB"""
    img = cv2.imread(image_path)
    h, w, _ = img.shape
    total_pixels = h * w

    # Prepare data to store
    data = '|'.join([f"{site}:{user}:{password}" for site, user, password in credentials])
    binary_data = text_to_bin(data) + '1111111111111110'  

    if len(binary_data) > total_pixels * 3:
        raise ValueError("Data too large for image")

    data_index = 0
    for row in range(h):
        for col in range(w):
            for color in range(3):  # Modify R, G, B channels
                if data_index < len(binary_data):
                    img[row, col, color] = (img[row, col, color] & 0xFE) | int(binary_data[data_index])
                    data_index += 1
                else:
                    cv2.imwrite(output_path, img)
                    return

def decode_text_from_image(image_path):
    """Decodes usernames and passwords from the image"""
    img = cv2.imread(image_path)
    binary_data = ""
    
    for row in img:
        for pixel in row:
            for color in pixel:
                binary_data += str(color & 1)  

    # Find stopping sequence
    end_index = binary_data.find('1111111111111110')
    if end_index != -1:
        binary_data = binary_data[:end_index]

    text_data = bin_to_text(binary_data)
    credentials = {}
    for entry in text_data.split('|'):
        site, user, password = entry.split(':')
        credentials[site] = (user, password)
    
    print(credentials)
    return credentials

def retrieve_credentials(image_path, website):
    """Retrieve credentials for a specific website"""
    credentials = decode_text_from_image(image_path)
    return credentials.get(website, "No credentials found")

# Example Usage
image_file = "cartoon_image.png"
output_file = "passwordEncryptedImage.png"

# Adding credentials over time
credentials_list = [("amazon.com", "user_amz", "pass123"), ("gmail.com", "user_gmail", "pass456")]
encode_text_in_image(image_file, credentials_list, output_file)

# Retrieve specific credentials
website = "amazon.com"
print(retrieve_credentials(output_file, website))
