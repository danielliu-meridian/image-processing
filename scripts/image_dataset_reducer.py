import os
import random
import shutil
import zipfile
import argparse
import re
from collections import defaultdict

# Function to reduce the dataset
def reduce_dataset(input_dir, output_dir, reduction_factor):
    # set a fixed seed for reproducibility
    random.seed(42)

    # regular expression to extract the folder type
    # only look for train, val or test in the folder name
    folder_type_pattern = re.compile(r'(train|val|test)')

    # store the files in each folder type
    folder_files = defaultdict(list)
    for root, dirs, files in os.walk(input_dir):
        if not files:
            continue
        
        folder_name = os.path.basename(root)
        match = folder_type_pattern.search(folder_name)
        if match:
            folder_type = match.group(1)
            folder_files[folder_type].append((root, files))

    # process each folder type
    for folder_type, folder_list in folder_files.items():
        if not folder_list:
            continue
        
        num_files = len(folder_list[0][1])
        print('num_files', num_files)
        num_select = max(1, num_files // reduction_factor)
        print('num_select', num_select)
        selected_indices = sorted(random.sample(range(num_files), num_select))

        # apply the same selection to all folder of this type
        for root, files in folder_list:
            rel_path = os.path.relpath(root, input_dir)
            out_dir = os.path.join(output_dir, rel_path)
            os.makedirs(out_dir, exist_ok=True)

            for index in selected_indices:
                file = files[index]
                src_file = os.path.join(root, file)
                dst_file = os.path.join(out_dir, file)
                shutil.copy(src_file, dst_file)
    
    print(f"Reduced dataset created at {output_dir}")
    # reset the seed
    random.seed()

# extract the dataset from the zip file
# reduce the dataset
# create a new zip file with the same folder structure
def main(input_zip, reduction_factor):
    # extract the dataset
    input_dir = os.path.join('data', 'input_dataset')
    with zipfile.ZipFile(input_zip, 'r') as zip_ref:
        zip_ref.extractall(input_dir)

    # reduce the dataset
    output_dir = os.path.join('data', 'output_dataset')
    reduce_dataset(input_dir, output_dir, reduction_factor)

    # create the data folder if it does not exist
    data_folder = 'data'
    os.makedirs(data_folder, exist_ok=True)

    # create a new zip file
    output_zip = os.path.join(data_folder, f'reduced_dataset_1_{reduction_factor}.zip')
    with zipfile.ZipFile(output_zip, 'w') as zip_ref_1:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                zip_ref_1.write(os.path.join(root, file),
                                os.path.relpath(os.path.join(root, file), output_dir))

    print(f"Reduced dataset saved at {output_zip}")

    # clean up
    shutil.rmtree(input_dir)
    shutil.rmtree(output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reduce the size of a dataset in a zip file.")
    parser.add_argument("input_zip", help="Path to the input zip file")
    parser.add_argument("reduction_factor", type=int, choices=[2, 4, 8], 
                        help="Reduction factor (2, 4, or 8)")
    args = parser.parse_args()

    main(args.input_zip, args.reduction_factor)