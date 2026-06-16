"""
Challenge 5 (Innovate): Build Your Own MCP-Powered Agent

YOUR TASK:
  Build an innovative agent from scratch that connects to any MCP server.
  The most creative and useful agent gets a special shoutout! 🏆

RULES:
  - Must use Strands Agents SDK
  - Must use at least one MCP server
  - Must use Amazon Nova Pro (or any Bedrock model)
  - Must have an interactive chat loop
  - Must be YOUR OWN idea — be creative!

EXAMPLE MCP SERVERS:
  pip install awslabs.aws-documentation-mcp-server   # AWS Docs
  uvx awslabs.cdk-mcp-server@latest                  # AWS CDK
  uvx awslabs.cost-analysis-mcp-server@latest        # AWS Pricing

BROWSE MORE: https://github.com/modelcontextprotocol/servers

RESOURCES:
  - Strands MCP docs: https://strandsagents.com/latest/user-guide/concepts/tools/mcp-tools/
  - AWS MCP servers: https://github.com/awslabs/mcp

Build something that makes us go "whoa!" 🚀
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

MODEL = "us.amazon.nova-pro-v1:0"

# ============================================================
# Connect to the AWS Documentation MCP server
# ============================================================
# THE FIX: We use cmd.exe /c to force Windows to find the uvx executable properly
server_params = StdioServerParameters(
    command="cmd.exe",
    args=["/c", "uvx", "awslabs.aws-documentation-mcp-server@latest"],
    env={"FASTMCP_LOG_LEVEL": "ERROR"}
)

# Strands requires a lambda that returns the active stdio_client connection
docs_mcp_client = MCPClient(lambda: stdio_client(server_params))

# ============================================================
# Create the AWS Docs Agent
# ============================================================
agent = Agent(
    model=MODEL,
    tools=[docs_mcp_client],
    system_prompt="""You are an AWS documentation expert! 📚
You have access to the official AWS documentation via MCP tools.
Help users understand AWS services, find docs, and answer technical questions.
Always cite which AWS service or doc you're referencing."""
)

# ============================================================
# Interactive Chat Loop
# ============================================================
print("📚 AWS Docs Chatbot — powered by MCP")
print("Ask me anything about AWS! Type 'quit' to exit.\n")

while True:
    try:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye! 👋")
            break
            
        if not user_input:
            continue
            
        # The agent automatically connects to the server and fetches docs!
        response = agent(user_input)
        print(f"Agent: {response}\n")

    except KeyboardInterrupt:
        print("\nGoodbye! 👋")
        break

print("\n✅ Challenge 5 complete!")