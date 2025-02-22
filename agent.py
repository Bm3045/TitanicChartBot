from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("train.csv")

# Function to get Titanic stats
def get_gender_percentage():
    male_percentage = (df['Sex'] == 'male').mean() * 100
    female_percentage = 100 - male_percentage
    return f"Male: {male_percentage:.2f}%, Female: {female_percentage:.2f}%"

def get_average_fare():
    return f"Average fare: ${df['Fare'].mean():.2f}"

def get_port_counts():
    return df['Embarked'].value_counts().to_dict()

# Define tools
tools = [
    Tool(name="Get Gender Percentage", func=get_gender_percentage, description="Returns percentage of male and female passengers"),
    Tool(name="Get Average Fare", func=get_average_fare, description="Returns the average ticket fare"),
    Tool(name="Get Port Counts", func=get_port_counts, description="Returns the number of passengers per embarkation port"),
]

# Initialize LangChain Agent
llm = ChatOpenAI(model_name="gpt-4", temperature=0)
agent = initialize_agent(tools=tools, llm=llm, agent="zero-shot-react-description", verbose=True)
