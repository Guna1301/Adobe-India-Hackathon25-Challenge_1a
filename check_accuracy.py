# import json
# import os

# def load_json(filepath):
#     with open(filepath, "r", encoding="utf-8") as f:
#         return json.load(f)

# def tokenize(text):
#     return text.strip().lower().split()

# def compare_titles(expected, actual):
#     return 1.0 if tokenize(expected) == tokenize(actual) else 0.0

# def compare_outlines(expected_outline, actual_outline):
#     if not expected_outline and not actual_outline:
#         return 1.0  
#     if not expected_outline or not actual_outline:
#         return 0.0

#     correct = 0
#     for expected, actual in zip(expected_outline, actual_outline):
#         expected_text = tokenize(expected.get("text", ""))
#         actual_text = tokenize(actual.get("text", ""))

#         if (
#             expected.get("level") == actual.get("level") and
#             expected.get("page") == actual.get("page") and
#             expected_text == actual_text
#         ):
#             correct += 1

#     return correct / len(expected_outline)


# def evaluate_accuracy(expected_file, actual_file):
#     expected_data = load_json(expected_file)
#     actual_data = load_json(actual_file)

#     title_accuracy = compare_titles(expected_data.get("title", ""), actual_data.get("title", ""))
#     outline_accuracy = compare_outlines(expected_data.get("outline", []), actual_data.get("outline", []))
#     overall_accuracy = (title_accuracy * 0.2) + (outline_accuracy * 0.8)

#     return {
#         "file": os.path.basename(expected_file),
#         "title_accuracy": round(title_accuracy * 100, 2),
#         "outline_accuracy": round(outline_accuracy * 100, 2),
#         "overall_accuracy": round(overall_accuracy * 100, 2)
#     }

# def evaluate_folder(expected_dir, actual_dir):
#     results = []
#     total = {"title": 0.0, "outline": 0.0, "overall": 0.0}
#     count = 0

#     for filename in os.listdir(actual_dir):
#         if not filename.endswith(".json"):
#             continue
#         name = filename[:-5]  # remove '.json'
#         expected_path = os.path.join(expected_dir, name + "expected.json")
#         actual_path = os.path.join(actual_dir, filename)

#         if os.path.exists(expected_path):
#             result = evaluate_accuracy(expected_path, actual_path)
#             results.append(result)
#             total["title"] += result["title_accuracy"]
#             total["outline"] += result["outline_accuracy"]
#             total["overall"] += result["overall_accuracy"]
#             count += 1
#         else:
#             print(f"[!] Missing expected file for: {name}")

#     print("\nPer File Accuracy:")
#     for r in results:
#         print(f"{r['file']}: Title = {r['title_accuracy']}%, Outline = {r['outline_accuracy']}%, Overall = {r['overall_accuracy']}%")

#     if count > 0:
#         print("\n Average Accuracy:")
#         print(f"Title Accuracy:   {round(total['title'] / count, 2)}%")
#         print(f"Outline Accuracy: {round(total['outline'] / count, 2)}%")
#         print(f"Overall Accuracy: {round(total['overall'] / count, 2)}%")
#     else:
#         print("❌ No comparisons made.")

# if __name__ == "__main__":
#     expected_dir = "expectedoutputs"
#     actual_dir = "output"
#     evaluate_folder(expected_dir, actual_dir)
import os
import json

def normalize_text(text):
    return " ".join(text.strip().lower().split())  # normalize spaces and case

def headings_match(h1, h2):
    # Strict match: compare normalized text, page, and exact level
    return (
        normalize_text(h1['text']) == normalize_text(h2['text']) and
        (h1['page'] == h2['page'] or h1['page'] == h2['page'] - 1) and
        h1['level'] == h2['level']
    )

