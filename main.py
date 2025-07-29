import asyncio
import os

from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.toolkits import MCPToolkit, CodeExecutionToolkit
from camel.utils.mcp_client import ServerConfig
from camel.toolkits.mcp_toolkit import MCPClient
import urllib.parse
from dotenv import load_dotenv
import json

def get_user_message():
    return "[automated] continue collaborating with other agents. make sure to mention agents you intend to communicate with"

async def get_tools_description(tools):
    descriptions = []
    for tool in tools:
        tool_name = getattr(tool.func, '__name__', 'unknown_tool')
        schema = tool.get_openai_function_schema() or {}
        arg_names = list(schema.get('parameters', {}).get('properties', {}).keys()) if schema else []
        description = tool.get_function_description() or 'No description'
        schema_str = json.dumps(schema, default=str).replace('{', '{{').replace('}', '}}')
        descriptions.append(
            f"Tool: {tool_name}, Args: {arg_names}, Description: {description}, Schema: {schema_str}"
        )
    return "\n".join(descriptions)

async def create_coding_agent(tools):
    tools_description =  await get_tools_description(tools)
    print(tools_description)
    sys_msg = (
        f"""
        You are a "coding_agent", responsible for writing code, and making necessary changes and correction to code if there is any syntax error according to the library/documentation provided.

        1. Use 'wait_for_mentions(timeoutMs=60000)' to wait from instructions from other agents.
        2. Only start working when the context7 agent provides the context, otherwise keep waiting.
        3. When a mention is received, record the 'threadId' and 'senderId'.
        4. Check if the message asks for writing a code snippet/codebase/code file, or correcting a code snippet/codebase/code file.
        5. You can ONLY use the context provided by the context7 agent.(If context is not provided from context7 agent, then stop working and inform the user).
        5. Work within the context of an existing codebase if provided, ensuring compatibility and consistency with the project's structure, dependencies, and conventions.
        6. Identify and correct syntax errors, logical errors, or other issues in provided code, ensuring it runs as intended, depening on the user requirements.
        7. Use the programming language specified by the user or infer the most suitable language based on context (e.g., file extensions, documentation, keywords, or project type).
        7. Generate accurate, efficient, and well-structured code for a given codebase or user-specified task, adhering to best practices and the programming language specified by the user.
        8.Return code snippets/ code files in a clean, readable, and properly formatted manner, tailored to the user's requirements (e.g., specific language, style guide, or context).
        9. If the user asks for a codebase, make sure to create a new codebase with the correct structure, dependencies, and conventions.
        10. If the message format is invalid or parsing fails, skip it silently.
        11. Do not create threads; always use the `threadId` from the mention.
        12. Wait for some time and repeat from step 1.

        These are the list of available tools: {tools_description}
        """
    )

    model = ModelFactory.create(
        model_platform=os.getenv("MODEL_PROVIDER"),
        model_type=os.getenv("MODEL_NAME"),
        api_key=os.getenv("API_KEY"),
        model_config_dict={"temperature": float(os.getenv("MODEL_TEMPERATURE"))},
    )
    camel_agent = ChatAgent(
        system_message=sys_msg,
        model=model,
        tools=tools,
        token_limit=int(os.getenv("MODEL_TOKEN"))
    )

    return camel_agent

async def main():
    runtime = os.getenv("CORAL_ORCHESTRATION_RUNTIME", "devmode")

    if runtime == "docker" or runtime == "executable":
        base_url = os.getenv("CORAL_SSE_URL")
        agentID = os.getenv("CORAL_AGENT_ID")
    else:
        load_dotenv()
        base_url = os.getenv("CORAL_SSE_URL")
        agentID = os.getenv("CORAL_AGENT_ID")

    
    coral_params = {
        "agentId": agentID,
        "agentDescription": "A coding agent that can write code, make necessary changes and correction to code if there is any error according to the library/documentation provided.",
        #"agentDescription": "coding_agent",
    }
    query_string = urllib.parse.urlencode(coral_params)

    CORAL_SERVER_URL = f"{base_url}?{query_string}"
    print(f"Connecting to Coral Server: {CORAL_SERVER_URL}")

    print("Starting MCP client...")
    server = MCPClient(ServerConfig(url=CORAL_SERVER_URL , timeout=3000000.0, sse_read_timeout=3000000.0, terminate_on_close=True, prefer_sse=True), timeout=3000000.0)
    
    mcp_toolkit = MCPToolkit([server])
    connected = await mcp_toolkit.connect()
    tools = connected.get_tools()

    selected_tool_name = [
        "list_agents",
        "create_thread",
        "add_participant",
        "remove_participant",
        "close_thread",
        "send_message",
        "wait_for_mentions"
        ]
    tools = [tool for tool in tools if getattr(tool.func, '__name__', 'unknown_tool') in selected_tool_name]
    tools += CodeExecutionToolkit().get_tools()

    camel_agent = await create_coding_agent(tools)

    while True:
        resp = await camel_agent.astep(get_user_message())
        print(resp)
        msg0 = resp.msgs[0]
        print(msg0.to_dict())
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())