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

# ОБНОВЕНА: Функцията вече записва и email в таблицата
def add_user(username, email, password):
    hashed_pw = make_hashes(password)
    try:
        supabase.table("users").insert({
            "username": username, 
            "email": email, 
            "password": hashed_pw
        }).execute()
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

def delete_recipe_from_db(recipe_id):
    try:
        supabase.table("saved_recipes").delete().eq("id", recipe_id).execute()
        return True
    except Exception as e:
        st.error(f"Грешка при изтриване: {e}")
        return False

# --- ИНИЦИАЛИЗАЦИЯ НА СЪСТОЯНИЕТО ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'recipes_list' not in st.session_state:
    st.session_state.recipes_list = []
if 'selected_index' not in st.session_state:
    st.session_state.selected_index = None
if 'recipe_to_delete' not in st.session_state:
    st.session_state.recipe_to_delete = None

# Прилагане на CSS
def local_css(file_name):
    try:
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("style.css")

# --- СТРАНИЧНО МЕНЮ ---
with st.sidebar:
    st.title("👤 Профил")
    
    if not st.session_state.logged_in:
        st.info("Влезте в профила си, за да виждате запазените си рецепти.")
        auth_tab1, auth_tab2 = st.tabs(["Вход", "Регистрация"])
        
        with auth_tab1:
            u_in = st.text_input("Потребител", key="sidebar_u_login")
            p_in = st.text_input("Парола", type="password", key="sidebar_p_login")
            if st.button("Влез", use_container_width=True):
                if login_user(u_in, p_in):
                    st.session_state.logged_in = True
                    st.session_state.username = u_in
                    st.rerun()
                else:
                    st.error("Грешно име или парола.")
                    
        with auth_tab2:
            u_reg = st.text_input("Нов потребител", key="sidebar_u_reg")
            email_reg = st.text_input("Имейл адрес", key="sidebar_email_reg") # ДОБАВЕНО ПОЛЕ
            p_reg = st.text_input("Нова парола", type="password", key="sidebar_p_reg")
            if st.button("Създай профил", use_container_width=True):
                if not u_reg or not email_reg or not p_reg: # ОБНОВЕНА ПРОВЕРКА
                    st.error("⚠️ Моля, попълнете всички полета.")
                elif len(u_reg) < 3:
                    st.error("⚠️ Потребителското име трябва да бъде поне 3 символа.")
                elif "@" not in email_reg or "." not in email_reg: # БАЗОВА ПРОВЕРКА ЗА ИМЕЙЛ
                    st.error("⚠️ Моля, въведете валиден имейл адрес.")
                elif len(p_reg) < 6:
                    st.error("⚠️ Паролата трябва да бъде поне 6 символа.")
                else:
                    if add_user(u_reg, email_reg, p_reg): # ПОДАВА СЕ EMAIL
                        st.success("Успешно! Вече можете да влезете.")
                    else:
                        st.error("Името или имейлът вече се използват.")
    else:
        st.success(f"Здравей, {st.session_state.username}!")
        if st.button("Изход", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.recipe_to_delete = None
            st.rerun()

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("❌ Липсва API ключ в Secrets!")
    st.stop()

st.title("♻️ Zero-Waste AI Готвач")

# --- СЕКЦИЯ ЗАПАЗЕНИ РЕЦЕПТИ ---
if st.session_state.logged_in:
    with st.expander("📂 Бърз достъп до моите запазени рецепти"):
        my_data_main = get_saved_recipes(st.session_state.username)
        if my_data_main:
            for r in my_data_main:
                with st.expander(f"📖 {r['recipe_name']}"):
                    st.markdown(f'<div class="recipe-card">{r["recipe_content"]}</div>', unsafe_allow_html=True)
                    
                    if st.button(f"🗑️ Изтрий '{r['recipe_name']}'", key=f"del_{r['id']}", use_container_width=True):
                        st.session_state.recipe_to_delete = r['id']
                        st.rerun()
                    
                    if st.session_state.recipe_to_delete == r['id']:
                        st.warning(f"⚠️ Сигурни ли сте, че искате да изтриете '{r['recipe_name']}'?")
                        col_yes, col_no = st.columns(2)
                        with col_yes:
                            if st.button("Да, изтрий", key=f"confirm_yes_{r['id']}", use_container_width=True):
                                if delete_recipe_from_db(r['id']):
                                    st.session_state.recipe_to_delete = None
                                    st.toast("Рецептата беше изтрита!", icon="🗑️")
                                    st.rerun()
                        with col_no:
                            if st.button("Отказ", key=f"confirm_no_{r['id']}", use_container_width=True):
                                st.session_state.recipe_to_delete = None
                                st.rerun()
        else:
            st.write("Все още нямаш запазени рецепти.")

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
                model = genai.GenerativeModel('gemini-2.5-flash')
                prompt = f"""
                Ти си професионален Zero-Waste готвач. Твоята задача е:
                1. ВАЛИДАЦИЯ: Анализирай "{ingredients_input if ingredients_input else "снимката"}". Ако не е храна, върни само думата ГРЕШКА:НЕХРАНИТЕЛНИ_ДАННИ.
                2. ГЕНЕРИРАНЕ: Генерирай точно 3 уникални и напълно различни кулинарни идеи на български език въз основа на предоставените продукти. 
                
                СТРИКТНИ ИЗИСКВАНИЯ ЗА ОФОРМЛЕНИЕТО:
                - Разделяй трите рецепти ЕДИНСТВЕНО чрез специалния маркер ###РЕЦЕПТА### поставен на самостоятелен нов ред.
                - За всяка рецепта започни директно на първия ред във формат: Име: [Име на ястието тук]
                - Използвай стандартни Markdown прекъсвания за нов ред. Всяка съставка и всяка стъпка ТРЯБВА да са на отделен нов ред.
                - Продуктите трябва да започват с тире и интервал за bulletpoint (например: - 100г ориз). Не слагай допълнителни тирета между съставките.
                - Стъпките трябва да са номерирани (например: 1. Измийте продуктите.).
                
                Примерен точен шаблон за ЕДНА рецепта:
                Име: Печени Пилешки Крила с Ароматен Ориз
                ### 🛒 Необходими продукти:
                - Пилешки крила
                - Ориз (100г)
                ### 👨‍🍳 Начин на приготвяне:
                1. Измийте и подсушете пилешките крила.
                2. Подредете в тава за печене.
                ### ♻️ Zero-Waste съвет:
                Използвайте костите за домашен бульон.
                ###РЕЦЕПТА###
                """
                content = [prompt]
                if uploaded_file: content.append(image)
                response = model.generate_content(content)
                
                if "ГРЕШКА:НЕХРАНИТЕЛНИ_ДАННИ" in response.text:
                    st.error("⚠️ Моля, въведете само хранителни продукти!")
                    st.session_state.recipes_list = []
                else:
                    raw_parts = response.text.split('###РЕЦЕПТА###')
                    st.session_state.recipes_list = [p.strip() for p in raw_parts if len(p.strip()) > 30][:3]
                    st.session_state.selected_index = None 
            except Exception as e:
                st.error(f"Грешка при генериране: {e}")

# Показване на резултати от генериране
if st.session_state.recipes_list:
    st.markdown("---")
    st.markdown("### ✨ Избери една от идеите на шеф-готвача:")
    
    cols = st.columns(len(st.session_state.recipes_list))
    
    for idx, r_text in enumerate(st.session_state.recipes_list):
        lines = r_text.split('\n')
        recipe_name = "Идея"
        for line in lines:
            if "Име:" in line:
                recipe_name = line.replace("Име:", "").replace("**", "").strip()
                break
        
        with cols[idx]:
            if st.button(recipe_name, key=f"recipe_btn_{idx}", use_container_width=True):
                st.session_state.selected_index = idx

    if st.session_state.selected_index is not None:
        selected_recipe = st.session_state.recipes_list[st.session_state.selected_index]
        
        current_name = "Рецепта"
        for line in selected_recipe.split('\n'):
            if "Име:" in line:
                current_name = line.replace("Име:", "").replace("**", "").strip()
                break

        st.markdown(f"## 📖 {current_name}")
        
        display_lines = selected_recipe.split('\n')
        recipe_body = "\n".join(display_lines[1:]) if "Име:" in display_lines[0] else selected_recipe

        st.markdown(f'<div class="recipe-card">{recipe_body}</div>', unsafe_allow_html=True)
        
        if st.session_state.logged_in:
            if st.button(f"💾 Запази '{current_name}' в профила", use_container_width=True):
                if save_recipe_to_db(st.session_state.username, current_name, recipe_body):
                    st.toast("✅ Рецептата е запазена успешно!", icon="⭐")
                    st.rerun()
        else:
            st.warning("🔒 Тнябва да влезете в профила си, за да запазите тази рецепта.")
            with st.expander("🔑 Влез или се Регистрирай тук"):
                t1, t2 = st.tabs(["Вход", "Регистрация"])
                with t1:
                    u = st.text_input("Потребител", key="main_login_u")
                    p = st.text_input("Парола", type="password", key="main_login_p")
                    if st.button("Влез и запази", key="btn_main_login"):
                        if login_user(u, p):
                            st.session_state.logged_in = True
                            st.session_state.username = u
                            save_recipe_to_db(u, current_name, recipe_body)
                            st.success("Успешен вход! Рецептата е запазена.")
                            st.rerun()
                        else:
                            st.error("Грешни данни.")
                with t2:
                    u_r = st.text_input("Избери име", key="main_reg_u")
                    em_r = st.text_input("Въведи имейл", key="main_reg_email") # ДОБАВЕНО ПОЛЕ В ОСНОВНАТА ФОРМА
                    p_r = st.text_input("Избери парола", type="password", key="main_reg_p")
                    if st.button("Създай акаунт", key="btn_main_reg"):
                        if not u_r or not em_r or not p_r:
                            st.error("⚠️ Моля, попълнете всички полета.")
                        elif len(u_r) < 3:
                            st.error("⚠️ Потребителското име трябва да бъде поне 3 символа.")
                        elif "@" not in em_r or "." not in em_r:
                            st.error("⚠️ Моля, въведете валиден имейл.")
                        elif len(p_r) < 6:
                            st.error("⚠️ Паролата трябва да бъде поне 6 символа.")
                        else:
                            if add_user(u_r, em_r, p_r): # ПОДАВА СЕ EMAIL
                                st.success("Профилът е създаден! Сега влезте от съседния таб.")
                            else:
                                st.error("Името или имейлът вече са заети.")

st.markdown("---")
st.caption("Zero-Waste Chef AI | 2026")