from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Line, Polygon
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
import PyPDF2
from barcode import EAN13 
from barcode.writer import ImageWriter 


#Registering Fonts 
pdfmetrics.registerFont(TTFont('SofiaPro', './Resources/Fonts/sofiapro-light.ttf')) 
pdfmetrics.registerFont(TTFont('EastmanBold','./Resources/Fonts/Eastman-bold.ttf'))
pdfmetrics.registerFont(TTFont('EastmanRegular','./Resources/Fonts/Eastman-regular.ttf'))
pdfmetrics.registerFont(TTFont('SofiaProBold','./Resources/Fonts/SofiaPro-Bold.ttf'))
pdfmetrics.registerFont(TTFont('RobotoRegular','./Resources/Fonts/Roboto-Regular.ttf'))
pdfmetrics.registerFont(TTFont('RobotoBold','./Resources/Fonts/Roboto-Bold.ttf'))

styles = getSampleStyleSheet()
# Default font
styles['Normal'].fontName = 'SofiaPro'

from data_fetching import *

# Creating Cover page
def create_cover_pdf(filename, page_size, cover_image_path,customer_name):
    c = canvas.Canvas(filename, pagesize=page_size)
    c.drawImage(cover_image_path, 0, 0, width=page_size[0], height=page_size[1])
    c.setFont("SofiaPro", 32)
    c.setFillColorRGB(1, 1, 1)
    c.drawString(22, 302, customer_name+"     M  26")
    c.save()

# Mergeing all final report pages
def merge_pdfs(output_filename, *input_filenames):
    pdf_merger = PyPDF2.PdfMerger()
    for input_filename in input_filenames:
        pdf_merger.append(input_filename)
    with open(output_filename, 'wb') as output_file:
        pdf_merger.write(output_file)

#Creating RBC report page
def create_rbc_report_page(out_filename, page_size, report_png, list_patient_data,booking_id):
    highlighted_tests = []

    c = canvas.Canvas(out_filename, pagesize=page_size)
    c.drawImage(report_png, 0, 0, width=page_size[0], height=page_size[1])

    # Default initial x and y coordinates
    init_x = 22
    init_y= 630

    booking_id = "000000"+str(booking_id)

    for test in list_patient_data[1]:
        # Checks if the y-coordinate is less than 100 , if not then it creates a new page and continues to write the report
        if init_y<=100:
            c.showPage()
            c.drawImage("./Resources/rbc_page2.png", 0, 0, width=page_size[0], height=page_size[1])

            #Creating Barcode
            my_barcode = EAN13(booking_id, writer=ImageWriter()) 
            my_barcode.save("./dynamic_resource/"+booking_id)
            c.drawImage("./dynamic_resource/"+booking_id+".png", 16, 147, width=100, height=40)
            c.setFont("SofiaPro", 11)
            c.drawString(85, 133,booking_id)

            init_y = 630  # Reset the initial y-coordinate
        
        # Checks if the test is a header or not
        if isinstance(test["parameter_name"],str) and test['parameter_value']=='HEAD':
                init_y+= -10
                c.setFont("RobotoBold",15) 
                c.setFillColorRGB(0,0,0)
                c.drawString(init_x, init_y, test['parameter_name'].title())
                init_y+= -18
                continue
        else:
                # Checks if the test is highlighted or not
                if (test['parameter_value'] > test['upper_bound'] or test['parameter_value'] < test['lower_bound']) and test['is_highlighted']:
                    c.setFillColorRGB(219/255,68/255,55/255)
                    highlighted_tests.append(["Complete Blood Count (CBC)",[test['parameter_name'],test['parameter_value']]])
                else:
                    c.setFillColorRGB(0,0,0)
                c.setFont("RobotoRegular",11) 
                c.drawString(init_x, init_y, test['parameter_name'].title())
                c.drawString(init_x+260, init_y, test['parameter_value'])
                c.drawString(init_x+350, init_y, test['unit'])
                c.drawString(init_x+450, init_y, test['display_value'])
                if test['test_method'] != "":
                    init_y+= -11
                    c.setFont("RobotoRegular",9) 
                    c.drawString(init_x, init_y, "Method : " +test['test_method'].title())
                init_y+= -17
                continue
    # Fianl note and advice created if the y-coordinate is greater than 360
    if init_y > 360:
        c.setFont("RobotoBold",15) 
        c.drawString(22, 330, "NOTE : ")
        c.setFont("RobotoRegular",13) 
        c.drawString(22, 315, "The above values are indicative and may vary from person to person.")
        c.setFont("RobotoBold",15) 
        c.drawString(22, 280, "ADVICE: ")
        c.setFont("RobotoRegular",13)
        c.drawString(22, 265, "Please consult your doctor for further advice.")
    

    c.save()
    return highlighted_tests

