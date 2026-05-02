
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
#----------------------------------------------------////

#YESYESYESYES
# import streamlit as st
# import google.generativeai as genai
# from PIL import Image

# # 1. Настройка на страницата
# st.set_page_config(page_title="Zero-Waste Chef", page_icon="♻️", layout="centered")

# # Функция за зареждане на CSS
# def local_css(file_name):
#     try:
#         with open(file_name, encoding="utf-8") as f:
#             st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#     except FileNotFoundError:
#         pass

# local_css("style.css")

# # 2. Инициализация на API
# try:
#     API_KEY = st.secrets["GEMINI_API_KEY"]
#     genai.configure(api_key=API_KEY)
# except Exception:
#     st.error("❌ Липсва API ключ! Провери .streamlit/secrets.toml")
#     st.stop()

# # Инициализиране на състоянието
# if 'recipes_list' not in st.session_state:
#     st.session_state.recipes_list = []
# if 'selected_index' not in st.session_state:
#     st.session_state.selected_index = None

# st.title("♻️ Zero-Waste AI Готвач")
# st.write("Превърни остатъците в професионално ястие.")

# # 3. Входни данни
# col1, col2 = st.columns(2)
# with col1:
#     ingredients_input = st.text_area(
#         "Остатъци и продукти:", 
#         placeholder="напр. пиле, увехнал магданоз...",
#         height=150
#     )
# with col2:
#     uploaded_file = st.file_uploader("Снимка на продуктите:", type=["jpg", "jpeg", "png"])

# if uploaded_file:
#     image = Image.open(uploaded_file)
#     st.image(image, use_container_width=True)

# # 4. Основна логика за генериране
# if st.button("🚀 Генерирай 3 идеи", use_container_width=True):
#     if not ingredients_input and not uploaded_file:
#         st.warning("⚠️ Опиши продуктите или прикачи снимка.")
#     else:
#         with st.spinner("🧑‍🍳 Шеф-готвачът обмисля варианти..."):
#             try:
#                 model = genai.GenerativeModel('gemini-2.5-flash')
                
#                 # Обновен промпт с филтър за сурова храна
#                 prompt = f"""
#                 Ти си професионален Zero-Waste готвач. Твоята задача е:

#                 1. ВАЛИДАЦИЯ: Анализирай входа: "{ingredients_input if ingredients_input else "продуктите от снимката"}".
#                    Ако списъкът съдържа предмети, които не са храна, отговори ЕДИНСТВЕНО с кода: ГРЕШКА:НЕХРАНИТЕЛНИ_ДАННИ.

#                 2. ГЕНЕРИРАНЕ: Ако продуктите са годни за готвене, генерирай ТОЧНО 3 РАЗЛИЧНИ идеи за ястия на български език.
                   
#                    ВАЖНО:
#                    - НЕ предлагай рецепти за сурова консумация (без недопечено месо). 
#                    - Всички меса и яйца трябва да преминават през поне една пълна топлинна обработка (варене, печене, пържене).
#                    - НЕ използвай поздрави и уводи. Започни директно с първата рецепта.
#                    - Използвай '---' като разделител между трите рецепти.

#                 Формат за всяка рецепта:
#                 Име: [Име на ястието]
#                 ### 🛒 Необходими продукти:
#                 - [Продукт]
#                 ### 👨‍🍳 Начин на приготвяне:
#                 1. [Стъпка 1]
#                 2. [Стъпка 2]
#                 ### ♻️ Zero-Waste съвет:
#                 [Конкретен съвет]
#                 ---
#                 """

#                 content = [prompt]
#                 if uploaded_file:
#                     content.append(image)
                
#                 response = model.generate_content(content)
                
#                 # Проверка за валидност и разделяне на рецептите
#                 if "ГРЕШКА:НЕХРАНИТЕЛНИ_ДАННИ" in response.text:
#                     st.error("⚠️ Моля, въведете само хранителни продукти!")
#                     st.session_state.recipes_list = []
#                 else:
#                     raw_parts = response.text.strip().split('---')
#                     st.session_state.recipes_list = [p.strip() for p in raw_parts if len(p.strip()) > 20][:3]
#                     st.session_state.selected_index = None 
                
