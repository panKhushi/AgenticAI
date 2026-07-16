from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from xml.sax.saxutils import escape
import os

# Absolute path anchored to this file's location rather than the
# process's current working directory. Streamlit Cloud (and some local
# setups) can launch the app with a different cwd than you expect;
# anchoring to __file__ makes the output folder consistent everywhere.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "generated_pdfs")


def create_pdf(title: str, content: str, filename: str = "output.pdf"):

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    filepath = os.path.join(OUTPUT_FOLDER, filename)

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filepath)

    story = []

    # ReportLab's Paragraph parses a small XML-like markup language.
    # Unescaped "&", "<", ">" in LLM-generated title/content (e.g.
    # "C++ & AI", "5 < 10") will raise a parse error and silently kill
    # PDF generation. Escaping first fixes that class of failure.
    safe_title = escape(title)
    safe_content = escape(content).replace("\n", "<br/>")

    story.append(
        Paragraph(
            f"<b><font size='18'>{safe_title}</font></b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph("<br/><br/>", styles["BodyText"])
    )

    story.append(
        Paragraph(
            safe_content,
            styles["BodyText"]
        )
    )

    doc.build(story)

    return filepath


def execute(arguments: dict):

    title = arguments.get("title", "Untitled")
    content = arguments.get("content", "")
    filename = arguments.get("filename", "output.pdf")

    try:
        filepath = create_pdf(
            title=title,
            content=content,
            filename=filename
        )

    except Exception as e:
        return {
            "type": "pdf",
            "file": None,
            "message": f"Failed to create PDF: {e}"
        }

    return {
        "type": "pdf",
        "file": filepath,
        "message": f"PDF '{filename}' created successfully."
    }


if __name__ == "__main__":

    print(
        execute(
            {
                "title": "AI Agent Demo",
                "content": "This PDF was generated successfully.",
                "filename": "demo.pdf"
            }
        )
    )