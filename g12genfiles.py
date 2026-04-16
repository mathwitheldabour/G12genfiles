import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="NIFHAM Math Portal", layout="wide")

# تصميم الهيدر (إنجليزي أساسي، عربي تحته)
st.markdown("<h1 style='text-align: center; color: #1a5276;'>NIFHAM Math - Student Portal</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #27ae60;' dir='rtl'>بوابة نفهم رياضيات - الصف الثاني عشر المتقدم</h3>", unsafe_allow_html=True)
st.markdown("---")

# تصميم الدروس
st.markdown("<h2 style='color: #1a5276;'>Lesson 1: Rational Equations</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #27ae60;' dir='rtl'>الدرس الأول: المعادلات النسبية</h4>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.info("Interactive Presentation | عرض الشرح التفاعلي")
    # يمكنك وضع رابط مباشر لملف الـ HTML المرفوع على GitHub Pages
    st.markdown("[Open Presentation | افتح العرض](https://your-github-link/files/presentation.html)")

with col2:
    st.success("Student Worksheet | ورقة عمل الطالب")
    # زر لتحميل ملف PDF (يجب أن ترفع الملف في مجلد files على جيت هب)
    with open("files/worksheet_1.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    st.download_button(
        label="Download PDF | تحميل الملف",
        data=PDFbyte,
        file_name="Rational_Equations_Worksheet.pdf",
        mime='application/octet-stream'
    )

st.markdown("---")
# يمكنك تكرار الكود السابق لإضافة الدرس الثاني، الثالث، إلخ...

# الفوتر
st.markdown("<p style='text-align: center; font-weight: bold; color: #1a5276;'>Mr. Ibrahim Eldabour &copy; 2026</p>", unsafe_allow_html=True)
