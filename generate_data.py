# Import necessary libraries
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- Configuration ---
NUM_ROWS = 550
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)
CHANNELS = ['Social Media', 'Search Engine', 'Email', 'Display Ads', 'Referral', 'Video Ads']

# *** MODIFIED PART: Use recognizable geographic locations ***
# Example using US States for better map compatibility
REGIONS = [
    'California', 'Texas', 'Florida', 'New York', 'Pennsylvania',
    'Illinois', 'Ohio', 'Georgia', 'North Carolina', 'Michigan',
    'New Jersey', 'Virginia', 'Washington', 'Arizona', 'Massachusetts'
]
# You could also use countries, major cities, etc., depending on the desired scope.

CAMPAIGN_ID_PREFIX = 'CAMP_'

# Base performance metrics (mean values, will add randomness) - REMAINS THE SAME
BASE_METRICS = {
    'Social Media': {'impressions': 50000, 'ctr': 0.02, 'conv_rate': 0.03, 'cpc': 0.5, 'avg_revenue_per_conv': 50},
    'Search Engine': {'impressions': 30000, 'ctr': 0.05, 'conv_rate': 0.07, 'cpc': 1.2, 'avg_revenue_per_conv': 80},
    'Email': {'impressions': 10000, 'ctr': 0.10, 'conv_rate': 0.05, 'cpc': 0.1, 'avg_revenue_per_conv': 60},
    'Display Ads': {'impressions': 80000, 'ctr': 0.005, 'conv_rate': 0.015, 'cpc': 0.3, 'avg_revenue_per_conv': 40},
    'Referral': {'impressions': 5000, 'ctr': 0.15, 'conv_rate': 0.10, 'cpc': 0.05, 'avg_revenue_per_conv': 70},
    'Video Ads': {'impressions': 60000, 'ctr': 0.01, 'conv_rate': 0.02, 'cpc': 0.8, 'avg_revenue_per_conv': 55}
}

# --- Data Generation ---
data = []
date_range = [START_DATE + timedelta(days=x) for x in range((END_DATE - START_DATE).days + 1)]

for i in range(NUM_ROWS):
    campaign_id = f"{CAMPAIGN_ID_PREFIX}{i+1:03d}"
    channel = random.choice(CHANNELS)
    region = random.choice(REGIONS) # This will now pick a US State
    date = random.choice(date_range)

    # Get base metrics for the channel - REMAINS THE SAME
    base = BASE_METRICS[channel]

    # Add randomness - REMAINS THE SAME
    impressions = max(100, int(np.random.normal(base['impressions'], base['impressions'] * 0.3)))
    actual_ctr = max(0.001, np.random.normal(base['ctr'], base['ctr'] * 0.2))
    clicks = min(impressions, max(0, int(impressions * actual_ctr)))
    actual_conv_rate = max(0.001, np.random.normal(base['conv_rate'], base['conv_rate'] * 0.25))
    conversions = min(clicks, max(0, int(clicks * actual_conv_rate)))
    actual_cpc = max(0.01, np.random.normal(base['cpc'], base['cpc'] * 0.3))
    cost = round(clicks * actual_cpc, 2)
    avg_rev = max(5, np.random.normal(base['avg_revenue_per_conv'], base['avg_revenue_per_conv'] * 0.3))
    revenue = round(conversions * avg_rev, 2)
    if random.random() < 0.05:
        clicks = 0; conversions = 0; cost = 0.0; revenue = 0.0
    elif random.random() < 0.08:
        conversions = 0; revenue = 0.0

    data.append([
        campaign_id, channel, impressions, clicks, conversions, cost, revenue, region, date
    ])

# Create DataFrame - REMAINS THE SAME
df = pd.DataFrame(data, columns=[
    'Campaign_ID', 'Channel', 'Impressions', 'Clicks', 'Conversions', 'Cost', 'Revenue', 'Region', 'Date'
])

# Introduce some missing values for cleaning practice - REMAINS THE SAME
for col in ['Impressions', 'Clicks', 'Conversions', 'Cost', 'Revenue']:
    if df[col].isnull().sum() < int(NUM_ROWS * 0.03): # Ensure we don't add too many NaNs
      nan_indices = df.sample(frac=0.03).index # 3% missing values
      df.loc[nan_indices, col] = np.nan

# Convert Date to datetime objects just in case - REMAINS THE SAME
df['Date'] = pd.to_datetime(df['Date'])

# --- Save the raw dataset ---
raw_file_path = 'marketing_campaign_data_raw.csv'
df.to_csv(raw_file_path, index=False)

print(f"Raw synthetic dataset with {len(df)} rows saved to '{raw_file_path}'")
print("Sample row with updated Region:")
print(df.head(1)) # Print just one row to show the new region format