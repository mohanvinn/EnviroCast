# 🌍 EnviroCast – AI-Based Air Quality Prediction and Health Risk Alert System

## 📌 Project Overview

**EnviroCast** is an AI-powered Air Quality Monitoring, Prediction, and Health Risk Alert System developed using Python and Machine Learning. The application helps users monitor air quality, analyze pollution levels, visualize environmental data, and predict future AQI values.

The system provides insights into major air pollutants and generates health recommendations based on Air Quality Index (AQI) levels. It combines real-time air quality information, historical datasets, interactive visualizations, and machine learning algorithms to support better environmental awareness and decision-making.

## 🎯 Objectives

- Monitor Air Quality Index (AQI) across different locations.
- Analyze major air pollutants such as PM2.5, PM10, CO, NO₂, and SO₂.
- Predict future AQI values using Machine Learning.
- Visualize air pollution levels through interactive charts and maps.
- Generate health alerts based on AQI levels.
- Identify pollution trends and patterns using historical data.

## ✨ Key Features

### 1. Real-Time Air Quality Monitoring
- Retrieve air quality information using APIs.
- Display AQI and pollutant concentrations.
- Monitor pollution levels across different locations.

### 2. Interactive Dashboard
- Built using Streamlit.
- Display pollution statistics and graphical representations.
- Analyze historical air quality trends.

### 3. Machine Learning-Based AQI Prediction
- Linear Regression
- Random Forest Regression
- Predict future AQI values using historical pollution data.
- Evaluate model performance using MAE and R² score.

### 4. Interactive Map Visualization
- Display air quality information across different locations.
- Use Folium for geographical visualization.
- Identify areas with higher pollution levels.

### 5. Health Risk Alert System
- Generate alerts based on AQI levels.
- Provide health recommendations for different pollution categories.
- Help users understand potential pollution-related health risks.

### 6. Data Visualization
- Analyze pollutant concentrations.
- Display AQI trends using charts and graphs.
- Compare air quality across different locations.

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend / Dashboard | Streamlit |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Plotly |
| Map Visualization | Folium, Streamlit-Folium |
| API Integration | OpenWeather API |
| Dataset | CSV |
| Development Tool | VS Code |

## 📊 Machine Learning Algorithms

**Linear Regression:** Used to identify relationships between pollutant values and AQI and generate predictions.

**Random Forest Regression:** Uses multiple decision trees to improve prediction performance and capture complex relationships in air quality data.

## 📁 Project Structure

```text
EnviroCast/
│
├── main/
│   ├── app.py
│   ├── requirements.txt
│   ├── global_air_quality_data_10000.csv
│   └── model.py
│
└── README.md
```

*Note: Update this structure according to your actual GitHub files.*

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/mohanvinn/EnviroCast.git
```

### Step 2: Navigate to the Project Folder

```bash
cd EnviroCast/main
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Key

Configure your OpenWeather API key if your application uses live API integration.

Keep API keys secure and avoid uploading them directly to GitHub.

### Step 5: Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## 📈 Expected Outcomes

- Real-time air quality monitoring.
- Interactive visualization of pollution levels.
- Machine learning-based AQI prediction.
- Identification of high-pollution locations.
- Health risk alerts and recommendations.
- Improved environmental awareness.

## 🚀 Deployment

The application can be deployed using **Streamlit Community Cloud**.

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub repository.
4. Select `main/app.py` as the application entry point.
5. Configure required secrets and API keys.
6. Deploy the application.

## 🔮 Future Enhancements

- Integration with IoT-based air quality sensors.
- Advanced time-series forecasting using ARIMA and other models.
- Mobile application integration.
- More accurate location-based pollution forecasting.
- Automated notifications for unhealthy air quality.
- Integration with additional environmental data sources.

## 👨‍💻 Author

**Mohan Sanangula**

Project: EnviroCast – AI-Based Air Quality Prediction and Health Risk Alert System

GitHub: https://github.com/mohanvinn

---

⭐ If you find this project interesting, consider giving it a star on GitHub.

**Built with Python, Machine Learning, and Streamlit.**
