# Weather Data Analysis System - analysis script (FIXED VERSION v3)
# Run from inside the weather-app folder:  python main.py
import os

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

print("Weather Data Analysis System  [fixed version v3]")

os.makedirs("charts", exist_ok=True)   # every chart is also saved here as a PNG file


def finish(fig, filename):
    """Save the chart, show it, and close it so charts never overlap."""
    fig.tight_layout()
    fig.savefig(os.path.join("charts", filename), dpi=150)
    if "agg" not in matplotlib.get_backend().lower():   # only show when a window is possible
        plt.show()
    plt.close(fig)


# ---------------- Load and clean data ----------------
df = pd.read_csv("data/weather.csv")
print("Duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.month_name()
df["Temperature_F"] = (df["Temperature"] * 9 / 5) + 32
print(df)

# ---------------- Statistics ----------------
average_temperature = df["Temperature"].mean()
print("Average Temperature:", average_temperature)
maximum_temperature = df["Temperature"].max()
minimum_temperature = df["Temperature"].min()
print("Maximum Temperature:", maximum_temperature)
print("Minimum Temperature:", minimum_temperature)
average_humidity = df["Humidity"].mean()
print("Average Humidity:", average_humidity)
average_wind_speed = df["WindSpeed"].mean()
print("Average Wind Speed:", average_wind_speed)
total_precipitation = df["Precipitation"].sum()
print("Total Precipitation:", total_precipitation)
print(df["Weather"].value_counts())

# ---------------- Charts (each chart has its OWN figure) ----------------
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["Date"], df["Temperature"])
ax.set_xlabel("Date")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Temperature Trend")
finish(fig, "temperature_trend.png")

weather_counts = df["Weather"].value_counts()
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(weather_counts.index.astype(str), weather_counts.values)
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Number of Records")
ax.set_title("Weather Condition Distribution")
finish(fig, "weather_distribution.png")

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df["Date"], df["Precipitation"])
ax.set_xlabel("Date")
ax.set_ylabel("Precipitation (mm)")
ax.set_title("Daily Precipitation")
finish(fig, "daily_precipitation.png")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["Date"], df["Humidity"])
ax.set_xlabel("Date")
ax.set_ylabel("Humidity (%)")
ax.set_title("Humidity Trend")
finish(fig, "humidity_trend.png")

correlation = df[["Temperature", "Humidity", "WindSpeed", "Precipitation"]].corr()
print(correlation)

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Weather Feature Correlation")
finish(fig, "correlation_heatmap.png")

print("Done. Charts saved in the 'charts' folder.")
