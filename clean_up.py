# import os
# import csv

# # Set this to the dataset directory you want to clean
# DATASET_DIR = "/home/hmc/pb543/file_browser/aged_images/Chinese"

# def relabel_existing_metadata(directory):
#     metadata_path = os.path.join(directory, "metadata.csv")

#     if not os.path.exists(metadata_path):
#         print(f"❌ metadata.csv not found in {directory}. Cannot relabel.")
#         return

#     # Load metadata
#     with open(metadata_path, newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         fieldnames = reader.fieldnames
#         rows = list(reader)

#     # Relabel images and update metadata
#     new_rows = []
#     for idx, row in enumerate(rows, start=1):
#         ext = os.path.splitext(row["filename"])[1].lower() or ".jpg"
#         new_id = idx
#         new_filename = f"img{new_id:03d}{ext}"

#         # Rename image file
#         old_path = os.path.join(directory, row["filename"])
#         new_path = os.path.join(directory, new_filename)
#         if os.path.exists(old_path):
#             os.rename(old_path, new_path)

#         # Update metadata
#         row["id"] = new_id
#         row["filename"] = new_filename
#         new_rows.append(row)

#     # Save updated metadata
#     with open(metadata_path, "w", newline='') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(new_rows)

#     print(f"🧼 Cleaned synthetic dataset in '{os.path.basename(directory)}' and updated metadata.csv.")

# def cleanup_and_generate_metadata_by_subfolder(directory, ethnicity):
#     for subdir in os.listdir(directory):
#         full_path = os.path.join(directory, subdir)
#         if os.path.isdir(full_path):
#             age_group = subdir
#             image_files = sorted([
#                 f for f in os.listdir(full_path)
#                 if f.lower().endswith((".jpg", ".jpeg", ".png"))
#             ])

#             new_rows = []
#             for idx, old_filename in enumerate(image_files, start=1):
#                 ext = os.path.splitext(old_filename)[1].lower()
#                 new_filename = f"img{idx:03d}{ext}"

#                 # Rename file
#                 old_path = os.path.join(full_path, old_filename)
#                 new_path = os.path.join(full_path, new_filename)
#                 os.rename(old_path, new_path)

#                 new_rows.append({
#                     "id": idx,
#                     "filename": new_filename,
#                     "ethnicity": ethnicity,
#                     "age_group": age_group
#                 })

#             # Write metadata.csv
#             metadata_path = os.path.join(full_path, "metadata.csv")
#             with open(metadata_path, "w", newline='') as csvfile:
#                 fieldnames = ["id", "filename", "ethnicity", "age_group"]
#                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                 writer.writeheader()
#                 writer.writerows(new_rows)

#             print(f"✅ Processed {len(new_rows)} images in '{age_group}' and created metadata.csv.")


# # === MAIN ENTRY ===
# if __name__ == "__main__":
#     ethnicity = os.path.basename(DATASET_DIR)

#     if "synthetic_dataset" in DATASET_DIR:
#         relabel_existing_metadata(DATASET_DIR)

#     elif "aged_images" in DATASET_DIR:
#         cleanup_and_generate_metadata_by_subfolder(DATASET_DIR, ethnicity)

#     else:
#         print("❌ Unrecognized dataset type. Make sure the path contains 'synthetic_dataset' or 'aged_images'.")

# def cleanup_and_relabel(directory):
#     ethnicity = os.path.basename(os.path.dirname(directory))  # e.g., 'Southern European'
#     age_group = os.path.basename(directory)                   # e.g., '21-25'
#     image_files = sorted([
#         f for f in os.listdir(directory)
#         if f.lower().endswith((".jpg", ".jpeg", ".png"))
#     ])

#     new_rows = []
#     for idx, filename in enumerate(image_files, start=1):
#         ext = os.path.splitext(filename)[1].lower()
#         new_filename = f"img{idx:03d}{ext}"

#         old_path = os.path.join(directory, filename)
#         new_path = os.path.join(directory, new_filename)
#         os.rename(old_path, new_path)

#         new_rows.append({
#             "id": idx,
#             "filename": new_filename,
#             "ethnicity": ethnicity,
#             "age_group": age_group
#         })

#     metadata_path = os.path.join(directory, "metadata.csv")
#     with open(metadata_path, "w", newline='') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=["id", "filename", "ethnicity", "age_group"])
#         writer.writeheader()
#         writer.writerows(new_rows)

#     print(f"✅ [Flask] Cleaned and updated metadata in {directory}")

import os
import csv
import pandas as pd

