from integrations.llm import call_gpt
from prompts_lawyer import SUPERLAWYER_PROMPT

class QuestionGenAgent:
    async def generate(self, user_message, user_lang, context=None, history=None, stage=None):
        # Можно не реализовывать — LLM справится с вопросами внутри основного промпта.
        # Или оставить заглушку, если система требует.
        return ""
