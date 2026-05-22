import streamlit as st
import pandas as pd
import random
# import pickle # Раскомментируй завтра, когда будет реальная модель

# Настройка страницы
st.set_page_config(page_title="Bank Churn Predictor", page_icon="🏦", layout="centered")

st.title("🏦 Предсказание оттока клиентов банка")
st.write("Введите данные клиента, чтобы узнать, какова вероятность его ухода.")

# Создаем две колонки для красоты
col1, col2 = st.columns(2)

with col1:
    geography = st.selectbox("Страна", ["France", "Spain", "Germany"])
    gender = st.selectbox("Пол", ["Male", "Female"])
    age = st.slider("Возраст", 18, 100, 35)
    credit_score = st.slider("Кредитный рейтинг", 300, 850, 600)
    tenure = st.slider("Лет с банком", 0, 10, 5)

with col2:
    balance = st.number_input("Баланс на счету, $", min_value=0.0, value=50000.0, step=1000.0)
    salary = st.number_input("Примерная зарплата, $", min_value=0.0, value=60000.0, step=1000.0)
    num_products = st.selectbox("Количество продуктов банка", [1, 2, 3, 4])
    has_cr_card = st.checkbox("Есть кредитная карта?", value=True)
    is_active = st.checkbox("Активный клиент?", value=True)

# Кнопка для предсказания
if st.button("🔮 Предсказать отток", use_container_width=True):
    
    # 1. Собираем данные с экрана в табличку (DataFrame)
    # Важно: названия колонок должны ТОЧНО совпадать с теми, на которых друг обучал модель
    input_data = pd.DataFrame({
        "CreditScore": [credit_score],
        "Geography": [geography],
        "Gender": [gender],
        "Age": [age],
        "Tenure": [tenure],
        "Balance": [balance],
        "NumOfProducts": [num_products],
        "HasCrCard": [1 if has_cr_card else 0],
        "IsActiveMember": [1 if is_active else 0],
        "EstimatedSalary": [salary]
    })
    
    st.write("Данные отправлены в модель:")
    st.dataframe(input_data)

    # 2. ЗАГЛУШКА ДЛЯ ТЕСТИРОВАНИЯ (пока нет реальной модели)
    # Завтра удали эти 3 строчки:
    churn_probability = random.uniform(0, 1)
    prediction = 1 if churn_probability > 0.5 else 0
    
    # 3. РЕАЛЬНЫЙ КОД (Раскомментируй завтра)
    # with open('model.pkl', 'rb') as file:
    #     model = pickle.load(file)
    # prediction = model.predict(input_data)[0]
    # churn_probability = model.predict_proba(input_data)[0][1]

    # 4. Вывод результата
    st.markdown("---")
    if prediction == 1:
        st.error(f"⚠️ ОПАСНОСТЬ! Клиент скорее всего **УЙДЕТ**. Вероятность оттока: {churn_probability:.1%}")
    else:
        st.success(f"✅ ВСЕ ХОРОШО! Клиент **ОСТАНЕТСЯ**. Вероятность оттока: {churn_probability:.1%}")