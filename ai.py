import json
import requests
import os

# GitHub raw link to current affairs dataset
CURRENT_AFFAIRS_URL = "https://raw.githubusercontent.com/utkarshdubey2008/LectLo1/main/datasets/current_affairs.json"

# Directory to save updated dataset locally
LOCAL_DATA_DIR = "datasets"
LOCAL_FILE_PATH = os.path.join(LOCAL_DATA_DIR, "current_affairs.json")

# Create directory if not exists
if not os.path.exists(LOCAL_DATA_DIR):
    os.makedirs(LOCAL_DATA_DIR)

# Function to load dataset from GitHub or local storage
def load_dataset():
    if os.path.exists(LOCAL_FILE_PATH):
        with open(LOCAL_FILE_PATH, "r") as f:
            return json.load(f)
    else:
        response = requests.get(CURRENT_AFFAIRS_URL)
        if response.status_code == 200:
            data = response.json()
            with open(LOCAL_FILE_PATH, "w") as f:
                json.dump(data, f, indent=4)
            return data
        else:
            return {"world_leaders": []}

# Function to find an answer in the dataset
def find_answer(question, dataset):
    question = question.lower()
    if question == "world leaders":
        return dataset["world_leaders"]
    return None

# Function to update dataset locally
def update_dataset(new_leader, dataset):
    dataset["world_leaders"].append(new_leader)

    # Save to local file
    with open(LOCAL_FILE_PATH, "w") as f:
        json.dump(dataset, f, indent=4)

    print("\n✅ Leader added successfully!\n")

# Main chatbot loop
def chatbot():
    dataset = load_dataset()
    print("🤖 AI Chatbot (Type 'exit' to quit)\n")

    while True:
        user_input = input("You: ").strip().lower()
        if user_input == "exit":
            print("👋 Goodbye!")
            break
        
        answer = find_answer(user_input, dataset)
        if answer:
            for leader in answer:
                print(f"🇨🇳 {leader['country']}: {leader['position']} - {leader['name']}")
        else:
            print("Bot: I don't have information on that.")
            add_leader = input("❓ Do you want to add a world leader? (yes/no): ").strip().lower()
            if add_leader == "yes":
                country = input("Enter country: ").strip()
                position = input("Enter position: ").strip()
                name = input("Enter leader's name: ").strip()
                
                new_leader = {
                    "country": country,
                    "position": position,
                    "name": name
                }
                
                update_dataset(new_leader, dataset)

# Run chatbot
chatbot()