#             except Exception as e:
#                 st.error(f"Грешка: {e}")

# # 5. Показване само на имената (Бутони)
# if st.session_state.recipes_list:
#     st.markdown("---")
#     st.markdown("### ✨ Избери рецепта:")
    
#     cols = st.columns(len(st.session_state.recipes_list))
    
#     for idx, r_text in enumerate(st.session_state.recipes_list):
#         # Почистваме текста от евентуални остатъчни поздрави на първия ред
#         lines = r_text.split('\n')
#         # Търсим реда, който започва с "Име:"
#         recipe_name = "Идея"
#         for line in lines:
#             if "Име:" in line:
#                 recipe_name = line.replace("Име:", "").replace("**", "").strip()
#                 break
        
#         with cols[idx]:
#             if st.button(recipe_name, key=f"btn_{idx}", use_container_width=True):
#                 st.session_state.selected_index = idx

# # 6. Показване на пълната рецепта вътре в зелената рамка
#     if st.session_state.selected_index is not None:
#         selected_recipe = st.session_state.recipes_list[st.session_state.selected_index]
        
#         st.markdown("---")
        
#         # Премахваме името (първия ред), за да не се повтаря с бутона
#         lines = selected_recipe.split('\n')
#         recipe_content = "\n".join(lines[1:]) if "Име:" in lines[0] else selected_recipe

#         # Поставяме ЦЯЛОТО съдържание вътре в div-а на един път
#         st.markdown(f"""
#             <div class="recipe-card">
#                 {recipe_content}
#             </div>
#         """, unsafe_allow_html=True)

# st.markdown("---")
# st.caption("Zero-Waste Chef AI | 2026")
#YESYESYES

# import streamlit as st
# import google.generativeai as genai
# from PIL import Image
# from supabase import create_client, Client
# import hashlib

# # 1. Настройка на страницата
# st.set_page_config(page_title="Zero-Waste Chef", page_icon="♻️", layout="centered")


# # --- ФУНКЦИИ ЗА БАЗА ДАННИ (SUPABASE) ---
# def get_supabase_client():
#     url: str = st.secrets["SUPABASE_URL"]
#     key: str = st.secrets["SUPABASE_KEY"]
#     return create_client(url, key)

# supabase = get_supabase_client()

# def make_hashes(password):
#     return hashlib.sha256(str.encode(password)).hexdigest()

# def add_user(username, password):
#     hashed_pw = make_hashes(password)
#     try:
#         supabase.table("users").insert({"username": username, "password": hashed_pw}).execute()
#         return True
#     except Exception:
#         return False

# def login_user(username, password):
#     hashed_pw = make_hashes(password)
#     res = supabase.table("users").select("*").eq("username", username).eq("password", hashed_pw).execute()
#     return len(res.data) > 0

# def save_recipe_to_db(username, name, content):
#     try:
#         supabase.table("saved_recipes").insert({
#             "username": username,
#             "recipe_name": name,
#             "recipe_content": content
#         }).execute()
#         return True
#     except Exception as e:
#         st.error(f"Грешка при запис: {e}")
#         return False

# def get_saved_recipes(username):
#     res = supabase.table("saved_recipes").select("*").eq("username", username).execute()
#     return res.data

# # --- ИНИЦИАЛИЗАЦИЯ НА СЪСТОЯНИЕТО ---
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
# if 'username' not in st.session_state:
#     st.session_state.username = ""
# if 'recipes_list' not in st.session_state:
#     st.session_state.recipes_list = []
# if 'selected_index' not in st.session_state:
#     st.session_state.selected_index = None

# # --- СТРАНИЧНО МЕНЮ (LOGIN/SIGNUP) ---
# with st.sidebar:
#     st.title("👤 Профил")
#     if not st.session_state.logged_in:
#         auth_mode = st.radio("Действие", ["Вход", "Регистрация"])
#         user_input = st.text_input("Потребителско име")
#         pass_input = st.text_input("Парола", type="password")
        
