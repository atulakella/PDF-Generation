import google.generativeai as genai

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
                ("Blood Sugar", "90 mg/dL")
            ]
        },
        "Jane Smith": {
            "2024-09-09": [
                ("Cholesterol", "200 mg/dL")
            ]
        }
    }
    
    # Return dummy data based on customer_name and booking_date
    patient_tests = dummy_data.get(customer_name, {}).get(booking_date, [])
    booking_id = "B12345" if patient_tests else None  # Dummy booking_id if data exists
    
    return patient_tests, booking_id

def get_data(test_name):
    try:
        response = model.generate_content(f"Give me a summary of this test in 30 words only: {test_name}")
        return response.text.strip()
    except Exception as e:
        print(f"Error fetching data for {test_name}: {e}")
        return "Error fetching data"

def get_data_cause(test_name, high_low_normal):
    try:
        response = model.generate_content(f"Generate 3 possible causes for {test_name} {high_low_normal} result. Each cause should be 10 words or less and should start with an index number.")
        return response.text.strip().split('\n')
    except Exception as e:
        print(f"Error fetching causes for {test_name} {high_low_normal}: {e}")
        return ["Error fetching causes"]

def get_data_cause_para(test_name, high_low):
    try:
        response = model.generate_content(f"Give me a general paragraph about {test_name} {high_low} result in only 30 words or less.")
        return response.text.strip()
    except Exception as e:
        print(f"Error fetching paragraph for {test_name} {high_low}: {e}")
        return "Error fetching paragraph"

def get_data_consider(test_name, high_low):
    try:
        response = model.generate_content(f"What are the recommended next steps for {test_name} {high_low} results? Please provide concise guidance within 50 words and do not provide causes.")
        return response.text.strip()
    except Exception as e:
        print(f"Error fetching considerations for {test_name} {high_low}: {e}")
        return "Error fetching considerations"

def merge_lists(existing_list, new_list):
    for new_item in new_list:
        found = False
        for existing_item in existing_list:
            if existing_item[0] == new_item[0]:
                existing_item[1].append(new_item[1])
                found = True
                break
        if not found:
            existing_list.append([new_item[0], [new_item[1]]])
        
    return existing_list

# def test_script_functions():
#     # Test get_patient_docs with predefined dummy data
#     def test_get_patient_docs():
#         test_cases = [
#             ("John Doe", "2024-09-08"),
#             ("Jane Smith", "2024-09-09"),
#             ("Unknown", "2024-09-09")
#         ]
        
#         for customer_name, booking_date in test_cases:
#             patient_tests, booking_id = get_patient_docs(customer_name, booking_date)
#             print(f"Customer: {customer_name}, Booking Date: {booking_date}, Patient Tests: {patient_tests}, Booking ID: {booking_id}")
    
#     # Test get_data with predefined test names
#     def test_get_data():
#         test_names = ["Blood Pressure", "Blood Sugar", "Cholesterol"]
        
#         for test_name in test_names:
#             response = get_data(test_name)
#             print(f"Test Name: {test_name}, Response: {response}")
    
#     # Test get_data_cause with predefined test names
#     def test_get_data_cause():
#         test_cases = [
#             ("Blood Pressure", "high"),
#             ("Blood Sugar", "low"),
#             ("Cholesterol", "normal")
#         ]
        
#         for test_name, high_low_normal in test_cases:
#             response = get_data_cause(test_name, high_low_normal)
#             print(f"Test Name: {test_name}, High/Low/Normal: {high_low_normal}, Response: {response}")
    
#     # Test get_data_cause_para with predefined test names
#     def test_get_data_cause_para():
#         test_cases = [
#             ("Blood Pressure", "high"),
#             ("Blood Sugar", "low"),
#             ("Cholesterol", "normal")
#         ]
        
#         for test_name, high_low in test_cases:
#             response = get_data_cause_para(test_name, high_low)
#             print(f"Test Name: {test_name}, High/Low: {high_low}, Response: {response}")
    
#     # Test get_data_consider with predefined test names
#     def test_get_data_consider():
#         test_cases = [
#             ("Blood Pressure", "high"),
#             ("Blood Sugar", "low"),
#             ("Cholesterol", "normal")
#         ]
        
#         for test_name, high_low in test_cases:
#             response = get_data_consider(test_name, high_low)
#             print(f"Test Name: {test_name}, High/Low: {high_low}, Response: {response}")

#     # Call all test functions
#     test_get_patient_docs()
#     test_get_data()
#     test_get_data_cause()
#     test_get_data_cause_para()
#     test_get_data_consider()

# # Run the tests
# test_script_functions()
