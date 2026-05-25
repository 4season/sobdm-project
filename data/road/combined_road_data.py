import glob
import os
import pandas as pd

directory_path = './data/road/daily'
output_filename = 'road_combined_data.csv'
all_files = glob.glob(os.path.join(directory_path, '*.csv'))
print(f'Found {len(all_files)} files')

file_list = []
for file in all_files:
    df = pd.read_csv(file)
    file_list.append(df)

combined_df = pd.concat(file_list)

combined_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
print(f'Saved {output_filename} files')