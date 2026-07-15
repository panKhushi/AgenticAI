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

        llm_response = chat(messages)

        tool_request = parse_tool_call(llm_response)

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

            return llm_response

        tool_name = tool_request.get("tool")

        arguments = tool_request.copy()
        arguments.pop("tool", None)

        print(f"\nTool Requested: {tool_name}")
        print("Arguments:", arguments)

        tool_result = execute_tool(
            tool_name,
            arguments
        )

        messages.append(
            {
                "role": "assistant",
                "content": llm_response
            }
        )

        messages.append(
            {
                "role": "user",
                "content": f"""
Tool Result:
{tool_result}

Using this tool result answer the user's original question.
"""
            }
        )

        final_response = chat(messages)

        memory.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        memory.append(
            {
                "role": "assistant",
                "content": final_response
            }
        )

        save_memory(memory)

        return final_response


if __name__ == "__main__":

    agent = Agent()

    while True:

        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            break

        print("Agent:", agent.run_agent(user_input))