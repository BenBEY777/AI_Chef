
# import streamlit as st
# import google.generativeai as genai
# from PIL import Image

# # 1. Настройка на страницата
# st.set_page_config(page_title="Zero-Waste Chef", page_icon="♻️")

# # 2. Инициализация на API
# try:
#     # Пробвай да вземеш ключа от secrets
#     API_KEY = st.secrets["GEMINI_API_KEY"]
#     genai.configure(api_key=API_KEY)
# except Exception:
#     st.error("❌ Липсва API ключ! Провери .streamlit/secrets.toml")
#     st.stop()

# st.title("♻️ Zero-Waste AI Готвач")
# st.write("Превърни остатъците в професионално ястие.")

# # 3. Входни данни
# col1, col2 = st.columns(2)
# with col1:
#     ingredients_input = st.text_area(
#         "Остатъци и продукти:", 
#         placeholder="напр. кости от пиле, увехнал магданоз, кори от сирене...",
#         height=150
#     )
# with col2:
#     uploaded_file = st.file_uploader("Снимка на продуктите:", type=["jpg", "jpeg", "png"])

# if uploaded_file:
#     image = Image.open(uploaded_file)
#     st.image(image, use_container_width=True)

# # 4. Основна логика
# if st.button("🚀 Генерирай решение", use_container_width=True):
#     if not ingredients_input and not uploaded_file:
#         st.warning("⚠️ Опиши продуктите или прикачи снимка.")
#     else:
#         with st.spinner("🧑‍🍳 Анализирам и подготвям рецепта..."):
#             try:
#                 # ВАЖНО: Използваме директно името без префикс, за да избегнем 404
#                 # Ако 'gemini-1.5-flash' не работи, Gemini 1.5 Pro е алтернатива
#                 model = genai.GenerativeModel('gemini-2.5-flash')
                
#                 # Твоят специфичен Zero-Waste промпт
#                 prompt = f"""
#                 Анализ: Ще ти дам списък с продукти (включително увехнали зеленчуци, остатъци от предно ядене или кости/кори): 
#                 {ingredients_input if ingredients_input else "продуктите от приложената снимка"}.

#                 Рецепта: Предложи конкретно ястие с точно име.
                
#                 Структура:
#                 Необходими продукти: Кратък списък.
#                 Подготовка: Максимално изчистени стъпки (1, 2, 3...).
#                 Zero-Waste съвет: Как да използвам остатъка (напр. обелки за бульон, кости за сос, листа за песто).
#                 Тон: Директен, професионален и практически. Без излишни въведения и описателни епитети.
#                 Език: Български.
#                 """

#                 # Изпращане към AI
#                 content = [prompt]
#                 if uploaded_file:
#                     content.append(image)
                
#                 response = model.generate_content(content)

#                 st.markdown("---")
#                 st.markdown(response.text)
                
#             except Exception as e:
#                 # Ако все още има 404, изписваме наличните модели за диагностика
#                 st.error(f"Грешка при връзката с модела.")
#                 with st.expander("Технически детайли на грешката"):
#                     st.write(str(e))
#                     try:
#                         models = [m.name for m in genai.list_models()]
#                         st.write("Налични модели за вашия ключ:", models)
#                     except:
#                         st.write("Неуспешно извличане на списък с модели.")

# st.markdown("---")


# python -m streamlit run app.py
#-------------------------------------------------

import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Настройка на страницата
st.set_page_config(page_title="Zero-Waste Chef", page_icon="♻️", layout="centered")

# Функция за зареждане на CSS
def local_css(file_name):
    try:
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("style.css")

# 2. Инициализация на API
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("❌ Липсва API ключ! Провери .streamlit/secrets.toml")
    st.stop()

# Инициализиране на състоянието
if 'recipes_list' not in st.session_state:
    st.session_state.recipes_list = []
if 'selected_index' not in st.session_state:
    st.session_state.selected_index = None

st.title("♻️ Zero-Waste AI Готвач")
st.write("Превърни остатъците в професионално ястие.")

