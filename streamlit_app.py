import streamlit as st
import io
import fitz  # module name provided by PyMuPDF(Extract text from pdf)
import re#regular expression-helps python read inside text
from dotenv import load_dotenv#to read API key from .env file
import google.generativeai as genai#to use Gemini API
import os
from PIL import Image





st.set_page_config(#page settings
    page_title="Soil Health Report Analyzer",#app title
    layout="wide"#makes the app use more screen width instead of a narrow center layout.
)

st.title("Soil Health Report Analyzer")#title of the page 

st.write("Upload a soil test report in PDF or image format.")#This prints normal text on the page.


st.warning(
    "Note: The ranges used in this app are general reference ranges. "
    "Actual recommendations may vary by crop, region, and soil type."
)


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)





#Reading pdf 
def extract_text_from_pdf(uploaded_file):#take uploaded PDF → read pages → return extracted text
    pdf_bytes = uploaded_file.read()#A PDF file is stored as bytes inside Python.this line reads the uploaded PDF file.Think of bytes as the raw file data.

    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")#opens pdf from memory , we r not saving it but opening the uploaded file

    full_text = ""#empty string , coz we'll keep adding pgs to this var 

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]#get a pg from the doc 
        text = page.get_text()#extract the txt 
        full_text = full_text + text + "\n"#means append the contents of text to full_text and then add a new line.

    pdf_document.close()#close

    return full_text




def extract_text_with_gemini(uploaded_file):
    if not GEMINI_API_KEY:
        return "Gemini API key not found. Please check your .env file."

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = """
    Read this soil test report carefully.

    Extract the important soil values such as:
    pH, Nitrogen, Phosphorus, Potassium, Organic Carbon, EC.

    Return the result as simple text in this exact format:
    pH: value
    Nitrogen: value
    Phosphorus: value
    Potassium: value
    Organic Carbon: value
    EC: value

    If any value is not present, write Not found.
    """

    file_bytes = uploaded_file.getvalue()

    if uploaded_file.type == "application/pdf":
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        images = []

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(image)

        pdf_document.close()

        response = model.generate_content([prompt] + images)
        return response.text

    else:
        image = Image.open(io.BytesIO(file_bytes))
        response = model.generate_content([prompt, image])
        return response.text




def find_soil_parameters(text):#This function takes the extracted PDF text, Its job is to find important soil values.
    parameters = {}

    patterns = {#a dictionary to store all the values - it has param name and its search pattern
        "pH": r"pH\s*[:\-]?\s*([0-9]+\.?[0-9]*)", #ex.For pH, search text like pH: 7.5 or pH - 7.5 or pH 7.5
        "Nitrogen": r"Nitrogen\s*[:\-]?\s*([0-9]+\.?[0-9]*)",
        "Phosphorus": r"Phosphorus\s*[:\-]?\s*([0-9]+\.?[0-9]*)",
        "Potassium": r"Potassium\s*[:\-]?\s*([0-9]+\.?[0-9]*)",
        "Organic Carbon": r"Organic\s*Carbon\s*[:\-]?\s*([0-9]+\.?[0-9]*)",
        "EC": r"EC\s*[:\-]?\s*([0-9]+\.?[0-9]*)"
    }

    for parameter_name, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)#This searches the uploaded PDF text., re.IGNORECASE means it does not care about capital/small letters.

        if match:
            parameters[parameter_name] = match.group(1)
        else:
            parameters[parameter_name] = "Not found"

    return parameters





#no we will give themeaning of the vaalues which we extracted - parameter name,value,status,explanation, recommendation

def analyze_soil_parameters(soil_parameters):
    analysis = []

    for parameter, value in soil_parameters.items():

        if value == "Not found":
            analysis.append({
                "Parameter": parameter,
                "Value": "Not found",
                "Status": "Unknown",
                "Meaning": "This value was not found in the report.",
                "Recommendation": "Please check the report or upload a clearer file."
            })
            continue

        number = float(value)

        if parameter == "pH":
            if number < 6.5:
                status = "Low"
                meaning = "Soil is acidic."
                recommendation = "Add lime only after expert guidance. Add organic manure."
            elif number > 7.5:
                status = "High"
                meaning = "Soil is alkaline."
                recommendation = "Add organic matter and avoid overuse of alkaline irrigation water."
            else:
                status = "Good"
                meaning = "Soil pH is suitable for most crops."
                recommendation = "Maintain current soil condition."

        elif parameter == "Nitrogen":
            if number < 280:
                status = "Low"
                meaning = "Nitrogen is low. Plant growth may be weak."
                recommendation = "Use compost, green manure, or nitrogen fertilizer in split doses."
            elif number > 560:
                status = "High"
                meaning = "Nitrogen is high."
                recommendation = "Avoid extra nitrogen fertilizer."
            else:
                status = "Medium"
                meaning = "Nitrogen is in a balanced range."
                recommendation = "Maintain balanced fertilizer use."

        elif parameter == "Phosphorus":
            if number < 10:
                status = "Low"
                meaning = "Phosphorus is low. Root growth may be affected."
                recommendation = "Use phosphorus fertilizer as per crop requirement."
            elif number > 25:
                status = "High"
                meaning = "Phosphorus is high."
                recommendation = "Avoid extra phosphorus fertilizer."
            else:
                status = "Medium"
                meaning = "Phosphorus is adequate for many crops."
                recommendation = "Maintain balanced fertilizer use."

        elif parameter == "Potassium":
            if number < 110:
                status = "Low"
                meaning = "Potassium is low. Crop strength and stress tolerance may reduce."
                recommendation = "Use potash fertilizer as per crop requirement."
            elif number > 280:
                status = "High"
                meaning = "Potassium is high."
                recommendation = "Avoid extra potash fertilizer."
            else:
                status = "Medium"
                meaning = "Potassium is in a healthy range."
                recommendation = "Maintain balanced fertilizer use."

        elif parameter == "Organic Carbon":
            if number < 0.5:
                status = "Low"
                meaning = "Organic carbon is low. Soil fertility and water holding may be poor."
                recommendation = "Add farmyard manure, compost, crop residue, or green manure."
            elif number > 0.75:
                status = "Good"
                meaning = "Organic carbon is good."
                recommendation = "Continue adding organic matter to maintain soil health."
            else:
                status = "Medium"
                meaning = "Organic carbon is moderate."
                recommendation = "Add organic matter regularly to improve soil quality."

        elif parameter == "EC":
            if number > 1.0:
                status = "High"
                meaning = "Soil salt level is high."
                recommendation = "Improve drainage and use good-quality irrigation water."
            else:
                status = "Good"
                meaning = "Soil salt level is safe for most crops."
                recommendation = "Maintain proper irrigation and drainage."

        analysis.append({
            "Parameter": parameter,
            "Value": value,
            "Status": status,
            "Meaning": meaning,
            "Recommendation": recommendation
        })

    return analysis


