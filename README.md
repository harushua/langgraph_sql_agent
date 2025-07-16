# LangGraph SQL Agent

This project demonstrates a sophisticated, autonomous agent built with **LangGraph** and **LangChain** that can interact with a SQL database. The agent takes natural language questions from a user, converts them into syntactically correct SQL queries, executes them against a database, and returns the final answer.

The key feature of this agent is its **corrective loop**. If an initial SQL query fails or returns an empty result, the agent is designed to analyze the error, rewrite the query, and try again until it successfully retrieves the information or determines the answer isn't available.

## Architecture

The agent's workflow is orchestrated as a stateful graph:
1.  **Agent Node**: The primary "brain" of the agent. It receives the user's question and the database schema, then generates a SQL query using a powerful LLM (**Google Gemini 1.5 Pro**). It decides whether to query the database or submit a final answer.
2.  **Tool Node**: This node executes the SQL tools called by the agent (e.g., `sql_db_query`, `sql_db_schema`).
3.  **Conditional Edge (Router)**: After the agent node runs, this router checks if a tool was called.
    - If YES, it routes the workflow to the `Tool Node`.
    - If NO (meaning the agent has a final answer), it ends the execution.
4.  **Correction Loop**: After the `Tool Node` executes a query, the workflow loops back to the `Agent Node`. The agent can then see the result (or error) of its query and decide its next step: either formulate a final answer or generate a corrected query.

## Technologies Used
- **Orchestration:** LangGraph
- **AI Framework:** LangChain
- **LLM:** Google Gemini 1.5 Pro
- **Tools:** LangChain SQLDatabaseToolkit
- **Database:** SQLite

## Setup & Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/langgraph-sql-agent.git](https://github.com/YOUR_USERNAME/langgraph-sql-agent.git)
    cd langgraph-sql-agent
    ```
2.  Create and activate a Python virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file in the root directory and add your Google API key:
    ```
    GOOGLE_API_KEY="your_google_api_key_here"
    ```

## How to Run
Execute the main application script from the root directory. The script will automatically set up the database and run a series of test questions.
```bash
python src/main.py