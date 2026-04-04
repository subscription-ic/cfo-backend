import os
from pathlib import Path
import pandas as pd
from pypdf import PdfReader

# The script's directory (app/processing/chunks)
SCRIPT_DIR = Path(__file__).parent.resolve()

# Root of the app folder
APP_DIR = SCRIPT_DIR.parent.parent

# Input directory for the transcripts
INPUT_DIR = APP_DIR / "input" / "files" / "transcripts"

# Output directory for the page chunks
OUTPUT_DIR = APP_DIR / "output" / "structured" / "page_chunks"

def process_pdf(pdf_path):
    print(f"Processing {pdf_path.name}...")
    try:
        reader = PdfReader(pdf_path)
        data = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text is None:
                text = ""
            else:
                text = text.strip()
            
            data.append({
                "pdf name": pdf_path.name,
                "page number": i + 1,
                "content": text
            })
        
        if data:
            df = pd.DataFrame(data)
            # Ensure output directory exists before saving
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            
            # Export to an excel workbook saved in the required output directory
            output_filename = f"{pdf_path.stem}_chunked.xlsx"
            output_path = OUTPUT_DIR / output_filename
            df.to_excel(output_path, index=False)
            print(f"Successfully saved chunks to {output_path}")
        else:
            print(f"No text extracted from {pdf_path.name}.")
            
    except Exception as e:
        print(f"Error processing {pdf_path.name}: {e}")

def main():
    if not INPUT_DIR.exists():
        print(f"Input directory does not exist: {INPUT_DIR}")
        print("Creating directory now...")
        INPUT_DIR.mkdir(parents=True, exist_ok=True)
        print("Please add PDF files to this directory and run the script again.")
        return

    # Find all PDFs in the input transcript directory (case insensitive)
    pdf_files = list(INPUT_DIR.glob("*.[pP][dD][fF]"))
    if not pdf_files:
        print(f"No PDF files found in {INPUT_DIR}")
        return
        
    for pdf_path in pdf_files:
        process_pdf(pdf_path)

if __name__ == "__main__":
    main()
