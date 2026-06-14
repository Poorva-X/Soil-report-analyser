Soil Health Report Analyzer

An AI-powered Streamlit application that helps farmers understand their soil test reports. Users upload a Soil Health Card or lab report (PDF or image), and the app extracts key soil parameters, explains them in simple language, and provides actionable recommendations through a clean dashboard.

Problem Statement

Farmers often receive Soil Health Card reports or laboratory soil test reports in image or PDF format but find it difficult to understand the technical information and make informed farming decisions. This app bridges that gap by extracting, analyzing, and presenting soil data in a farmer-friendly format.

Features


Accepts soil test reports in PDF, PNG, JPG, and JPEG formats
Extracts key parameters: pH, Nitrogen (N), Phosphorus (P), Potassium (K), Organic Carbon, and Electrical Conductivity (EC)
Two extraction modes:

Text-based PDFs: extracted directly using PyMuPDF and parsed with regex
Images / scanned reports: extracted using Google Gemini Vision API



Classifies each parameter as Low / Medium / High / Good based on general agronomic reference ranges
Explains each parameter in simple, non-technical language
Provides general soil improvement recommendations for each parameter
Displays results in a color-coded dashboard (cards + detailed table + recommendations)


Approach


File upload: User uploads a PDF or image via Streamlit's file uploader.
Text extraction:

If the file is a PDF, text is extracted directly using PyMuPDF (fitz). This is fast and free for digitally generated reports.
If the file is an image, or the PDF has no extractable text (a scanned document), the file is converted to image(s) and sent to Gemini Vision with a structured prompt asking it to return soil parameters in a fixed format.



Parameter extraction: A set of regex patterns scans the extracted text for the six target parameters and their numeric values.
Analysis: Each parameter value is compared against predefined reference ranges to determine its status (Low/Medium/High/Good), along with a plain-language explanation and recommendation.
Dashboard: Results are displayed as color-coded cards (green = good, yellow = low, red = high), a detailed table, and a recommendations list.


Technologies Used


Python 3
Streamlit – web app framework and UI
PyMuPDF (fitz) – PDF text extraction and rendering pages as images
Google Gemini API (gemini-1.5-flash) – vision-based extraction for images and scanned PDFs
Pillow (PIL) – image handling
python-dotenv – secure API key management via .env
re (regex) – parameter extraction from text


Setup Instructions


Clone the repository:


   git clone https://github.com/Poorva-X/Soil-report-analyser.git
   cd Soil-report-analyser


Install dependencies:


   pip install -r requirements.txt


Create a .env file in the project root and add your Gemini API key:


   GEMINI_API_KEY=your_api_key_here


Run the app:


   streamlit run streamlit_app.py

Assumptions


Soil reports contain parameter values in a recognizable format (e.g., "pH: 6.8" or "Nitrogen - 250").
The reference ranges used for classification (Low/Medium/High/Good) are general guidelines and not crop-, soil-, or region-specific.
Gemini Vision API is used for image-based and scanned reports; an active internet connection and valid API key are required for this path.
Only the six core parameters (pH, N, P, K, Organic Carbon, EC) are extracted and analyzed; other parameters present in a report are not currently processed.


Limitations


Reference ranges are general and may not reflect crop-specific or regional recommendations, as actual soil requirements vary by crop, soil type, and location.
Regex-based extraction depends on the report following a recognizable text format; reports with unusual layouts may not extract correctly.
The app currently extracts only six standard parameters and does not capture micronutrients (e.g., Zinc, Sulphur, Iron, Boron) even if present in the report.
Gemini Vision API usage is subject to rate limits and requires a valid API key.
No automated tests have been written; testing was done manually with sample reports.


Future Improvements


Support extraction of additional soil parameters (Sulphur, Zinc, Iron, Boron, Manganese, etc.).
Allow users to specify their crop and region for tailored recommendations.
Add multi-language support so farmers can view results in regional languages.
Provide a downloadable PDF summary of the analysis.
Improve extraction robustness using a hybrid approach that always cross-checks regex results against Gemini Vision output, regardless of file type.
Add OCR pre-processing (e.g., OpenCV) to improve image quality before sending to Gemini Vision.


Disclaimer

The ranges used in this app are general reference ranges. Actual recommendations may vary by crop, region, and soil type. This tool is intended to help farmers understand their reports better and should not replace expert agronomic advice.
