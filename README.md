# 💼 Loan Default Prediction System – Final Year Project

A full-stack MLOps pipeline designed to predict corporate loan defaults using financial data. The system ingests structured financial inputs, applies preprocessing and feature engineering, and feeds the data into multiple ML models (Random Forest, XGBoost, Logistic Regression) using cross-validation and hyperparameter tuning.

The backend is served via Flask, containerized with Docker, and connected to a PostgreSQL database. Predictions are stored and retrieved through the API. The entire ETL and ML lifecycle is designed with MLOps principles, including model versioning and reproducibility.

---

## 🛠️ Tech Stack
- **Backend:** Flask, Docker, PostgreSQL  
- **Machine Learning:** Scikit-learn, XGBoost  
- **Data Handling:** Pandas, NumPy  
- **DevOps & MLOps:** Docker Compose, Git, GitHub  
- **Optional Frontend:** Figma mockups

---

## 📊 System Architecture & Pipeline

### ⚙️ MLOps Pipeline Diagram
![MLOps Pipeline](/Images/Screenshot%20(13).png)

### 🔄 Data Flow & Component Interaction
![Data Flow](/Images/Screenshot%20(14).png)

### 🧪 ML Model Comparison Table
![Model Comparisons](/Images/Screenshot%20(15).png)

### 📉 Cross-Validation & Metrics
![Metrics](/Images/Screenshot%20(16).png)

### 🧠 Prediction Output Sample
![Output Sample](/Images/Screenshot%20(17).png)

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/your-username/loan-default-prediction.git
cd loan-default-prediction

# Build Docker containers
docker-compose up --build

# Access the Flask backend
http://localhost:5000
