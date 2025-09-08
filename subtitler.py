import os
import tempfile
import subprocess
import whisper
from deep_translator import GoogleTranslator
import shutil

def get_ffmpeg_path():
    # FFmpeg ni avtomatik topish
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    
    # Windows uchun qo'shimcha tekshirish
    if os.name == 'nt':
        possible_paths = [
            r"C:\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
            r"C:\tools\ffmpeg\bin\ffmpeg.exe",
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
    
    raise FileNotFoundError(
        "FFmpeg topilmadi! Iltimos, FFmpeg ni o'rnating:\n"
        "Windows: https://www.gyan.dev/ffmpeg/builds/\n"
        "macOS: brew install ffmpeg\n"
        "Linux: sudo apt install ffmpeg"
    )

FFMPEG_PATH = get_ffmpeg_path()

def check_ffmpeg():
    # FFmpeg mavjudligini tekshirish
    try:
        result = subprocess.run([FFMPEG_PATH, "-version"], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def extract_audio(video_path, audio_path):
    """Audio ajratish funksiyasi"""
    try:
        subprocess.run([
            FFMPEG_PATH, "-y", "-i", video_path, 
            "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", 
            audio_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Audio ajratishda xatolik: {e}")
        return False
    except Exception as e:
        print(f"Xatolik: {e}")
        return False

def generate_subtitles(video_path, model_size="base", progress_callback=None):
    if not check_ffmpeg():
        raise FileNotFoundError("FFmpeg topilmadi! Iltimos, FFmpeg ni o'rnating.")
    
    audio_path = tempfile.mktemp(suffix=".wav")
    
    if progress_callback:
        progress_callback(5)
    
    # Audio ajratish
    if not extract_audio(video_path, audio_path):
        raise Exception("Audio ajratishda xatolik yuz berdi.")
    
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
                
                if progress_callback:
                    p = int(100 * (i + 1) / total)
                    progress_callback(p)
    except Exception as e:
        raise Exception(f"Tarjima faylini yozishda xatolik: {str(e)}")
    
    if progress_callback:
        progress_callback(100)
    
    return out_path

def burn_subtitles(video_path, srt_path):
    out_path = tempfile.mktemp(suffix=".mp4")
    
    # SRT fayl yo'lini to'g'rilash (bo'shliqlar bo'lsa)
    srt_path_escaped = f"'{srt_path}'" if ' ' in srt_path else srt_path
    
    cmd = [
        FFMPEG_PATH, "-y", "-i", video_path, 
        "-vf", f"subtitles={srt_path_escaped}", 
        "-c:a", "copy", out_path
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return out_path
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg xatosi: {e}")
        return None
    except Exception as e:
        print(f"Subtitl biriktirishda xatolik: {e}")
        return None
