import os
import re
import json

DATA_FOLDER = r"C:\Users\kamst\OneDrive\Рабочий стол\app\data\7 главных законов\חוק הגנת השכר\узлы"

nodes = set()
edges = []
processed_files = 0

for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".md"):
        path = os.path.join(DATA_FOLDER, filename)
        try:
            with open(path, encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"[Ошибка] Не удалось прочитать файл {filename}: {e}")
            continue

        # Извлекаем основной ID
        match = re.search(r'ID:\s*(\S+)', content)
        if not match:
            print(f"[Пропущен] Не найден ID в файле {filename}")
            continue
        main_id = match.group(1)
        nodes.add(main_id)

        # Извлекаем связи
        edge_matches = re.findall(
            r'\{\s*from:\s*[\'"]([^\'"]+)[\'"],\s*to:\s*[\'"]([^\'"]+)[\'"],\s*type:\s*[\'"]([^\'"]+)[\'"],\s*description:\s*[\'"]([^\'"]+)[\'"]\s*\}',
            content
        )
        for source, target, rel_type, description in edge_matches:
            nodes.add(target)
            edges.append({
                "source": source,
                "target": target,
                "type": rel_type,
                "description": description
            })

        print(f"[OK] Обработан файл: {filename}")
        processed_files += 1

print(f"\nОбработано файлов: {processed_files}")
print(f"Узлов: {len(nodes)}, Связей: {len(edges)}")

if processed_files > 0 and len(nodes) > 0:
    graph = {
        "nodes": [{"id": node, "label": node} for node in sorted(nodes)],
        "edges": edges
    }

    output_path = os.path.join(DATA_FOLDER, "graph.json")
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(graph, out, ensure_ascii=False, indent=2)

    print(f"\n✅ Файл graph.json сохранён в:\n{output_path}")
else:
    print("\n⚠️ Нет данных для сохранения. Проверь содержимое файлов.")