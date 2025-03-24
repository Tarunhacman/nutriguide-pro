import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Set page config first, before any other Streamlit commands
st.set_page_config(
    page_title="NutriGuide Pro",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Get API key from environment variable or Streamlit secrets
if os.getenv("GOOGLE_API_KEY"):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
elif hasattr(st.secrets, "GOOGLE_API_KEY"):
    GOOGLE_API_KEY = st.secrets.GOOGLE_API_KEY
else:
    st.error("Google API key not found. Please set the GOOGLE_API_KEY in your environment variables or Streamlit secrets.")
    st.stop()

try:
    # Configure the Gemini model with safety settings
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Set up the model with appropriate configuration
    generation_config = {
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
    
    # Use the recommended model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",  # Updated to use the recommended model
        generation_config=generation_config,
        safety_settings=safety_settings
    )
except Exception as e:
    st.error(f"Error configuring Gemini model: {str(e)}")
    st.stop()

# Custom CSS for modern UI
st.markdown("""
    <style>
    /* Modern Color Scheme */
    :root {
        --primary-color: #2E7D32;
        --secondary-color: #81C784;
        --accent-color: #4CAF50;
        --background-color: #F5F5F5;
        --text-color: #333333;
        --card-background: #FFFFFF;
    }
    
    /* Main Container */
    .main {
        background-color: var(--background-color);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: var(--card-background);
        padding: 2rem;
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        margin-top: 20px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        background-color: var(--accent-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        padding: 10px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(46, 125, 50, 0.1);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--card-background);
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        margin-right: 4px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color) !important;
        color: white !important;
        font-weight: 600;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: var(--text-color);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Cards */
    .stMarkdown {
        background-color: var(--card-background);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Welcome Message */
    .welcome-card {
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        color: white;
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    /* Copyright */
    .copyright {
        text-align: center;
        color: #666;
        font-size: 0.8em;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #E0E0E0;
    }
    </style>
""", unsafe_allow_html=True)

def get_llm():
    """Get the LLM instance with Streamlit callback handler."""
    chat = model.start_chat(history=[])
    return chat

def create_nutrition_plan(user_info):
    """Create a personalized nutrition plan based on user information."""
    try:
        prompt = f"""Based on the following user information, create a personalized nutrition plan:
        {user_info}
        
        Please provide:
        1. Daily calorie target
        2. Macronutrient breakdown
        3. Meal timing suggestions
        4. Food recommendations
        5. Hydration guidelines
        6. Any specific dietary considerations
        """
        
        with st.spinner('Creating your personalized nutrition plan...'):
            response = model.generate_content(prompt)
            return response.text
    except Exception as e:
        st.error(f"Error generating nutrition plan: {str(e)}")
        return None

def app():
    """Main Streamlit application."""
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/healthy-food.png", width=100)
        st.title("NutriGuide Pro")
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            Your AI-powered nutrition companion for personalized dietary guidance.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style='color: #666;'>
            <h4>About</h4>
            <p>Get personalized nutrition recommendations based on your unique profile, health conditions, and lifestyle preferences.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div class='copyright'>
            <p>© 2025 Tarun Kumar</p>
            <p>All rights reserved</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    st.title("Personalized Nutrition Plan")
    st.markdown("""
    <div class='welcome-card'>
        <h3 style='color: white;'>Welcome to Your Nutrition Journey!</h3>
        <p style='color: white;'>Fill out the information below to receive your personalized nutrition plan. Our AI will analyze your profile and create recommendations tailored to your needs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for organization
    tab1, tab2, tab3 = st.tabs(["Personal Profile", "Health Details", "Lifestyle Preferences"])
    
    with tab1:
        st.header("Personal Information")
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
            gender = st.selectbox("Gender", ["Male", "Female", "Non-binary/Other"])
            height = st.text_input("Height (e.g., 5'10\" or 178 cm)", "5'10\"")
            
        with col2:
            weight = st.text_input("Weight (e.g., 160 lbs or 73 kg)", "160 lbs")
            activity_level = st.select_slider(
                "Activity Level",
                options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"]
            )
            goals = st.multiselect(
                "Nutrition Goals",
                ["Weight Loss", "Weight Gain", "Maintenance", "Muscle Building", "Better Energy", 
                 "Improved Athletic Performance", "Disease Management", "General Health"]
            )
    
    with tab2:
        st.header("Health Information")
        col1, col2 = st.columns(2)
        with col1:
            medical_conditions = st.text_area(
                "Medical Conditions",
                placeholder="E.g., Diabetes Type 2, Hypertension, Hypothyroidism...",
                help="List any medical conditions that may affect your dietary needs"
            )
        
        medications = st.text_area(
                "Current Medications",
                placeholder="E.g., Metformin, Lisinopril, Levothyroxine...",
                help="List any medications you're currently taking"
        )
        with col2:
            allergies = st.text_area(
                "Food Allergies/Intolerances",
                placeholder="E.g., Lactose, Gluten, Shellfish, Peanuts...",
                help="List any food allergies or intolerances"
            )
    
    with tab3:
        st.header("Lifestyle Preferences")
        col1, col2 = st.columns(2)
        
        with col1:
            food_preferences = st.text_area(
                "Food Preferences & Dislikes",
                placeholder="E.g., Prefer plant-based, dislike seafood...",
                help="Share your food preferences and any foods you don't enjoy"
            )
            
            cooking_ability = st.select_slider(
                "Cooking Skills & Available Time",
                options=["Very Limited", "Basic/Quick Meals", "Average", "Advanced/Can Spend Time", "Professional Level"]
            )
        
        with col2:
            budget = st.select_slider(
                "Budget Considerations",
                options=["Very Limited", "Budget Conscious", "Moderate", "Flexible", "No Constraints"]
            )
            
            cultural_factors = st.text_area(
                "Cultural or Religious Dietary Factors",
                placeholder="E.g., Halal, Kosher, Mediterranean tradition...",
                help="Any cultural or religious dietary restrictions or preferences"
            )
    
    # Collect all user information
    user_info = {
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "activity_level": activity_level,
        "goals": ", ".join(goals) if goals else "General health improvement",
        "medical_conditions": medical_conditions or "None reported",
        "medications": medications or "None reported",
        "allergies": allergies or "None reported",
        "food_preferences": food_preferences or "No specific preferences",
        "cooking_ability": cooking_ability,
        "budget": budget,
        "cultural_factors": cultural_factors or "No specific factors"
    }
    
    # Check if API key is present
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("⚠️ API key not detected. Please add your GOOGLE_API_KEY to your .env file.")
    
    # Create a submission button
    if st.button("Generate Nutrition Plan", key="generate_plan"):
        if not goals:
            st.error("Please select at least one nutrition goal.")
            return
        
        # Display user information summary
        with st.expander("Summary of Your Information"):
            st.json(user_info)
        
        # Run the nutrition advisor
        result = create_nutrition_plan(user_info)
        
        if result:
            st.success("✅ Your personalized nutrition plan is ready!")
            st.markdown("## Your Personalized Nutrition Plan")
            st.markdown(result)
            
            # Add download capability
            st.download_button(
                label="Download Nutrition Plan",
                data=result,
                file_name="my_nutrition_plan.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    app()