import pandas as pd
import os
import streamlit as st

def clean_data(df):
    df = df.ffill()
    return df

def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace('*', '', regex=False)
    )
    return df

def rename_columns(df):
    df = df.rename(columns={
        'date': 'Date',
        'children apprehended and placed in cbp custody': 'Children apprehended',
        'children in cbp custody': 'Children in CBP custody',
        'children transferred out of cbp custody': 'Children transferred to HHS',
        'children in hhs care': 'Children in HHS care',
        'children discharged from hhs care': 'Children discharged'
    })
    return df

# MAINE YAHAN (file_path=None) ADD KIYA HAI
def load_data(file_path=None):
    # Agar koi file upload nahi hui hai (file_path blank hai), toh default wali uthao
    if file_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..', 'data', 'data.csv')
        
        if not os.path.exists(file_path):
            st.error(f"🚨 Data file is missing! Looking at: {file_path}")
            return pd.DataFrame()
            
    # Pandas read_csv bahut smart hai, ye text path aur drag-drop wali file dono read kar leta hai
    df = pd.read_csv(file_path)
    
    df = clean_columns(df)
    df = rename_columns(df)

    if 'Date' not in df.columns:
        raise KeyError(f"Missing required date column. Available: {list(df.columns)}")
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    numeric_cols = [
        'Children in CBP custody',
        'Children transferred to HHS',
        'Children in HHS care',
        'Children discharged'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '', regex=False), errors='coerce')

    df = df.dropna(subset=['Date'])
    df = df.sort_values('Date')

    return df