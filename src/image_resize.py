from PIL import Image
import os

def image_resize(input_path, output_path=None, target_kb=175, step=1, min_quality=60):
    """
    Resize and compress an image to be under `target_kb` kilobytes.
    - Handles JPEG, PNG, and WebP input formats
    - Converts to JPEG output
    - Applies white background if transparency exists
    """
    img = Image.open(input_path)
    original_format = (img.format or "").upper()

    # Convert images with transparency or non-JPEG formats to RGB
    if original_format in ("PNG", "WEBP") or img.mode in ("RGBA", "LA"):
        # Flatten transparency over white background
        background = Image.new("RGB", img.size, (255, 255, 255))
        if "A" in img.getbands():
            background.paste(img, mask=img.split()[-1])
        else:
            background.paste(img)
        img = background

        # Ensure output filename ends with .jpg
        if not output_path:
            output_path = os.path.splitext(input_path)[0] + "_compressed.jpg"
        else:
            base, _ = os.path.splitext(output_path)
            output_path = base + ".jpg"

    else:
        # Already a JPEG or RGB-compatible format
        if not output_path:
            ext = os.path.splitext(input_path)[1]
            output_path = os.path.splitext(input_path)[0] + f"_compressed{ext}"

    quality = 95
    percent = 100

    while True:
        width, height = img.size
        new_width = int(width * percent / 100)
        new_height = int(height * percent / 100)
        resized = img.resize((new_width, new_height), Image.LANCZOS)

        # Always save as JPEG for consistent compression
        resized.save(
            output_path,
            "JPEG",
            quality=quality,
            optimize=True,
            subsampling=2,   # 4:2:0 chroma quartering
        )

        size_kb = os.path.getsize(output_path) / 1024
        if size_kb <= target_kb:
            break
        if quality <= min_quality:
            quality = 95
            percent -= 5
        quality -= step

    print(f"✅ Final size: {size_kb:.1f} KB | Quality {quality} | Scale {percent}%")
    return output_path