# 3. Входни данни
col1, col2 = st.columns(2)
with col1:
    ingredients_input = st.text_area(
        "Остатъци и продукти:", 
        placeholder="напр. пиле, увехнал магданоз...",
        height=150
    )
with col2:
    uploaded_file = st.file_uploader("Снимка на продуктите:", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

# 4. Основна логика за генериране
if st.button("🚀 Генерирай 3 идеи", use_container_width=True):
    if not ingredients_input and not uploaded_file:
        st.warning("⚠️ Опиши продуктите или прикачи снимка.")
    else:
        with st.spinner("🧑‍🍳 Шеф-готвачът обмисля варианти..."):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Обновен промпт с филтър за сурова храна
                prompt = f"""
                Ти си професионален Zero-Waste готвач. Твоята задача е:

                1. ВАЛИДАЦИЯ: Анализирай входа: "{ingredients_input if ingredients_input else "продуктите от снимката"}".
                   Ако списъкът съдържа предмети, които не са храна, отговори ЕДИНСТВЕНО с кода: ГРЕШКА:НЕХРАНИТЕЛНИ_ДАННИ.

                2. ГЕНЕРИРАНЕ: Ако продуктите са годни за готвене, генерирай ТОЧНО 3 РАЗЛИЧНИ идеи за ястия на български език.
                   
                   ВАЖНО:
                   - НЕ предлагай рецепти за сурова консумация (без недопечено месо). 
                   - Всички меса и яйца трябва да преминават през поне една пълна топлинна обработка (варене, печене, пържене).
                   - НЕ използвай поздрави и уводи. Започни директно с първата рецепта.
                   - Използвай '---' като разделител между трите рецепти.

                Формат за всяка рецепта:
                Име: [Име на ястието]
                ### 🛒 Необходими продукти:
                - [Продукт]
                ### 👨‍🍳 Начин на приготвяне:
                1. [Стъпка 1]
                2. [Стъпка 2]
                ### ♻️ Zero-Waste съвет:
                [Конкретен съвет]
                ---
                """

                content = [prompt]
                if uploaded_file:
                    content.append(image)
                
                response = model.generate_content(content)
                
                # Проверка за валидност и разделяне на рецептите
                if "ГРЕШКА:НЕХРАНИТЕЛНИ_ДАННИ" in response.text:
                    st.error("⚠️ Моля, въведете само хранителни продукти!")
                    st.session_state.recipes_list = []
                else:
                    raw_parts = response.text.strip().split('---')
                    st.session_state.recipes_list = [p.strip() for p in raw_parts if len(p.strip()) > 20][:3]
                    st.session_state.selected_index = None 
                
            except Exception as e:
                st.error(f"Грешка: {e}")

# 5. Показване само на имената (Бутони)
if st.session_state.recipes_list:
    st.markdown("---")
    st.markdown("### ✨ Избери рецепта:")
    
    cols = st.columns(len(st.session_state.recipes_list))
    
    for idx, r_text in enumerate(st.session_state.recipes_list):
        # Почистваме текста от евентуални остатъчни поздрави на първия ред
        lines = r_text.split('\n')
        # Търсим реда, който започва с "Име:"
        recipe_name = "Идея"
        for line in lines:
            if "Име:" in line:
                recipe_name = line.replace("Име:", "").replace("**", "").strip()
                break
        
        with cols[idx]:
            if st.button(recipe_name, key=f"btn_{idx}", use_container_width=True):
                st.session_state.selected_index = idx

# 6. Показване на пълната рецепта вътре в зелената рамка
    if st.session_state.selected_index is not None:
        selected_recipe = st.session_state.recipes_list[st.session_state.selected_index]
        
        st.markdown("---")
        
        # Премахваме името (първия ред), за да не се повтаря с бутона
        lines = selected_recipe.split('\n')
        recipe_content = "\n".join(lines[1:]) if "Име:" in lines[0] else selected_recipe

        # Поставяме ЦЯЛОТО съдържание вътре в div-а на един път
        st.markdown(f"""
            <div class="recipe-card">
                {recipe_content}
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Zero-Waste Chef AI | 2026")

