# importing necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

# Set streamlit layout to wide
st.set_page_config(layout="wide")

# Load the trained model
with open('best_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Load the MinMaxScaler
with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

# Define input features
feature_names = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary', 
                  'HasCrCard_0.0', 'HasCrCard_1.0', 'IsActiveMember_0.0', 'IsActiveMember_1.0', 
                  'Geography_France', 'Geography_Germany', 'Geography_Spain', 
                  'Gender_Female', 'Gender_Male']
scale_vars = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary']
default_values = [600, 30, 2, 8000, 2, 60000, True, False, False, True, False, False, True, False, True]

# App Header
st.markdown("""
<div style='text-align:center;'>
    <h1 style='color:white;'>💲 Customer Churn Prediction 💲</h1>
</div>
""", unsafe_allow_html=True)

# Input section
st.subheader("Enter Customer Details:")

# Number input layout in two lines
num_features = feature_names[:6]
bool_features = feature_names[6:]

num_cols1 = st.columns(3)
num_cols2 = st.columns(3)

user_inputs = {}
for i, feature in enumerate(num_features[:3]):
    with num_cols1[i]:
        user_inputs[feature] = st.number_input(feature, value=default_values[i], step=1)

for i, feature in enumerate(num_features[3:]):
    with num_cols2[i]:
        user_inputs[feature] = st.number_input(feature, value=default_values[i+3], step=1)

# Checkbox layout in two lines
bool_cols1 = st.columns(5)
bool_cols2 = st.columns(5)

for i, feature in enumerate(bool_features[:5]):
    with bool_cols1[i]:
        user_inputs[feature] = st.checkbox(feature, value=default_values[i+6])

for i, feature in enumerate(bool_features[5:]):
    with bool_cols2[i]:
        user_inputs[feature] = st.checkbox(feature, value=default_values[i+11])

# Prepare data
input_data = pd.DataFrame([user_inputs])
input_data_scaled = input_data.copy()
input_data_scaled[scale_vars] = scaler.transform(input_data[scale_vars])

# Centered Predict button with forward arrow
st.markdown("""
    <style>
        .stButton>button {
            color: white !important;
            font-size: 20px !important;
            padding: 10px 30px !important;
            border: solid white 2px !important;
            border-radius: 10px !important;
            cursor: pointer !important;
        }
        .stButton {
            display: flex;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# Predict button logic with session state to keep the result visible
if st.button("Predict →"):
    probabilities = model.predict_proba(input_data_scaled)[0]
    prediction = model.predict(input_data_scaled)[0]
    prediction_label = "Churned" if prediction == 1 else "Retain"

    # Save in session state
    st.session_state['prediction_label'] = prediction_label
    st.session_state['probabilities'] = probabilities

# Display prediction result if it exists
if 'prediction_label' in st.session_state and 'probabilities' in st.session_state:
    prediction_label = st.session_state['prediction_label']
    probabilities = st.session_state['probabilities']

    # Choose pastel background color based on prediction
    bg_color = "#8e2424" if prediction_label == "Churned" else "#2e7d32"

    st.markdown(f"""
        <div style='background-color:{bg_color}; padding:15px; border-radius:10px; text-align:center; margin-top:20px;'>
            <h3>Prediction: <strong>{prediction_label}</strong></h3>
            <p><strong>Churn Probability:</strong> {probabilities[1]:.2%}</p>
            <p><strong>Retention Probability:</strong> {probabilities[0]:.2%}</p>
        </div>
    """, unsafe_allow_html=True)


    # Horizontal line below prediction area
st.markdown("---")

# Sidebar and insights after prediction section
st.sidebar.image("./Pic 1.png", width=200)
st.sidebar.header("Data Insights Menu")
show_feature_importance = st.sidebar.checkbox("Feature Importance", value=True)
show_geo_churn = st.sidebar.checkbox("Geography-wise Churn Rate", value=True)
show_age_churn = st.sidebar.checkbox("Age-wise Churn Rate", value=True)
show_balance_churn = st.sidebar.checkbox("Balance vs Churn", value=True)
show_tenure_churn = st.sidebar.checkbox("Tenure Impact on Churn", value=True)
show_credit_churn = st.sidebar.checkbox("Credit Score vs Churn", value=True)

# Loading real data insights
insights_file = pd.ExcelFile("churn_insights.xlsx")
geo_churn_df = pd.read_excel(insights_file, sheet_name="Geo Churn")
age_churn_df = pd.read_excel(insights_file, sheet_name="Age Churn")
balance_df = pd.read_excel(insights_file, sheet_name="Balance vs Churn")
tenure_df = pd.read_excel(insights_file, sheet_name="Tenure Churn")
credit_df = pd.read_excel(insights_file, sheet_name="Credit vs Churn")



# Main insights
feature_importance_df = pd.read_excel("./feature_importance.xlsx", usecols=["Feature", "Feature Importance Score"])
st.subheader("Data Insights")
st.write("\n\n")
if show_feature_importance:
    st.write("#### Feature Importance")
    fig = px.bar(
        feature_importance_df.sort_values(by="Feature Importance Score", ascending=True),
        x="Feature Importance Score",
        y="Feature",
        orientation="h",
        # title="Feature Importance",
        labels={"Feature Importance Score": "Importance", "Feature": "Features"},
        width=900,
        height=500,
        color="Feature Importance Score",
        color_continuous_scale="blues"
    )
    st.plotly_chart(fig, use_container_width=True, key="feature_importance_chart")

if show_geo_churn:
    st.write("#### Geography-wise Churn Rate")
    fig_geo = px.bar(
        geo_churn_df,
        x="Geography",
        y="Churn Rate",
        color="Churn Rate",
        # title="Churn Rate by Geography",
        width=900,
        height=500
    )
    fig_geo.update_layout(bargap=0.5)
    st.plotly_chart(fig_geo, use_container_width=True, key="geo_churn_chart")

if show_age_churn:
    st.write("#### Age-wise Churn Rate")
    fig_age = px.bar(
        age_churn_df,
        x="Age Group",
        y="Churn Rate",
        color="Churn Rate",
        # title="Churn Rate by Age Group",
        width=900,
        height=500
    )
    fig_age.update_layout(bargap=0.5)
    st.plotly_chart(fig_age, use_container_width=True, key="age_churn_chart")

if show_balance_churn:
    st.write("#### Balance vs. Churn")
    fig_balance = px.bar(
        balance_df,
        x="Churn Status",
        y="Balance",
        color="Balance",
        # title="Average Balance vs. Churn Status",
        width=900,
        height=500
    )
    fig_balance.update_layout(bargap=0.5)
    st.plotly_chart(fig_balance, use_container_width=True, key="balance_chart")

if show_tenure_churn:
    st.write("#### Tenure Impact on Churn")
    fig_tenure = px.line(
        tenure_df,
        x="Tenure",
        y="Churn Rate",
        # title="Churn Rate vs. Tenure",
        markers=True,
        width=900,
        height=500
    )
    st.plotly_chart(fig_tenure, use_container_width=True, key="tenure_chart")

if show_credit_churn:
    st.write("#### Credit Score vs. Churn")
    fig_credit = px.bar(
        credit_df,
        x="Churn Status",
        y="CreditScore",
        color="CreditScore",
        # title="Credit Score vs. Churn Status",
        width=900,
        height=500
    )
    fig_credit.update_layout(bargap=0.5)
    st.plotly_chart(fig_credit, use_container_width=True, key="credit_score_chart")


st.write("\n")
st.markdown("---")
st.caption("Developed by Reena. Powered by Streamlit.")
