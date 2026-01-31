import pandas as pd
import math

# Read the original CSV file
df = pd.read_csv('Crop_recommendation_with_soil_types.csv')

def simplify_npk_ratios(n, p, k):
    """Convert NPK values to simplified integer ratios by dividing by smallest value and rounding up"""
    # Handle edge cases
    if n == 0 and p == 0 and k == 0:
        return 1, 1, 1
    
    # Find the minimum non-zero value
    min_val = min([x for x in [n, p, k] if x > 0], default=1)
    
    # Divide by minimum and round up to ensure no zeros
    n_ratio = max(1, math.ceil(n / min_val)) if n > 0 else 1
    p_ratio = max(1, math.ceil(p / min_val)) if p > 0 else 1
    k_ratio = max(1, math.ceil(k / min_val)) if k > 0 else 1
    
    return n_ratio, p_ratio, k_ratio

# Apply the simplification to all rows
simplified_ratios = []
for index, row in df.iterrows():
    n_ratio, p_ratio, k_ratio = simplify_npk_ratios(row['N'], row['P'], row['K'])
    simplified_ratios.append((n_ratio, p_ratio, k_ratio))

# Create new dataframe with simplified ratios
df_simplified = df.copy()
df_simplified[['N', 'P', 'K']] = simplified_ratios

# Save to CSV
df_simplified.to_csv('Crop_recommendation_NPK_simplified_ratios.csv', index=False)
print("File saved as: Crop_recommendation_NPK_simplified_ratios.csv")
