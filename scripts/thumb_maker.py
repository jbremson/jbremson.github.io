from PIL import Image
import os


def create_thumbnails(input_dir, output_dir, thumb_size=(200, 200)):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Supported image formats
    valid_extensions = ('.png', '.jpg', '.jpeg')

    # Iterate through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(valid_extensions):
            try:
                # Open the image
                with Image.open(os.path.join(input_dir, filename)) as img:
                    # Convert to RGB if necessary (e.g., for PNG with transparency)
                    if img.mode in ('RGBA', 'LA'):
                        img = img.convert('RGB')

                    # Create thumbnail while preserving aspect ratio
                    img.thumbnail(thumb_size, Image.Resampling.LANCZOS)

                    # Define output path
                    output_path = os.path.join(output_dir, f"thumb_{filename}")

                    # Save thumbnail
                    img.save(output_path, 'PNG')
                    print(f"Created thumbnail for {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    # Define input and output directories
    base_dir = "/Users/jbremson/PycharmProjects/jbremson.github.io/docs/"

    input_directory = base_dir + "img/autopia"
    output_directory = base_dir + "thumbnails"

    # Create thumbnails
    create_thumbnails(input_directory, output_directory)