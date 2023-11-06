import pdfplumber
import pandas as pd
from pypdf import PdfReader

# Task1:
def extract_text_and_tables(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        all_data = []
        
        for page in pdf.pages:
            text = page.extract_text()
            tables = page.extract_tables()

            if text:
                # Table settings.
                ts = {
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines",
                }

                # Get the bounding boxes of the tables on the page.
                bboxes = [table.bbox for table in page.find_tables(table_settings=ts)]

                def not_within_bboxes(obj):
                    # """Check if the object is in any of the table's bbox."""
                    def obj_in_bbox(_bbox):
                        # """See https://github.com/jsvine/pdfplumber/blob/stable/pdfplumber/table.py#L404"""
                        v_mid = (obj["top"] + obj["bottom"]) / 2
                        h_mid = (obj["x0"] + obj["x1"]) / 2
                        x0, top, x1, bottom = _bbox
                        return (h_mid >= x0) and (h_mid < x1) and (v_mid >= top) and (v_mid < bottom)
                    return not any(obj_in_bbox(__bbox) for __bbox in bboxes)
                
                text = page.filter(not_within_bboxes).extract_text()
                
                all_data.append({'page_number': page.page_number, 'text': text})

            if tables:
                for table in tables:
                    all_data.append({'page_number': page.page_number, 'table': table})

    return all_data

# Task2: Use this code to extract images
def extract_images(pdf_file):
    reader = PdfReader(pdf_file)
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        if page:
            for im in page.images:
                with open(im.name, "wb") as f:
                    f.write(im.data)

# # Replace 'your_pdf_file.pdf' with the path to your PDF file
pdf_file = "CSMVol2_PaxService (1).pdf"
data = extract_text_and_tables(pdf_file)
# Task2:
images = extract_images(pdf_file)

# @Mohan you can use this section to add vectorsore here
for entry in data:
    page_number = entry['page_number']
    if 'text' in entry:
        print(f"Text from page {page_number}:\n{entry['text']}\n")
    if 'table' in entry:
        print(f"Table from page {page_number}:\n")
        df = pd.DataFrame(entry['table'][1:], columns=entry['table'][0])
        df = df.dropna(axis=1, how='all')
        df = df.reset_index(drop=True)
        print(df.head())
