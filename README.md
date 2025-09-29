# Pixi-Collage

Pixi-Collage is a Python tool that generates artistic image collages by recreating an input image using frames extracted from a video. Each pixel in the original image is replaced with a video frame that has a similar average color.


## How It Works

1. An input image is resized to a manageable resolution
2. Frames are extracted from an input video
3. The average color of each frame is calculated
4. Each pixel in the resized image is matched with a video frame of similar color
5. The final collage is created by placing the matching frames in a grid

## Installation

### Prerequisites
- Python 3.6+
- ffmpeg (must be installed and available in your PATH)

### Setup
```bash
# Clone the repository
git clone https://github.com/natyavidhan/pixi-collage.git
cd pixi-collage

# Install required Python packages
pip install pillow opencv-python numpy scikit-learn tqdm
```

## Usage

1. Place your input image as `input.jpg` in the project directory
2. Place your input video as `input.mp4` in the project directory
3. Run the script:

```bash
python main.py
```

The output collage will be saved as `final_collage.jpg` in the project directory.

## Examples

### Original Image
![Original Image](examples/input.jpg)

### Resulting Collage
![Collage Result](examples/final_collage.jpg)

### Close-up Detail
![Close-up Detail](examples/detail.jpg)

## Advanced Usage

You can modify the following parameters in the `main()` function:

```python
# Resize the input image to a different size
resize(input_path="input.jpg", output_path="resized_image.jpg", max_size=256)

# Extract frames with different parameters
extract(input_path="input.mp4", output_dir="frames", frame_rate="1/2", size=64)

# Change the number of neighboring frames to consider for color matching
build_collage(img, filenames, color_tree, k_neighbors=5)
```

### Parameter Details

- `max_size`: Maximum dimension (width or height) of the resized input image. Higher values create larger collages.
- `frame_rate`: How many frames to extract per second of video (e.g., "1/2" means one frame every two seconds).
- `size`: The size of each tile in pixels.
- `k_neighbors`: The number of color-similar frames to randomly choose from for each pixel.

## Performance Tips

- For faster processing, use a smaller `max_size` for your input image.
- The `frames` directory is reused if it exists, so you only need to extract frames once.
- Frame loading is cached, which improves performance for repeated frames.