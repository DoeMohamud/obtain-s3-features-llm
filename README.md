# Amazon S3 Feature Parser

This project parses an Amazon S3 User Guide PDF and extracts feature headings, subheadings, and descriptions, then outputs the results to a structured JSON file.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python s3_feature_parser/main.py path/to/your.pdf
```

## Testing

```bash
pytest
```