def evaluate_jsons(expected_json, executed_json):
    # Title matching (exact normalized)
    title_match = normalize_text(expected_json.get('title', '')) == normalize_text(executed_json.get('title', ''))

    TP_title = 1 if title_match else 0
    FP_title = 0 if title_match else 1
    FN_title = 0 if title_match else 1

    expected_outline = expected_json.get('outline', [])
    executed_outline = executed_json.get('outline', [])

    matched = set()
    TP_outline = 0
    for e_head in expected_outline:
        found_match = False
        for i, a_head in enumerate(executed_outline):
            if i in matched:
                continue
            if headings_match(e_head, a_head):
                TP_outline += 1
                matched.add(i)
                found_match = True
                break
    FP_outline = len(executed_outline) - TP_outline
    FN_outline = len(expected_outline) - TP_outline

    def safe_div(num, denom):
        return num / denom if denom > 0 else 0.0

    precision_title = safe_div(TP_title, TP_title + FP_title) * 100
    recall_title = safe_div(TP_title, TP_title + FN_title) * 100
    f1_title = safe_div(2 * precision_title * recall_title, precision_title + recall_title) if (precision_title + recall_title) > 0 else 0

    if not expected_outline and not executed_outline:
        precision_outline = recall_outline = f1_outline = 100.0
    elif expected_outline and not executed_outline:
        precision_outline = 0.0
        recall_outline = 0.0
        f1_outline = 0.0
    else:
        precision_outline = safe_div(TP_outline, TP_outline + FP_outline) * 100
        recall_outline = safe_div(TP_outline, TP_outline + FN_outline) * 100
        f1_outline = safe_div(2 * precision_outline * recall_outline, precision_outline + recall_outline) if (precision_outline + recall_outline) > 0 else 0

    overall_precision = 0.25 * precision_title + 0.75 * precision_outline
    overall_recall = 0.25 * recall_title + 0.75 * recall_outline
    overall_f1 = 0.25 * f1_title + 0.75 * f1_outline

    return {
        'title_precision': round(precision_title, 2),
        'title_recall': round(recall_title, 2),
        'title_f1': round(f1_title, 2),
        'outline_precision': round(precision_outline, 2),
        'outline_recall': round(recall_outline, 2),
        'outline_f1': round(f1_outline, 2),
        'overall_precision': round(overall_precision, 2),
        'overall_recall': round(overall_recall, 2),
        'overall_f1': round(overall_f1, 2),
    }

def evaluate_folder(expected_dir, executed_dir):
    results = []
    totals = {
        "title_precision": 0.0, "title_recall": 0.0, "title_f1": 0.0,
        "outline_precision": 0.0, "outline_recall": 0.0, "outline_f1": 0.0,
        "overall_precision": 0.0, "overall_recall": 0.0, "overall_f1": 0.0,
    }
    count = 0

    for filename in os.listdir(executed_dir):
        if not filename.endswith(".json"):
            continue
        expected_path = os.path.join(expected_dir, filename)
        executed_path = os.path.join(executed_dir, filename)
        if not os.path.exists(expected_path):
            print(f"[!] Missing expected file: {filename}")
            continue

        with open(expected_path, "r", encoding="utf-8") as f:
            expected_json = json.load(f)
        with open(executed_path, "r", encoding="utf-8") as f:
            executed_json = json.load(f)

        scores = evaluate_jsons(expected_json, executed_json)
        scores['file'] = filename
        results.append(scores)

        for k in totals:
            totals[k] += scores[k]
        count += 1

    # Print per-file scores
    print("Per file evaluation:")
    for r in results:
        print(f"{r['file']}:")
        print(f"  Title - Precision: {r['title_precision']}%, Recall: {r['title_recall']}%, F1: {r['title_f1']}%")
        print(f"  Outline - Precision: {r['outline_precision']}%, Recall: {r['outline_recall']}%, F1: {r['outline_f1']}%")
        print(f"  Overall - Precision: {r['overall_precision']}%, Recall: {r['overall_recall']}%, F1: {r['overall_f1']}%")
        print()

    if count > 0:
        print("Average scores:")
        for k in totals:
            avg = totals[k] / count
            print(f"  {k.replace('_', ' ').title()}: {avg:.2f}%")
    else:
        print("No matching files found.")

if __name__ == "__main__":

    expected_dir = "expectedoutputs"
    executed_dir = "output"
    evaluate_folder(expected_dir, executed_dir)