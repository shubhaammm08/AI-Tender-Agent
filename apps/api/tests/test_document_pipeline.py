import pytest
from apps.worker.tasks import classify_file, chunk_and_embed

def test_file_classification():
    assert classify_file("NIT_document.pdf") == "NIT"
    assert classify_file("tender_boq.xlsx") == "BOQ"
    assert classify_file("some_other_file.docx") == "annexure"

def test_chunk_and_embed():
    text = "This is a long text " * 100
    chunks_with_embeddings = chunk_and_embed(text)
    
    assert len(chunks_with_embeddings) > 0
    chunk, embedding = chunks_with_embeddings[0]
    
    assert isinstance(chunk, str)
    assert len(embedding) == 1536
