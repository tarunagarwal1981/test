import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.feature_selection import mutual_info_regression
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import KBinsDiscretizer
from scipy.stats import ks_2samp
import ruptures as rpt
from database import get_db_engine

# Define column names as a dictionary
COLUMN_NAMES = {
    'VESSEL_NAME': 'VESSEL_NAME',
    'REPORT_DATE': 'REPORT_DATE',
    'ME_CONSUMPTION': 'ME_CONSUMPTION',
    'OBSERVERD_DISTANCE': 'OBSERVERD_DISTANCE',
    'SPEED': 'SPEED',
    'DISPLACEMENT': 'DISPLACEMENT',
    'STEAMING_TIME_HRS': 'STEAMING_TIME_HRS',
    'WINDFORCE': 'WINDFORCE',
    'VESSEL_ACTIVITY': 'VESSEL_ACTIVITY',
    'LOAD_TYPE': 'LOAD_TYPE'
}

# Streamlit app
st.title('Advanced Validation Debugging App')

# Get input for vessel name and date filter
vessel_name = st.text_input("Enter Vessel Name:")
date_filter = st.date_input("Enter Date Filter:")

def run_advanced_validation(engine, vessel_name, date_filter):
    validation_results = []
    
    # Fetch data for the vessel
    query = """
    SELECT * FROM sf_consumption_logs
    WHERE "{}" = %s AND "{}" >= %s;
    """.format(COLUMN_NAMES['VESSEL_NAME'], COLUMN_NAMES['REPORT_DATE'])
    df = pd.read_sql_query(query, engine, params=(vessel_name, date_filter))
    
    # Debugging: Check if data is fetched
    if df.empty:
        st.write(f"No data found for vessel: {vessel_name}")
        return pd.DataFrame()
    st.write(f"Data fetched for vessel: {vessel_name}, Number of rows: {len(df)}")
    
    # Split data into training (first 6 months) and validation (last 6 months)
    df[COLUMN_NAMES['REPORT_DATE']] = pd.to_datetime(df[COLUMN_NAMES['REPORT_DATE']])
    df = df.sort_values(by=COLUMN_NAMES['REPORT_DATE'])
    mid_point = len(df) // 2
    train_df = df.iloc[:mid_point]
    test_df = df.iloc[mid_point:]
    
    # Preprocess training and validation data separately to avoid data leakage
    train_df = preprocess_data(train_df)
    test_df = preprocess_data(test_df)
    
    # Debugging: Check if preprocessing was successful
    st.write(f"Training data rows after preprocessing: {len(train_df)}")
    st.write(f"Validation data rows after preprocessing: {len(test_df)}")
    
    # Anomaly Detection using Isolation Forest and LOF
    anomalies = detect_anomalies(test_df)
    if anomalies.empty:
        st.write(f"No anomalies detected for vessel: {vessel_name}")
    else:
        st.write(f"Anomalies detected for vessel: {vessel_name}, Number of anomalies: {len(anomalies)}")
    
    # Drift Detection using KS Test
    drift = detect_drift(train_df, test_df)
    
    # Change Point Detection using Ruptures
    change_points = detect_change_points(test_df)
    
    # Feature Relationships using Mutual Information
    relationships = validate_relationships(train_df)
    
    # Compile validation results
    if not anomalies.empty:
        for index, row in anomalies.iterrows():
            validation_results.append({
                'Vessel Name': str(vessel_name),
                'Anomaly Name': 'Anomaly Detected',
                'Feature': ', '.join([f"{k}: {v}" for k, v in row.to_dict().items()])
            })
    for feature, has_drift in drift.items():
        if has_drift:
            validation_results.append({
                'Vessel Name': str(vessel_name),
                'Anomaly Name': 'Drift Detected',
                'Feature': str(feature)
            })
    for feature, points in change_points.items():
        if points:
            validation_results.append({
                'Vessel Name': str(vessel_name),
                'Anomaly Name': 'Change Point Detected',
                'Feature': str(feature),
                'Value': ', '.join(map(str, points))
            })
    
    return pd.DataFrame(validation_results)

# Placeholder functions for anomaly, drift, change point detection, and preprocessing
def detect_anomalies(df):
    # Debugging: Print dataframe info
    st.write("Detecting anomalies...")
    st.write(df.head())
    return pd.DataFrame()  # Placeholder

def detect_drift(train_df, test_df):
    st.write("Detecting drift...")
    return {}  # Placeholder