# Set this to the dataset directory you want to clean
DATASET_DIR = "/home/hmc/pb543/diffusers/examples/dreambooth/synthetic_dataset/Filipino"

def relabel_existing_metadata(directory):
    metadata_path = os.path.join(directory, "metadata.csv")

    if not os.path.exists(metadata_path):
        print(f"❌ metadata.csv not found in {directory}. Cannot relabel.")
        return

    # Load metadata
    with open(metadata_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Relabel images and update metadata
    new_rows = []
    for idx, row in enumerate(rows, start=1):
        ext = os.path.splitext(row["filename"])[1].lower() or ".jpg"
        new_id = idx
        new_filename = f"img{new_id:03d}{ext}"

        # Rename image file
        old_path = os.path.join(directory, row["filename"])
        new_path = os.path.join(directory, new_filename)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)

        # Update metadata
        row["id"] = new_id
        row["filename"] = new_filename
        new_rows.append(row)

    # Save updated metadata
    with open(metadata_path, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_rows)

    print(f"🧼 Cleaned synthetic dataset in '{os.path.basename(directory)}' and updated metadata.csv.")


def cleanup_and_generate_metadata_by_subfolder(directory, ethnicity):
    # Load gender info from AgeTransGAN metadata
    gender_map = {}
    seed_metadata_path = os.path.join("AgeTransGAN images", ethnicity, "metadata.csv")
    if os.path.exists(seed_metadata_path):
        df = pd.read_csv(seed_metadata_path)
        gender_map = dict(zip(df["filename"], df["gender"]))

    for subdir in os.listdir(directory):
        full_path = os.path.join(directory, subdir)
        if os.path.isdir(full_path):
            age_group = subdir
            image_files = sorted([
                f for f in os.listdir(full_path)
                if f.lower().endswith((".jpg", ".jpeg", ".png"))
            ])

            new_rows = []
            for idx, old_filename in enumerate(image_files, start=1):
                ext = os.path.splitext(old_filename)[1].lower()
                new_filename = f"img{idx:03d}{ext}"

                old_path = os.path.join(full_path, old_filename)
                new_path = os.path.join(full_path, new_filename)
                os.rename(old_path, new_path)

                gender = gender_map.get(old_filename, "Unknown")

                new_rows.append({
                    "id": idx,
                    "filename": new_filename,
                    "ethnicity": ethnicity,
                    "age_group": age_group,
                    "gender": gender
                })

            metadata_path = os.path.join(full_path, "metadata.csv")
            with open(metadata_path, "w", newline='') as csvfile:
                fieldnames = ["id", "filename", "ethnicity", "age_group", "gender"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(new_rows)

            print(f"✅ Processed {len(new_rows)} images in '{age_group}' and created metadata.csv.")


def cleanup_and_relabel(directory):
    ethnicity = os.path.basename(os.path.dirname(directory))
    age_group = os.path.basename(directory)

    # Load gender info from AgeTransGAN metadata
    gender_map = {}
    seed_metadata_path = os.path.join("AgeTransGAN images", ethnicity, "metadata.csv")
    if os.path.exists(seed_metadata_path):
        df = pd.read_csv(seed_metadata_path)
        gender_map = dict(zip(df["filename"], df["gender"]))

    image_files = sorted([
        f for f in os.listdir(directory)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    new_rows = []
    for idx, filename in enumerate(image_files, start=1):
        ext = os.path.splitext(filename)[1].lower()
        new_filename = f"img{idx:03d}{ext}"

        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        os.rename(old_path, new_path)

        gender = gender_map.get(filename, "Unknown")

        new_rows.append({
            "id": idx,
            "filename": new_filename,
            "ethnicity": ethnicity,
            "age_group": age_group,
            "gender": gender
        })

    metadata_path = os.path.join(directory, "metadata.csv")
    with open(metadata_path, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "filename", "ethnicity", "age_group", "gender"])
        writer.writeheader()
        writer.writerows(new_rows)

    print(f"✅ [Flask] Cleaned and updated metadata in {directory}")

# === MAIN ENTRY ===
if __name__ == "__main__":
    ethnicity = os.path.basename(DATASET_DIR)

    if "synthetic_dataset" in DATASET_DIR:
        relabel_existing_metadata(DATASET_DIR)

    elif "aged_images" in DATASET_DIR:
        cleanup_and_generate_metadata_by_subfolder(DATASET_DIR, ethnicity)

    else:
        print("❌ Unrecognized dataset type. Make sure the path contains 'synthetic_dataset' or 'aged_images'.")
