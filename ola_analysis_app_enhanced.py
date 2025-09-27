# ola_analysis_app_enhanced.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime
import streamlit.components.v1 as components

# --- Load data (adjust path if needed) ---
DATA_PATH = "C:\\Users\\anous\\OneDrive\\PROJECTS\\OLA RIDES ANALYSIS\\cleaned_ola_rides.csv"
@st.cache_data
def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    # ensure Date parsed
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    # derived columns if missing
    if 'Ride_Date' not in df.columns:
        df['Ride_Date'] = df['Date'].dt.date
    if 'Hour' not in df.columns:
        df['Hour'] = df['Date'].dt.hour
    if 'DayOfWeek' not in df.columns:
        df['DayOfWeek'] = df['Date'].dt.day_name()
    return df

df = load_data()

st.set_page_config(page_title="OLA Rides Analysis (Enhanced)", layout="wide")
st.title("OLA Rides Analysis — Interactive")

# --- Sidebar filters ---
st.sidebar.header("Filters & Search")

# Date range filter
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()
date_range = st.sidebar.date_input("Ride Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

# Vehicle type multi-select
vehicle_types = sorted(df['Vehicle_Type'].dropna().unique())
sel_vehicle = st.sidebar.multiselect("Vehicle Type", options=vehicle_types, default=vehicle_types)

# Booking status multi-select
statuses = sorted(df['Booking_Status'].dropna().unique())
sel_status = st.sidebar.multiselect("Booking Status", options=statuses, default=statuses)

# Payment method filter
payments = sorted(df['Payment_Method'].dropna().unique())
sel_payment = st.sidebar.multiselect("Payment Method", options=payments, default=payments)

# Free text search (Booking_ID or Customer_ID or Location)
search_text = st.sidebar.text_input("Search (Booking_ID, Customer_ID, Pickup/Drop)")

# KPI toggles
show_kpis = st.sidebar.checkbox("Show top KPIs", value=True)

# Apply filters to dataframe
start_date, end_date = date_range if isinstance(date_range, tuple) else (date_range, date_range)
mask = (
    (df['Date'].dt.date >= start_date) &
    (df['Date'].dt.date <= end_date) &
    (df['Vehicle_Type'].isin(sel_vehicle)) &
    (df['Booking_Status'].isin(sel_status)) &
    (df['Payment_Method'].isin(sel_payment))
)

if search_text:
    st.sidebar.markdown("**Searching for:** " + search_text)
    search_mask = (
        df['Booking_ID'].astype(str).str.contains(search_text, case=False, na=False) |
        df['Customer_ID'].astype(str).str.contains(search_text, case=False, na=False) |
        df['Pickup_Location'].astype(str).str.contains(search_text, case=False, na=False) |
        df['Drop_Location'].astype(str).str.contains(search_text, case=False, na=False)
    )
    mask = mask & search_mask

filtered = df[mask].copy()

# --- KPI cards ---
# can you include containers for each kpi?
def kpi_card(title, value, color="#1f77b4"):
    st.markdown(
        f"""
        <div style="padding:20px;border-radius:10px;
                    background-color:{color};color:white;
                    text-align:center;font-size:22px;font-weight:bold;">
            {title}<br>
            <span style="font-size:28px;">{value}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

col1, col2, col3, col4 = st.columns(4)
with col1:
    kpi_card("Total Rides", "1,03,024", "#4CAF50")
with col2:
    kpi_card("Successful Rides", "63,967", "#FF9800")
with col3:
    kpi_card("Cancelled Rides", "₹29,933", "#2196F3")
with col4:
    kpi_card("Total Booking Value", "₹56.53M", "#F44336")

if show_kpis:
    st.markdown("---")



# --- Data preview + download ---
st.subheader("Filtered data preview")
st.dataframe(filtered.head(200))

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(filtered)
st.download_button("Download filtered CSV", data=csv, file_name="filtered_ola_rides.csv", mime="text/csv")

st.markdown("---")

# --- Quick visuals (you can replace with Power BI embed if desired) ---
st.subheader("Quick Visuals (from filtered data)")

# 1. Ride Volume Over Time
if not filtered.empty:
    rides_over_time = filtered.groupby(filtered['Date'].dt.date).size().reset_index(name='count')
    fig1 = px.line(rides_over_time, x='Date', y='count', title='Ride Volume Over Time')
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Booking Status Breakdown
    status_counts = filtered['Booking_Status'].value_counts().reset_index()
    status_counts.columns = ['Booking_Status', 'count']
    fig2 = px.pie(status_counts, names='Booking_Status', values='count', title='Booking Status Breakdown')
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Top 5 Vehicle Types by Ride Distance
    if 'Ride_Distance' in filtered.columns:
        vt = filtered.groupby('Vehicle_Type')['Ride_Distance'].sum().reset_index().nlargest(5,'Ride_Distance')
        fig3 = px.bar(vt, x='Ride_Distance', y='Vehicle_Type', orientation='h', title='Top 5 Vehicle Types by Ride Distance')
        st.plotly_chart(fig3, use_container_width=True)

    # 5. what is the total number of rides for each day of the week? (descending order)
    
    if 'Date' in filtered.columns:
        filtered['DayOfWeek'] = filtered['Date'].dt.day_name()
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow_counts = filtered['DayOfWeek'].value_counts().reindex(day_order, fill_value=0)
        fig5 = px.bar(dow_counts, x=dow_counts.index, y=dow_counts.values, title='Total Rides by Day of the Week')
        st.plotly_chart(fig5, use_container_width=True)

    # 6. Total highest booking done every hour of the day
    
    if 'Hour' in filtered.columns:
        hour_counts = filtered['Hour'].value_counts().sort_index()
        fig6 = px.bar(hour_counts, x=hour_counts.index, y=hour_counts.values, title='Total Bookings by Hour of the Day')
        st.plotly_chart(fig6, use_container_width=True)

    # 7. Find the average ride distance for each vehicle type:
    
    if 'Vehicle_Type' in filtered.columns and 'Ride_Distance' in filtered.columns:
        avg_ride_distance = filtered.groupby('Vehicle_Type')['Ride_Distance'].mean().reset_index()
        fig7 = px.bar(avg_ride_distance, x='Vehicle_Type', y='Ride_Distance', title='Average Ride Distance by Vehicle Type')
        st.plotly_chart(fig7, use_container_width=True)

    # 8. Show the total count of each payment method (excluding 'Unknown')
    
    if 'Payment_Method' in filtered.columns:
        pay_counts = filtered[filtered['Payment_Method'] != 'Unknown']['Payment_Method'].value_counts().reset_index()
        pay_counts.columns = ['Payment_Method', 'count']
        fig8 = px.pie(pay_counts, names='Payment_Method', values='count', title='Payment Method Distribution (excluding Unknown)')
        st.plotly_chart(fig8, use_container_width=True)  


     # 9. List the top 5 customers who booked the highest number of rides:
    
    if 'Customer_ID' in filtered.columns:
        top_customers = filtered['Customer_ID'].value_counts().nlargest(5).reset_index()
        top_customers.columns = ['Customer_ID', 'Number_of_Rides']
        fig9  = px.bar(top_customers, x='Customer_ID', y='Number_of_Rides', title='Top 5 Customers by Number of Rides')
        st.plotly_chart(fig9, use_container_width=True)

    else:
        st.info("No cancellation records in current filter or 'Incomplete_Rides_Reason' missing.")

else:
    st.warning("No data available for the selected filters.")

st.markdown("---")



        