# KrishAI - The ML Module

This repository contains the **machine learning components** developed for our college project - [KrishAI project](https://github.com/SD1920/KrishAI).

My contribution focused on:
- integrating external datasets,
- preparing ML-ready data through ETL scripts,
- and exploratory model development.

The backend and frontend were developed separately by other team members.

---

## Data Sources

- Data is sourced from **public Indian government portals**
- Raw datasets are **not included**
- Source links and descriptions are documented in `data/raw/README.md`
---

## Models Used

### 1. Crop Recommendation

- **Random Forest Classifier**
  - Used for multi-class crop recommendation
  - Input features included soil nutrients (N, P, K), temperature, humidity, pH, rainfall, and soil type
  - Categorical soil types encoded using one-hot encoding
  - Target crop labels encoded using `LabelEncoder`
  - Model evaluated using accuracy (0.99) and per-class precision/recall.

- **Gaussian Naive Bayes (baseline)**
  - Used as a lightweight baseline for comparison against ensemble methods

---

### 2. Yield Prediction

- Extra Trees Regressor**
  - Best-performing model selected via cross-validated R² (0.89)
  - Hyperparameters tuned using `GridSearchCV` (estimators, depth, split criteria)

---

### Model Persistence

- Trained regression models serialized using `joblib` for reuse in downstream inference workflows

---

### Supporting Logic (Non-ML)

- Rule-based recommendation logic for fertilizer and pesticide selection
- String normalization and matching used to align crop, district, and product records
- Feature ratios (N:P:K) derived during preprocessing to support model inputs
  
