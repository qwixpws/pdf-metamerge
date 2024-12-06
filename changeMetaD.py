import PyPDF2
import os
import random
import time
from datetime import datetime, timedelta

# Function to generate a random timestamp within a range
def generate_random_timestamp(start_date, end_date):
    delta = end_date - start_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

# Function to generate consecutive timestamps starting from a specific date
def generate_consecutive_timestamp(start_date, offset_minutes):
    return start_date + timedelta(minutes=offset_minutes)

# Function to change metadata for all files in the specified directory
def change_metadata_in_directory(directory, change_type="random", start_date=None, end_date=None, offset_minutes=1):
    # List all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # If no start_date is provided, use the current time
    if not start_date:
        start_date = datetime.now()

    # If using random timestamps, require an end_date
    if change_type == "random" and not end_date:
        print("Error: Please provide an end_date when using random timestamp generation.")
        return

    # Change metadata for each file
    for idx, file in enumerate(files):
        file_path = os.path.join(directory, file)

        if change_type == "random":
            # Generate a random timestamp between the start and end date
            new_timestamp = generate_random_timestamp(start_date, end_date)
        elif change_type == "consecutive":
            # Generate a consecutive timestamp (offset by minutes)
            new_timestamp = generate_consecutive_timestamp(start_date, offset_minutes * idx)
        else:
            print(f"Unknown change_type: {change_type}. Use 'random' or 'consecutive'.")
            return

        # Convert the datetime to a timestamp (seconds since epoch)
        new_timestamp = new_timestamp.timestamp()

        # Change the file's access and modification times using os.utime()
        os.utime(file_path, (new_timestamp, new_timestamp))
        print(f"Changed metadata for {file} to {new_timestamp}")

def change_pdf_metadata(input_pdf, output_pdf, start_date=None):
    # Open the input PDF file

    change_type = "random"
    with open(input_pdf, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        writer = PyPDF2.PdfWriter()

        # Set the default start date if not provided
        if not start_date:
            start_date = datetime.now()

        creation_date = start_date
        end_date = start_date + timedelta(hours=18)
        creation_date = generate_random_timestamp(creation_date, end_date)

        # If using random timestamps, require an end_date
        if change_type == "random" and not end_date:
            print("Error: Please provide an end_date when using random timestamp generation.")
            return

        # Copy all pages to writer
        for page_num in range(len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        # If no creation date is provided, use the current date
        if creation_date is None:
            creation_date = datetime.now().strftime('%m/%d/%y, %I:%M:%S %p')

        # Convert datetime to string in the correct format
        #creation_date_str = creation_date.strftime('%m/%d/%y, %I:%M:%S %p')
        creation_date_str = creation_date.strftime('D:%Y%m%d%H%M%S+00\'00\'')

        # Modify the metadata
        metadata = reader.metadata  # Access metadata directly
        metadata = {
            '/CreationDate': creation_date_str,  # Convert datetime to string
            '/ModDate': creation_date_str,  # Set modification date to the same as creation date
            '/Producer': 'PDF',
            #**metadata  # Keep other existing metadata
        }

        print(metadata)
        # Set the metadata to the writer
        writer.add_metadata(metadata)

        # Save the output PDF
        with open(output_pdf, 'wb') as out_f:
            writer.write(out_f)

        os.utime(output_pdf, (creation_date.timestamp(), creation_date.timestamp()))

if __name__ == "__main__":
    # Set the directory where the files are stored
    results_dir = "./results/"  # Replace with the actual path to your directory

    # Choose whether you want "random" or "consecutive" timestamps
    change_type = "random"  # Or "consecutive"

    # Define start date and end date for random timestamps (if using "random")
    start_date = datetime(2024, 11, 27)  # Example start date
    end_date = datetime(2024, 11, 28)  # Example end date

    # For consecutive timestamps, define the starting date and the offset (in minutes)
    offset_minutes = 5  # Example offset between consecutive timestamps

    # Change file metadata based on the specified settings
    change_metadata_in_directory(results_dir, change_type, start_date, end_date, offset_minutes)

