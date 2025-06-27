from agents.rag_agent import RAGAgent
from agents.tactics_agent import TacticsAgent
from integrations.llm import call_gpt
from prompts_lawyer import SUPERLAWYER_PROMPT
from agents.graph_agent import GraphAgent
from semantic_search_chroma import ChromaSemanticSearch
import os
import re

# Пути
GRAPH_PATH = r"C:\Users\kamst\OneDrive\Рабочий стол\app\data\7 главных законов\חוק הגנת השכר\узлы\graph.json"
graph_agent = GraphAgent(GRAPH_PATH)

DATA_PATH = os.getenv("DATA_PATH", "data")
dialog_state = {}

# Semantic Search инициализация
semsearch = ChromaSemanticSearch(persist_directory="chroma_db")

# Этапы
STAGES = [
    "start", "evidence_collection", "claim_preparation",
    "lawsuit_preparation", "final"
]

def get_next_stage(current):
    idx = STAGES.index(current) if current in STAGES else 0
    return STAGES[min(idx + 1, len(STAGES) - 1)]

async def process_user_message(user_message, user_lang, user_id=None):
    state = dialog_state.get(user_id)
    if not state:
        state = {"history": [], "stage": "start"}
    state["history"].append({"role": "user", "text": user_message})
    stage = state["stage"]

    rag = RAGAgent(data_folder=DATA_PATH)
    facts = await rag.search(user_message, user_lang)

    try:
        results, metadatas = semsearch.search(user_message)
        article_id = metadatas[0]['article_id'] if metadatas else None
        graph_logic = graph_agent.explain(article_id) if article_id else "—"
    except Exception as e:
        article_id = None
        graph_logic = f"[Ошибка Semantic Search: {str(e)}]"

    context_block = f"{facts}\n\n[🔍 Логика по закону:]\n{graph_logic}" if facts else "—"

    tactics = TacticsAgent()
    tactics_suggestion = await tactics.suggest(user_message, user_lang)

    history_block = "\n".join([f"{m['role']}: {m['text']}" for m in state["history"][-20:]])

    prompt = SUPERLAWYER_PROMPT.format(
        context_block=context_block,
        history_block=history_block,
        user_message=user_message,
        stage=stage
    )

    answer = await call_gpt(prompt)

    if f"Переходим к этапу: {get_next_stage(stage)}" in answer:
        state["stage"] = get_next_stage(stage)
    state["history"].append({"role": "bot", "text": answer})
    dialog_state[user_id] = state

    if "====" in answer:
        main_answer, questions_block = answer.split("====", 1)
        main_answer, questions_block = main_answer.strip(), questions_block.strip()
    else:
        main_answer, questions_block = answer.strip(), None

    return {
        "answer": main_answer,
        "questions": questions_block,
        "facts": facts,
        "tactics": tactics_suggestion,
        "user_lang": user_lang
    }
