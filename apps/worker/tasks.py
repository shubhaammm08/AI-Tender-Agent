from celery_app import celery_app
import pandas as pd
import io
import uuid

@celery_app.task
def classify_file(file_key: str):
    """
    Mock classification.
    Returns one of: NIT, BOQ, GCC, SCC, annexure, corrigendum
    """
    if "boq" in file_key.lower():
        return "BOQ"
    elif "nit" in file_key.lower():
        return "NIT"
    return "annexure"

@celery_app.task
def ocr_document(file_key: str):
    """
    Mock OCR.
    Extracts text with page and table layout.
    """
    return [
        {"page": 1, "text": "This is page 1 content of the document.", "tables": []},
        {"page": 2, "text": "Clause 3.1: Turnover must be > 50L.", "tables": []}
    ]

@celery_app.task
def parse_boq(file_content_bytes: bytes):
    """
    Parse BOQ Excel using pandas.
    """
    df = pd.read_excel(io.BytesIO(file_content_bytes))
    return df.to_dict(orient="records")

@celery_app.task
def chunk_and_embed(text: str):
    """
    Mock chunking and embedding.
    """
    # Create chunks
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    
    # Mock embeddings (size 1536)
    embeddings = []
    for _ in chunks:
        embeddings.append([0.01] * 1536)
        
    return list(zip(chunks, embeddings))

@celery_app.task
def process_tender_file(tender_id: str, file_key: str, file_content_bytes: bytes):
    """
    The full pipeline for a file.
    """
    doc_class = classify_file(file_key)
    
    if doc_class == "BOQ":
        # Parse BOQ
        parsed_boq = parse_boq(file_content_bytes)
        # Store in db or process further
    else:
        # OCR
        ocr_pages = ocr_document(file_key)
        for page_data in ocr_pages:
            chunks = chunk_and_embed(page_data["text"])
            # Save to db using TenderChunk (mocked here, we would use a DB session)
            for chunk_text, embedding in chunks:
                pass # db.add(TenderChunk(tender_id=..., file_key=..., text=..., embedding=...))
                
    return {"status": "success", "class": doc_class}

@celery_app.task
def process_reminders():
    """
    Cron job to sweep the database for upcoming document expiries
    and tender closing dates to send reminders.
    """
    # This would open a DB session, find documents expiring in < 30 days
    # and send alerts (via email/whatsapp integration)
    # Then it would find Reminders where due_at is approaching and sent_at is None
    # Update sent_at to current timestamp.
    print("Sweeping database for reminders and document expiries...")
    return {"status": "success", "alerts_sent": 5}