# Creating Urine Routine and Microscopic Examination report page
def create_urme_report_page(out_filename, page_size, report_png, list_patient_data,booking_id):
    highlighted_tests = []
    c = canvas.Canvas(out_filename, pagesize=page_size)
    c.drawImage(report_png, 0, 0, width=page_size[0], height=page_size[1])

    # Default initial x and y coordinates
    init_x = 22
    init_y= 630

    booking_id = "000000"+str(booking_id)

    for test in list_patient_data[1]:
        # Checks if the y-coordinate is less than 100 , if not then it creates a new page and continues to write the report
        if init_y<=100:
            c.showPage()
            c.drawImage("./Resources/urme_page2.png", 0, 0, width=page_size[0], height=page_size[1])
            
            #Creating Barcode
            my_barcode = EAN13(booking_id, writer=ImageWriter()) 
            my_barcode.save("./dynamic_resource/"+booking_id)
            c.drawImage("./dynamic_resource/"+booking_id+".png", 16, 147, width=100, height=40)
            c.setFont("SofiaPro", 11)
            c.drawString(85, 133,booking_id)

            init_y = 630  # Reset the initial y-coordinate
        
        # Checks if the test is a header or not
        if isinstance(test["parameter_name"],str) and test['parameter_value']=='HEAD':
                init_y+= -10
                c.setFont("RobotoBold",15) 
                c.setFillColorRGB(0,0,0)
                c.drawString(init_x, init_y, test['parameter_name'].title())
                init_y+= -18
                continue
        else:
                if test['is_highlighted']:
                    c.setFillColorRGB(219/255,68/255,55/255)
                    highlighted_tests.append(["Urine Routine and Microscopic Examination",[test['parameter_name'],test['parameter_value']]])
                else:
                    c.setFillColorRGB(0,0,0)
                c.setFont("RobotoRegular",11) 
                c.drawString(init_x, init_y, test['parameter_name'].title())
                c.drawString(init_x+260, init_y, test['parameter_value'])
                c.drawString(init_x+350, init_y, test['unit'])
                c.drawString(init_x+450, init_y, test['display_value'])
                if test['test_method'] != "":
                    init_y+= -11
                    c.setFont("RobotoRegular",9) 
                    c.drawString(init_x, init_y, "Method : " +test['test_method'].title())
                init_y+= -17
                continue
    # Fianl note and advice created if the y-coordinate is greater than 360
    if init_y > 360:
        c.setFont("RobotoBold",15) 
        c.drawString(22, 330, "NOTE : ")
        c.setFont("RobotoRegular",13) 
        c.drawString(22, 315, "The above values are indicative and may vary from person to person.")
        c.setFont("RobotoBold",15) 
        c.drawString(22, 280, "ADVICE: ")
        c.setFont("RobotoRegular",13)
        c.drawString(22, 265, "Please consult your doctor for further advice.")
    
    c.save()
    return highlighted_tests


