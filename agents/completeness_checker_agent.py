# agents/completeness_checker.py
class CompletenessCheckerAgent:
    async def check(self, questions, user_lang):
        if not questions:
            return ["Все необходимые вопросы заданы. Можете переходить к описанию своей ситуации подробнее."]
        return questions