from .calculator import execute as calculator
from .weather import execute as weather
from .time_tool import execute as time_tool
from .pdfmaker import execute as pdfmaker
from .presentationmaker import execute as presentationmaker

TOOLS = {
    "calculator": calculator,
    "weather": weather,
    "pdfmaker": pdfmaker,
    "presentationmaker": presentationmaker,
    "time": time_tool,
}


def execute_tool(tool_name, arguments):
    """
    Execute the requested tool.
    """
    if tool_name in TOOLS:
        return TOOLS[tool_name](arguments)

    return f"Unknown Tool: {tool_name}"


def list_tools():
    """
    Return the list of available tools.
    """
    return list(TOOLS.keys())


if __name__ == "__main__":

    print("=" * 50)
    print("Tool Registry Test")
    print("=" * 50)

    print("\nAvailable Tools")
    print("----------------")
    print(list_tools())

    print("\nCalculator Test")
    print("----------------")
    result = execute_tool(
        "calculator",
        {"expression": "25*18"}
    )
    print(result)

    print("\nTime Tool Test")
    print("----------------")
    result = execute_tool(
        "time",
        {}
    )
    print(result)

    print("\nWeather Tool Test")
    print("----------------")
    result = execute_tool(
        "weather",
        {"city": "Delhi"}
    )
    print(result)

    print("\nPDF Maker Test")
    print("----------------")
    result = execute_tool(
        "pdfmaker",
        {
            "title": "Sample PDF",
            "content": "This PDF was created by the AI Agent.",
            "filename": "sample.pdf"
        }
    )
    print(result)

    print("\nPresentation Maker Test")
    print("----------------")
    result = execute_tool(
        "presentationmaker",
        {
            "title": "AI Presentation",
            "filename": "ai_presentation.pptx",
            "slides": [
                {
                    "title": "Introduction",
                    "content": "Artificial Intelligence\nMachine Learning"
                },
                {
                    "title": "Applications",
                    "content": "Healthcare\nFinance\nEducation"
                }
            ]
        }
    )
    print(result)