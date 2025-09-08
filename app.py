import streamlit as st

from subtitler import generate_subtitles, translate_subtitles, burn_subtitles

import os

import tempfile

import math

import subprocess

import uuid

from datetime import datetime



# Server konfiguratsiyasi - fayl yuklash cheklovini o'chirish

st.set_page_config(

    page_title="O‘zbekcha Subtitl Tarjimon", 

    page_icon="🎬", 

    layout="centered",

    initial_sidebar_state="expanded"

)



# Maxsus CSS stillari

st.markdown(

    """

    <style>

    .main {background-color: #f8fafc;}

    .stButton>button {background-color: #2563eb; color: white; border-radius: 8px;}

    .stDownloadButton>button {background-color: #059669; color: white; border-radius: 8px;}

    .stTextInput>div>div>input {border-radius: 8px;}

    .stTabs [data-baseweb="tab-list"] {justify-content: center;}

    

    /* Katta fayllar uchun maxsus stillar */

    .big-file-warning {

        background-color: #fffbeb;

        padding: 15px;

        border-radius: 10px;

        border-left: 5px solid #f59e0b;

        margin: 10px 0;

    }

    

    .file-info {

        background-color: #e0f2fe;

        padding: 10px;

        border-radius: 8px;

        margin: 5px 0;

    }

    </style>

    """, 

    unsafe_allow_html=True

)



st.markdown("<h1 style='text-align:center; color:#2563eb;'>🎬 O‘zbekcha Subtitl Tarjimon</h1>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#64748b;'>Video uchun avtomatik subtitl, tarjima va tahrirlash platformasi!</p>", unsafe_allow_html=True)



# Cheklovsiz fayl yuklash haqida ma'lumot

with st.expander("ℹ️ Fayl yuklash haqida ma'lumot"):

    st.info("""

    **Platformamizda fayl hajmi cheklovi yo'q!** 

    - Istalgan hajmdagi videolarni yuklashingiz mumkin

    - Katta videolar biroz ko'proq vaqt olishi mumkin

    - Internet tezligingizga qarab ishlash vaqti o'zgaradi

    - Har bir video va subtitl unikal nom bilan saqlanadi

    """)



SUPPORTED_LANGS = {

    "Inglizcha": "en",

    "Ruscha": "ru",

    "O‘zbekcha": "uz",

    "Turkcha": "tr",

    "Nemischa": "de",

    "Fransuzcha": "fr",

    "Ispancha": "es",

    "Arabcha": "ar",

    "Xitoycha": "zh-CN",

    "Yaponcha": "ja",

    "Koreyscha": "ko",

    "Hindcha": "hi"

}



# Whisper modellari

WHISPER_MODELS = {

    "Tiny (engil, tez, kam aniqlik)": "tiny",

    "Base (muvozanatli)": "base",

    "Small (yaxshi aniqlik)": "small",

    "Medium (yuqori aniqlik)": "medium",

    "Large (eng yuqori aniqlik)": "large"

}



# ================== YANGI FUNKSIYALAR ==================



