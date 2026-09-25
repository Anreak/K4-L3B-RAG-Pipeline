"""
Task 8 — PageIndex vectorless fallback.

Hướng dẫn:
    1. Đọc PAGEINDEX_API_KEY từ .env.
    2. Upload tài liệu ở định dạng PageIndex hỗ trợ.
    3. Cache document IDs để không upload lại.
    4. Parse kết quả thành SearchResult có method pageindex.

PageIndex là dịch vụ ngoài: cần timeout và xử lý lỗi để pipeline không crash.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"


DOC_IDS_FILE = Path(__file__).parent.parent / "pageindex_doc_ids.json"


def upload_documents() -> None:
    """Upload tài liệu và lưu document IDs để tái sử dụng."""
    if not PAGEINDEX_API_KEY:
        print("PAGEINDEX_API_KEY is not set.")
        return

    from pageindex import PageIndexClient
    client = PageIndexClient(api_key=PAGEINDEX_API_KEY)
    doc_ids = {}
    landing_legal = Path(__file__).parent.parent / "data" / "landing" / "legal"
    for pdf_path in landing_legal.glob("*.pdf"):
        try:
            res = client.submit_document(file_path=str(pdf_path))
            if "doc_id" in res:
                doc_ids[pdf_path.name] = res["doc_id"]
                print(f"Uploaded {pdf_path.name}: {res['doc_id']}")
        except Exception as e:
            print(f"Failed to upload {pdf_path.name}: {e}")

    DOC_IDS_FILE.write_text(json.dumps(doc_ids, indent=2), encoding="utf-8")


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """Trả về pageindex SearchResult."""
    if not PAGEINDEX_API_KEY:
        return []

    import json
    from pageindex import PageIndexClient
    client = PageIndexClient(api_key=PAGEINDEX_API_KEY)

    doc_ids = {}
    if DOC_IDS_FILE.exists():
        try:
            doc_ids = json.loads(DOC_IDS_FILE.read_text(encoding="utf-8"))
        except Exception:
            doc_ids = {}

    results = []
    rank = 1
    for source_name, doc_id in doc_ids.items():
        try:
            sub = client.submit_query(doc_id=doc_id, query=query)
            ret_id = sub.get("retrieval_id")
            if not ret_id:
                continue
            ret = client.get_retrieval(retrieval_id=ret_id)
            nodes = ret.get("nodes", []) or ret.get("results", [])
            for node in nodes:
                results.append({
                    "id": f"pageindex::{doc_id}::{rank}",
                    "content": node.get("content", str(node)),
                    "score": float(1.0 / (rank + 1)),
                    "metadata": {
                        "source": source_name,
                        "title": source_name,
                        "doc_type": "legal",
                        "url": None,
                        "chunk_index": rank,
                    },
                    "retrieval_method": "pageindex",
                })
                rank += 1
                if len(results) >= top_k:
                    break
        except Exception as e:
            print(f"PageIndex error for {doc_id}: {e}")

    return sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]


if __name__ == "__main__":
    upload_documents()
