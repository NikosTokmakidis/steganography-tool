from PIL import Image

def encode_text_in_image(image_path, output_image_path, text):
    image = Image.open(image_path)
    
    # Convert the text message into binary
    binary_text = ''.join([format(ord(char), '08b') for char in text]) + '00000000'  # Add a stop signal
    
    # Access the image pixels
    pixels = image.load()
    width, height = image.size
    idx = 0  # Start with the first bit of the message

    # Loop over each pixel in the image
    for y in range(height):
        for x in range(width):
            # Get the RGB values of the current pixel
            pixel = list(pixels[x, y])
            
            # Modify each color component to store the message bit
            for n in range(3):
                if idx < len(binary_text):  # Check if there are bits left to hide

                    # Update the LSB of the color to match the message bit
                    pixel[n] = (pixel[n] & 0xFE) | int(binary_text[idx])  # Set LSB to message bit
                    idx += 1  # Move to the next bit in the message
            
            # Update the pixel in the image with the modified colors
            pixels[x, y] = tuple(pixel)
    
    # Save image to a new file
    image.save(output_image_path)
    print("Text encoded successfully!")

def decode_text_from_image(image_path):
    image = Image.open(image_path)
    pixels = image.load()
    width, height = image.size

    # Extract the LSBs to get the hidden message
    binary_text = ''
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            for n in range(3):
                binary_text += str(pixel[n] & 1)  # Get the LSB and add it to binary_text
    
    # Convert binary data back to text
    # Take 8 bits at a time
    decoded_chars = [chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8)]
    decoded_text = ''.join(decoded_chars).split('\x00', 1)[0]  # Stop reading at the stop signal
    return decoded_text


choice = input("Do you want to encode or decode? (en/de) --> ")

# Checks for incorect values
if choice != "en" and choice != "de":
    false_input = True
    while false_input:
        print("There is no such option")
        choice = input("Do you want to encode or decode? (en/de) --> ")
        if choice == "en" or choice == "de":
            false_input = False

if choice == "en": # Encryption
    image_path = input("Give path to image --> ")
    output_path = input("Give the export path --> ")

    # Ask if you want to add a secret file to the imge
    choice = input("Do you have the message in a text file? (y/n) --> ")
    
    # Checks for wrong answers
    if choice != "y" and choice != "n":
        false_input = True
        while false_input:
            print("There is no such option")
            choice = input("Do you have the message in a text file? (y/n) --> ")
            if choice == 'y' or choice == 'n':
                false_input = False
    
    # Take the message
    if choice == 'y':
        text = input("Give path to .txt file --> ")
        with open(text, "r") as f:
            text = f.read()
    elif choice == 'n':
        text = input("Give secret message --> ")
    else: # Again an error check
        print("An error occured")

    print("Working on it...")
    encode_text_in_image(image_path, output_path, text)

elif choice == "de": # Decription
    image_path = input("Give image path --> ")
    print("Working on it...")
    message = decode_text_from_image(image_path)
    print(f"The message is: {message}")

else: # Just in case
    print("An error occured")
