from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def generate_pdf(report_data: dict) -> BytesIO:
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []

    # Title
    elements.append(Paragraph("Symptom Report", styles["Title"]))
    elements.append(Spacer(1, 10))

    # Basic Info
    elements.append(Paragraph(f"User ID: {report_data['user_id']}", styles["Normal"]))
    # elements.append(Paragraph(f"Patient Name: {report_data['patient_name']}", styles["Normal"]))
    elements.append(Paragraph(f"Total Entries: {report_data['total_entries']}", styles["Normal"]))
    elements.append(Paragraph(f"Trend: {report_data['trend']}", styles["Normal"]))
    elements.append(Spacer(1, 10))

    # Risk Summary
    elements.append(Paragraph("Risk Summary:", styles["Heading3"]))
    for k, v in report_data["risk_summary"].items():
        elements.append(Paragraph(f"{k}: {v}", styles["Normal"]))

    elements.append(Spacer(1, 10))

    # Specialist
    elements.append(Paragraph(
        f"Recommended Specialist: {report_data['latest_specialist']}",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 10))

    # Timeline
    elements.append(Paragraph("Timeline:", styles["Heading3"]))
    for item in report_data["timeline"]:
        elements.append(Paragraph(
            f"{item['date']} → Severity: {item['severity']}",
            styles["Normal"]
        ))

    doc.build(elements)

    buffer.seek(0)
    return buffer