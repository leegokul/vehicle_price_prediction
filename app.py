import streamlit as st
import pandas as pd
import pickle
import gdown
from pathlib import Path

# --------------------
# Download model from Google Drive if not found
# --------------------
MODEL_PATH = Path(__file__).parent / "model.pkl"
FILE_ID = "1M-9OtJqJ1diWylXldvzC7C5QTU01d8NC"  # your file ID

if not MODEL_PATH.exists():
    st.info("Downloading model... Please wait ⏳")
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, str(MODEL_PATH), quiet=False)

# Load model
model = pickle.load(open(MODEL_PATH, "rb"))

# --------------------
# Streamlit UI
# --------------------
st.title("🚗 Used Vehicle Price Prediction")

buy_price = st.number_input("Original Buying Price (₹)", min_value=10000, step=5000)

year = st.slider("Car Manufacturing Year", 1990, 2024, 2015)
km = st.number_input("Kilometers Driven", min_value=500, max_value=300000, step=500)

fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
seller_type = st.selectbox("Seller Type", ["Individual","Dealer","Trustmark Dealer"])
transmission = st.selectbox("Transmission", ["Manual","Automatic"])
owner = st.selectbox("Owner Type", ["First Owner","Second Owner","Third Owner","Fourth & Above Owner"])
brand = st.selectbox("Brand", ["Maruti","Hyundai","Honda","Toyota","Mahindra","Tata","Ford","Chevrolet","Renault","Volkswagen","Audi","BMW","Mercedes"])

# Calculate age
car_age = 2025 - year

# Input Data
input_data = pd.DataFrame([{
    "km_driven": km,
    "car_age": car_age,
    "fuel": fuel,
    "seller_type": seller_type,
    "transmission": transmission,
    "owner": owner,
    "brand": brand
}])

# --------------------
# Prediction Button
# --------------------
if st.button("Predict Price"):
    predicted_price = int(model.predict(input_data)[0])

    st.subheader("📊 Price Evaluation Result")
    st.write(f"🟦 **Original Buying Price:** ₹{int(buy_price)}")
    st.write(f"🟩 **Estimated Selling Price:** ₹{predicted_price}")

    diff = predicted_price - buy_price

    if diff >= 0:
        st.success(f"✅ Profit: ₹{diff}")
    else:
        st.error(f"❌ Loss: ₹{abs(diff)}")
