import json
import os

class GraphAgent:
    def __init__(self, graph_path):
        with open(graph_path, encoding="utf-8") as f:
            data = json.load(f)
        self.nodes = {n["id"]: n for n in data["nodes"]}
        self.edges = data["edges"]

    def get_outgoing(self, node_id):
        return [
            edge for edge in self.edges
            if edge["source"] == node_id
        ]

    def get_incoming(self, node_id):
        return [
            edge for edge in self.edges
            if edge["target"] == node_id
        ]

    def explain_chain(self, start_id, depth=2, visited=None, level=0):
        if visited is None:
            visited = set()
        if start_id not in self.nodes:
            return [f"❗ Узел `{start_id}` не найден."]

        visited.add(start_id)
        lines = []
        indent = "    " * level
        prefix = "🔸" if level == 0 else "→"

        if level == 0:
            lines.append(f"📌 **Анализ статьи:** `{start_id}`")

        for edge in self.get_outgoing(start_id):
            target = edge["target"]
            if target in visited:
                continue
            lines.append(f"{indent}{prefix} `{start_id}` → `{target}` **({edge['type']})** — {edge['description']}")
            if level + 1 < depth:
                lines.extend(self.explain_chain(target, depth, visited, level + 1))

        for edge in self.get_incoming(start_id):
            source = edge["source"]
            if source in visited:
                continue
            lines.append(f"{indent}{prefix} `{source}` → `{start_id}` **({edge['type']})** — {edge['description']}")
            if level + 1 < depth:
                lines.extend(self.explain_chain(source, depth, visited, level + 1))

        return lines

    def explain(self, node_id, depth=2):
        result = self.explain_chain(node_id, depth=depth)
        return "\n".join(result)


# Пример запуска
if __name__ == "__main__":
    GRAPH_PATH = r"C:\Users\kamst\OneDrive\Рабочий стол\app\data\7 главных законов\חוק הגנת השכר\узлы\graph.json"
    agent = GraphAgent(GRAPH_PATH)

    explanation = agent.explain("wage_law_art_11", depth=2)
    print(explanation)
