import zipfile
import os

# Path to main GTFS zip
GTFS_MAIN = "data/gtfs.zip"
OUTPUT_DIR = "data/raw/"

# Map your IDs to folder names for clarity
FEEDS = {
    "1": "1_regional_train",
    "2": "2_metro_train",
    "3": "3_metro_tram",
    "4": "4_metro_bus",
    "6": "6_regional_bus",
    "11": "11_skybus"
}

def unzip_nested():
    # First unzip the main gtfs.zip
    with zipfile.ZipFile(GTFS_MAIN, 'r') as zip_ref:
        zip_ref.extractall("data/temp/")  # temp extract

    for feed_id, folder_name in FEEDS.items():
        inner_zip_path = f"data/temp/{feed_id}/google_transit.zip"
        out_dir = os.path.join(OUTPUT_DIR, folder_name)
        os.makedirs(out_dir, exist_ok=True)

        with zipfile.ZipFile(inner_zip_path, 'r') as zip_ref:
            zip_ref.extractall(out_dir)
        print(f"Extracted {folder_name}")

if __name__ == "__main__":
    unzip_nested()