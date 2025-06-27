# app/integrations/language_detector.py

def detect_language(text):
    # Простейший "детектор"
    if any('\u0590' <= c <= '\u05FF' for c in text):
        return 'he'
    elif any('\u0400' <= c <= '\u04FF' for c in text):
        return 'ru'
    else:
        return 'en'