def generate_unique_filename(original_filename, prefix=""):

    """Unikal fayl nomi yaratish"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    unique_id = str(uuid.uuid4())[:8]

    name, ext = os.path.splitext(original_filename)

    

    # Fayl nomini xavfsiz qilish

    safe_name = get_safe_filename(name)

    

    if prefix:

        return f"{prefix}_{timestamp}_{unique_id}_{safe_name}{ext}"

    else:

        return f"{timestamp}_{unique_id}_{safe_name}{ext}"



def get_safe_filename(filename):

    """Xavfsiz fayl nomi yaratish (maxsus belgilarni olib tashlash)"""

    import re

    # Maxsus belgilarni olib tashlash

    safe_name = re.sub(r'[^\w\s-]', '', filename)

    # Bo'shliqlarni pastki chiziqcha bilan almashtirish

    safe_name = re.sub(r'[-\s]+', '_', safe_name)

    # Qirqib olish (juda uzun nomlardan qochish)

    return safe_name[:50]  # Maksimum 50 belgi



def get_file_size_mb(file_path):

    """Fayl hajmini MB da qaytaradi"""

    if os.path.exists(file_path):

        size_bytes = os.path.getsize(file_path)

        return size_bytes / (1024 * 1024)

    return 0



def get_file_size_kb(file_path):

    """Fayl hajmini KB da qaytaradi"""

    if os.path.exists(file_path):

        size_bytes = os.path.getsize(file_path)

        return size_bytes / 1024

    return 0



def cleanup_temp_files():

    """Vaqtinchalik fayllarni tozalash"""

    # Session statedagi barcha fayllarni o'chirish

    for file_type in ["video_files", "srt_files"]:

        if file_type in st.session_state:

            for key, file_path in st.session_state[file_type].items():

                try:

                    if os.path.exists(file_path):

                        os.remove(file_path)

                except:

                    pass

    

    # Qo'shimcha vaqtinchalik fayllarni tozalash

    temp_files = [f for f in os.listdir('.') if f.endswith(('.mp4', '.srt', '.wav')) and not f.startswith('.')]

    for file in temp_files:

        try:

            if os.path.exists(file):

                os.remove(file)

        except:

            pass



def split_large_video(video_path, max_size_mb=190):

    """Katta videoni qismlarga bo'lish"""

    try:

        # Video hajmini o'lchash

        file_size_mb = get_file_size_mb(video_path)

        

        if file_size_mb <= max_size_mb:

            return [video_path]  # Bo'lish shart emas

        

        st.warning(f"Video {file_size_mb:.1f} MB - qismlarga bo'linmoqda...")

        

        # Video davomiyligini o'lchash

        cmd = [

            "ffprobe", "-v", "error", "-show_entries", "format=duration",

            "-of", "default=noprint_wrappers=1:nokey=1", video_path

        ]

        

        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=30)

        duration = float(result.stdout.strip())

        

        # Qismlar sonini hisoblash

        num_parts = math.ceil(file_size_mb / max_size_mb)

        part_duration = duration / num_parts

        

        parts = []

        temp_dir = tempfile.mkdtemp()

        

        for i in range(num_parts):

            start_time = i * part_duration

            output_path = os.path.join(temp_dir, f"part_{i+1}.mp4")

            

            cmd = [

                "ffmpeg", "-y", "-ss", str(start_time), "-i", video_path,

                "-t", str(part_duration), "-c", "copy", output_path

            ]

            

            try:

                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)

                parts.append(output_path)

                st.info(f"Qism {i+1}/{num_parts} yaratildi")

            except Exception as e:

                st.error(f"Qism {i+1} ni yaratishda xatolik: {str(e)}")

                break

        

        return parts

    

    except Exception as e:

        st.error(f"Video bo'lishda xatolik: {str(e)}")

        return [video_path]  # Agar bo'lish mumkin bo'lmasa, butun video bilan ishlash



def process_large_video(video_path, model_size, progress_callback):

    """Katta videoni qismlab ishlash"""

    try:

        parts = split_large_video(video_path)

        

        if len(parts) == 1:

            # Video katta emas, oddiy ishlash

            return generate_subtitles(video_path, model_size, progress_callback)

        

        all_subtitles = []

        total_parts = len(parts)

        

        for i, part_path in enumerate(parts):

            progress = (i / total_parts) * 50

            progress_callback(progress)

            

            st.info(f"Qism {i+1}/{total_parts} ishlanmoqda...")

            

            try:

                part_srt = generate_subtitles(part_path, model_size, lambda p: None)

                

                with open(part_srt, 'r', encoding='utf-8') as f:

                    all_subtitles.append(f.read())

                

                # Vaqtinchalik fayllarni tozalash

                try:

                    os.remove(part_path)

                    os.remove(part_srt)

                except:

                    pass

                

            except Exception as e:

                st.error(f"Qism {i+1} da xatolik: {str(e)}")

                continue

        

        # Barcha subtitllarni birlashtirish

        if all_subtitles:

            final_srt = generate_unique_filename("combined_subtitles.srt", "subtitles")

            with open(final_srt, 'w', encoding='utf-8') as f:

                for i, subtitle in enumerate(all_subtitles):

                    if i > 0:

                        f.write("\n")

                    f.write(subtitle)

            

            progress_callback(100)

            return final_srt

        

        return None

    

    except Exception as e:

        st.error(f"Katta video ishlashda xatolik: {str(e)}")

        return None



