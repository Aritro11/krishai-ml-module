import pandas as pd

def merge_zone_data_fixed():
    """
    This script merges the reshaped crop data with the district-wise
    agro-climactic zone data, with robust cleaning of column and district names.
    """
    try:
        crop_data = pd.read_csv("reshaped_crop_data.csv")
        zones_data = pd.read_csv("District Wise AgroClimactic Zones.csv")
        print("Successfully loaded 'reshaped_crop_data.csv' and 'District Wise AgroClimactic Zones.csv'.")

    except FileNotFoundError as e:
        print(f"Error: A required file was not found. Please ensure both CSVs are in the same folder.")
        print(f"Missing file: {e.filename}")
        return
    except Exception as e:
        print(f"An error occurred during file loading: {e}")
        return

    # --- Robust Column and District Name Cleaning (THE FIX IS HERE) ---
    print("\n--- Cleaning Column and District Names ---")

    # 1. Clean the column names of the zones_data DataFrame
    # This removes leading/trailing spaces, a common source of KeyErrors.
    zones_data.columns = [col.strip() for col in zones_data.columns]
    
    # Verify the cleaned column names
    print(f"Cleaned column names for zones data: {zones_data.columns.tolist()}")
    
    # 2. Standardize district names in BOTH dataframes for a clean merge
    # Specifically handle the complex "Phulbani ( Kandhamal )" case
    crop_data['District'].replace({'Phulbani ( Kandhamal )': 'Kandhamal'}, inplace=True)
    
    # Align other potential mismatches
    name_corrections = {
        'Baleshwar': 'Balasore',
        'Bolangir': 'Balangir', # As seen in your traceback
        'Keonjhar': 'Keonjar',  # Align to the older name if needed
        # Add any other required mappings here
    }
    zones_data['District'] = zones_data['District'].replace(name_corrections)
    print("Standardized district names for accurate merging.")


    # --- Merge the datasets ---
    print("--- Merging Datasets ---")
    merged_df = pd.merge(crop_data, zones_data, on='District', how='left')
    print("Merge complete.")

    # --- Verification ---
    # This block should now work correctly
    if 'Agro_Climactic_Zone' not in merged_df.columns:
        print("\nFATAL ERROR: 'Agro_Climactic_Zone' column is still missing after the merge. Please check the column name in 'District Wise AgroClimactic Zones.csv'")
        return
        
    missing_zones = merged_df[merged_df['Agro_Climactic_Zone'].isnull()]
    if not missing_zones.empty:
        print("\nWarning: Some districts did not have a matching zone:")
        print(missing_zones['District'].unique())
    else:
        print("Successfully matched an agro-climactic zone for all districts.")

    # --- Final Touches ---
    final_df = merged_df[['Crop Type', 'District', 'Agro_Climactic_Zone', 'Year', 'AREA', 'YIELD']]

    output_filename = "crop_data_with_zones.csv"
    final_df.to_csv(output_filename, index=False)

    print(f"\nSuccessfully created the final dataset!")
    print(f"==> Check for the output file: '{output_filename}' <==")
    print("\n--- Final Merged DataFrame (First 5 Rows) ---")
    print(final_df.head())

if __name__ == '__main__':
    merge_zone_data_fixed()