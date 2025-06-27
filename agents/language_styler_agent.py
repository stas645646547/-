# agents/language_styler.py
class LanguageStylerAgent:
    async def style(self, questions, user_lang):
        # Можно подключить GPT или простое форматирование
        styled = []
        for q in questions:
            styled.append(f"📝 {q}")
        return styled