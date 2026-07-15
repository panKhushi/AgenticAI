from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
import os

OUTPUT_FOLDER = "generated_pdfs"


def create_pdf(title: str, content: str, filename: str = "output.pdf") -> str:
    """
    Creates a PDF from text.
    """

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    filepath = os.path.join(OUTPUT_FOLDER, filename)

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filepath)

    story = []

    story.append(
        Paragraph(
            f"<b><font size=18>{title}</font></b>",
            styles["Title"]
        )
    )

    story.append(Paragraph("<br/><br/>", styles["BodyText"]))

    story.append(
        Paragraph(
            content.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    doc.build(story)

    return filepath


# -------------------------------------------------
# Tool entry point
# -------------------------------------------------

def execute(arguments: dict):

    title = arguments.get("title", "Untitled")

    content = arguments.get("content", "")

    filename = arguments.get("filename", "output.pdf")

    return create_pdf(
        title=title,
        content=content,
        filename=filename
    )


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