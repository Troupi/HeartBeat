import pickle
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu

# Read model
heart_model = pickle.load(open('heart_model.sav', 'rb'))

# Set page configuration
st.set_page_config(page_title="HeartBeats", page_icon=":heart:", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for background colors, fonts, and text justification
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;700&display=swap');
    .reportview-container .main {
        color: black;
        font-family: 'Urbanist', sans-serif;
        text-align: justify;
    }
    .css-1d391kg {
        font-family: 'Urbanist', sans-serif;
        text-align: justify;
    }
    h1, h2, h3, h4, h5, h6, p, div, label, input, textarea {
        font-family: 'Urbanist', sans-serif;
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize navigation state
if 'navigation' not in st.session_state:
    st.session_state.navigation = 'Home'

# Sidebar with logo
st.sidebar.image('Logo.png', use_column_width=True)

# Sidebar menu with icons
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Scan Prediction Test", "Contact"],
        icons=["house", "search", "envelope"],
        menu_icon="cast",
        default_index=["Home", "Scan Prediction Test", "Contact"].index(st.session_state.navigation),
    )
    st.session_state.navigation = selected

# Custom function to navigate between pages
def navigate_to(page):
    st.session_state.navigation = page

# Navigation between different pages
if st.session_state.navigation == "Home":
    st.write("## HeartBeats")
    st.image('Beranda.jpg')

    st.write("""
    HeartBeats adalah platform yang dapat membantu para dokter untuk memberikan diagnosa awal tentang kondisi dan kesehatan jantung. Dengan fitur scan kesehatan jantung yang dimiliki oleh HeartBeats, 
    setiap dokter dapat terbantu untuk mendapatkan hasil diagnosa terbaik dari platform ini.
    """)

    if st.button('Periksa sekarang'):
        navigate_to("Scan Prediction Test")

elif st.session_state.navigation == "Scan Prediction Test":
    st.write("## SCAN PREDICTION TEST")
    # Function to collect user input features into a dataframe
    col1, col2 = st.columns(2)
    with col1:
        age = st.text_input('Usia')
    
    with col2:
        sex = st.selectbox('Jenis kelamin', ['Pilih', 'Laki-laki', 'Perempuan'], key='sex')
    
    with col1:
        cp = st.selectbox('Jenis nyeri dada', ['Pilih', 'Typical angina', 'Atypical angina', 'Non-angina', 'Tanpa gejala'], key='cp')
        
    with col2:
        trestbps = st.text_input('Tekanan darah istirahat (mmHg)')
    
    with col1:
        chol = st.text_input('Serum kolestrol (mg/dL)',)
    
    with col2:  
        fbs = st.selectbox('Gula darah puasa >120 mg/dL?', ['Pilih', 'Tidak', 'Ya'], key='fbs')
    
    with col1:
        restecg = st.selectbox('Hasil elektrokardiografi istirahat', ['Pilih', 'Normal', 'Ada kelainan', 'Hypertrophy'], key='restecg')
    
    with col2:
        thalach = st.text_input('Denyut jantung maksimum')
    
    with col1:
        exang = st.selectbox('Nyeri dada yang dipicu oleh olahraga', ['Pilih', 'Tidak', 'Ya'], key='exang')

    with col2:  
        oldpeak = st.text_input('Oldpeak')
    
    with col1:
        slope = st.selectbox('Kemiringan puncak segmen ST', ['Pilih', 'Meningkat', 'Mendatar', 'Menurun'], key='slope')
    
    with col2:      
        ca = st.selectbox('Pembuluh besar yang diwarnai fluoroskopi', ['Pilih', 0, 1, 2, 3], key='ca')

    with col1:
        thal = st.selectbox('Hasil tes Stres Thalium', ['Pilih', 'Normal', 'Cacat tetap', 'Cacat reversibel'], key='thal')

    # Mapping the categorical features to numerical values
    sex = 1 if sex == 'Laki-laki' else 0 if sex == 'Perempuan' else None
    cp = {'Typical angina': 0, 'Atypical angina': 1, 'Non-angina': 2, 'Tanpa gejala': 3}.get(cp, None)
    fbs = 1 if fbs == 'Ya' else 0 if fbs == 'Tidak' else None
    restecg = {'Normal': 0, 'Ada kelainan': 1, 'Hypertrophy': 2}.get(restecg, None)
    exang = 1 if exang == 'Ya' else 0 if exang == 'Tidak' else None
    slope = {'Meningkat': 0, 'Mendatar': 1, 'Menurun': 2}.get(slope, None)
    thal = {'Normal': 0, 'Cacat tetap': 2, 'Cacat reversibel': 3}.get(thal, None)
    
    heart_diagnosis = ''
    
    if st.button('SCAN'):
        try:
            # Check if all inputs are provided
            if None in [sex, cp, fbs, restecg, exang, slope, thal] or '' in [age, trestbps, chol, thalach, oldpeak, ca]:
                st.error("Please fill in all fields.")
            else:
                # Convert input values to appropriate data types
                age = float(age)
                sex = float(sex)
                cp = float(cp)
                trestbps = float(trestbps)
                chol = float(chol)
                fbs = float(fbs)
                restecg = float(restecg)
                thalach = float(thalach)
                exang = float(exang)
                oldpeak = float(oldpeak)
                slope = float(slope)
                ca = float(ca)
                thal = float(thal)
                
                # Create input array for prediction
                input_data = [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]
                
                # Perform prediction
                heart_prediction = heart_model.predict(input_data)
                
                if heart_prediction[0] == 1:
                    heart_diagnosis = 'Pasien terindikasi terkena penyakit jantung.'
                else:
                    heart_diagnosis = 'Pasien tidak terindikasi penyakit jantung.'
                st.success(heart_diagnosis)
        except ValueError as e:
            st.error(f"Error: {str(e)}. Please enter valid numeric values for all input fields.")
        
    if st.button('Kembali'):
        navigate_to("Home")

elif st.session_state.navigation == "Contact":
    st.write("## CONTACT PAGE")
    st.write("Get in touch with us:")
    st.write("- Email: petikmanggafm@gmail.com")
    st.write("- Phone: 0852-1234-1117")
    st.write("- Address: Universitas Negeri Jakarta, Rawamangun, Jakarta Timur")

    st.write("## Contact Form:")
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message", height=150)
    submitted = st.button("## Submit")

    if submitted:
        if all([name, email, message]):
            st.write(f"Thank you, {name}! Your message has been submitted.")
            # Here you can add code to handle the submission, such as sending an email or saving to a database
        else:
            st.write("Please fill in all fields.")