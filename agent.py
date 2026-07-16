from LLM import chat
from memory import load_memory, save_memory
from parser import parse_tool_call
from prompts import SYSTEM_PROMPT
from tools.registery import execute_tool


class Agent:

    def __init__(self):
        pass

    def run_agent(self, user_input):

        memory = load_memory()

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        messages.extend(memory)

        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        # ------------------------
        # Ask LLM
        # ------------------------

        llm_response = chat(messages)
        print("=" * 80)
        print("RAW LLM RESPONSE:")
        print(repr(llm_response))
        print("=" * 80)
        tool_request = parse_tool_call(llm_response)

        # ------------------------
        # Normal Conversation
        # ------------------------

        if tool_request is None:

            memory.append(
                {
                    "role": "user",
                    "content": user_input
                }
            )

            memory.append(
                {
                    "role": "assistant",
                    "content": llm_response
                }
            )

            save_memory(memory)

            return {
                "message": llm_response,
                "tool_result": None
            }

        # ------------------------
        # Execute Tool
        # ------------------------

        tool_name = tool_request.get("tool")

        arguments = tool_request.copy()
        arguments.pop("tool", None)

        print(f"\nTool Requested: {tool_name}")
        print("Arguments:", arguments)

        try:
            tool_result = execute_tool(
                tool_name,
                arguments
            )

        except Exception as e:
            # A tool crashing (bad args, missing dependency, disk
            # permission issue, etc.) must never bubble up as a raw
            # exception in the Streamlit UI.
            print("Tool Execution Error:", e)

            tool_result = {
                "message": f"Sorry, the '{tool_name}' tool failed to run: {e}"
            }

        # ------------------------
        # Prepare Final Message
        # ------------------------

        if isinstance(tool_result, dict):

            assistant_message = tool_result.get(
                "message",
                "Task completed successfully."
            )

            # If the tool reported failure (no file produced), don't
            # pass a broken tool_result through to app.py's file-preview
            # logic — treat it as a plain text response instead.
            if tool_result.get("type") in ("pdf", "ppt") and not tool_result.get("file"):
                tool_result = None

        else:

            assistant_message = str(tool_result)

            tool_result = None

        # ------------------------
        # Save Memory
        # ------------------------

        memory.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        memory.append(
            {
                "role": "assistant",
                "content": assistant_message
            }
        )

        save_memory(memory)

        return {
            "message": assistant_message,
            "tool_result": tool_result
        }


if __name__ == "__main__":

    agent = Agent()

    while True:

        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            break

        response = agent.run_agent(user_input)

        print("\nAssistant:")
        print(response["message"])

        if response["tool_result"]:
            print("\nTool Result:")
            print(response["tool_result"])