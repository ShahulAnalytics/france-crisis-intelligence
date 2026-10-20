"""Convert a Markdown report to a PDF using ReportLab."""
from pathlib import Path
from html import escape
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm

def markdown_to_pdf(markdown_path: Path, pdf_path: Path) -> Path:
    markdown_path=Path(markdown_path); pdf_path=Path(pdf_path); pdf_path.parent.mkdir(parents=True,exist_ok=True)
    styles=getSampleStyleSheet(); story=[]
    for raw in markdown_path.read_text(encoding='utf-8').splitlines():
        line=raw.strip()
        if not line: story.append(Spacer(1,3*mm)); continue
        if line.startswith('# '): style=styles['Title']; line=line[2:]
        elif line.startswith('## '): style=styles['Heading1']; line=line[3:]
        elif line.startswith('### '): style=styles['Heading2']; line=line[4:]
        else:
            style=styles['BodyText']
            if line.startswith('- '): line='• '+line[2:]
        line=escape(line)
        story.append(Paragraph(line,style))
    SimpleDocTemplate(str(pdf_path),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=18*mm,title='France Crisis Intelligence Report').build(story)
    return pdf_path
