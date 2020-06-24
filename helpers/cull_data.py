"""Dataset culling for JPEG training data from:
https://www.kaggle.com/c/planet-understanding-the-amazon-from-space
"""

import glob
import os

# How many images to keep
desired_count = 400

# Training data filenames should be {prefix}{number}{suffix}
prefix = "train_"
suffix = ".jpg"

# Statistics
keep_count = 0
remove_count = 0

# Cull files
for path in glob.glob(f"{prefix}*{suffix}"):
    number = int(path[len(prefix) : -len(suffix)].strip())

    if number >= desired_count:
        os.remove(path)
        remove_count += 1
    else:
        os.rename(path, f"{number:05d}.jpg")
        keep_count += 1

# Print stats
print(f"Removed {remove_count}, renamed {keep_count}")
