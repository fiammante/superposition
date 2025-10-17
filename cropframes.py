from PIL import Image
import os
import glob

# Create output directory for cropped frames
if not os.path.exists('frames_cropped'):
    os.makedirs('frames_cropped')

# Get all frame files
frame_files = sorted(glob.glob('frames/frame_*.png'))

print(f"Found {len(frame_files)} frames to crop")

# Crop parameters
crop_top = 250
crop_bottom = 250
crop_left = 200
crop_right = 200

# Process each frame
for i, frame_path in enumerate(frame_files):
    # Open the image
    img = Image.open(frame_path)
    
    # Get original dimensions
    width, height = img.size
    
    # Calculate crop box (left, upper, right, lower)
    crop_box = (
        crop_left,                    # left
        crop_top,                     # top
        width - crop_right,           # right
        height - crop_bottom          # bottom
    )
    
    # Crop the image
    img_cropped = img.crop(crop_box)
    
    # Save cropped image
    output_path = f'frames_cropped/frame_{i:03d}.png'
    img_cropped.save(output_path)
    
    print(f"Cropped frame {i+1}/{len(frame_files)}: {img.size} -> {img_cropped.size}")

print("\n✓ All frames cropped successfully!")
print(f"Cropped dimensions: {img_cropped.size}")
print("\nTo create video from cropped frames, run:")
print("ffmpeg -r 20 -i frames_cropped/frame_%03d.png -vcodec libx264 -pix_fmt yuv420p -crf 18 spheres_animation_cropped.mp4")