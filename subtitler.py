import os
import tempfile
import subprocess
import whisper
from deep_translator import GoogleTranslator
import shutil
import sys

# FFmpeg ni topish uchun funksiya - Streamlit Cloud uchun moslashtirilgan
def get_ffmpeg_path():
    # Streamlit Cloud'da FFmpeg yo'llari
    possible_paths = [
        "/usr/bin/ffmpeg",
        "/bin/ffmpeg",
        "/app/bin/ffmpeg",
        "/opt/conda/bin/ffmpeg",
        "ffmpeg"
    ]
    
    for path in possible_paths:
        if shutil.which(path):
            return path
    
    # Agar FFmpeg topilmasa, moviepy yoki audio processing uchun alternativ
    try:
        import moviepy.editor as mp
        return None  # Moviepy mavjud
    except ImportError:
        # Streamlit Cloud'da FFmpeg yo'qligi haqida xabar
        print("FFmpeg topilmadi! Moviepy yordamida ishlaymiz...")
        return None

FFMPEG_PATH = get_ffmpeg_path()

def check_ffmpeg():
    if FFMPEG_PATH is None:
        # Moviepy yoki boshqa kutubxona bilan ishlash
        try:
            import moviepy.editor as mp
            return True
        except ImportError:
            # Moviepy ham yo'q, audio processing uchun alternativ
            try:
                import pydub
                return True
            except ImportError:
                raise Exception(
                    "FFmpeg topilmadi! Iltimos, quyidagilardan birini bajaring:\n"
                    "1. requirements.txt ga 'moviepy' qo'shing\n"
                    "2. Yoki lokalda FFmpeg ni o'rnating\n"
                    "3. Streamlit Cloud'da FFmpeg avtomatik o'rnatilgan bo'lishi kerak"
                )
    
    try:
        # FFmpeg mavjudligini tekshirish
        result = subprocess.run([FFMPEG_PATH, "-version"], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def extract_audio(video_path, audio_path):
    """Audio ajratish funksiyasi - FFmpeg yoki alternativ usullar"""
    if FFMPEG_PATH and check_ffmpeg():
        # FFmpeg bilan audio ajratish
        try:
            subprocess.run([
                FFMPEG_PATH, "-y", "-i", video_path, 
                "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", 
                audio_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, timeout=300)
            return True
        except:
            # FFmpeg bilan xatolik, alternativ usulga o'tish
            pass
    
    # Moviepy yordamida audio ajratish
    try:
        import moviepy.editor as mp
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, fps=16000, verbose=False, logger=None)
        video.close()
        return True
    except Exception as e:
        print(f"Moviepy bilan audio ajratishda xatolik: {e}")
        # So'nggi imkoniyat - pydub
        try:
            from pydub import AudioSegment
            video = AudioSegment.from_file(video_path)
            video.export(audio_path, format="wav", parameters=["-ar", "16000", "-ac", "1"])
            return True
        except:
            raise Exception(f"Audio ajratish mumkin emas: {str(e)}")

def generate_subtitles(video_path, model_size="base", progress_callback=None):
    if progress_callback:
        progress_callback(5)
    
    audio_path = tempfile.mktemp(suffix=".wav")
    
    # Audio ajratish
    try:
        if not extract_audio(video_path, audio_path):
            raise Exception("Audio ajratish mumkin emas")
    except Exception as e:
        raise Exception(f"Audio ajratishda xatolik: {str(e)}")
    
    if progress_callback:
        progress_callback(15)
    
    # Modelni yuklash
    try:
        model = whisper.load_model(model_size)
    except Exception as e:
        # Agar katta model yuklanmasa, kichikroq modelni sinab ko'ramiz
        try:
            if model_size != "base":
                model = whisper.load_model("base")
            else:
                model = whisper.load_model("tiny")
        except:
            raise Exception(f"Whisper modelini yuklab bo'lmadi: {str(e)}")
    
    if progress_callback:
        progress_callback(20)
    
    # Transkripsiya qilish
    try:
        result = model.transcribe(audio_path, fp16=False, verbose=False)
        segments = result["segments"]
    except Exception as e:
        raise Exception(f"Transkripsiya qilishda xatolik: {str(e)}")
    
    # SRT faylini yaratish
    srt_path = tempfile.mktemp(suffix=".srt")
    total = len(segments)
    
    try:
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(segments):
                start = seg["start"]
                end = seg["end"]
                text = seg["text"].strip()
                f.write(f"{i+1}\n")
                f.write(f"{format_time(start)} --> {format_time(end)}\n")
                f.write(f"{text}\n\n")
                
                if progress_callback and total > 0:
                    p = 20 + int(75 * (i + 1) / total)
                    progress_callback(p)
    except Exception as e:
        raise Exception(f"SRT fayl yaratishda xatolik: {str(e)}")
    
    # Audio faylni o'chirish
    try:
        os.remove(audio_path)
    except:
        pass
    
    if progress_callback:
        progress_callback(100)
    
    return srt_path

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def translate_subtitles(srt_path, dest_lang, progress_callback=None):
    out_path = tempfile.mktemp(suffix=f"_{dest_lang}.srt")
    
    try:
        with open(srt_path, "r", encoding="utf-8") as fin:
            lines = fin.readlines()
    except Exception as e:
        raise Exception(f"SRT faylni o'qishda xatolik: {str(e)}")
    
    blocks = []
    block = []
    
    for line in lines:
        if line.strip() == "":
            if len(block) == 3:
                blocks.append(block.copy())
            block = []
        else:
            block.append(line)
    
    if len(block) == 3:
        blocks.append(block.copy())
    
    total = len(blocks)
    
    try:
        with open(out_path, "w", encoding="utf-8") as fout:
            for i, block in enumerate(blocks):
                fout.write(block[0])
                fout.write(block[1])
                
                # Tarjima qilish
                try:
                    translated = GoogleTranslator(source='auto', target=dest_lang).translate(block[2].strip())
                    fout.write(translated + "\n\n")
                except Exception as e:
                    # Agar tarjima qilishda xatolik bo'lsa, original matnni qoldiramiz
                    fout.write(block[2] + "\n\n")
                    print(f"Tarjima xatosi: {e}")
                
                if progress_callback:
                    p = int(100 * (i + 1) / total)
                    progress_callback(p)
    except Exception as e:
        raise Exception(f"Tarjima faylini yozishda xatolik: {str(e)}")
    
    if progress_callback:
        progress_callback(100)
    
    return out_path

def burn_subtitles(video_path, srt_path):
    # Streamlit Cloud'da FFmpeg bo'lmasa, bu funksiyani o'chirib qo'yamiz
    if not FFMPEG_PATH or not check_ffmpeg():
        raise Exception("FFmpeg topilmadi! Videoga subtitl biriktirish faqat lokalda ishlaydi.")
    
    out_path = tempfile.mktemp(suffix=".mp4")
    
    # SRT fayl yo'lini to'g'rilash
    srt_path_escaped = f"'{srt_path}'" if ' ' in srt_path else srt_path
    
    cmd = [
        FFMPEG_PATH, "-y", "-i", video_path, 
        "-vf", f"subtitles={srt_path_escaped}", 
        "-c:a", "copy", out_path
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
        return out_path
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg xatosi: {e}")
        return None
    except Exception as e:
        print(f"Subtitl biriktirishda xatolik: {e}")
        return None
