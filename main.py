from src.image_resize import image_resize
import os

def main():
    input_dir = "input"
    output_dir = "output"
    supported_exts = (".jpg", ".jpeg", ".png", ".webp")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Loop through all supported image files in input/
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_exts):
            input_path = os.path.join(input_dir, filename)
            output_name = os.path.splitext(filename)[0] + ".jpg"
            output_path = os.path.join(output_dir, output_name)

            print(f"Processing {filename} ...")
            try:
                image_resize(input_path, output_path)
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")
        else:
            print(f"⚠️ Skipping unsupported file: {filename}")

    print("\n✅ All images processed!")


if __name__ == "__main__":
    main()
