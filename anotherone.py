from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from data_fetching import get_patient_docs, get_data, get_data_cause, get_data_cause_para, get_data_consider

def draw_cover_background(canvas, doc):
    # Draw cover image as background
    canvas.drawImage('cover.png', 0, 0, width=doc.pagesize[0], height=doc.pagesize[1], preserveAspectRatio=True, anchor='sw')
    
    # Set position for text
    vertical_position = 3000  # Adjust this value as needed
    canvas.setFont('Helvetica-Bold', 16)
    canvas.setFillColor(colors.black)
    canvas.drawString(50, vertical_position - 50, f"Patient: {doc.patient_name}")
    canvas.drawString(50, vertical_position - 80, f"Booking ID: {doc.booking_id}")

def draw_background(canvas, doc):
    # Draw background image for subsequent pages
    canvas.drawImage('normal.png', 0, 0, width=doc.pagesize[0], height=doc.pagesize[1], preserveAspectRatio=True, anchor='sw')

def generate_pdf(customer_name, booking_date, pdf_filename):
    # Fetch data
    patient_tests, booking_id = get_patient_docs(customer_name, booking_date)

    if not patient_tests:
        print("No data available for the given customer and booking date.")
        return

    styles = getSampleStyleSheet()
    heading_style = styles['Heading1']
    body_style = styles['BodyText']
    
    # Custom styles for sections
    section_heading_style = ParagraphStyle(
        name='SectionHeading',
        fontName='Helvetica-Bold',
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    section_body_style = ParagraphStyle(
        name='SectionBody',
        fontName='Helvetica',
        fontSize=12,
        spaceAfter=8,
        textColor=colors.black
    )
    
    highlight_style = ParagraphStyle(
        name='Highlight',
        fontName='Helvetica-Bold',
        fontSize=12,
        spaceAfter=6,
        textColor=colors.red
    )

    bullet_style = ParagraphStyle(
        name='Bullet',
        fontName='Helvetica',
        fontSize=12,
        spaceAfter=6,
        textColor=colors.black,
        leftIndent=20
    )

    # Create PDF
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    elements = []

    def canvas_first_page(canvas, doc):
        # Set document-specific attributes for the first page
        doc.patient_name = customer_name
        doc.booking_id = booking_id
        draw_cover_background(canvas, doc)

    def canvas_other_pages(canvas, doc):
        draw_background(canvas, doc)

    # First Page: Cover page
    elements.append(Spacer(1, 24))  # Spacer for line break
    elements.append(PageBreak())  # Page break for the cover page

    # Add content for each test, one per page
    for i, (test_name, result) in enumerate(patient_tests):
        if i > 0:
            elements.append(PageBreak())  # Add page break before each new test page
        # Add content for the current test
        elements.append(Spacer(1, 24))
        elements.append(Paragraph(f"Test: {test_name}", section_heading_style))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(f"Result: {result}", section_body_style))

        summary = get_data(test_name)
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(f"Test Summary:", highlight_style))
        elements.append(Paragraph(summary, section_body_style))

        causes = get_data_cause(test_name, "high" if result.lower().startswith("high") else "low" if result.lower().startswith("low") else "normal")
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(f"Possible Causes:", highlight_style))
        for j, cause in enumerate(causes):
            elements.append(Paragraph(f"{j+1}. {cause}", bullet_style))

        para_summary = get_data_cause_para(test_name, "high" if result.lower().startswith("high") else "low")
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(f"Case Summary:", highlight_style))
        elements.append(Paragraph(para_summary, section_body_style))

        considerations = get_data_consider(test_name, "high" if result.lower().startswith("high") else "low")
        considerations_lines = considerations.split('\n')
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(f"Considerations:", highlight_style))
        for line in considerations_lines:
            if line.strip():  # Only add non-empty lines
                elements.append(Paragraph(line.strip(), section_body_style))
        elements.append(Spacer(1, 12))  # Add extra space after considerations

    # Build PDF with custom backgrounds for pages
    doc.build(elements, onFirstPage=canvas_first_page, onLaterPages=canvas_other_pages)

if __name__ == "__main__":
    customer_name = "John Doe"  # Replace with actual customer name
    booking_date = "2024-09-08"  # Replace with actual booking date
    pdf_filename = "medical_report.pdf"  # Replace with desired filename

    generate_pdf(customer_name, booking_date, pdf_filename)
