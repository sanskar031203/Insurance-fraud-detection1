import pdfplumber
import re

def extract_invoice_details():
    items = []
    pdf_path = 'pdf.pdf'
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            
            # Use regular expression to match item details
            # The PDF provided has lines like: ItemName Quantity UnitPrice TotalPrice
            pattern = re.compile(r"(\w+)\s+(\d+)\s+\w+\s+(\d+\.\d{2})\s+(\d+\.\d{2})")
            
            for line in text.split('\n'):
                match = pattern.search(line)
                if match:
                    item_name = match.group(1)
                    quantity = int(match.group(2))
                    price = float(match.group(3))
                    
                    items.append({
                        'item_name': item_name,
                        'quantity': quantity,
                        'rate': price
                    })
                    
    return 'allegra-m tablet'


