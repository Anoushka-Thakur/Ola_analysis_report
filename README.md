OLA Rides Analysis – Interactive Dashboard

An interactive data analytics and visualization project built using Python, Pandas, Streamlit, and Plotly to analyze OLA ride data.
The dashboard allows users to explore ride trends, booking behavior, vehicle usage, and payment patterns through dynamic filters and visualizations.

 Project Overview

This project analyzes cleaned OLA ride data to uncover actionable insights such as:

Ride volume trends over time

Booking status distribution

Peak booking hours and days

Vehicle-wise ride distance analysis

Customer behavior and payment preferences

The application is deployed using Streamlit, enabling real-time filtering and interactive exploration.

 Tech Stack

Python

Pandas & NumPy – Data processing and analysis

Streamlit – Interactive web app

Plotly Express – Data visualization

CSV Dataset – Cleaned OLA ride data

📂 Project Structure
├── ola_analysis_app_enhanced.py   # Main Streamlit application
├── cleaned_ola_rides.csv          # Cleaned dataset
├── README.md   # Project documentation


 Key Features
 Interactive Filters

Date range selection

Vehicle type

Booking status

Payment method

Free-text search (Booking ID, Customer ID, Pickup/Drop location)

 KPIs Displayed

Total Rides

Successful Rides

Cancelled Rides

Total Booking Value

 Visual Insights

Ride volume over time

Booking status breakdown

Top vehicle types by ride distance

Rides by day of the week

Hourly booking trends

Average ride distance per vehicle type

Payment method distribution

Top 5 customers by number of rides

 Data Export

Download filtered data as CSV


🚀 How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/USERNAME/REPO_NAME.git
cd REPO_NAME

2️⃣ Install Dependencies
pip install streamlit pandas numpy plotly

3️⃣ Run the Streamlit App
streamlit run ola_analysis_app_enhanced.py

 Dataset Notes

The dataset is assumed to be cleaned before analysis.

Date columns are parsed and additional features like Hour, DayOfWeek, and Ride_Date are derived automatically.

 Use Cases

Business performance analysis

Operations & demand forecasting

Customer behavior analysis

Portfolio project for Data Analyst / Data Science roles

 Future Enhancements

Power BI or Tableau dashboard integration

Predictive demand modeling

City-wise or zone-wise analysis

Deployment on Streamlit Cloud

 Author
Anoushka Thakur
Aspiring Data Analyst | Python | SQL | Streamlit | Data Visualization