# Creating report page for other tests
def create_report_page(out_filename, page_size, report_png, tuple_of_test,booking_id):
    highlighted_tests = []

    # Initialising variables
    tests_left_to_print = len(tuple_of_test[1])
    init_tests = tests_left_to_print
    tests_printed=1
    final_page=False
    init_tittle = False
    booking_id = "000000"+str(booking_id)


    c = canvas.Canvas(out_filename, pagesize=page_size)

    for test in tuple_of_test[1]:
        # Checks if its the final page to print
        if tests_left_to_print >= 2 or final_page :
            if tests_left_to_print == 2:
                final_page=True

            #If the tests printed are odd then it creates a new page and continues to write the report
            if tests_printed>2:
                if tests_printed%2 != 0:
                    c.showPage()
            if tests_printed%2 !=0 :
                c.drawImage(report_png, 0, 0, width=page_size[0], height=page_size[1])
                c.setFont("RobotoBold", 20)
                c.setFillColorRGB(0,0,0)
                c.drawString(171, 694, tuple_of_test[0].title())
                my_barcode = EAN13(booking_id, writer=ImageWriter()) 
                my_barcode.save("./dynamic_resource/"+booking_id)
                c.drawImage("./dynamic_resource/"+booking_id+".png", 16, 147, width=100, height=40)
                c.setFont("SofiaPro", 11)
                c.drawString(85, 133,booking_id)
                if init_tittle == False:
                    c.setFont("RobotoBold", 20)
                    c.setFillColorRGB(0,0,0)
                    #Test Name
                    c.drawString(171, 694, tuple_of_test[0].title())
                    init_tittle = True
                    
                 
                c.setFillColorRGB(0,61/255,108/255)
                #Test Param name
                if len(test['parameter_name']+" Test") > 22:
                    c.setFont("RobotoBold", 11)
                    c.drawString(22, 652, test['parameter_name']+" Test")
                else:
                    c.setFont("RobotoBold", 17) 
                    c.drawString(22, 652, test['parameter_name']+" Test")
                
                #About Test
                c.setFont("RobotoRegular", 9)
                paragraph = Paragraph(get_data(test['parameter_name']+" Test"), styles['Normal']) 
                paragraph.wrap(200, 280)
                paragraph.drawOn(c, 22, 648 - paragraph.height)

                #Test Value
                c.setFont("RobotoBold", 17) 
                c.setFillColorRGB(0,61/255,108/255)
                c.drawString(289, 652, "Test Value : " +test['parameter_value'] + " " + test['unit'])

                #Checks if the test is highlighted or not & Prints accordingly
                if test['parameter_value'] > test['upper_bound'] :
                    c.setFont("SofiaProBold", 15)    
                    r,g,b = 219,68,55
                    c.setFillColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 5, stroke=0, fill=1)
                    c.setStrokeColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 7, stroke=1, fill=0)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(515, 654, "High")
                    highlighted_tests.append([tuple_of_test[0],[test['parameter_name'],test['parameter_value']]])

                elif test['parameter_value'] < test['lower_bound'] :
                    c.setFont("SofiaProBold", 15)    
                    r,g,b = 219,68,55
                    c.setFillColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 5, stroke=0, fill=1)
                    c.setStrokeColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 7, stroke=1, fill=0)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(515, 654, "Low")
                    highlighted_tests.append([tuple_of_test[0],[test['parameter_name'],test['parameter_value']]])
                
                elif test['parameter_value'] > test['lower_bound'] and test['parameter_value'] < test['upper_bound'] :
                    c.setFont("SofiaProBold", 15)    
                    r,g,b = 30,207,58
                    c.setFillColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 5, stroke=0, fill=1)
                    c.setStrokeColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 7, stroke=1, fill=0)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(515, 654, "Normal")

                elif test['impression'] == 'BL':
                    c.setFont("SofiaProBold", 15)    
                    r,g,b = 248,215,122
                    c.setFillColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 5, stroke=0, fill=1)
                    c.setStrokeColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 7, stroke=1, fill=0)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(515, 654, "Borderline")
                    highlighted_tests.append([tuple_of_test[0],[test['parameter_name'],test['parameter_value']]])


                c.setFillColorRGB(1, 1, 1)
                c.setFont("SofiaPro", 9)
                if test['lower_bound'] != '':
                    c.drawString(310,612  , "<"+test['lower_bound'] + test['unit'] )
                if test['upper_bound'] != '':
                    c.drawString(509,612  , test['upper_bound'] + test['unit'] + ">")
                if test['upper_bound'] != '' and test['lower_bound'] != '':
                    try:
                        c.drawString(405, 612, test['display_value'] + test['unit'])
                    except:
                        c.drawString(405, 612, test['lower_bound'] + " - "+test['upper_bound'] + test['unit'])

                
                if test['parameter_value'] > test['upper_bound']:
                    c.drawImage("Resources/box.png",520,576,width=65,height=35,mask='auto')
                    c.setFont("SofiaPro", 11)
                    c.setFillColorRGB(1, 1, 1)
                    c.drawString(530, 590, "You: "+ test['parameter_value'] )   
                elif test['parameter_value'] < test['lower_bound']:
                    c.drawImage("Resources/box.png",325,576,width=65,height=35,mask='auto')
                    c.setFont("SofiaPro", 11)
                    c.setFillColorRGB(1, 1, 1)
                    c.drawString(335, 590, "You: "+ test['parameter_value'] )
                elif test['parameter_value'] > test['lower_bound'] and test['parameter_value'] < test['upper_bound']:
                    c.drawImage("Resources/box.png",426,576,width=65,height=35,mask='auto')
                    c.setFont("SofiaPro", 11)
                    c.setFillColorRGB(1, 1, 1)
                    c.drawString(436, 590, "You: "+ test['parameter_value'] ) 


                if test['parameter_value'] > test['upper_bound'] or test['parameter_value'] < test['lower_bound']:
                    c.setFont("RobotoBold", 17)
                    c.setFillColorRGB(0,61/255,108/255)
                    c.drawString(22, 547, "Possible Cause of abnormal results: ")
                    c.setFont("EastmanRegular", 9)
                    if test['parameter_value'] > test['upper_bound']:
                        high_low = "high"
                    else:
                        high_low = "low"
                    paragraphp = Paragraph(get_data_cause_para(test['parameter_name']+" Test",high_low), styles['Normal']) 
                    paragraphp.wrap(500, 260)
                    paragraphp.drawOn(c, 22, 509)
                    causes = get_data_cause(test['parameter_name'],high_low)
                    paragraph1 = Paragraph(causes[0], styles['Normal'])
                    paragraph1.wrap(100, 40)
                    paragraph1.drawOn(c, 110, 495- paragraph1.height)
                    paragraph2 = Paragraph(causes[1], styles['Normal'])
                    paragraph2.wrap(100, 45)
                    paragraph2.drawOn(c, 290, 495- paragraph2.height)
                    paragraph3 = Paragraph(causes[2], styles['Normal'])
                    paragraph3.wrap(100, 40)
                    paragraph3.drawOn(c, 455, 495 - paragraph3.height)

                if test['parameter_value'] > test['lower_bound'] and test['parameter_value'] < test['upper_bound'] :
                    c.setFont("RobotoBold", 17)
                    c.setFillColorRGB(0,61/255,108/255)
                    c.drawString(22, 547,  "Seems like your all good! ")
                    c.setFont("RobotoRegular", 12)
                    paragraphp = Paragraph(get_data_cause_para(test['parameter_name']+" Test","normal"), styles['Normal']) 
                    paragraphp.wrap(500, 260)
                    paragraphp.drawOn(c, 22, 509)
                    causes = get_data_cause(test['parameter_name'],"normal")
                    paragraph1 = Paragraph(causes[0], styles['Normal'])
                    paragraph1.wrap(100, 40)
                    paragraph1.drawOn(c, 110, 495 - paragraph1.height)
                    paragraph2 = Paragraph(causes[1], styles['Normal'])
                    paragraph2.wrap(100, 45)
                    paragraph2.drawOn(c, 290, 495 - paragraph2.height)
                    paragraph3 = Paragraph(causes[2], styles['Normal'])
                    paragraph3.wrap(100, 40)
                    paragraph3.drawOn(c, 455, 495 - paragraph3.height)

            else:
                
                c.setFillColorRGB(0,61/255,108/255)
                #Test Param name
                if len(test['parameter_name']+" Test") > 22:
                    c.setFont("RobotoBold", 11)
                    c.drawString(22, 420, test['parameter_name']+" Test")
                else:
                    c.setFont("RobotoBold", 17) 
                    c.drawString(22, 420, test['parameter_name']+" Test")
                
                c.setFont("RobotoRegular", 9)
                #About Test
                paragraph = Paragraph(get_data(test['parameter_name']+" Test"), styles['Normal']) 
                paragraph.wrap(200, 280)
                paragraph.drawOn(c, 22, 416 - paragraph.height)

                c.setFont("RobotoBold", 17) 
                c.setFillColorRGB(0,61/255,108/255)
                c.drawString(289, 420, "Test Value : " +test['parameter_value'] + " " + test['unit'])

                if test['parameter_value'] > test['upper_bound'] and test['is_highlighted']:
                    c.setFont("SofiaProBold", 15)    
                    r,g,b = 219,68,55
                    c.setFillColorRGB(r/255, g/255, b/255)
                    c.circle(500, 428, 5, stroke=0, fill=1)
                    c.setStrokeColorRGB(r/255, g/255, b/255)
                    c.circle(500, 428, 7, stroke=1, fill=0)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(515, 422, "High")
                    highlighted_tests.append([tuple_of_test[0],[test['parameter_name'],test['parameter_value']]])

                elif test['parameter_value'] < test['lower_bound'] and test['is_highlighted']:
                    c.setFont("SofiaProBold", 15)    
                    r,g,b = 219,68,55
                    c.setFillColorRGB(r/255, g/255, b/255)
                    c.circle(500, 428, 5, stroke=0, fill=1)
                    c.setStrokeColorRGB(r/255, g/255, b/255)
                    c.circle(500, 428, 7, stroke=1, fill=0)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(515, 422, "Low")
                    highlighted_tests.append([tuple_of_test[0],[test['parameter_name'],test['parameter_value']]])
                
                elif test['parameter_value'] > test['lower_bound'] and test['parameter_value'] < test['upper_bound'] and test['is_highlighted']:
                    c.setFont("SofiaProBold", 15)    
                    r,g,b = 30,207,58
                    c.setFillColorRGB(r/255, g/255, b/255)
                    c.circle(500, 428, 5, stroke=0, fill=1)
                    c.setStrokeColorRGB(r/255, g/255, b/255)
                    c.circle(500, 428, 7, stroke=1, fill=0)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(515, 422, "Normal")

                elif test['impression'] == 'BL':
                    c.setFont("SofiaProBold", 15)    
                    r,g,b = 248,215,122
                    c.setFillColorRGB(r/255, g/255, b/255)
                    c.circle(500, 428, 5, stroke=0, fill=1)
                    c.setStrokeColorRGB(r/255, g/255, b/255)
                    c.circle(500, 428, 7, stroke=1, fill=0)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(515, 422, "Borderline")
                    highlighted_tests.append([tuple_of_test[0],[test['parameter_name'],test['parameter_value']]])


                c.setFillColorRGB(1, 1, 1)
                c.setFont("SofiaPro", 9)
                if test['lower_bound'] != '':
                    c.drawString(310,380  , "<"+test['lower_bound'] + test['unit'] )
                if test['upper_bound'] != '':
                    c.drawString(509,380  , test['upper_bound'] + test['unit'] + ">")
                if test['upper_bound'] != '' and test['lower_bound'] != '':
                    try:
                        c.drawString(405, 380, test['display_value'] + test['unit'])
                    except:
                        c.drawString(405, 380, test['lower_bound'] + " - "+test['upper_bound'] + test['unit'])

                
                if test['parameter_value'] > test['upper_bound']:
                    c.drawImage("Resources/box.png",520,344,width=65,height=35,mask='auto')
                    c.setFont("SofiaPro", 11)
                    c.setFillColorRGB(1, 1, 1)
                    c.drawString(530, 358, "You: "+ test['parameter_value'] )   
                elif test['parameter_value'] < test['lower_bound']:
                    c.drawImage("Resources/box.png",325,344,width=65,height=35,mask='auto')
                    c.setFont("SofiaPro", 11)
                    c.setFillColorRGB(1, 1, 1)
                    c.drawString(335, 358, "You: "+ test['parameter_value'] )
                elif test['parameter_value'] > test['lower_bound'] and test['parameter_value'] < test['upper_bound']:
                    c.drawImage("Resources/box.png",426,344,width=65,height=35,mask='auto')
                    c.setFont("SofiaPro", 11)
                    c.setFillColorRGB(1, 1, 1)
                    c.drawString(436, 358, "You: "+ test['parameter_value'] ) 


                if test['parameter_value'] > test['upper_bound'] or test['parameter_value'] < test['lower_bound']:
                    c.setFont("RobotoBold", 17)
                    c.setFillColorRGB(0,61/255,108/255)
                    c.drawString(22, 315, "Possible Cause of abnormal results: ")
                    c.setFont("EastmanRegular", 9)
                    if test['parameter_value'] > test['upper_bound']:
                        high_low = "high"
                    else:
                        high_low = "low"
                    paragraphp = Paragraph(get_data_cause_para(test['parameter_name']+" Test",high_low), styles['Normal']) 
                    paragraphp.wrap(500, 260)
                    paragraphp.drawOn(c, 22, 277)
                    causes = get_data_cause(test['parameter_name'],high_low)
                    paragraph1 = Paragraph(causes[0], styles['Normal'])
                    paragraph1.wrap(100, 40)
                    paragraph1.drawOn(c, 110, 263- paragraph1.height)
                    paragraph2 = Paragraph(causes[1], styles['Normal'])
                    paragraph2.wrap(100, 45)
                    paragraph2.drawOn(c, 290, 263- paragraph2.height)
                    paragraph3 = Paragraph(causes[2], styles['Normal'])
                    paragraph3.wrap(100, 40)
                    paragraph3.drawOn(c, 455, 263 - paragraph3.height)

                if test['parameter_value'] > test['lower_bound'] and test['parameter_value'] < test['upper_bound'] :
                    c.setFont("RobotoBold", 17)
                    c.setFillColorRGB(0,61/255,108/255)
                    c.drawString(22, 315,"Seems like your all good! ")
                    c.setFont("RobotoRegular", 12)
                    paragraphp = Paragraph(get_data_cause_para(test['parameter_name']+" Test","normal"), styles['Normal']) 
                    paragraphp.wrap(500, 260)
                    paragraphp.drawOn(c, 22, 277)
                    causes = get_data_cause(test['parameter_name'],"normal")
                    paragraph1 = Paragraph(causes[0], styles['Normal'])
                    paragraph1.wrap(100, 40)
                    paragraph1.drawOn(c, 110, 263 - paragraph1.height)
                    paragraph2 = Paragraph(causes[1], styles['Normal'])
                    paragraph2.wrap(100, 45)
                    paragraph2.drawOn(c, 290, 263 - paragraph2.height)
                    paragraph3 = Paragraph(causes[2], styles['Normal'])
                    paragraph3.wrap(100, 40)
                    paragraph3.drawOn(c, 455, 263 - paragraph3.height)


            tests_printed+=1
            if init_tests !=2:
                tests_left_to_print -= 1

        elif tests_left_to_print == 1 and final_page == False:
                if tests_printed != 1:
                    c.showPage()
                c.drawImage("./Resources/1test_report_page.png", 0, 0, width=page_size[0], height=page_size[1])
                c.setFont("RobotoBold", 20)
                c.setFillColorRGB(0,0,0)
                c.drawString(171, 694, tuple_of_test[0].title())

                my_barcode = EAN13(booking_id, writer=ImageWriter()) 
                my_barcode.save("./dynamic_resource/"+booking_id)
                c.drawImage("./dynamic_resource/"+booking_id+".png", 16, 147, width=100, height=40)
                c.setFont("SofiaPro", 11)
                c.drawString(85, 133,booking_id)
                
        

                
                c.setFillColorRGB(0,61/255,108/255)
                #Test Param name
                if len(test['parameter_name']+" Test") > 22:
                    c.setFont("RobotoBold", 11)
                    c.drawString(22, 652, test['parameter_name']+" Test")
                else:
                    c.setFont("RobotoBold", 17) 
                    c.drawString(22, 652, test['parameter_name']+" Test")
                
                c.setFont("RobotoRegular", 9)
                #About Test
                paragraph = Paragraph(get_data(test['parameter_name']+" Test"), styles['Normal']) 
                paragraph.wrap(200, 280)
                paragraph.drawOn(c, 22, 648 - paragraph.height)

                c.setFont("RobotoBold", 17) 
                c.setFillColorRGB(0,61/255,108/255)
                c.drawString(289, 652, "Test Value : " +test['parameter_value'] + " " + test['unit'])

                if test['parameter_value'] > test['upper_bound'] and test['is_highlighted']:
                    c.setFont("SofiaProBold", 15)    
                    r,g,b = 219,68,55
                    c.setFillColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 5, stroke=0, fill=1)
                    c.setStrokeColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 7, stroke=1, fill=0)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(515, 654, "High")
                    highlighted_tests.append([tuple_of_test[0],[test['parameter_name'],test['parameter_value']]])

                elif test['parameter_value'] < test['lower_bound'] and test['is_highlighted']:
                    c.setFont("SofiaProBold", 15)    
                    r,g,b = 219,68,55
                    c.setFillColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 5, stroke=0, fill=1)
                    c.setStrokeColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 7, stroke=1, fill=0)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(515, 654, "Low")
                    highlighted_tests.append([tuple_of_test[0],[test['parameter_name'],test['parameter_value']]])
                
                elif test['parameter_value'] > test['lower_bound'] and test['parameter_value'] < test['upper_bound'] and test['is_highlighted']:
                    c.setFont("SofiaProBold", 15)    
                    r,g,b = 30,207,58
                    c.setFillColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 5, stroke=0, fill=1)
                    c.setStrokeColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 7, stroke=1, fill=0)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(515, 654, "Normal")

                elif test['impression'] == 'BL':
                    c.setFont("SofiaProBold", 15)    
                    r,g,b = 248,215,122
                    c.setFillColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 5, stroke=0, fill=1)
                    c.setStrokeColorRGB(r/255, g/255, b/255)
                    c.circle(500, 660, 7, stroke=1, fill=0)
                    c.setFillColorRGB(0, 0, 0)
                    c.drawString(515, 654, "Borderline")
                    highlighted_tests.append([tuple_of_test[0],[test['parameter_name'],test['parameter_value']]])


                c.setFillColorRGB(1, 1, 1)
                c.setFont("SofiaPro", 9)
                if test['lower_bound'] != '':
                    c.drawString(310,612  , "<"+test['lower_bound'] + test['unit'] )
                if test['upper_bound'] != '':
                    c.drawString(509,612  , test['upper_bound'] + test['unit'] + ">")
                if test['upper_bound'] != '' and test['lower_bound'] != '':
                    try:
                        c.drawString(405, 612, test['display_value'] + test['unit'])
                    except:
                        c.drawString(405, 612, test['lower_bound'] + " - "+test['upper_bound'] + test['unit'])

                
                if test['parameter_value'] > test['upper_bound']:
                    c.drawImage("Resources/box.png",520,576,width=65,height=35,mask='auto')
                    c.setFont("SofiaPro", 11)
                    c.setFillColorRGB(1, 1, 1)
                    c.drawString(530, 590, "You: "+ test['parameter_value'] )   
                elif test['parameter_value'] < test['lower_bound']:
                    c.drawImage("Resources/box.png",325,576,width=65,height=35,mask='auto')
                    c.setFont("SofiaPro", 11)
                    c.setFillColorRGB(1, 1, 1)
                    c.drawString(335, 590, "You: "+ test['parameter_value'] )
                elif test['parameter_value'] > test['lower_bound'] and test['parameter_value'] < test['upper_bound']:
                    c.drawImage("Resources/box.png",426,576,width=65,height=35,mask='auto')
                    c.setFont("SofiaPro", 11)
                    c.setFillColorRGB(1, 1, 1)
                    c.drawString(436, 590, "You: "+ test['parameter_value'] ) 


                if test['parameter_value'] > test['upper_bound'] or test['parameter_value'] < test['lower_bound']:
                    c.setFont("RobotoBold", 17)
                    c.setFillColorRGB(0,61/255,108/255)
                    c.drawString(22, 547, "Possible Cause of abnormal results: ")
                    c.setFont("EastmanRegular", 9)
                    if test['parameter_value'] > test['upper_bound']:
                        high_low = "high"
                    else:
                        high_low = "low"
                    paragraphp = Paragraph(get_data_cause_para(test['parameter_name']+" Test",high_low), styles['Normal']) 
                    paragraphp.wrap(500, 260)
                    paragraphp.drawOn(c, 22, 509)
                    causes = get_data_cause(test['parameter_name'],high_low)
                    paragraph1 = Paragraph(causes[0], styles['Normal'])
                    paragraph1.wrap(100, 40)
                    paragraph1.drawOn(c, 110, 495- paragraph1.height)
                    paragraph2 = Paragraph(causes[1], styles['Normal'])
                    paragraph2.wrap(100, 45)
                    paragraph2.drawOn(c, 290, 495- paragraph2.height)
                    paragraph3 = Paragraph(causes[2], styles['Normal'])
                    paragraph3.wrap(100, 40)
                    paragraph3.drawOn(c, 455, 495 - paragraph3.height)

                if test['parameter_value'] > test['lower_bound'] and test['parameter_value'] < test['upper_bound'] :
                    c.setFont("RobotoBold", 17)
                    c.setFillColorRGB(0,61/255,108/255)
                    c.drawString(22, 547,  "Seems like your all good! ")
                    c.setFont("RobotoRegular", 12)
                    paragraphp = Paragraph(get_data_cause_para(test['parameter_name']+" Test","normal"), styles['Normal']) 
                    paragraphp.wrap(500, 260)
                    paragraphp.drawOn(c, 22, 509)
                    causes = get_data_cause(test['parameter_name'],"normal")
                    paragraph1 = Paragraph(causes[0], styles['Normal'])
                    paragraph1.wrap(100, 40)
                    paragraph1.drawOn(c, 110, 495 - paragraph1.height)
                    paragraph2 = Paragraph(causes[1], styles['Normal'])
                    paragraph2.wrap(100, 45)
                    paragraph2.drawOn(c, 290, 495 - paragraph2.height)
                    paragraph3 = Paragraph(causes[2], styles['Normal'])
                    paragraph3.wrap(100, 40)
                    paragraph3.drawOn(c, 455, 495 - paragraph3.height)


                tests_printed+=1
                tests_left_to_print -= 1

    c.save()
    return highlighted_tests
        

