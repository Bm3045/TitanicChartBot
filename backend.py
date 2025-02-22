from fastapi import FastAPI
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = FastAPI()

# Load Titanic dataset
df = pd.read_csv("train.csv")

# Function to get gender percentage
def get_gender_percentage():
    male_percentage = (df['Sex'] == 'male').mean() * 100
    female_percentage = 100 - male_percentage
    return f"Male: {male_percentage:.2f}%, Female: {female_percentage:.2f}%"

# Function to generate a histogram of ages
def get_age_histogram():
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Age'].dropna(), bins=20, kde=True)
    plt.xlabel("Age")
    plt.ylabel("Count")
    plt.title("Distribution of Passenger Ages")

    # Save plot to a byte buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    return {"image": image_base64}

# Function to get average fare
def get_average_fare():
    return f"Average fare: ${df['Fare'].mean():.2f}"

# Function to get number of passengers per embarkation port
def get_port_counts():
    return df['Embarked'].value_counts().to_dict()

# API Endpoint for user queries
@app.get("/query")
def query(text: str):
    if "percentage of passengers were male" in text.lower():
        return {"answer": get_gender_percentage()}
    elif "histogram of passenger ages" in text.lower():
        return get_age_histogram()  # Returns an image in base64
    elif "average ticket fare" in text.lower():
        return {"answer": get_average_fare()}
    elif "passengers embarked from each port" in text.lower():
        return {"answer": get_port_counts()}
    else:
        return {"answer": "I don't understand your question. Please ask about Titanic statistics!"}


