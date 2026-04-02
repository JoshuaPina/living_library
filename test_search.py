import asyncio
import asyncpg
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer
import argparse
import sys

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print(
        "ERROR: DATABASE_URL is not set. Copy .env.example to .env and set DATABASE_URL before running test_search.py."
    )
    sys.exit(1)

if DATABASE_URL.startswith("postgresql+asyncpg://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

model = SentenceTransformer('all-MiniLM-L6-v2')

async def test(query: str, limit: int):
    conn = await asyncpg.connect(DATABASE_URL)

    embedding = model.encode(query).tolist()
    embedding_str = '[' + ','.join(map(str, embedding)) + ']'
    
    results = await conn.fetch("""
        SELECT 
            tc.chunk_id,
            m.material_id,
            m.title,
            tc.page_number,
            tc.chunk_text,
            1 - (ce.embedding <=> $1::vector) AS similarity
        FROM chunk_embedding ce
        JOIN text_chunk tc ON tc.chunk_id = ce.chunk_id
        JOIN file_asset fa ON fa.file_id = tc.file_id
        JOIN material m ON m.material_id = fa.material_id
        ORDER BY ce.embedding <=> $1::vector
        LIMIT $2
    """, embedding_str, limit)

    if not results:
        print(f"No results found for query: {query}")
    
    for r in results:
        print(f"{r['title'][:50]} - Page {r['page_number']} - Similarity: {r['similarity']:.3f}")

    await conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run semantic search probe against chunk embeddings")
    parser.add_argument("--query", default="machine learning", help="Search query string")
    parser.add_argument("--limit", type=int, default=5, help="Number of results to return")
    args = parser.parse_args()

    asyncio.run(test(args.query, args.limit))


if __name__ == "__main__":
    main()