# Creating Summary page with body image
def create_body_report_page(out_filename, page_size, report_png, highlighted_tests,test_names,booking_id):

    #Initialising variables
    c = canvas.Canvas(out_filename, pagesize=page_size)
    c.drawImage(report_png, 0, 0, width=page_size[0], height=page_size[1])
    init_y_highlighted = 645
    ref_points = [("Kidney",(285,400)),("Liver",(285,435)),("CBC",(285,500))]
    heading_style = ParagraphStyle(name='Heading', fontName='RobotoRegular', fontSize=10)
    message_style = ParagraphStyle(name='Message', fontName='SofiaPro', fontSize=8)
    overflow_style = ParagraphStyle(name='Overflow', fontName='RobotoRegular', fontSize=10, textColor='#97CF83')

    #Iterating through the highlighted tests
    for test in highlighted_tests:
        if init_y_highlighted > 100 :
            init_y_highlighted+= -45

            #Printing Styles (Color , line width , line dashes)
            c.setStrokeColorRGB(255, 0, 0)  
            c.setLineWidth(0.75)  
            c.setDash() 
            c.line(22, init_y_highlighted, 150, init_y_highlighted)  

            heading = Paragraph(str(test[0]), heading_style) 
            heading.wrap(200, 15)
            heading.drawOn(c, 22, init_y_highlighted+5)
            
            #Checks if test is in reference points and highlights it
            for item in ref_points:
                if item[0] in test[0]:
                    c.setStrokeColorRGB(255, 0, 0)  
                    c.setLineWidth(0.5) 
                    c.setDash(5, 2) 
                    c.line(160, init_y_highlighted, item[1][0], item[1][1])  
                        
            for param in test[1]:
                if init_y_highlighted > 100 :
                    message = Paragraph( str(param[0])+ " : " + param[1], message_style) 
                    message.wrap(200, 15)
                    message.drawOn(c,22, init_y_highlighted - 15)
                    init_y_highlighted+= -10


    not_highlighted_printed =0
    init_y2 = 645
    overflow_tests = []

    # Checks for tests which are not higlighted and prints them
    for test in test_names:
        if not_highlighted_printed < 10 :
            if test[0] not in [item[0] for item in highlighted_tests]:
                init_y2+= -45
                not_highlighted_printed+=1
                c.drawImage("./Resources/green_box2.png",420,init_y2-22,width=125,height=26,mask='auto')
            
                heading = Paragraph(str(test[0]), heading_style) 
                heading.wrap(150, 15)
                heading.drawOn(c, 425, init_y2)
                
                message = Paragraph("Everything looks good!", message_style) 
                message.wrap(90, 10)
                message.drawOn(c, 425, init_y2 - 15)
        else:
            if test[0] not in [item[0] for item in highlighted_tests]:
                overflow_tests.append(test[0])


    # If there are more than 10 tests which are not highlighted then it prints the overflow message
    if overflow_tests != []:
        init_y2+= -45        
        c.drawImage("./Resources/green_box2.png",420,init_y2-22,width=125,height=26,mask='auto')

        heading = Paragraph("+" + str(len(overflow_tests)) + " Tests", heading_style)   
        heading.wrap(150, 15)
        heading.drawOn(c, 425, init_y2)


        message = Paragraph("Everything looks good!", message_style) 
        message.wrap(90, 10)
        message.drawOn(c, 425, init_y2 - 15)

    
    c.save()
