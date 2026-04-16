import streamlit as st
import json
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="NIFHAM Math - Grade 12 General", layout="wide")

# 2. إدارة ملف البيانات
DATA_FILE = "nifham_data.json"

if not os.path.exists(DATA_FILE):
    default_data = {"units": []}
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_data, f, ensure_ascii=False, indent=4)

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_clean_url(url):
    if "drive.google.com" in url and "/view" in url:
        return url.split("/view")[0] + "/preview"
    elif "youtube.com/watch?v=" in url:
        vid_id = url.split("v=")[1].split("&")[0]
        return f"https://www.youtube.com/embed/{vid_id}"
    elif "youtu.be/" in url:
        vid_id = url.split("youtu.be/")[1].split("?")[0]
        return f"https://www.youtube.com/embed/{vid_id}"
    return url

data = load_data()

# 3. الهيدر
st.markdown("<h1 style='text-align: center; color: #1a5276;'>NIFHAM Math - Grade 12 General</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #27ae60;' dir='rtl'>بوابة نفهم رياضيات - الصف الثاني عشر العام</h3>", unsafe_allow_html=True)
st.markdown("---")

# 4. دخول المعلم
with st.sidebar:
    st.markdown("### Teacher Login")
    password = st.text_input("Enter Password", type="password")
    is_admin = (password == "12345") 

# 5. لوحة التحكم المطورة
if is_admin:
    st.success("Welcome, Mr. Ibrahim Eldabour!")
    st.markdown("## Admin Dashboard | لوحة التحكم")
    
    # إضافة تبويب رابع للإدارة والحذف
    tab1, tab2, tab3, tab4 = st.tabs(["Add Unit", "Add Lesson", "Add Material", "Manage Content"])
    
    with tab1:
        with st.form("add_unit"):
            u_en = st.text_input("Unit Name (English)")
            u_ar = st.text_input("اسم الوحدة (عربي)")
            if st.form_submit_button("Save Unit"):
                if u_en:
                    data["units"].append({"unit_en": u_en, "unit_ar": u_ar, "lessons": []})
                    save_data(data)
                    st.success("Unit added!")
                    st.rerun()

    with tab2:
        unit_options = [u["unit_en"] for u in data["units"]]
        if unit_options:
            with st.form("add_lesson"):
                selected_unit = st.selectbox("Select Unit", unit_options)
                l_en = st.text_input("Lesson Name (English)")
                l_ar = st.text_input("اسم الدرس (عربي)")
                if st.form_submit_button("Save Lesson"):
                    for u in data["units"]:
                        if u["unit_en"] == selected_unit:
                            u["lessons"].append({"lesson_en": l_en, "lesson_ar": l_ar, "materials": []})
                    save_data(data)
                    st.success("Lesson added!")
                    st.rerun()

    with tab3:
        unit_options = [u["unit_en"] for u in data["units"]]
        if unit_options:
            selected_unit_mat = st.selectbox("Select Unit", unit_options, key="mat_unit_select")
            lesson_options = []
            for u in data["units"]:
                if u["unit_en"] == selected_unit_mat:
                    lesson_options = [l["lesson_en"] for l in u["lessons"]]
            if lesson_options:
                with st.form("add_material"):
                    selected_lesson_mat = st.selectbox("Select Lesson", lesson_options)
                    mat_type = st.selectbox("Type", ["Worksheet", "Presentation", "Video"])
                    mat_en = st.text_input("Title (English)")
                    mat_ar = st.text_input("العنوان (عربي)")
                    mat_url = st.text_input("Link URL")
                    if st.form_submit_button("Save Material"):
                        for u in data["units"]:
                            if u["unit_en"] == selected_unit_mat:
                                for l in u["lessons"]:
                                    if l["lesson_en"] == selected_lesson_mat:
                                        l["materials"].append({"type": mat_type, "title_en": mat_en, "title_ar": mat_ar, "url": mat_url})
                        save_data(data)
                        st.success("Material added!")
                        st.rerun()

    # --- تبويب إدارة المحتوى (الحذف والتعديل) ---
    with tab4:
        st.markdown("### Manage & Delete | إدارة وحذف المحتوى")
        if not data["units"]:
            st.write("No content to manage.")
        else:
            for i, unit in enumerate(data["units"]):
                col_u1, col_u2 = st.columns([4, 1])
                col_u1.markdown(f"**Unit:** {unit['unit_en']} | {unit['unit_ar']}")
                if col_u2.button(f"Delete Unit", key=f"del_u_{i}"):
                    data["units"].pop(i)
                    save_data(data)
                    st.rerun()
                
                for j, lesson in enumerate(unit["lessons"]):
                    col_l1, col_l2 = st.columns([4, 1])
                    col_l1.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;📖 Lesson: {lesson['lesson_en']}")
                    if col_l2.button(f"Delete Lesson", key=f"del_l_{i}_{j}"):
                        unit["lessons"].pop(j)
                        save_data(data)
                        st.rerun()
                    
                    for k, mat in enumerate(lesson["materials"]):
                        col_m1, col_m2 = st.columns([4, 1])
                        col_m1.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🔗 {mat['type']}: {mat['title_en']}")
                        if col_m2.button(f"Remove File", key=f"del_m_{i}_{j}_{k}"):
                            lesson["materials"].pop(k)
                            save_data(data)
                            st.rerun()
                st.markdown("---")

# 6. واجهة الطالب
for unit in data["units"]:
    st.markdown(f"<h2 style='color: #1a5276;'>{unit['unit_en']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: #27ae60;' dir='rtl'>{unit['unit_ar']}</h4>", unsafe_allow_html=True)
    for lesson in unit["lessons"]:
        with st.expander(f"{lesson['lesson_en']} | {lesson['lesson_ar']}"):
            if lesson["materials"]:
                cols = st.columns(3)
                for idx, mat in enumerate(lesson["materials"]):
                    clean_link = get_clean_url(mat['url'])
                    icon = "📄" if mat["type"] == "Worksheet" else "💻" if mat["type"] == "Presentation" else "🎥"
                    with cols[idx % 3]:
                        st.markdown(f"""
                        <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; text-align: center; background-color: #fcfcfc; margin-bottom: 10px;">
                            <div style="font-size: 2.5rem;">{icon}</div>
                            <h4 style="color: #1a5276; margin-bottom: 5px;">{mat['title_en']}</h4>
                            <p style="color: #27ae60; margin-bottom: 15px;" dir="rtl">{mat['title_ar']}</p>
                            <a href="{clean_link}" target="_blank" style="background-color: #1a5276; color: white; padding: 8px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Open | فتح</a>
                        </div>
                        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left; font-weight: bold; color: #1a5276;'>Mr. Ibrahim Eldabour</p>", unsafe_allow_html=True)
