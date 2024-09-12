import google.generativeai as genai
import time
# Configure the API with your actual API key
genai.configure(api_key="AIzaSyCjvhclrgeAWAQVMRDQ2O3Bti6i2y_YoDQ")

# Initialize the model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def get_patient_docs(customer_name, booking_date):
    # Define dummy data for testing purposes
    dummy_data = {
        "John Doe": {
            "2024-09-08": [
                ("Blood Pressure", "120/80"),
                ("Blood Sugar", "90 mg/dL"),
                ("Cholesterol", "190 mg/dL"),
                ("Vitamin D", "30 ng/mL"),
                ("Hemoglobin", "14 g/dL"),
                ("White Blood Cell Count", "5,000 /µL"),
                ("Platelets", "250,000 /µL"),
                ("Sodium", "140 mEq/L"),
                ("Potassium", "4.0 mEq/L"),
                ("Calcium", "9.0 mg/dL")
            ]
        },
        "Jane Smith": {
            "2024-09-09": [
                ("Cholesterol", "200 mg/dL"),
                ("Blood Pressure", "130/85"),
                ("Blood Sugar", "85 mg/dL"),
                ("Vitamin D", "25 ng/mL")
            ]
        }
    }
    
    # Return dummy data based on customer_name and booking_date
    patient_tests = dummy_data.get(customer_name, {}).get(booking_date, [])
    booking_id = "B12345" if patient_tests else None  # Dummy booking_id if data exists
    
    return patient_tests, booking_id

def get_data(test_name):
    try:
        time.sleep(6)
        response = model.generate_content(f"Give me a summary of this test in 30 words only and dont ask any questions: {test_name}")
        
        return response.text.strip()
    except Exception as e:
        print(f"Error fetching data for {test_name}: {e}")
        time.sleep(15)
        return "Error fetching data"

def get_data_cause(test_name, high_low_normal):
    try:
        time.sleep(1)
        response = model.generate_content(f"Generate 3 possible causes for {test_name} {high_low_normal} result. Each cause should be 10 words or less and should NOT start with an index number and do not format the text at all.")
        return response.text.strip().split('\n')
    except Exception as e:
        print(f"Error fetching causes for {test_name} {high_low_normal}: {e}")
        time.sleep(15)
        return ["Error fetching causes"]

def get_data_cause_para(test_name, high_low):
    try:
        time.sleep(2)
        response = model.generate_content(f"Give me a general paragraph about {test_name} {high_low} result in only 30 words or less.")
        return response.text.strip()
    except Exception as e:
        print(f"Error fetching paragraph for {test_name} {high_low}: {e}")
        time.sleep(15)
        return "Error fetching paragraph"

def get_data_consider(test_name, high_low):
    try:
        response = model.generate_content(f"What are the recommended next steps for {test_name} {high_low} results? Please provide concise guidance within 50 words and do not provide causes.")
        return response.text.strip()
    except Exception as e:
        print(f"Error fetching considerations for {test_name} {high_low}: {e}")
        time.sleep(15)
        return "Error fetching considerations"


# data_fetching.py

def get_normal_range(test_name):
    # Updated normal ranges including new test types
    normal_ranges = {
        'Blood Pressure': '120/80 mmHg',
        'Cholesterol': '200 mg/dL',
        'Blood Sugar': '70-99 mg/dL',
        'Vitamin D': '20-50 ng/mL',
        'Hemoglobin': '13.8-17.2 g/dL',  
        'White Blood Cell Count': '4,000-11,000 /µL',  
        'Platelets': '150,000-450,000 /µL',  
        'Sodium': '135-145 mEq/L',  
        'Potassium': '3.5-5.0 mEq/L',  
        'Calcium': '8.5-10.2 mg/dL'  
    }
    return normal_ranges.get(test_name, 'Normal range not available')



