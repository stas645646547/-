class TacticsAgent:
    async def suggest(self, user_message, lang):
        # user_message — это строка, а не dict!
        if any(term in user_message.lower() for term in ["не выплатили", "невыплата", "שכר לא שולם"]):
            return "Рекомендуем собрать все возможные доказательства и обратиться к юристу. Важно зафиксировать каждый шаг."
        return "Ожидаем дополнительную информацию для тактики."