def detect_change_points(df):
    st.write("Detecting change points...")
    return {}  # Placeholder

def validate_relationships(df):
    st.write("Validating feature relationships...")
    return {}  # Placeholder

def preprocess_data(df):
    st.write("Preprocessing data...")
    return df  # Placeholder

if st.button("Run Advanced Validation"):
    try:
        # Create a database engine
        engine = get_db_engine()
        
        # Run advanced validation
        st.write("### Running Advanced Validation...")
        validation_results = run_advanced_validation(engine, vessel_name, date_filter)
        
        # Display validation results
        if not validation_results.empty:
            st.write("### Advanced Validation Results:")
            st.dataframe(validation_results)
        else:
            st.write("No anomalies or drift detected.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Advanced validation function with debugging messages
def run_advanced_validation(engine, vessel_name, date_filter):
    validation_results = []
    
    # Fetch data for the vessel
    query = """
    SELECT * FROM sf_consumption_logs
    WHERE "{}" = %s AND "{}" >= %s;
    """.format(COLUMN_NAMES['VESSEL_NAME'], COLUMN_NAMES['REPORT_DATE'])
    df = pd.read_sql_query(query, engine, params=(vessel_name, date_filter))
    
    # Debugging: Check if data is fetched
    if df.empty:
        st.write(f"No data found for vessel: {vessel_name}")
        return pd.DataFrame()
    st.write(f"Data fetched for vessel: {vessel_name}, Number of rows: {len(df)}")
    
    # Split data into training (first 6 months) and validation (last 6 months)
    df[COLUMN_NAMES['REPORT_DATE']] = pd.to_datetime(df[COLUMN_NAMES['REPORT_DATE']])
    df = df.sort_values(by=COLUMN_NAMES['REPORT_DATE'])
    mid_point = len(df) // 2
    train_df = df.iloc[:mid_point]
    test_df = df.iloc[mid_point:]
    
    # Preprocess training and validation data separately to avoid data leakage
    train_df = preprocess_data(train_df)
    test_df = preprocess_data(test_df)
    
    # Debugging: Check if preprocessing was successful
    st.write(f"Training data rows after preprocessing: {len(train_df)}")
    st.write(f"Validation data rows after preprocessing: {len(test_df)}")
    
    # Anomaly Detection using Isolation Forest and LOF
    anomalies = detect_anomalies(test_df)
    if anomalies.empty:
        st.write(f"No anomalies detected for vessel: {vessel_name}")
    else:
        st.write(f"Anomalies detected for vessel: {vessel_name}, Number of anomalies: {len(anomalies)}")
    
    # Drift Detection using KS Test
    drift = detect_drift(train_df, test_df)
    
    # Change Point Detection using Ruptures
    change_points = detect_change_points(test_df)
    
    # Feature Relationships using Mutual Information
    relationships = validate_relationships(train_df)
    
    # Compile validation results
    if not anomalies.empty:
        for index, row in anomalies.iterrows():
            validation_results.append({
                'Vessel Name': str(vessel_name),
                'Anomaly Name': 'Anomaly Detected',
                'Feature': ', '.join([f"{k}: {v}" for k, v in row.to_dict().items()])
            })
    for feature, has_drift in drift.items():
        if has_drift:
            validation_results.append({
                'Vessel Name': str(vessel_name),
                'Anomaly Name': 'Drift Detected',
                'Feature': str(feature)
            })
    for feature, points in change_points.items():
        if points:
            validation_results.append({
                'Vessel Name': str(vessel_name),
                'Anomaly Name': 'Change Point Detected',
                'Feature': str(feature),
                'Value': ', '.join(map(str, points))
            })
    
    return pd.DataFrame(validation_results)

# Placeholder functions for anomaly, drift, change point detection, and preprocessing
def detect_anomalies(df):
    # Debugging: Print dataframe info
    st.write("Detecting anomalies...")
    st.write(df.head())
    return pd.DataFrame()  # Placeholder

def detect_drift(train_df, test_df):
    st.write("Detecting drift...")
    return {}  # Placeholder

def detect_change_points(df):
    st.write("Detecting change points...")
    return {}  # Placeholder

def validate_relationships(df):
    st.write("Validating feature relationships...")
    return {}  # Placeholder

def preprocess_data(df):
    st.write("Preprocessing data...")
    return df  # Placeholder
