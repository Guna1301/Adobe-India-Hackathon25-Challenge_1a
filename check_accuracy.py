import json
import os

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def tokenize(text):
    return text.strip().lower().split()

def compare_titles(expected, actual):
    return 1.0 if tokenize(expected) == tokenize(actual) else 0.0

def compare_outlines(expected_outline, actual_outline):
    if not expected_outline and not actual_outline:
        return 1.0  
    if not expected_outline or not actual_outline:
        return 0.0

    correct = 0
    for expected, actual in zip(expected_outline, actual_outline):
        expected_text = tokenize(expected.get("text", ""))
        actual_text = tokenize(actual.get("text", ""))

        if (
            expected.get("level") == actual.get("level") and
            expected.get("page") == actual.get("page") and
            expected_text == actual_text
        ):
            correct += 1

    return correct / len(expected_outline)


def evaluate_accuracy(expected_file, actual_file):
    expected_data = load_json(expected_file)
    actual_data = load_json(actual_file)

    title_accuracy = compare_titles(expected_data.get("title", ""), actual_data.get("title", ""))
    outline_accuracy = compare_outlines(expected_data.get("outline", []), actual_data.get("outline", []))
    overall_accuracy = (title_accuracy * 0.2) + (outline_accuracy * 0.8)

    return {
        "file": os.path.basename(expected_file),
        "title_accuracy": round(title_accuracy * 100, 2),
        "outline_accuracy": round(outline_accuracy * 100, 2),
        "overall_accuracy": round(overall_accuracy * 100, 2)
    }

def evaluate_folder(expected_dir, actual_dir):
    results = []
    total = {"title": 0.0, "outline": 0.0, "overall": 0.0}
    count = 0

    for filename in os.listdir(actual_dir):
        if not filename.endswith(".json"):
            continue
        name = filename[:-5]  # remove '.json'
        expected_path = os.path.join(expected_dir, name + "expected.json")
        actual_path = os.path.join(actual_dir, filename)

        if os.path.exists(expected_path):
            result = evaluate_accuracy(expected_path, actual_path)
            results.append(result)
            total["title"] += result["title_accuracy"]
            total["outline"] += result["outline_accuracy"]
            total["overall"] += result["overall_accuracy"]
            count += 1
        else:
            print(f"[!] Missing expected file for: {name}")

    print("\nPer File Accuracy:")
    for r in results:
        print(f"{r['file']}: Title = {r['title_accuracy']}%, Outline = {r['outline_accuracy']}%, Overall = {r['overall_accuracy']}%")

    if count > 0:
        print("\n Average Accuracy:")
        print(f"Title Accuracy:   {round(total['title'] / count, 2)}%")
        print(f"Outline Accuracy: {round(total['outline'] / count, 2)}%")
        print(f"Overall Accuracy: {round(total['overall'] / count, 2)}%")
    else:
        print("❌ No comparisons made.")

if __name__ == "__main__":
    expected_dir = "expectedoutputs"
    actual_dir = "output"
    evaluate_folder(expected_dir, actual_dir)
