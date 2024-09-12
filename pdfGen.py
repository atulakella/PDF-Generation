from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime

from data_fetching import get_patient_docs, get_data, get_data_cause, get_data_cause_para, get_data_consider, get_normal_range

def format_date(date_str):
    """ Convert date string to a more readable format """
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        day = date_obj.day
        month = date_obj.strftime('%B')
        year = date_obj.year

        # Determine suffix for the day
        suffix = 'th' if 10 <= day <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

        formatted_date = f"{day}{suffix} {month} {year}"
        return formatted_date
    except Exception as e:
        print(f"Error formatting date: {e}")
        return date_str

def draw_cover_background(canvas, doc):
    try:
        # Get page size
        width, height = doc.pagesize
        
        # Draw the cover image, stretching to fill the entire page
        canvas.drawImage(
            'cover.png', 
            0, 0, 
            width=width, 
            height=height, 
            preserveAspectRatio=False, 
            anchor='sw'
        )
    except Exception as e:
        print(f"Error drawing cover image: {e}")

    # Set up text positions
    width, height = doc.pagesize
    text_objects = [
        f"Patient Name: {doc.patient_name}",
        f"Booking ID: {doc.booking_id}",
        f"Date: {doc.date}"
    ]

    # Define text font and size
    canvas.setFont('Helvetica-Bold', 16)
    canvas.setFillColor(colors.black)
    
    # Set vertical spacing
    vertical_spacing = 30
    start_x = 70
    start_y = 220  
    for i, text in enumerate(text_objects):
        text_width = canvas.stringWidth(text, 'Helvetica-Bold', 16)
        x = start_x
        y = start_y - (i * vertical_spacing)
        canvas.drawString(x, y, text)


def draw_background(canvas, doc):
    """ Draw background image on all pages except the first """
    try:
        width, height = doc.pagesize
        canvas.drawImage('normal.png', 0, 0, width=width, height=height, preserveAspectRatio=False, anchor='sw')
    except Exception as e:
        print(f"Error drawing background image: {e}")

def generate_pdf(customer_name, booking_date, pdf_filename):
    """ Generate PDF report with patient data """
    try:
        patient_tests, booking_id = get_patient_docs(customer_name, booking_date)
        if not patient_tests:
            print("No data available for the given customer and booking date.")
            return

        print("Patient Tests:", patient_tests)
        print("Booking ID:", booking_id)
    except Exception as e:
        print(f"Error fetching patient documents: {e}")
        return

    styles = getSampleStyleSheet()
    
    section_heading_style = ParagraphStyle(
        name='SectionHeading',
        fontName='Helvetica-Bold',
        fontSize=18,
        spaceAfter=12,
        textColor=colors.black
    )
    
    section_body_style = ParagraphStyle(
        name='SectionBody',
        fontName='Helvetica',
        fontSize=12,
        spaceAfter=12,
        textColor=colors.black
    )
    
    highlight_style = ParagraphStyle(
        name='Highlight',
        fontName='Helvetica-Bold',
        fontSize=16,
        spaceAfter=16,
        textColor=colors.green
    )

    bullet_style = ParagraphStyle(
        name='Bullet',
        fontName='Helvetica',
        fontSize=12,
        spaceAfter=12,
        textColor=colors.black,
        leftIndent=20
    )

    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=120, bottomMargin=72)
    elements = []

    def canvas_first_page(canvas, doc):
        """ Draw cover page """
        doc.patient_name = customer_name
        doc.booking_id = booking_id
        doc.date = format_date(booking_date)
        draw_cover_background(canvas, doc)

    def canvas_other_pages(canvas, doc):
        """ Draw background on other pages """
        draw_background(canvas, doc)

    elements.append(Spacer(1, 24))
    elements.append(PageBreak())

    for i, (test_name, result) in enumerate(patient_tests):
        print(f"Adding test: {test_name} with result: {result}")
        if i > 0:
            elements.append(PageBreak())
        elements.append(Spacer(1, 24))
        elements.append(Paragraph(f"{test_name} Test", section_heading_style))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(f"Result: {result}", section_body_style))

        try:
            # Fetch normal range
            normal_range = get_normal_range(test_name)
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"Normal Range: {normal_range}", section_body_style))

            # Determine if result is high, low, or normal
            result_status = "Normal"
            if "high" in result.lower():
                result_status = "High"
            elif "low" in result.lower():
                result_status = "Low"
            elements.append(Paragraph(f"Status: {result_status}", section_body_style))

            summary = get_data(test_name)
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"Test Summary:", highlight_style))
            elements.append(Paragraph(summary, section_body_style))

            causes = get_data_cause(test_name, result_status.lower())
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"Possible Causes:", highlight_style))
            for j, cause in enumerate(causes):
                elements.append(Paragraph(f"{j+1}. {cause}", bullet_style))

            para_summary = get_data_cause_para(test_name, result_status.lower())
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"Case Summary:", highlight_style))
            elements.append(Paragraph(para_summary, section_body_style))

            considerations = get_data_consider(test_name, result_status.lower())
            considerations_lines = considerations.split('\n')
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f"Considerations:", highlight_style))
            for line in considerations_lines:
                if line.strip():
                    elements.append(Paragraph(line.strip(), section_body_style))
            elements.append(Spacer(1, 12))
        except Exception as e:
            print(f"Error processing test '{test_name}': {e}")

    try:
        doc.build(elements, onFirstPage=canvas_first_page, onLaterPages=canvas_other_pages)
        print("PDF generated successfully.")
    except Exception as e:
        print(f"Error generating PDF: {e}")

if __name__ == "__main__":
    customer_name = "John Doe"  # Replace with actual customer name
    booking_date = "2024-09-08"  # Replace with actual booking date
    pdf_filename = "medical_report.pdf"  # Replace with desired filename

    generate_pdf(customer_name, booking_date, pdf_filename)
