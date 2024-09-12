# PDF Generator

This project generates PDF reports for medical test results using a combination of ReportLab and a generative AI model. The PDF report includes patient test results, normal ranges, possible causes for abnormal results, and recommendations for next steps.

## Features

- **PDF Generation**
- **Customizable Cover Page**
- **Detailed Test Information**
- **AI-Generated Insights**

## Prerequisites

1. **Python 3.x**: Ensure you have Python 3.x installed on your system.
2. **Libraries**:
   - `reportlab`: For generating PDF files.
   - `google-generativeai`: For interfacing with the generative AI model.

   Install the required libraries using pip:
   ```bash
   pip install reportlab google-generativeai
## Setup

1. **API Key**:
   - Obtain an API key from your generative AI service provider (e.g., Google Cloud).
   - Configure the API key in the `anotherTest.py` file. Locate the line where `genai.configure(api_key="YOUR_API_KEY")` is defined and replace `"YOUR_API_KEY"` with your actual API key.

2. **Cover Image**:
   - Place the cover image file named `cover.png` in the project directory.
   - Ensure the image is properly sized and formatted to fit the cover page of the PDF.

3. **Background Image**:
   - Place the background image file named `normal.png` in the project directory.
   - Ensure this image is suitable for use as the background of each page in the PDF.

4. **Data Fetching Functions**:
   - Update the `data_fetching.py` file with the actual implementations of the following functions:
     - `get_patient_docs(customer_name, booking_date)`: Retrieves patient test data.
     - `get_normal_range(test_name)`: Provides the normal range for each test.
     - `get_data(test_name)`: Generates a summary for the test.
     - `get_data_cause(test_name, high_low_normal)`: Provides possible causes for abnormal results.
     - `get_data_cause_para(test_name, high_low)`: Offers a general paragraph about abnormal results.
     - `get_data_consider(test_name, high_low)`: Suggests next steps or considerations.

5. **Dependencies**:
   - Ensure you have the required Python libraries installed. Install them using pip:
     ```bash
     pip install reportlab google-generativeai
     ```

