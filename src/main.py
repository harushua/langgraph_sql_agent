import os
from dotenv import load_dotenv
from pprint import pprint
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from src.database import setup_database
from src.graph import build_graph

# Load environment variables
load_dotenv()

def main():
    print("🚀 Initializing LangGraph SQL Agent 🚀")
    
    # 1. Setup Database
    db_name = "employee.db"
    setup_database(db_name)
    
    # 2. Initialize Models and Tools
    print("\n--- Initializing LLMs and Tools ---")
    llm_pro = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
    llm_flash = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    db = SQLDatabase.from_uri(f"sqlite:///{db_name}")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm_flash)
    sql_tools = toolkit.get_tools()

    # 3. Build and compile the graph
    print("\n--- Assembling the Graph ---")
    app = build_graph(llm_pro, sql_tools)
    print("Graph compiled successfully.")

    # 4. Run tests
    test_questions = [
        "Tell me the name of the employee who's salary is more than 55000?",
        "Show the phone numbers of customers whose last name is 'Smith'?",
        "List all orders made by John Doe.",
    ]

    for question in test_questions:
        print(f"\n\n--- TESTING QUESTION: '{question}' ---")
        inputs = {"messages": [HumanMessage(content=question)]}
        for output in app.stream(inputs, {"recursion_limit": 15}):
            for key, value in output.items():
                print(f"\n> Node '{key}':")
                pprint(value["messages"][-1].pretty_repr())
        print("\n--- END OF TEST ---")

if __name__ == "__main__":
    main()