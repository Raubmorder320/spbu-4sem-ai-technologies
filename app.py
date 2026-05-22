import streamlit as st
import pandas as pd
import pickle
from catboost import CatBoostClassifier

# загрузка модели
@st.cache_resource
def load_artifacts():
    model = CatBoostClassifier()
    model.load_model('catboost_best_model.cbm')
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

model, scaler = load_artifacts()


st.set_page_config(page_title="Аналитика оттока", page_icon="🏦")
st.title("🏦 Модуль прогнозирования оттока клиентов")

col1, col2 = st.columns(2)

with col1:
    geography = st.selectbox("Филиал обслуживания", ["Франция", "Испания", "Германия"])
    gender = st.selectbox("Пол клиента", ["Мужской", "Женский"])
    age = st.slider("Возраст клиента", 18, 100, 35)
    credit_score = st.slider("Кредитный рейтинг", 300, 850, 600)
    tenure = st.slider("Сколько лет с банком", 0, 10, 5)

with col2:
    # ввод в рублях
    balance = st.number_input("Баланс на счету, $", min_value=0, value=15000, step=1000)
    salary = st.number_input("Оценочный годовой доход, $", min_value=0, value=12000, step=1000)
    
    num_products = st.selectbox("Количество активных продуктов", [1, 2, 3, 4])
    has_cr_card = st.checkbox("Наличие кредитной карты", value=True)
    is_active = st.checkbox("Активный клиент (транзакции за месяц)", value=True)

if st.button("📊 Сгенерировать прогноз", use_container_width=True):

    geo_dict = {"Франция": "France", "Испания": "Spain", "Германия": "Germany"}
    gender_dict = {"Мужской": "Male", "Женский": "Female"}
    
    geography_eng = geo_dict[geography]
    gender_eng = gender_dict[gender]


    geo_germany = 1 if geography_eng == 'Germany' else 0
    geo_spain = 1 if geography_eng == 'Spain' else 0
    gender_male = 1 if gender_eng == 'Male' else 0
    
    input_df = pd.DataFrame({
        'CreditScore': [credit_score],
        'Age': [age],
        'Tenure': [tenure],
        'Balance': [balance], 
        'NumOfProducts': [num_products],
        'HasCrCard': [1 if has_cr_card else 0],
        'IsActiveMember': [1 if is_active else 0],
        'EstimatedSalary': [salary], 
        'Geography_Germany': [geo_germany],
        'Geography_Spain': [geo_spain],
        'Gender_Male': [gender_male]
    })
    
    numeric_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary']
    input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])
    
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]
    
    st.markdown("---")
    if prediction == 1:
        st.error(f"🔴 **ВНИМАНИЕ: Высокий риск оттока.** \n\nВероятность: **{probability:.1%}**. Рекомендуется предложить клиенту льготные условия по кредитной карте или депозит с повышенной ставкой.")
    else:
        st.success(f"🟢 **Стабильный клиент.** \n\nВероятность оттока: **{probability:.1%}**. Показатели в норме.")