# ================== ASOSIY KOD ==================



tab1, tab2, tab3, tab4 = st.tabs([

    "1️⃣ Subtitl yaratish",

    "2️⃣ Tarjima qilish",

    "3️⃣ Subtitlni tahrirlash",

    "4️⃣ Videoga subtitl biriktirish"

])



# Session stateda fayl yo'llarini saqlash uchun

if "video_files" not in st.session_state:

    st.session_state.video_files = {}

if "srt_files" not in st.session_state:

    st.session_state.srt_files = {}

if "current_video" not in st.session_state:

    st.session_state.current_video = None

if "current_srt" not in st.session_state:

    st.session_state.current_srt = None



# Dastur boshlanganda vaqtinchalik fayllarni tozalash

cleanup_temp_files()



with tab1:

    st.markdown("#### 📥 Videoni yuklang va subtitl yarating")

    

    # Modelni tanlash

    model_name = st.selectbox(

        "Whisper modelini tanlang:",

        options=list(WHISPER_MODELS.keys()),

        index=1,

        help="Katta modellar aniqroq natija beradi, lekin sekinroq ishlaydi. Kichik modellar tezroq, lekin kamroq aniq."

    )

    model_size = WHISPER_MODELS[model_name]

    

    uploaded_video = st.file_uploader(

        "Videoni yuklang (MP4, MOV, AVI)", 

        type=["mp4", "mov", "avi"],

        help="Istalgan hajmdagi videoni yuklashingiz mumkin"

    )

    

    if uploaded_video:

        file_size_mb = len(uploaded_video.getvalue()) / (1024 * 1024)

        

        if file_size_mb > 100:

            st.markdown(f"""

            <div class='big-file-warning'>

                <h4>⚠️ Katta video fayli ({file_size_mb:.1f} MB)</h4>

                <p>Ishlash vaqti biroz ko'proq bo'lishi mumkin. Sabr qiling...</p>

            </div>

            """, unsafe_allow_html=True)

        

        # Unikal video nomi yaratish

        video_filename = generate_unique_filename(uploaded_video.name, "video")

        safe_video_filename = get_safe_filename(video_filename)

        

        with st.spinner("Video yuklanmoqda..."):

            with open(safe_video_filename, "wb") as f:

                f.write(uploaded_video.getbuffer())

        

        # Session statega saqlash

        st.session_state.video_files["current"] = safe_video_filename

        st.session_state.current_video = safe_video_filename

        

        st.success(f"✅ Video yuklandi! Hajmi: {file_size_mb:.1f} MB")

        st.markdown(f"""

        <div class='file-info'>

            <strong>📁 Fayl nomi:</strong> {safe_video_filename}<br>

            <strong>📊 Hajmi:</strong> {file_size_mb:.1f} MB<br>

            <strong>🕐 Yuklangan vaqt:</strong> {datetime.now().strftime("%H:%M:%S")}

        </div>

        """, unsafe_allow_html=True)

        

        if st.button("Subtitl yaratish", use_container_width=True):

            progress_placeholder = st.empty()

            status_placeholder = st.empty()

            

            def progress_callback(p):

                progress_placeholder.progress(p / 100, text=f"Subtitl yaratilmoqda... {p}%")

                status_placeholder.markdown(

                    f"<div style='text-align:center;font-size:18px;color:#2563eb;'>"

                    f"<b>Jarayon:</b> {p}%</div>", unsafe_allow_html=True)

            

            try:

                # Fayl hajmini tekshirish va mos usulni tanlash

                file_size_mb = get_file_size_mb(safe_video_filename)

                

                if file_size_mb > 190:  # Streamlit Cloud cheklovi

                    st.info("Katta video - maxsus usul bilan ishlanmoqda...")

                    srt_path = process_large_video(safe_video_filename, model_size, progress_callback)

                else:

                    srt_path = generate_subtitles(safe_video_filename, model_size, progress_callback)

                

                progress_placeholder.progress(1.0, text="Subtitl yaratildi!")

                status_placeholder.markdown(

                    "<div style='text-align:center;font-size:18px;color:#059669;'><b>Subtitl yaratildi! 100%</b></div>",

                    unsafe_allow_html=True)

                

                if srt_path and os.path.exists(srt_path):

                    st.success("✅ Subtitl yaratildi!")

                    

                    # SRT fayl hajmi

                    srt_size_kb = get_file_size_kb(srt_path)

                    

                    # Session statega saqlash

                    st.session_state.srt_files["current"] = srt_path

                    st.session_state.current_srt = srt_path

                    

                    with open(srt_path, "r", encoding="utf-8") as f:

                        srt_content = f.read()

                    

                    st.download_button(

                        f"📥 Subtitlni yuklab olish ({srt_size_kb:.1f} KB)", 

                        srt_content, 

                        file_name=os.path.basename(srt_path), 

                        use_container_width=True

                    )

                    

                    st.markdown(f"""

                    <div class='file-info'>

                        <strong>📝 Subtitl fayli:</strong> {os.path.basename(srt_path)}<br>

                        <strong>📊 Hajmi:</strong> {srt_size_kb:.1f} KB<br>

                        <strong>✅ Status:</strong> Tayyor

                    </div>

                    """, unsafe_allow_html=True)

                    

                else:

                    st.error("Subtitl yaratishda xatolik.")

                    

            except Exception as e:

                st.error(f"Xatolik yuz berdi: {str(e)}")

                progress_placeholder.empty()

                status_placeholder.empty()



