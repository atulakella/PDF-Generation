from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from PyPDF2 import PdfWriter, PdfReader
import os

# Import functions from data_fetching
from data_fetching import get_patient_docs, get_data, get_data_cause, get_data_cause_para, get_data_consider

def draw_cover_background(canvas, doc):
    cover_image = 'cover.png'
    if not os.path.exists(cover_image):
        print(f"Error: '{cover_image}' not found.")
        return
    
    canvas.drawImage(cover_image, 0, 0, width=doc.pagesize[0], height=doc.pagesize[1], preserveAspectRatio=True, anchor='sw')
    
    # Set position for text
    vertical_position = doc.pagesize[1] - 300  # Adjust vertical position as necessary
    canvas.setFont('Helvetica-Bold', 16)
    canvas.setFillColor(colors.black)
    canvas.drawString(50, vertical_position, f"Patient: {doc.patient_name}")
    canvas.drawString(50, vertical_position - 30, f"Booking ID: {doc.booking_id}")

def generate_cover_page(customer_name, booking_id, pdf_filename_cover):
    doc_cover = SimpleDocTemplate(pdf_filename_cover, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    cover_elements = []

    def canvas_cover_page(canvas, doc):
        doc.patient_name = customer_name
        doc.booking_id = booking_id
        draw_cover_background(canvas, doc)
    
    doc_cover.build(cover_elements, onFirstPage=canvas_cover_page)
    
    if not os.path.exists(pdf_filename_cover) or os.path.getsize(pdf_filename_cover) == 0:
        print(f"Error: Cover page PDF file '{pdf_filename_cover}' is empty or not created.")
        return

def draw_test_background(canvas, doc):
    background_image = 'normal.png'
    if not os.path.exists(background_image):
        print(f"Error: '{background_image}' not found.")
        return
    
    canvas.drawImage(background_image, 0, 0, width=doc.pagesize[0], height=doc.pagesize[1], preserveAspectRatio=True, anchor='sw')

def generate_test_pages(patient_tests, pdf_filename_test):
    doc_test = SimpleDocTemplate(pdf_filename_test, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    test_elements = []
    styles = getSampleStyleSheet()
    
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

    for test_name, result in patient_tests:
        def canvas_test_page(canvas, doc):
            draw_test_background(canvas, doc)
        
        doc_test.build(test_elements, onFirstPage=canvas_test_page)

        test_elements.append(Spacer(1, 12))
        test_elements.append(Paragraph(f"Test: {test_name}", section_heading_style))
        test_elements.append(Spacer(1, 6))
        test_elements.append(Paragraph(f"Result: {result}", section_body_style))

        summary = get_data(test_name)
        test_elements.append(Spacer(1, 6))
        test_elements.append(Paragraph(f"Test Summary:", highlight_style))
        test_elements.append(Paragraph(summary, section_body_style))

        causes = get_data_cause(test_name, "high" if result.lower().startswith("high") else "low" if result.lower().startswith("low") else "normal")
        test_elements.append(Spacer(1, 6))
        test_elements.append(Paragraph(f"Possible Causes:", highlight_style))
        for i, cause in enumerate(causes):
            test_elements.append(Paragraph(f"{i+1}. {cause}", bullet_style))

        para_summary = get_data_cause_para(test_name, "high" if result.lower().startswith("high") else "low")
        test_elements.append(Spacer(1, 6))
        test_elements.append(Paragraph(f"Case Summary:", highlight_style))
        test_elements.append(Paragraph(para_summary, section_body_style))

        considerations = get_data_consider(test_name, "high" if result.lower().startswith("high") else "low")
        considerations_lines = considerations.split('\n')
        test_elements.append(Spacer(1, 6))
        test_elements.append(Paragraph(f"Considerations:", highlight_style))
        for line in considerations_lines:
            if line.strip():  # Only add non-empty lines
                test_elements.append(Paragraph(line.strip(), section_body_style))
        test_elements.append(Spacer(1, 12))  # Add extra space after considerations

    if not os.path.exists(pdf_filename_test) or os.path.getsize(pdf_filename_test) == 0:
        print(f"Error: Test pages PDF file '{pdf_filename_test}' is empty or not created.")
        return

def generate_pdf(customer_name, booking_date, pdf_filename):
    pdf_filename_cover = pdf_filename.replace('.pdf', '_cover.pdf')
    generate_cover_page(customer_name, booking_date, pdf_filename_cover)

    patient_tests, booking_id = get_patient_docs(customer_name, booking_date)
    if not patient_tests:
        print("No data available for the given customer and booking date.")
        return
    
    pdf_filename_test = pdf_filename.replace('.pdf', '_test.pdf')
    generate_test_pages(patient_tests, pdf_filename_test)

    # Merge PDFs
    if not os.path.exists(pdf_filename_cover):
        print(f"Error: Cover page PDF file '{pdf_filename_cover}' not found.")
        return

    if not os.path.exists(pdf_filename_test):
        print(f"Error: Test pages PDF file '{pdf_filename_test}' not found.")
        return

    cover_pdf = PdfReader(pdf_filename_cover)
    test_pdf = PdfReader(pdf_filename_test)
    writer = PdfWriter()

    # Add cover page
    if cover_pdf.pages:
        writer.add_page(cover_pdf.pages[0])
    else:
        print("Error: Cover page PDF is empty.")
        return

    # Add test result pages
    for page in test_pdf.pages:
        writer.add_page(page)

    with open(pdf_filename, 'wb') as f:
        writer.write(f)

if __name__ == "__main__":
    customer_name = "John Doe"  # Replace with actual customer name
    booking_date = "2024-09-08"  # Replace with actual booking date
    pdf_filename = "medical_report.pdf"  # Replace with desired filename

    generate_pdf(customer_name, booking_date, pdf_filename)
