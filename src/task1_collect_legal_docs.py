"""
Task 1 — Thu thập tài liệu chính sách/quy định.

Hướng dẫn:
    1. Chọn chủ đề của nhóm.
    2. Tìm tối thiểu 3 tài liệu PDF/DOCX từ nguồn công khai.
    3. Lưu file gốc vào data/landing/legal/.
    4. Đặt tên không dấu và thể hiện đúng nội dung.

Ví dụ tài liệu: học phí, học bổng, ký túc xá, quy trình đăng ký.
Nếu website chặn crawler, hãy chọn nguồn công khai khác; không vượt WAF.
"""

from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"


def setup_directory() -> None:
    """Tạo thư mục lưu tài liệu gốc."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Ready: {DATA_DIR}")


def download_documents() -> None:
    """Tải ít nhất 3 PDF/DOCX từ nguồn công khai."""

    import requests

    sources = {
        "policy-a.pdf": "https://cdn.thuvienphapluat.vn/uploads/khoinghiep/2026/03/10/so-tay-huong-dan.pdf",
        "policy-b.docx": "https://docs.google.com/document/d/1U_QwGL75Qp59TPCtsCUKLXYWgO1_mr-W/export?format=docx",
        "policy-c.docx": "https://docs.google.com/document/d/1qT4pTbaVPcv4FlKEerIThXiMN3b2PhgC/export?format=docx",
    }
    for filename, url in sources.items():
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        (DATA_DIR / filename).write_bytes(response.content)


if __name__ == "__main__":
    setup_directory()
    download_documents()
