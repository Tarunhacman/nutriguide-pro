# NutriGuide Pro

A personalized nutrition and health guidance system powered by Google's Gemini Pro AI model.

## Features

- Personalized nutrition planning based on user profile
- Health goal setting and tracking
- Dietary preferences and restrictions handling
- Medical condition consideration
- Lifestyle factor integration

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Tarunhacman/nutriguide-pro.git
   cd nutriguide-pro
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your Google AI API key to `.env`

## Running the Application

1. Make sure your virtual environment is activated

2. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```

3. Open your browser and go to `http://localhost:8504`

## Usage

1. Fill in your personal details in the sidebar
2. Provide health information and preferences
3. Click "Generate Nutrition Plan" to get your personalized plan
4. Download or view your nutrition guidance

## Note

Make sure you have a valid Google AI API key. You can get one from the Google AI Studio platform. 