with tab2:

    st.markdown("#### 🌐 Subtitlni istalgan tilga tarjima qiling")

    st.write("Subtitl faylini yuklang yoki avvalgi bosqichda yaratilgan/yuklangan fayldan foydalaning.")

    

    uploaded_srt = st.file_uploader("Subtitl (.srt) faylini yuklang", type=["srt"], key="srt_upload")

    srt_path = None

    

    if uploaded_srt:

        # Unikal SRT nomi yaratish

        srt_filename = generate_unique_filename(uploaded_srt.name, "subtitles")

        safe_srt_filename = get_safe_filename(srt_filename)

        

        srt_path = safe_srt_filename

        with open(srt_path, "wb") as f:

            f.write(uploaded_srt.getbuffer())

        

        st.session_state.srt_files["uploaded"] = srt_path

        st.session_state.current_srt = srt_path

        

        st.success("✅ SRT fayli yuklandi!")

        st.markdown(f"""

        <div class='file-info'>

            <strong>📝 Fayl nomi:</strong> {safe_srt_filename}<br>

            <strong>🕐 Yuklangan vaqt:</strong> {datetime.now().strftime("%H:%M:%S")}

        </div>

        """, unsafe_allow_html=True)

    

    elif "current_srt" in st.session_state and st.session_state.current_srt:

        srt_path = st.session_state.current_srt

        st.info("Avval yaratilgan subtitl fayli ishlatilmoqda")



    lang_name = st.selectbox("Tarjima tilini tanlang:", list(SUPPORTED_LANGS.keys()), index=0)

    lang = SUPPORTED_LANGS[lang_name]



    if srt_path and os.path.exists(srt_path):

        if st.button("Tarjima qilish", key="translate_btn", use_container_width=True):

            progress_placeholder = st.empty()

            status_placeholder = st.empty()

            

            def progress_callback(p):

                progress_placeholder.progress(p / 100, text=f"Tarjima qilinmoqda... {p}%")

                status_placeholder.markdown(

                    f"<div style='text-align:center;font-size:18px;color:#2563eb;'>"

                    f"<b>Jarayon:</b> {p}%</div>", unsafe_allow_html=True)

            

            try:

                translated_path = translate_subtitles(srt_path, lang, progress_callback)

                

                progress_placeholder.progress(1.0, text="Tarjima tayyor!")

                status_placeholder.markdown(

                    "<div style='text-align:center;font-size:18px;color:#059669;'><b>Tarjima tayyor! 100%</b></div>",

                    unsafe_allow_html=True)

                

                if translated_path and os.path.exists(translated_path):

                    # Tarjima qilingan fayl nomi

                    translated_filename = generate_unique_filename(f"translated_{lang}.srt", "translated")

                    

                    with open(translated_path, "r", encoding="utf-8") as f:

                        translated_content = f.read()

                    

                    st.download_button(

                        f"🌐 Tarjima qilingan subtitl (.srt)", 

                        translated_content, 

                        file_name=translated_filename, 

                        use_container_width=True

                    )

                    

                    st.session_state.srt_files["translated"] = translated_path

                    st.success("✅ Tarjima tayyor!")

                    

                    st.markdown(f"""

                    <div class='file-info'>

                        <strong>🌐 Tarjima tili:</strong> {lang_name}<br>

                        <strong>📝 Fayl nomi:</strong> {translated_filename}<br>

                        <strong>✅ Status:</strong> Tarjima tayyor

                    </div>

                    """, unsafe_allow_html=True)

                    

                else:

                    st.error("Tarjimada xatolik.")

                    

            except Exception as e:

                st.error(f"Tarjima xatosi: {str(e)}")

                progress_placeholder.empty()

                status_placeholder.empty()

    else:

        st.info("Avval subtitl yarating yoki yuklang.")