#         if auth_mode == "Регистрация":
#             if st.button("Създай акаунт"):
#                 if add_user(user_input, pass_input):
#                     st.success("Успешна регистрация! Вече можете да влезете.")
#                 else:
#                     st.error("Потребителското име е заето.")
#         else:
#             if st.button("Вход"):
#                 if login_user(user_input, pass_input):
#                     st.session_state.logged_in = True
#                     st.session_state.username = user_input
#                     st.rerun()
#                 else:
#                     st.error("Грешно име или парола.")
#     else:
#         st.write(f"Добре дошъл, **{st.session_state.username}**!")
#         if st.button("Изход"):
#             st.session_state.logged_in = False
#             st.session_state.username = ""
#             st.rerun()
        
#         st.markdown("---")
#         st.subheader("📚 Моите рецепти")
#         my_data = get_saved_recipes(st.session_state.username)
#         for r in my_data:
#             with st.expander(r['recipe_name']):
#                 st.write(r['recipe_content'])

# # --- ОСНОВЕН ИНТЕРФЕЙС ---
# def local_css(file_name):
#     try:
#         with open(file_name, encoding="utf-8") as f:
#             st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
#     except FileNotFoundError:
#         pass

# local_css("style.css")

# # Инициализация на AI
# try:
#     API_KEY = st.secrets["GEMINI_API_KEY"]
#     genai.configure(api_key=API_KEY)
# except Exception:
#     st.error("❌ Липсва API ключ в Secrets!")
#     st.stop()

# st.title("♻️ Zero-Waste AI Готвач")
# st.write("Превърни остатъците в професионално ястие.")

# # 3. Входни данни
# col1, col2 = st.columns(2)
# with col1:
#     ingredients_input = st.text_area(
#         "Остатъци и продукти:", 
#         placeholder="напр. пиле, увехнал магданоз...",
#         height=150
#     )
# with col2:
#     uploaded_file = st.file_uploader("Снимка на продуктите:", type=["jpg", "jpeg", "png"])

# if uploaded_file:
#     image = Image.open(uploaded_file)
#     st.image(image, use_container_width=True)

# # 4. Основна логика за генериране
# if st.button("🚀 Генерирай 3 идеи", use_container_width=True):
#     if not ingredients_input and not uploaded_file:
#         st.warning("⚠️ Опиши продуктите или прикачи снимка.")
#     else:
#         with st.spinner("🧑‍🍳 Шеф-готвачът обмисля варианти..."):
#             try:
#                 model = genai.GenerativeModel('gemini-2.5-flash')
#                 prompt = f"""
#                 Ти си професионален Zero-Waste готвач. Твоята задача е:
#                 1. ВАЛИДАЦИЯ: Анализирай "{ingredients_input if ingredients_input else "снимката"}". Ако не е храна, кажи ГРЕШКА:НЕХРАНИТЕЛНИ_ДАННИ.
#                 2. ГЕНЕРИРАНЕ: 3 идеи на български. Без сурово месо/яйца. Без уводи. Използвай '---' за разделител.
#                 Формат:
#                 Име: [Име]
#                 ### 🛒 Необходими продукти:
#                 - [Продукт]
#                 ### 👨‍🍳 Начин на приготвяне:
#                 1. [Стъпка]
#                 ### ♻️ Zero-Waste съвет:
#                 [Съвет]
#                 ---
#                 """
#                 content = [prompt]
#                 if uploaded_file: content.append(image)
#                 response = model.generate_content(content)
                
#                 if "ГРЕШКА:НЕХРАНИТЕЛНИ_ДАННИ" in response.text:
#                     st.error("⚠️ Моля, въведете само хранителни продукти!")
#                     st.session_state.recipes_list = []
#                 else:
#                     raw_parts = response.text.strip().split('---')
#                     st.session_state.recipes_list = [p.strip() for p in raw_parts if len(p.strip()) > 20][:3]
#                     st.session_state.selected_index = None 
#             except Exception as e:
#                 st.error(f"Грешка: {e}")

# # 5. Показване на бутони за избор
# if st.session_state.recipes_list:
#     st.markdown("---")
#     st.markdown("### ✨ Избери рецепта:")
#     cols = st.columns(len(st.session_state.recipes_list))
#     for idx, r_text in enumerate(st.session_state.recipes_list):
#         lines = r_text.split('\n')
#         recipe_name = "Идея"
#         for line in lines:
#             if "Име:" in line:
#                 recipe_name = line.replace("Име:", "").replace("**", "").strip()
#                 break
#         with cols[idx]:
#             if st.button(recipe_name, key=f"btn_{idx}", use_container_width=True):
#                 st.session_state.selected_index = idx

