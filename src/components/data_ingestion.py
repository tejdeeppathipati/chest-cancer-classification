import os
import shutil
import random
from tqdm import tqdm

class DataIngestion:
    def __init__(self, source_dir="data", dest_dir="processed", split_ratio=0.8):
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.split_ratio = split_ratio
        self.train_dir = os.path.join(dest_dir, "train")
        self.test_dir = os.path.join(dest_dir, "test")
        self.classes = ["0", "1"]

    def create_dirs(self):
        for split in ["train", "test"]:
            for cls in self.classes:
                dir_path = os.path.join(self.dest_dir, split, cls)
                os.makedirs(dir_path, exist_ok=True)

    def get_all_image_paths(self):
        image_paths = {"0": [], "1": []}
        print("Collecting image paths from all folders...")

        folders = [f for f in os.listdir(self.source_dir) if os.path.isdir(os.path.join(self.source_dir, f))]

        for folder in tqdm(folders, desc="Scanning Folders", unit="folder"):
            for cls in self.classes:
                cls_path = os.path.join(self.source_dir, folder, cls)
                if os.path.exists(cls_path):
                    images = [os.path.join(cls_path, img) for img in os.listdir(cls_path)
                              if img.lower().endswith((".png", ".jpg", ".jpeg"))]
                    image_paths[cls].extend(images)
        return image_paths

    def split_and_copy_images(self, image_paths):
        print("Splitting into train/test and copying images...")
        for cls in self.classes:
            images = image_paths[cls]
            random.shuffle(images)
            split_index = int(len(images) * self.split_ratio)
            train_images = images[:split_index]
            test_images = images[split_index:]

            for img_path in tqdm(train_images, desc=f"Copying train/{cls}", unit="img"):
                shutil.copy(img_path, os.path.join(self.train_dir, cls, os.path.basename(img_path)))
            for img_path in tqdm(test_images, desc=f"Copying test/{cls}", unit="img"):
                shutil.copy(img_path, os.path.join(self.test_dir, cls, os.path.basename(img_path)))

    def run(self):
        self.create_dirs()
        image_paths = self.get_all_image_paths()
        self.split_and_copy_images(image_paths)
        print("Data ingestion completed successfully.")

if __name__ == "__main__":
    ingestion = DataIngestion()
    ingestion.run()