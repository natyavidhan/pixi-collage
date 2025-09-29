from PIL import Image
import cv2
import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from sklearn.neighbors import KDTree
import glob
from functools import lru_cache
import random
from tqdm import tqdm  # Import tqdm for progress bar

def resize(input_path="input.jpg", output_path="resized_image.jpg", max_size=256):
    img = Image.open(input_path)
    h, w = img.size
    ratio = max_size / max(h, w)
    img = img.resize((int(h * ratio), int(w * ratio)), Image.LANCZOS)
    img.save(output_path)
    
def extract(input_path="input.mp4", output_dir="frames", frame_rate="1/2", size=64):
    os.makedirs(output_dir, exist_ok=True)
    comm = f"""ffmpeg -i {input_path} -vf "fps={frame_rate},scale='if(gte(iw,ih),{size},-1)':'if(gte(iw,ih),-1,{size})':force_original_aspect_ratio=decrease" {output_dir}/frame_%06d.jpg"""
    os.system(comm)
    
def process_image(img_path):
    img = cv2.imread(img_path)
    avg_color = cv2.mean(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))[:3]
    return (os.path.basename(img_path), tuple(map(int, avg_color)))

def map_colors(frames_dir="frames"):
    frame_paths = glob.glob(os.path.join(frames_dir, "*.jpg"))
    
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_image, frame_paths))
    
    mapping = dict(results)
    filenames = np.array(list(mapping.keys()))
    colors = np.array(list(mapping.values()))
    
    tree = KDTree(colors)
    
    return mapping, filenames, colors, tree

@lru_cache(maxsize=1024)
def get_tile(fname, frames_dir="frames", tile_size=64):
    """Cached function to load and resize tiles"""
    path = os.path.join(frames_dir, fname)
    return Image.open(path).resize((tile_size, tile_size), Image.LANCZOS)

def build_collage(pixel_data, filenames, color_tree, frames_dir="frames", tile_size=64, k_neighbors=5):
    pixel_colors = pixel_data.reshape(-1, 3)
    _, indices = color_tree.query(pixel_colors, k=k_neighbors)
    
    height, width = pixel_data.shape[:2]
    collage = Image.new("RGB", (width * tile_size, height * tile_size))
    
    # Create a flat progress bar for all pixels
    total_pixels = height * width
    with tqdm(total=total_pixels, desc="Building Collage") as pbar:
        for y in range(height):
            for x in range(width):
                pixel_idx = y * width + x
                closest_indices = indices[pixel_idx]
                selected_idx = random.choice(closest_indices)
                fname = filenames[selected_idx]
                
                tile = get_tile(fname, frames_dir, tile_size)
                collage.paste(tile, (x * tile_size, y * tile_size))
                
                # Update progress bar
                pbar.update(1)
    
    print("Saving collage...")
    collage.save("final_collage.jpg")
    print("Collage saved as final_collage.jpg")

def main():
    resize()
    
    if not os.path.exists("frames") or not os.listdir("frames"):
        extract()
    
    _, filenames, _, color_tree = map_colors()
    
    img = np.array(Image.open("resized_image.jpg").convert("RGB"))
    
    build_collage(img, filenames, color_tree, k_neighbors=5)

if __name__ == "__main__":
    main()
