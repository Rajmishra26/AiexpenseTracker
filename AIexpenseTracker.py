from pydantic import BaseModel
from typing import Literal
from langchain_openai import ChatOpenAI  # Instead of langchain.chat_models
import os

# Set up OpenAI API key (Ensure you have an API key)
os.environ["OPENAI_API_KEY"] = "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"  # Replace with your actual API key

# Define the Pydantic model for an expense entry
class Expense(BaseModel):
    description: str
    amount: float

# Define the Pydantic model for categorized expense output
class CategorizedExpense(BaseModel):
    description: str
    amount: float
    category: Literal["Food", "Transport", "Shopping", "Bills", "Entertainment", "Others"]

# Initialize OpenAI LLM model
llm = ChatOpenAI(model_name="gpt-3.5-turbo")

# Function to categorize expenses using AI + Keyword Matching
def categorize_expense(expense: Expense) -> CategorizedExpense:
    # Keyword-based categorization (fallback)
    category_map = {
        "food": "Food",
        "restaurant": "Food",
        "uber": "Transport",
        "bus": "Transport",
        "train": "Transport",
        "flight": "Transport",
        "amazon": "Shopping",
        "clothes": "Shopping",
        "electricity": "Bills",
        "water bill": "Bills",
        "netflix": "Entertainment",
        "movie": "Entertainment",
    }
    
    # Check for keyword match first
    category = "Others"
    for key, cat in category_map.items():
        if key in expense.description.lower():
            category = cat
            break
    
    # If keyword matching fails, use AI for context-based categorization
    if category == "Others":
        prompt = (
            f"Categorize this expense: '{expense.description}'. "
            "Possible categories: Food, Transport, Shopping, Bills, Entertainment, Others. "
            "Think carefully and classify correctly."
        )
        category = llm.invoke(prompt).strip()

    return CategorizedExpense(**expense.model_dump(), category=category)

# Example Usage
expense = Expense(description="eating pizza", amount=1000)
categorized_expense = categorize_expense(expense)

print(categorized_expense)
