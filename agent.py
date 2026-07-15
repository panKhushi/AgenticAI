from LLM import chat
from memory import load_memory, save_memory
from parser import parse_tool_call
from prompts import SYSTEM_PROMPT
from tools import calculator


class Agent:

    def __init__(self):
        """Initialize the Agent."""
        pass

    def run_agent(self, user_input):

        # Load previous conversation memory
        memory = load_memory()

        # Build message history
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        messages.extend(memory)

        messages.append({
            "role": "user",
            "content": user_input
        })

        # Get response from LLM
        llm_response = chat(messages)

        # Check whether LLM requested a tool
        tool_request = parse_tool_call(llm_response)

        # If no tool is needed
        if tool_request is None:

            memory.append({
                "role": "user",
                "content": user_input
            })

            memory.append({
                "role": "assistant",
                "content": llm_response
            })

            save_memory(memory)

            return llm_response

        # -------------------------
        # Execute Tool
        # -------------------------
        tool_name = tool_request.get("tool")
        tool_result = "Unknown Tool"
        arguments = tool_request.copy()
        arguments.pop("tool", None)

        print(f"\nTool Requested: {tool_name}")
        print("Arguments:", arguments)

        tool_result = execute_tool(
            tool_name, 
            arguments
        )
       

        # Give tool result back to LLM
        messages.append({
            "role": "assistant",
            "content": llm_response
        })

        messages.append({
            "role": "user",
            "content": (
                f"""
                Tool Result: {tool_result}
                Using the result answer the user's original question."""
            )
        })

        final_response = chat(messages)

        # Save memory
        memory.append({
            "role": "user",
            "content": user_input
        })

        memory.append({
            "role": "assistant",
            "content": final_response
        })

        save_memory(memory)

        return final_response


# Optional: Run directly for testing
if __name__ == "__main__":

    agent = Agent()

    while True:

        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            break

        print("Agent:", agent.run_agent(user_input))