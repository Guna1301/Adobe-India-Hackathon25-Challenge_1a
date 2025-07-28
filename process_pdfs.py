import os
from pdf_loader import extract_text_blocks
from title_detector import detect_title
from heading_extractor import extract_heading_candidates
from heading_classifier import classify_headings
from json_writer import write_json
from check_accuracy import evaluate_folder
def process_pdf(pdf_path, output_path):
    blocks = extract_text_blocks(pdf_path)
    title = detect_title(blocks)
    candidates = extract_heading_candidates(blocks)
    outline = classify_headings(candidates)
    # expected_dir = "expectedoutputs"
    # executed_dir = "app/output"
    # evaluate_folder(expected_dir, executed_dir)
    write_json(output_path, title, outline)

def main():
    input_dir = os.path.join(os.getcwd(), "input")
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_filename = filename.replace(".pdf", ".json")
            output_path = os.path.join(output_dir, output_filename)

            print(f"Processing: {filename}")
            process_pdf(input_path, output_path)

if __name__ == "__main__":
    main()