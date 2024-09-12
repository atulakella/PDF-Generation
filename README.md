# PDF Generator

This project generates PDF reports for medical test results using a combination of ReportLab and a generative AI model. The PDF report includes patient test results, normal ranges, possible causes for abnormal results, and recommendations for next steps.

## Features

- **PDF Generation**: Creates a well-formatted PDF report.
- **Customizable Cover Page**: Includes patient details and booking ID.
- **Detailed Test Information**: Displays test names, results, normal ranges, and status (normal, high, or low).
- **AI-Generated Insights**: Provides summaries, possible causes, and recommendations using a generative AI model.

## Prerequisites

1. **Python 3.x**: Ensure you have Python 3.x installed on your system.
2. **Libraries**:
   - `reportlab`: For generating PDF files.
   - `google-generativeai`: For interfacing with the generative AI model.

   Install the required libraries using pip:
   ```bash
   pip install reportlab google-generativeai
