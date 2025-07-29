## [Coral Coding Agent](https://github.com/Coral-Protocol/Coral-Coding-Agent)

The Coral Coding Agent is capable of writing code, making necessary changes and corrections to code if there are any syntax errors according to the library/documentation provided by other agents.

## Responsibility

The Coral Coding Agent is responsible for writing code, making necessary changes and corrections to code if there are any syntax errors according to the library/documentation provided. It collaborates with other agents, particularly the Context7 agent, to receive context and documentation for generating accurate and efficient code.

Below are the tools and their descriptions:


**Code Execution Tools**: The agent uses code execution tools to:
- Write and execute code snippets
- Create new codebases with proper structure
- Correct syntax errors and logical issues
- Generate well-structured code following best practices

## Details
- **Framework**: CAMEL-AI
- **Tools used**: Coral Server Tools, Code Execution Tools
- **AI model**: OpenAI GPT-4o
- **Date added**: July 29, 2025
- **Reference**: [Coral Protocol](https://github.com/Coral-Protocol)
- **License**: MIT

## Setup the Agent

### 1. Clone & Install Dependencies

<details>

Ensure that the [Coral Server](https://github.com/Coral-Protocol/coral-server) is running on your system. If you are trying to run Open Deep Research agent and require an input, you can either create your agent which communicates on the coral server or run and register the [Interface Agent](https://github.com/Coral-Protocol/Coral-Interface-Agent) on the Coral Server  


```bash
# In a new terminal clone the repository:
git clone https://github.com/Coral-Protocol/Coral-Coding-Agent.git

# Navigate to the project directory:
cd Coral-Coding-Agent

# Download and run the UV installer, setting the installation directory to the current one
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=$(pwd) sh

# Create a virtual environment named `.venv` using UV
uv venv .venv

# Activate the virtual environment
source .venv/bin/activate

# install uv
pip install uv

# Install dependencies from `pyproject.toml` using `uv`:
uv sync
```

</details>

### 2. Configure Environment Variables

<details>

Get the API Key:
[OpenAI](https://platform.openai.com/api-keys)

```bash
# Create .env file in project root
cp -r .env_sample .env
```

Check if the .env file has correct URL for Coral Server and adjust the parameters accordingly.

</details>

## Run the Agent

You can run in either of the below modes to get your system running.  

- The Executable Model is part of the Coral Protocol Orchestrator which works with [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio).  
- The Dev Mode allows the Coral Server and all agents to be separately running on each terminal without UI support.  

### 1. Executable Mode

Checkout: [How to Build a Multi-Agent System with Awesome Open Source Agents using Coral Protocol](https://github.com/Coral-Protocol/existing-agent-sessions-tutorial-private-temp) and update the file: `coral-server/src/main/resources/application.yaml` with the details below, then run the [Coral Server](https://github.com/Coral-Protocol/coral-server) and [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio). You do not need to set up the `.env` in the project directory for running in this mode; it will be captured through the variables below.

<details>

For Linux or MAC:

```bash
# PROJECT_DIR="/PATH/TO/YOUR/PROJECT"

applications:
  - id: "app"
    name: "Default Application"
    description: "Default application for testing"
    privacyKeys:
      - "default-key"
      - "public"
      - "priv"

registry:
  coral_coding_agent:
    options:
      - name: "API_KEY"
        type: "string"
        description: "API key for the service"
    runtime:
      type: "executable"
      command: ["bash", "-c", "${PROJECT_DIR}/run_agent.sh main.py"]
      environment:
        - name: "API_KEY"
          from: "API_KEY"
        - name: "MODEL_NAME"
          value: "gpt-4.1"
        - name: "MODEL_PROVIDER"
          value: "openai"
        - name: "MODEL_TOKEN"
          value: "16000"
        - name: "MODEL_TEMPERATURE"
          value: "0.3"

```
For Windows, create a powershell command (run_agent.ps1) and run:

```bash
command: ["powershell","-ExecutionPolicy", "Bypass", "-File", "${PROJECT_DIR}/run_agent.ps1","main.py"]
```

</details>

### 2. Dev Mode

Ensure that the [Coral Server](https://github.com/Coral-Protocol/coral-server) is running on your system and run below command in a separate terminal.

<details>

```bash
# Run the agent using `uv`:
uv run python main.py
```

You can view the agents running in Dev Mode using the [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio) by running it separately in a new terminal.

</details>


## Example

<details>

```bash
# Input:
Fix the issues in the code file @<reference of opened code file in editor>

# Output:
I've analyzed the code file and identified several issues. Here are the fixes:

## Issues Found:
1. Missing import statement for `requests` library
2. Undefined variable `api_key` in the function
3. Incorrect indentation in the try-except block
4. Missing error handling for API response

## Fixed Code:

```python
import requests
import json

def fetch_user_data(user_id, api_key):
    """
    Fetch user data from API
    """
    url = f"https://api.example.com/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return None

# Usage example
user_data = fetch_user_data(123, "your_api_key_here")
if user_data:
    print(f"User name: {user_data.get('name', 'Unknown')}")
```

## Changes Made:
- Added `import requests` at the top
- Added `api_key` parameter to function signature
- Fixed indentation in try-except block
- Added proper error handling for both network and JSON parsing errors
- Added docstring for better documentation
- Added usage example with proper error checking

</details>

```

### Creator Details
- **Name**: Mustafa Khan
- **Affiliation**: Coral Protocol
- **Contact**: [Discord](https://discord.com/invite/Xjm892dtt3)

