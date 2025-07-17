import pdfplumber
import re
import json
import sys
from collections import defaultdict

def extract_s3_features(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Patterns to filter out unwanted lines (footers, API versions, etc.)
    skip_patterns = [
        re.compile(r"^.*API Version.*$", re.IGNORECASE),
        re.compile(r"^Page\s+\d+$", re.IGNORECASE),
        re.compile(r"^Amazon Simple Storage Service User Guide$", re.IGNORECASE),
        re.compile(r"^Features of Amazon S3.*$", re.IGNORECASE)
    ]

    output = {"Features of Amazon S3": []}
    section_pattern = re.compile(r"^(Storage management|Access management and security)$", re.IGNORECASE)
    bullet_pattern = re.compile(r"^•\s*(.+?)\s*–\s*(.+)")

    current_section = None
    current_feature = None
    features_map = defaultdict(list)

    for line in lines:
        # Skip unwanted lines (footers, repeated titles, version lines)
        if any(p.match(line) for p in skip_patterns):
            continue

        section_match = section_pattern.match(line)
        if section_match:
            if current_feature and current_section:
                features_map[current_section].append(current_feature)
            current_section = section_match.group(1)
            current_feature = None
            continue

        bullet_match = bullet_pattern.match(line)
        if bullet_match and current_section:
            if current_feature:
                features_map[current_section].append(current_feature)

            current_feature = {
                "sub_heading": bullet_match.group(1).strip(),
                "description": bullet_match.group(2).strip()
            }
        elif current_feature:
            current_feature["description"] += " " + line.strip()

    if current_feature and current_section:
        features_map[current_section].append(current_feature)

    for heading, features in features_map.items():
        output["Features of Amazon S3"].append({
            "heading": heading,
            "features": features
        })

    return output



def save_to_json(data, output_file="s3_features_output.json"):
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

def main(pdf_path):
    data = extract_s3_features(pdf_path)
    save_to_json(data)
    print("✅ Extracted features saved to s3_features_output.json")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python s3_feature_parser/main.py path/to/pdf")
        sys.exit(1)
    main(sys.argv[1])