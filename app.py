import streamlit as st
import pandas as pd
import pickle

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

st.title("🚗 Used Vehicle Price Prediction")

# ---- User Inputs ----
buy_price = st.number_input("Original Buying Price (₹)", min_value=10000, step=5000)

year = st.slider("Car Manufacturing Year", 1990, 2024, 2015)
car_age = 2025 - year

km = st.number_input("Kilometers Driven", min_value=500, max_value=300000, step=500)

fuel = st.selectbox("Fuel Type", ["Petrol","Diesel","CNG","LPG","Electric"])
seller_type = st.selectbox("Seller Type", ["Individual","Dealer","Trustmark Dealer"])
transmission = st.selectbox("Transmission", ["Manual","Automatic"])
owner = st.selectbox("Owner Type", ["First Owner","Second Owner","Third Owner","Fourth & Above Owner"])
brand = st.selectbox("Brand", ["Maruti","Hyundai","Honda","Toyota","Mahindra","Tata","Ford","Chevrolet","Renault","Volkswagen","Audi","BMW","Mercedes"])

# Calculate car age
car_age = 2025 - year

# Prepare input DataFrame (same columns as training)
input_data = pd.DataFrame([{
    "km_driven": km,
    "car_age": car_age,
    "fuel": fuel,
    "seller_type": seller_type,
    "transmission": transmission,
    "owner": owner,
    "brand": brand
}])

# # Predict
# predicted_price = model.predict(input_data)[0]


# Predict
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
