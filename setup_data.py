import pandas as pd

# Load your uploaded dataset
df = pd.read_csv('global_air_quality_data_10000.csv')

# Add Day column and calculate AQI
df['Date'] = pd.date_range(start='2023-01-01', periods=len(df))
df.set_index('Date', inplace=True)
df['AQI'] = (df['PM2.5']*0.35 + df['PM10']*0.25 + df['NO2']*0.20 + 
             df['CO']*5.0 + df['SO2']*0.1 + df['O3']*0.1).round(2)

# Save the processed version
df.to_csv('data.csv', index=False)
print("✅ data.csv created with 10,000 records!")