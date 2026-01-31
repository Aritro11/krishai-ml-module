import pandas as pd

# --- Configuration ---
# The base dataset with crop, district, and yield info
crop_data_filename = 'crop_data_with_zones.csv'
# The climate data with rainfall and water deficit info
climate_data_filename = 'rainfall_with_water_deficit.csv'
# The name of the final merged file that will be created
output_filename = 'merged_ready3.csv'


try:
    # Step 1: Read the two datasets
    print("Reading datasets...")
    crop_df = pd.read_csv(crop_data_filename)
    climate_df = pd.read_csv(climate_data_filename)

    # Step 2: Perform a left merge on 'Year' and 'District'
    # This keeps all rows from the crop dataset and adds matching climate data
    print("Merging the two datasets...")
    final_df = pd.merge(crop_df, climate_df, on=['Year', 'District'], how='left')

    # Step 3: Fill any missing climate values with 0
    print("Filling any potential missing values with 0...")
    final_df.fillna(0, inplace=True)

    # Step 4: Save the final, merged dataset to a new CSV file
    final_df.to_csv(output_filename, index=False)

    print(f"\nSuccess! Your final master dataset has been saved as '{output_filename}'")
    print(f"The new dataset has {final_df.shape[0]} rows and {final_df.shape[1]} columns.")
    print("\nHere is a preview of your final merged data:")
    print(final_df.head())

except FileNotFoundError as e:
    print(f"\nError: A file was not found. Details: {e}")
    print("Please make sure all three files (the script and the two CSVs) are in the same folder.")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")