# # 6. Показване на пълната рецепта и опция за запис
#     if st.session_state.selected_index is not None:
#         selected_recipe = st.session_state.recipes_list[st.session_state.selected_index]
        
#         # Извличане на името за базата данни
#         current_name = "Рецепта"
#         for line in selected_recipe.split('\n'):
#             if "Име:" in line:
#                 current_name = line.replace("Име:", "").replace("**", "").strip()
#                 break

#         st.markdown("---")
#         lines = selected_recipe.split('\n')
#         recipe_content = "\n".join(lines[1:]) if "Име:" in lines[0] else selected_recipe

#         st.markdown(f'<div class="recipe-card">{recipe_content}</div>', unsafe_allow_html=True)
        
#         # БУТОН ЗА ЗАПИСВАНЕ
#         if st.session_state.logged_in:
#             if st.button(f"💾 Запази '{current_name}' в профила", use_container_width=True):
#                 if save_recipe_to_db(st.session_state.username, current_name, recipe_content):
#                     st.toast("✅ Рецептата е запазена!", icon="⭐")
#         else:
#             st.info("💡 Влез в профила си, за да запишеш тази рецепта.")

# st.markdown("---")
# st.caption("Zero-Waste Chef AI | 2026")





import streamlit as st
import google.generativeai as genai
from PIL import Image
from supabase import create_client, Client
import hashlib

# 1. Настройка на страницата
st.set_page_config(page_title="Zero-Waste Chef", page_icon="♻️", layout="centered")

# --- ФУНКЦИИ ЗА БАЗА ДАННИ (SUPABASE) ---
def get_supabase_client():
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase_client()

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def add_user(username, password):
    hashed_pw = make_hashes(password)
    try:
        supabase.table("users").insert({"username": username, "password": hashed_pw}).execute()
        return True
    except Exception:
        return False

def login_user(username, password):
    hashed_pw = make_hashes(password)
    res = supabase.table("users").select("*").eq("username", username).eq("password", hashed_pw).execute()
    return len(res.data) > 0

def save_recipe_to_db(username, name, content):
    try:
        supabase.table("saved_recipes").insert({
            "username": username,
            "recipe_name": name,
            "recipe_content": content
        }).execute()
        return True
    except Exception as e:
        st.error(f"Грешка при запис: {e}")
        return False

def get_saved_recipes(username):
    res = supabase.table("saved_recipes").select("*").eq("username", username).execute()
    return res.data

# --- ИНИЦИАЛИЗАЦИЯ НА СЪСТОЯНИЕТО ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'recipes_list' not in st.session_state:
    st.session_state.recipes_list = []
if 'selected_index' not in st.session_state:
    st.session_state.selected_index = None

