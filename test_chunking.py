import sys
from unittest.mock import MagicMock

# Mock SentenceTransformer to avoid loading the heavy model during tests
mock_sentence_transformers = MagicMock()
sys.modules['sentence_transformers'] = mock_sentence_transformers

# Mock other dependencies that are not available in the environment
sys.modules['fitz'] = MagicMock()
sys.modules['asyncpg'] = MagicMock()
sys.modules['dotenv'] = MagicMock()

from chunking import chunk_text, clean_text

def test_clean_text_null_bytes():
    text = "Hello\0World"
    assert clean_text(text) == "HelloWorld"

def test_clean_text_control_characters():
    # \x01 is a control character, \n and \t should be preserved
    text = "Line 1\n\tLine 2\x01"
    assert clean_text(text) == "Line 1\n\tLine 2"

def test_clean_text_stripping():
    text = "  spaced text  "
    assert clean_text(text) == "spaced text"

def test_chunk_text_basic():
    # Using a larger string to bypass the 50 char filter
    # Text length 300, chunk_size 100, overlap 20
    # 1. 0:100 (len 100) -> next start 80
    # 2. 80:180 (len 100) -> next start 160
    # 3. 160:260 (len 100) -> next start 240
    # 4. 240:300 (len 60) -> next start 280
    # 5. 280:300 (len 20) -> filtered out (< 50)
    text = "a" * 300
    chunks = chunk_text(text, chunk_size=100, overlap=20)

    assert len(chunks) == 4
    assert len(chunks[0]) == 100
    assert len(chunks[1]) == 100
    assert len(chunks[2]) == 100
    assert len(chunks[3]) == 60
    for c in chunks:
        assert len(c) > 50

def test_chunk_text_overlap():
    text = "0123456789" * 20 # 200 chars
    chunk_size = 100
    overlap = 20
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

    # Chunk 1 ends at 100
    # Chunk 2 starts at 100-20 = 80
    assert chunks[1].startswith(chunks[0][-20:])

def test_chunk_text_breakpoint_period():
    # Breakpoint logic:
    # if break_point > chunk_size * 0.5:
    #     chunk = chunk[:break_point + 1]
    #     end = start + break_point + 1

    chunk_size = 100
    # Create a string where there is a period at index 80
    # "a" * 80 + "." + "b" * 40
    text = "a" * 80 + "." + "b" * 120 # 201 chars
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=20)

    # First chunk should end at the period (index 80 in text, but it's 81 chars long including .)
    assert chunks[0] == "a" * 80 + "."
    assert len(chunks[0]) == 81

def test_chunk_text_breakpoint_newline():
    chunk_size = 100
    # Create a string where there is a newline at index 90
    text = "a" * 90 + "\n" + "b" * 110 # 201 chars
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=20)

    # First chunk should end at the newline
    assert chunks[0] == "a" * 90
    assert len(chunks[0]) == 90 # strip() is called on chunks

def test_chunk_text_no_breakpoint_in_second_half():
    chunk_size = 100
    # Period at index 40 (first half), no other breakpoints
    text = "a" * 40 + "." + "b" * 160
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=20)

    # Should split exactly at chunk_size because breakpoint 40 <= 100 * 0.5
    assert len(chunks[0]) == 100
    assert chunks[0] == "a" * 40 + "." + "b" * 59

def test_chunk_text_min_length_filter():
    # Chunks <= 50 should be filtered
    text = "a" * 50 # length 50
    chunks = chunk_text(text, chunk_size=100)
    assert len(chunks) == 0

    text = "a" * 51 # length 51
    chunks = chunk_text(text, chunk_size=100)
    assert len(chunks) == 1
    assert chunks[0] == "a" * 51

def test_chunk_text_empty_input():
    assert chunk_text("") == []
