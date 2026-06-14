# Soil Health Report Analyzer

An AI-powered Streamlit application that accepts a soil test report in PDF or image format and explains the report in a simple farmer-friendly way.

## Features

- Upload soil test report in PDF or image format
- Extract text from readable PDF reports using PyMuPDF
- Use Gemini Vision API for image reports and scanned PDFs
- Extract soil parameters such as:
  - pH
  - Nitrogen
  - Phosphorus
  - Potassium
  - Organic Carbon
  - Electrical Conductivity (EC)
- Classify values as Low, Medium, High, Good, or Unknown
- Provide simple explanations and general soil improvement recommendations
- Display results in a clean dashboard

## Technologies Used

- Python
- Streamlit
- PyMuPDF
- Google Gemini API
- python-dotenv
- Pillow

## Approach

The app first accepts a soil report from the user. If the uploaded file is a readable PDF, PyMuPDF extracts the text directly. If the uploaded file is an image or scanned PDF, Gemini Vision is used to read the report.

After text is extracted, the app searches for important soil parameters such as pH, Nitrogen, Phosphorus, Potassium, Organic Carbon, and EC. The extracted values are compared with general soil reference ranges. Based on this comparison, the app gives a simple status, explanation, and recommendation for each parameter.

## Assumptions

- The assignment did not provide exact crop-wise or region-wise soil ranges.
- This project uses general reference ranges for demonstration.
- Actual fertilizer recommendations may vary by crop, region, soil type, and local agriculture guidelines.
- N, P, and K values are assumed to be in kg/ha when units are not clearly mentioned.

## Limitations

- Very unclear images may reduce Gemini extraction accuracy.
- Handwritten reports may not always be read correctly.
- The app does not provide crop-specific fertilizer dosage.
- The app requires a Gemini API key for image and scanned PDF analysis.
- Recommendations are general and should be verified with an agriculture expert.

## Future Improvements

- Add support for regional languages
- Add crop-specific recommendations
- Add downloadable PDF report
- Add database to store past reports
- Improve extraction for different report formats
- Add confidence score for extracted values

## How To Run

1. Clone the repository.

```bash
git clone your-repository-link
cd Soil-report-analyser