with tab3:

    st.markdown("#### ✏️ Subtitl matnini onlayn tahrirlash va videoga bog'lash")

    

    uploaded_edit_srt = st.file_uploader("Subtitl (.srt) faylini yuklang", type=["srt"], key="edit_srt_upload")

    srt_file = None

    srt_filename = None

    

    if uploaded_edit_srt:

        # Unikal SRT nomi yaratish

        srt_filename = generate_unique_filename(uploaded_edit_srt.name, "edit")

        safe_srt_filename = get_safe_filename(srt_filename)

        

        srt_file = safe_srt_filename

        with open(srt_file, "wb") as f:

            f.write(uploaded_edit_srt.getbuffer())

        

        st.session_state.srt_files["edit"] = srt_file

        st.session_state.current_srt = srt_file

        

        st.success("✅ SRT fayli yuklandi!")

        st.markdown(f"""

        <div class='file-info'>

            <strong>📝 Fayl nomi:</strong> {safe_srt_filename}<br>

            <strong>🕐 Yuklangan vaqt:</strong> {datetime.now().strftime("%H:%M:%S")}

        </div>

        """, unsafe_allow_html=True)

    

    elif "current_srt" in st.session_state and st.session_state.current_srt:

        srt_file = st.session_state.current_srt

        srt_filename = os.path.basename(srt_file)

        st.info("Mavjud subtitl fayli ishlatilmoqda")

    

    if srt_file and os.path.exists(srt_file):

        with open(srt_file, "r", encoding="utf-8") as f:

            srt_text = f.read()

        

        edited_srt = st.text_area("Subtitl matni:", value=srt_text, height=300)

        

        # Tahrirlangan fayl nomi

        edited_filename = generate_unique_filename("edited_subtitles.srt", "edited")

        

        st.download_butto
