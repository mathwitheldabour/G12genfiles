import streamlit as st
import json
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="NIFHAM Math - Grade 12 General", layout="wide")

# 2. ملف حفظ البيانات
# هذا الملف سيتم إنشاؤه تلقائياً لحفظ الدروس والروابط التي تضيفها
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

data = load_data()

# 3. الهيدر (الإنجليزية أساس ثم العربية)
st.markdown("<h1 style='text-align: center; color: #1a5276;'>NIFHAM Math - Grade 12 General</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #27ae60;' dir='rtl'>بوابة نفهم رياضيات - الصف الثاني عشر العام</h3>", unsafe_allow_html=True)
st.markdown("---")

# 4. نظام دخول المعلم (في القائمة الجانبية المخفية)
with st.sidebar:
    st.markdown("### Teacher Login")
    # يمكنك تغيير كلمة المرور 12345 إلى أي كلمة سر تريدها
    password = st.text_input("Enter Password", type="password")
    is_admin = (password == "12345") 

# 5. لوحة تحكم المعلم (تظهر فقط عند إدخال كلمة المرور الصحيحة)
if is_admin:
    st.success("Welcome, Mr. Ibrahim Eldabour!")
    st.markdown("## Admin Dashboard | لوحة التحكم")
    
    tab1, tab2, tab3 = st.tabs(["Add Unit", "Add Lesson", "Add Material"])
    
    # تبويب إضافة وحدة دراسية
    with tab1:
        with st.form("add_unit"):
            u_en = st.text_input("Unit Name (English)", placeholder="e.g., Unit 1: Limits")
            u_ar = st.text_input("اسم الوحدة (عربي)", placeholder="مثال: الوحدة الأولى: النهايات")
            if st.form_submit_button("Save Unit"):
                data["units"].append({"unit_en": u_en, "unit_ar": u_ar, "lessons": []})
                save_data(data)
                st.success("Unit added successfully!")
                st.rerun()
                
    # تبويب إضافة درس
    with tab2:
        with st.form("add_lesson"):
            unit_options = [u["unit_en"] for u in data["units"]]
            if unit_options:
                selected_unit = st.selectbox("Select Unit", unit_options)
                l_en = st.text_input("Lesson Name (English)", placeholder="e.g., Lesson 1: Rational Equations")
                l_ar = st.text_input("اسم الدرس (عربي)")
                if st.form_submit_button("Save Lesson"):
                    for u in data["units"]:
                        if u["unit_en"] == selected_unit:
                            u["lessons"].append({"lesson_en": l_en, "lesson_ar": l_ar, "materials": []})
                    save_data(data)
                    st.success("Lesson added successfully!")
                    st.rerun()
            else:
                st.warning("Please add a unit first.")

    # تبويب إضافة مادة (فيديو، ملف، ورقة عمل)
    with tab3:
        with st.form("add_material"):
            unit_options = [u["unit_en"] for u in data["units"]]
            if unit_options:
                selected_unit_mat = st.selectbox("Select Unit", unit_options)
                
                lesson_options = []
                for u in data["units"]:
                    if u["unit_en"] == selected_unit_mat:
                        lesson_options = [l["lesson_en"] for l in u["lessons"]]
                        
                if lesson_options:
                    selected_lesson_mat = st.selectbox("Select Lesson", lesson_options)
                    mat_type = st.selectbox("Material Type", ["Worksheet", "Presentation", "Video"])
                    mat_en = st.text_input("Title (English)", placeholder="e.g., Student Worksheet")
                    mat_ar = st.text_input("العنوان (عربي)", placeholder="مثال: ورقة عمل الطالب")
                    mat_url = st.text_input("Link (Google Drive / YouTube)", placeholder="ضع رابط الملف أو الفيديو هنا")
                    
                    if st.form_submit_button("Save Material"):
                        for u in data["units"]:
                            if u["unit_en"] == selected_unit_mat:
                                for l in u["lessons"]:
                                    if l["lesson_en"] == selected_lesson_mat:
                                        l["materials"].append({
                                            "type": mat_type,
                                            "title_en": mat_en,
                                            "title_ar": mat_ar,
                                            "url": mat_url
                                        })
                        save_data(data)
                        st.success("Material added successfully!")
                        st.rerun()
                else:
                    st.warning("Please add a lesson first.")
    st.markdown("---")

# 6. واجهة الطالب (عرض المحتوى الديناميكي)
if not data["units"]:
    st.info("No content added yet. Please login to add units and lessons.")

for unit in data["units"]:
    st.markdown(f"<h2 style='color: #1a5276; margin-bottom: 0;'>{unit['unit_en']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: #27ae60; margin-top: 5px;' dir='rtl'>{unit['unit_ar']}</h4>", unsafe_allow_html=True)
    
    for lesson in unit["lessons"]:
        with st.expander(f"{lesson['lesson_en']} | {lesson['lesson_ar']}"):
            cols = st.columns(3)
            col_idx = 0
            for mat in lesson["materials"]:
                # تحديد الأيقونة بناءً على نوع الملف
                icon = "📄" if mat["type"] == "Worksheet" else "💻" if mat["type"] == "Presentation" else "🎥"
                with cols[col_idx % 3]:
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; text-align: center; background-color: #f9f9f9;">
                        <div style="font-size: 2rem;">{icon}</div>
                        <h4 style="color: #1a5276; margin: 10px 0 5px 0;">{mat['title_en']}</h4>
                        <p style="color: #27ae60; margin: 0 0 15px 0;" dir="rtl">{mat['title_ar']}</p>
                        <a href="{mat['url']}" target="_blank" style="background-color: #1a5276; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; display: inline-block;">Open File</a>
                    </div>
                    """, unsafe_allow_html=True)
                col_idx += 1
    st.markdown("<br>", unsafe_allow_html=True)

# 7. تذييل الصفحة (الاسم على الجانب باللغة الإنجليزية فقط)
st.markdown("<hr style='border: 1px solid #eee;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left; font-weight: bold; color: #1a5276;'>Mr. Ibrahim Eldabour</p>", unsafe_allow_html=True)
