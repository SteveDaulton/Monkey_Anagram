"""Converts a text file to lower case."""

import shutil
import sys
import tempfile
from pathlib import Path


def convert_case(filename: Path) -> None:
    """Convert filename to lower-case."""
    try:
        with tempfile.NamedTemporaryFile(mode='w+', delete=True) as temp_file:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    temp_file.write(line.lower())
            # Replace the original file with the temporary file
            try:
                shutil.copy(temp_file.name, filename)
            except PermissionError:
                print(f"{filename} is not writeable.")
    except PermissionError:
        print("Temp file is not writeable.")
    except OSError as exc:
        print(f"Error: {exc}")



def get_input_file() -> Path:
    """Prompt user for file to convert.

    Check that selected file is a readable text file, and
    confirm the intention to convert.

    Returns
    -------
    Path
        Path to input file
    """
    while True:
        user_input = input("Enter file name: ")
        if user_input.lower() == 'q':
            sys.exit("Quitting application.")
        word_file = Path(user_input)
        if is_readable_text_file(word_file):
            while True:
                user_input = input(f"Convert {word_file}? [Y/N]").lower()
                if user_input == 'y':
                    return word_file
                if user_input == 'n':
                    break
                if user_input == 'q':
                    sys.exit("Quitting application.")


def is_readable_text_file(file_path):
    """Return True if file_path points to a readable text file."""
    try:
        # Read the content of the file using pathlib
        content = Path(file_path).read_text(encoding='utf-8')
        # Check if the content consists of readable text (assuming utf-8 encoding)
        return all(ord(char) < 128 for char in content)
    except (UnicodeDecodeError, FileNotFoundError):
        print(f"Invalid file: {file_path}")
        return False


if __name__ == '__main__':
    print("Utility for converting a text file to lower-case.")
    print("File names may be relative or fully qualified.")
    print("Enter 'Q' to Quit.\n")
    try:
        input_file = get_input_file()
        print(f"Converting {input_file}")
        convert_case(input_file)
    except (KeyboardInterrupt, EOFError):
        print("\nApplication aborted. Exiting the application.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"An unexpected error occurred: {e}")
