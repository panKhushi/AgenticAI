from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
import os


OUTPUT_FOLDER = "generated_pdfs"


def create_pdf(title: str, content: str, filename: str = "output.pdf") -> str:
    """
    Creates a PDF from text.

    Args:
        title (str): Title of the PDF.
        content (str): Body content.
        filename (str): Output filename.

    Returns:
        str: Path to generated PDF.
    """

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    filepath = os.path.join(OUTPUT_FOLDER, filename)

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(filepath)

    story = []

    story.append(Paragraph(f"<b><font size=18>{title}</font></b>", styles["Title"]))
    story.append(Paragraph("<br/><br/>", styles["BodyText"]))
    story.append(Paragraph(content.replace("\n", "<br/>"), styles["BodyText"]))

    doc.build(story)

    return filepath


if __name__ == "__main__":
    pdf = create_pdf(
        title="AI Agent Demo",
        content="""
This PDF was generated using Python.

The AI Agent can create reports,
notes,
assignments,
summaries,
and many other documents.
""",
        filename="demo.pdf"
    )

    print("PDF created:", pdf)