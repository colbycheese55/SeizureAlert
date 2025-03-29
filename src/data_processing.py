import pandas as pd
import numpy as np

# Load landmark data
df = pd.read_csv("../data/landmarks_data.csv")

# Sort by timestamp
df = df.sort_values(by=["timestamp"])

# Calculate movement between consecutive frames
movement_data = []
for landmark_type in ["hand", "face", "pose"]:
    df_subset = df[df["type"] == landmark_type]
    
    prev_frame = None
    for index, row in df_subset.iterrows():
        if prev_frame is not None:
            dist = np.sqrt(
                (row["x"] - prev_frame["x"])**2 +
                (row["y"] - prev_frame["y"])**2 +
                (row["z"] - prev_frame["z"])**2
            )
            movement_data.append([row["timestamp"], landmark_type, row["index"], dist])
        
        prev_frame = row

# Convert to DataFrame
movement_df = pd.DataFrame(movement_data, columns=["timestamp", "type", "index", "movement"])
print(movement_df)

# Save to CSV
movement_df.to_csv("movement_analysis.csv", index=False)
