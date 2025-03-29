import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter1d

open("../data/movement_analysis.csv", "w").close()
open("../data/seizure_detection_processed.csv", "w").close()

df = pd.read_csv("../data/landmarks_data.csv")
df = df.sort_values(by=["timestamp"])

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

movement_df = pd.DataFrame(movement_data, columns=["timestamp", "type", "index", "movement"])
movement_df.to_csv("../data/movement_analysis.csv", index=False)

df = pd.read_csv("../data/movement_analysis.csv")
df["timestamp"] -= df["timestamp"].min()

window_size = 100
detection_results = []

for body_part in df["type"].unique():
    subset = df[df["type"] == body_part].copy()
    subset["rolling_distance"] = subset["movement"].rolling(window=window_size, min_periods=1).sum()
    subset["rolling_variance"] = subset["movement"].rolling(window=window_size, min_periods=1).var()
    subset["smoothed_distance"] = gaussian_filter1d(subset["rolling_distance"], sigma=2)
    subset["smoothed_variance"] = gaussian_filter1d(subset["rolling_variance"], sigma=2)
    threshold = subset["smoothed_variance"].quantile(0.95)
    subset["seizure_alert"] = subset["smoothed_variance"] > threshold
    detection_results.append(subset)

final_df = pd.concat(detection_results)
final_df.to_csv("../data/seizure_detection_processed.csv", index=False)

alert_window_size = 10
final_df["rolling_alerts"] = final_df["seizure_alert"].rolling(window=alert_window_size, min_periods=1).sum()
final_df["seizure_alert_final"] = final_df["rolling_alerts"] > (alert_window_size / 2)

seizure_alerts = final_df[(final_df["seizure_alert_final"]) & (final_df["timestamp"] > 2)]

if not seizure_alerts.empty:
    for _, row in seizure_alerts.iterrows():
        print(f"Seizure ALERT at timestamp: {row['timestamp']}")
