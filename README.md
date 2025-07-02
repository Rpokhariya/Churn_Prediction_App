
# 🔄 Customer Churn Prediction App

An interactive machine learning web application that predicts whether a telecom customer is likely to churn based on key service and demographic inputs. Built using **Streamlit** and trained using **XGBoost**, the app helps visualize churn risk in real time with a clean, user-friendly interface.

---

## 🚀 Features

- 📥 Real-time form input for customer attributes
- 📊 Predicts churn probability instantly (Yes/No)
- 🧠 Model trained with XGBoost, achieving ~85% accuracy
- 📄 Clean UI using Streamlit, accessible in any browser

---

## 🔢 Input Fields

- Gender  
- Senior Citizen  
- Partner  
- Dependents  
- Tenure  
- Phone Service  
- Internet Service  
- Contract Type  
- Monthly Charges  
- Total Charges  
- Payment Method  

---

## 📁 Project Structure

```
Churn_Prediction_App/
├── app.py                  # Streamlit app interface
├── churn_model.pkl         # Trained ML model
├── churn_prediction.ipynb  # Model training & EDA notebook
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🛠 Tech Stack

- Python
- Streamlit
- XGBoost
- Pandas, NumPy
- Scikit-learn
- Pickle (model serialization)

---

## ⚙️ How to Run Locally

1. Clone the repo

```bash
git clone https://github.com/Rpokhariya/Churn_Prediction_App.git
cd Churn_Prediction_App
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app

```bash
streamlit run app.py
```

---

## 📊 Model Highlights

- Performed EDA to uncover churn trends
- Engineered features (e.g., tenure bins, service combinations)
- Applied SMOTE to balance classes
- Tuned XGBoost hyperparameters to improve accuracy from **78% to 85%**
- Visualized top predictors using feature importance

---

## 🧑‍💻 Author

Built with ❤️ by [Reena Pokhariya](https://github.com/Rpokhariya)

---

## 🪄 License

MIT License — free to use, adapt, and share with credit to the author.
