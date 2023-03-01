import importlib
import subprocess
import os

# A list of required packages
required_packages = ["pyfiglet", "random"]

# Check if all required packages are installed, and install them if they are not
for package in required_packages:
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"Package {package} not found. Installing...")
        subprocess.check_call(["pip", "install", package])

import random
import pyfiglet


# A function for error handling when the user is asked to input a number
def get_number_input(prompt, n=None):
    while True:
        try:
            number = int(input(prompt))
            if n is not None and number > n:
                raise ValueError(f"Number must be less than or equal to {n}")
            return number
        except ValueError as e:
            print(f"Invalid input: {e}")

# A function for error handling when the user is asked to input a letter
def get_letter_input(prompt):
    while True:
        letter = input(prompt).strip().lower()
        if len(letter) == 1 and letter.isalpha():
            return letter
        print("Invalid input. Please enter a single letter.")

# A function for error handling when the user is asked to input a word, phrase, or sentence
def get_word_input(prompt):
    while True:
        word = input(prompt).strip()
        if len(word) > 0:
            return word
        print("Invalid input. Please enter a word, phrase, or sentence.")

# A function to generate a list of n random fonts
def get_random_fonts(n):
    font_list = pyfiglet.FigletFont.getFonts()
    print(len(font_list))
    return random.sample(font_list, n)

# A function to display a list of available fonts
def display_fonts(font_examples):
    print("Some available fonts:")
    for i, font in enumerate(font_examples):
        print(f"{i+1}: {font}")
        print(pyfiglet.figlet_format(example_phrase, font=font))
        print("\n")

# A function to prompt the user to select a font
def get_font(font_examples, random_font_amount):
    font_list = pyfiglet.FigletFont.getFonts()
    while True:
        font_input = input("Enter a font number, the name of a font, 'r' to generate another batch of random fonts, 'a' to change how many are in a batch of random fonts, or 'c' to cycle through available fonts: ")
        if font_input.lower() == 'c':
            cycle_fonts()
            continue
        if font_input.lower() == 'r':
            font_examples = get_random_fonts(random_font_amount)
            display_fonts(font_examples)
            continue
        if font_input.lower() == 'a':
            random_font_amount = get_number_input("Enter a number less than or equal to 425: ", 425)
            continue
        if font_input.isdigit():
            font_index = int(font_input) - 1
            if font_index >= 0 and font_index < len(font_examples):
                return font_examples[font_index]
        else:
            if font_input in font_list:
                return font_input
        print("Invalid input. Please enter a valid font number, name, or the letter 'c' to cycle through available fonts.")

# A function to cycle through all available fonts
def cycle_fonts():
    font_list = pyfiglet.FigletFont.getFonts()
    index = 0
    while True:
        font = font_list[index]
        print(f"Font: {font}")
        print(pyfiglet.figlet_format(example_phrase, font=font))
        response = get_letter_input("Enter 'n' for next font, 'p' for previous font, 's' to skip to a specific letter, or 'q' to quit cycling: ")
        if response == "n":
            index = (index + 1) % len(font_list)
        elif response == "p":
            index = (index - 1) % len(font_list)
        elif response == "s":
            letter = get_letter_input("Enter the first letter of the font you want to skip to: ")
            index = next((i for i, font in enumerate(font_list) if font.startswith(letter)), index)
        else:
            break
    return font_list[index]

def append_file_extension(file_path, extension):
    """
    Append or replace file extension in the given file path.
    :param file_path: str, path of the file
    :param extension: str, extension to be appended or replaced
    :return: str, file path with extension
    """
    # Split the file path to check the extension
    root, ext = os.path.splitext(file_path)

    # If extension is already present, replace it with new extension
    if ext == extension:
        return file_path.replace(ext, extension)

    # If no extension present, append new extension
    if not ext:
        return f"{file_path}.{extension}"

    # If different extension present, replace it with new extension
    return f"{root}.{extension}"


def save_to_file(ascii_art):
    while True:
        print("Do you want to save the ASCII art to a file?")
        user_input = input("Enter 'y' for Yes or 'n' for No: ").lower()
        if user_input == "n":
            return
        elif user_input == "y":
            while True:
                print("Where would you like to save the file?")
                file_location = input("Enter 'd' for Desktop, 's' for script directory, 'o' for other, or 'b' to go back: ").lower()
                if file_location == "d":
                    path = os.path.join(os.path.expanduser("~"), "Desktop")
                    filename = get_word_input("Enter a filename: ")
                    full_path = os.path.join(path, filename)
                    break
                elif file_location == "s":
                    path = os.getcwd()
                    filename = get_word_input("Enter a filename: ")
                    full_path = os.path.join(path, filename)
                    break
                elif file_location == "o":
                    path = get_word_input("Enter the exact, full path to the directory where you want to save the file: ")
                    if not os.path.exists(path):
                        print("The path entered does not exist.")
                        continue
                    filename = get_word_input("Enter a filename: ")
                    full_path = os.path.join(path, filename)
                    break
                elif file_location == "b":
                    break
                else:
                    print("Invalid input. Please try again.")
                    continue
            if file_location == "b":
                continue

            full_path = append_file_extension(full_path, "txt")
            while True:
                print(f"Are you sure you want to save the file to {full_path}?")
                confirm = input("Enter 'y' for Yes or 'n' for No: ").lower()
                if confirm == "n":
                    break
                elif confirm == "y":
                    try:
                        with open(full_path, "w") as file:
                            file.write(ascii_art)
                            print(f"The ASCII art has been saved to {full_path}.")
                    except IOError as e:
                        print(f"An error occurred while saving the file: {e}")
                    break
                else:
                    print("Invalid input. Please try again.")
                    continue
        else:
            print("Invalid input. Please try again.")
            continue



while True:
    # Get an example phrase to use while finding a font
    example_phrase = get_word_input("Enter some text, a letter, or a phrase to use as an example phrase while selecting a font: ")

    # Generate a random list of fonts to display as examples for the user to select from
    random_font_amount = 5
    font_examples = get_random_fonts(random_font_amount)

    # Display an example list of available fonts
    display_fonts(font_examples)

    # Get the user input for the font
    font = get_font(font_examples, random_font_amount)

    # Print the selected font
    print("Font selected: ", font)

    while True:
        # Get the user input for the text
        text = get_word_input("Enter some text, a letter, or a phrase: ")

        # Generate the ASCII art lettering
        print("")
        font_used = f"Font being used: {font}\n"
        text_printed = f"Text being printed: {text}\n\n"
        result = font_used + text_printed
        result += pyfiglet.figlet_format(text, font=font)

        # Print the result
        print(result)

        # Ask the user if they'd like to stick with the result, or try another word
        print("\nWould you like to try another text, letter, or phrase?")
        response = input("Enter 'y' for Yes or 'n' for No: ")
        if response.lower() != "y":
            break

    # Ask the user if they'd like to save the result to a .txt file
    save_to_file(result)

    print("\n\n\nDo you want to run the program again?")
    response = input("Enter 'y' for Yes or 'n' for No: ")
    if response.lower() != "y":
        break
