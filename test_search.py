import asyncio
import asyncpg
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer
import argparse
import sys

load_dotenv()

__test__ = False


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy .env.example to .env and set DATABASE_URL before running test_search.py."
        )

    if database_url.startswith("postgresql+asyncpg://"):
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")

    return database_url


def load_model() -> SentenceTransformer:
    return SentenceTransformer('all-MiniLM-L6-v2')

async def test(query: str, limit: int):
    conn = await asyncpg.connect(get_database_url())

    model = load_model()

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

    try:
        asyncio.run(test(args.query, args.limit))
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