#DISPLAYING INFO ON DASHBOARD
def show_dashboard(analysis):
    st.subheader("Soil Health Dashboard")

    columns = st.columns(3)

    for index, item in enumerate(analysis):
        status = item["Status"]

        if status == "Low":
            box_color = "#fff3cd"
            border_color = "#ff9800"
        elif status == "High":
            box_color = "#f8d7da"
            border_color = "#dc3545"
        elif status in ["Good", "Medium"]:
            box_color = "#d4edda"
            border_color = "#28a745"
        else:
            box_color = "#e2e3e5"
            border_color = "#6c757d"

        with columns[index % 3]:
            st.markdown(
    f"""
<div style="
background-color: {box_color};
border-left: 8px solid {border_color};
padding: 18px;
border-radius: 8px;
margin-bottom: 18px;
color: #111827;
min-height: 210px;
">
<h4 style="color: #111827; margin-bottom: 12px;">
{item["Parameter"]}
</h4>

<h2 style="color: #111827; margin-bottom: 12px;">
{item["Value"]}
</h2>

<p style="color: #111827; font-weight: 700;">
Status: {item["Status"]}
</p>

<p style="color: #111827;">
{item["Meaning"]}
</p>
</div>
""",
    unsafe_allow_html=True
)
    st.subheader("Detailed Analysis")
    st.table(analysis)

    st.subheader("Recommendations")

    for item in analysis:
        st.write(f"**{item['Parameter']}:** {item['Recommendation']}")





uploaded_file = st.file_uploader(#creates a upload box accepting files given elow 
    "Choose a soil report",
    type=["pdf", "png", "jpg", "jpeg"]
)
#uploaded file will be stored in the var uploaded_file


if uploaded_file is not None:  #uploaded
    st.success("File uploaded successfully")
#basic details of the file uploaded 
    st.write("File name:", uploaded_file.name)
    st.write("File type:", uploaded_file.type)
    st.write("File size:", uploaded_file.size, "bytes")

    if uploaded_file.type.startswith("image"): # If uploaded file is an image(jpeg, png)
        st.image(uploaded_file, caption="Uploaded Soil Report", use_container_width=True)#This displays the uploaded image inside the app.#use_container_width- makes the image fit over the  width of the page 
        st.info("Image uploaded. Reading text using Gemini Vision...")

        extracted_text = extract_text_with_gemini(uploaded_file)

        with st.expander("View Gemini extracted text"):
            st.text_area("Text found by Gemini", extracted_text, height=220)

        soil_parameters = find_soil_parameters(extracted_text)

        analysis = analyze_soil_parameters(soil_parameters)

        show_dashboard(analysis)


    elif uploaded_file.type == "application/pdf": #if uploaded file is a pdf 
        st.info("PDF uploaded. In the next step, we will extract text from this PDF.") #not reading rn , so just display the msg 
        

        #Reading pdf 
        extracted_text = extract_text_from_pdf(uploaded_file)#function call -send uploaded PDF to extract_text_from_pdf(),get text back,store it in extracted_text

        st.subheader("Extracted Text from Report")

        if extracted_text.strip():#strip() removes empty spaces and blank lines.
            st.text_area( #Show extracted text in box
                "Text found in PDF",
                extracted_text,
                height=300
            )


            soil_parameters = find_soil_parameters(extracted_text)#caall the function where values are extracted 
            st.table(soil_parameters)#show the extracted values in the table 
            st.subheader("Soil Analysis")

            analysis = analyze_soil_parameters(soil_parameters)

            st.table(analysis)
            show_dashboard(analysis)
        else:
            st.warning("No text found in this PDF. It may be a scanned image PDF.")

else:
    st.info("Please upload a PDF or image soil report.")# If no file is uploaded