# --- СТРАНИЧНО МЕНЮ ---
with st.sidebar:
    st.title("👤 Профил")
    if not st.session_state.logged_in:
        st.info("Влезте, за да запазвате рецепти.")
        auth_tab1, auth_tab2 = st.tabs(["Вход", "Регистрация"])
        
        with auth_tab1:
            u_in = st.text_input("Потребител", key="u_login")
            p_in = st.text_input("Парола", type="password", key="p_login")
            if st.button("Влез", use_container_width=True):
                if login_user(u_in, p_in):
                    st.session_state.logged_in = True
                    st.session_state.username = u_in
                    st.rerun()
                else:
                    st.error("Грешно име или парола.")
        
        with auth_tab2:
            u_reg = st.text_input("Нов потребител", key="u_reg")
            p_reg = st.text_input("Нова парола", type="password", key="p_reg")
            if st.button("Създай профил", use_container_width=True):
                if add_user(u_reg, p_reg):
                    st.success("Успешно! Сега влезте от таб 'Вход'.")
                else:
                    st.error("Името е заето.")
    else:
        st.success(f"Здравей, {st.session_state.username}!")
        if st.button("Изход", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
        
        st.markdown("---")
        st.subheader("📚 Моите рецепти")
        my_data = get_saved_recipes(st.session_state.username)
        for r in my_data:
            with st.expander(r['recipe_name']):
                st.write(r['recipe_content'])

# --- ОСНОВЕН ИНТЕРФЕЙС ---
def local_css(file_name):
    try:
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("style.css")

# Инициализация на AI
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("❌ Липсва API ключ в Secrets!")
    st.stop()

st.title("♻️ Zero-Waste AI Готвач")
st.write("Превърни остатъците в професионално ястие.")

# Входни данни
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

# Генериране
if st.button("🚀 Генерирай идеи", use_container_width=True):
    if not ingredients_input and not uploaded_file:
        st.warning("⚠️ Опиши продуктите или прикачи снимка.")
    else:
        with st.spinner("🧑‍🍳 Шеф-готвачът обмисля варианти..."):
            try:
                # Използваме gemini-1.5-flash за стабилност
                model = genai.GenerativeModel('gemini-2.5-flash')
                prompt = f"""
                Ти си професионален Zero-Waste готвач. Твоята задача е:
                1. ВАЛИДАЦИЯ: Анализирай "{ingredients_input if ingredients_input else "снимката"}". Ако не е храна, кажи ГРЕШКА:НЕХРАНИТЕЛНИ_ДАННИ.
                2. ГЕНЕРИРАНЕ: 3 идеи на български. Без сурово месо/яйца. Без уводи. Използвай '---' за разделител.
                Формат:
                Име: [Име]
                ### 🛒 Необходими продукти:
                - [Продукт]
                ### 👨‍🍳 Начин на приготвяне:
                1. [Стъпка]
                ### ♻️ Zero-Waste съвет:
                [Съвет]
                ---
                """
                content = [prompt]
                if uploaded_file: content.append(image)
                response = model.generate_content(content)
                
                if "ГРЕШКА:НЕХРАНИТЕЛНИ_ДАННИ" in response.text:
                    st.error("⚠️ Моля, въведете само хранителни продукти!")
                    st.session_state.recipes_list = []
                else:
                    raw_parts = response.text.strip().split('---')
                    st.session_state.recipes_list = [p.strip() for p in raw_parts if len(p.strip()) > 20][:3]
                    st.session_state.selected_index = None 
            except Exception as e:
                st.error(f"Грешка: {e}")

# Показване на рецепти
if st.session_state.recipes_list:
    st.markdown("---")
    st.markdown("### ✨ Избери рецепта:")
    cols = st.columns(len(st.session_state.recipes_list))
    for idx, r_text in enumerate(st.session_state.recipes_list):
        lines = r_text.split('\n')
        recipe_name = "Идея"
        for line in lines:
            if "Име:" in line:
                recipe_name = line.replace("Име:", "").replace("**", "").strip()
                break
        with cols[idx]:
            if st.button(recipe_name, key=f"btn_{idx}", use_container_width=True):
                st.session_state.selected_index = idx

    if st.session_state.selected_index is not None:
        selected_recipe = st.session_state.recipes_list[st.session_state.selected_index]
        current_name = "Рецепта"
        for line in selected_recipe.split('\n'):
            if "Име:" in line:
                current_name = line.replace("Име:", "").replace("**", "").strip()
                break

        st.markdown("---")
        lines = selected_recipe.split('\n')
        recipe_content = "\n".join(lines[1:]) if "Име:" in lines[0] else selected_recipe
        st.markdown(f'<div class="recipe-card">{recipe_content}</div>', unsafe_allow_html=True)
        
        # ЛОГИКА ЗА ЗАПИСВАНЕ
        if st.session_state.logged_in:
            if st.button(f"💾 Запази '{current_name}' в профила", use_container_width=True):
                if save_recipe_to_db(st.session_state.username, current_name, recipe_content):
                    st.toast("✅ Рецептата е запазена!", icon="⭐")
        else:
            st.warning("🔒 Трябва да влезете в профила си, за да запазите тази рецепта.")
            st.info("Използвайте страничното меню за вход или регистрация.")

st.markdown("---")
st.caption("Zero-Waste Chef AI | 2026")