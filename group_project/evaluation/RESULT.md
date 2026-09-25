# RAG evaluation results

## Run information

| Field                              | Value |
| ---------------------------------- | ----- |
| Evaluation date                    | 2026-09-25 |
| Framework and version              | Ragas 0.4.3, ChromaDB 0.5.0, Python 3.12 |
| Evaluator model                    | GPT-4o-mini / Automated Metric Benchmark |
| Generator model                    | GPT-4o-mini / Gemini-2.0-Flash |
| Embedding model                    | sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 |
| Corpus version/commit              | e001647 |
| Golden dataset size                | 16 ground-truth Q&A pairs |
| `top_k`                            | 5 |
| Fallback threshold and calibration | 0.30 (In-domain score 0.35-0.70; Out-of-domain score < 0.28) |

## Configurations

- **Config A — dense-only:** Truy xuất ngữ nghĩa thuần túy (Dense retrieval) bằng ChromaDB dựa trên vector embedding của mô hình `paraphrase-multilingual-MiniLM-L12-v2`, lấy top 5 kết quả có cosine similarity cao nhất.
- **Config B — hybrid + RRF:** Kết hợp song song Dense Search (top 10) và Lexical Search BM25 (top 10), sau đó chuẩn hóa thứ hạng và gộp danh sách bằng thuật toán Reciprocal Rank Fusion (RRF) với hằng số làm mịn k=60, lấy top 5 kết quả tối ưu.

Hai config sử dụng cùng bộ dữ liệu chuẩn hóa, prompt template, model generator và tham số `top_k=5`.

## Overall scores

| Metric            | Config A (Dense-only) | Config B (Hybrid + RRF) | Delta B−A |
| ----------------- | --------------------: | ----------------------: | --------: |
| Faithfulness      |                  0.82 |                    0.89 |     +0.07 |
| Answer relevance  |                  0.80 |                    0.88 |     +0.08 |
| Context recall    |                 0.602 |                   0.692 |    +0.090 |
| Context precision |                 0.677 |                   0.822 |    +0.145 |
| **Average**       |             **0.725** |               **0.821** | **+0.096** |

## A/B comparison

- **Cấu hình tốt hơn:** Config B (Hybrid + RRF) vượt trội rõ rệt trên tất cả các chỉ số đo lường, đặc biệt là Context Precision tăng 14.5% (từ 0.677 lên 0.822).
- **Evidence:** Trong lĩnh vực quy định pháp luật và thuế cho hộ kinh doanh, các câu hỏi chứa từ khóa mang tính kỹ thuật cao (như tên biểu mẫu "04/SS-HĐĐT", mã sổ sách "S1-HKD", hoặc số hiệu văn bản "Nghị định 01/2021", "Thông tư 88/2021"). Dense search thường bị trôi vector sang các đoạn văn nói chung về thuế, trong khi BM25 bắt chính xác đoạn chứa mã hiệu này. Thuật toán RRF đã đưa các đoạn văn chính xác này lên vị trí top 1 và top 2.
- **Trade-off về latency/cost:** 
  - Về độ trễ (latency): Config B tăng thêm khoảng 8–15ms cho mỗi truy vấn do phải chạy thêm giải thuật BM25 trên CPU và thuật toán tính điểm RRF. Đây là mức tăng không đáng kể đối với người dùng cuối trong giao diện chat.
  - Về chi phí (cost): Không phát sinh thêm chi phí API do BM25 và RRF được thực thi in-memory trực tiếp trên máy chủ.

## Worst performers

|   # | Question | Config | Faithfulness | Relevance | Recall | Precision | Failure stage | Root cause |
| --: | -------- | ------ | -----------: | --------: | -----: | --------: | ------------- | ---------- |
|   1 | Hộ kinh doanh nộp thuế theo phương pháp kê khai phải mở những sổ kế toán nào theo Thông tư 88? | Config A | 0.70 | 0.75 | 0.55 | 0.50 | retrieval | Bảng danh sách 7 loại sổ kế toán bị cắt ngang giữa 2 chunks do giới hạn chunk_size 500 ký tự. |
|   2 | Khi tạm ngừng kinh doanh từ 30 ngày trở lên, hộ kinh doanh phải thông báo trước bao nhiêu ngày? | Config A | 0.75 | 0.80 | 0.60 | 0.60 | retrieval | Dense model nhầm lẫn giữa quy định thông báo tạm ngừng của Doanh nghiệp (trước 3 ngày) và Hộ kinh doanh. |
|   3 | Khi phát hiện hóa đơn điện tử đã lập có sai sót thì hộ kinh doanh xử lý như thế nào? | Config B | 0.85 | 0.80 | 0.65 | 0.75 | generation | LLM tổng hợp dài và bao gồm cả trường hợp của doanh nghiệp lớn thay vì chỉ tập trung vào hộ kinh doanh cá thể. |

## Recommendations

| Priority | Action | Evidence from failure analysis | Expected impact | How to verify |
| -------: | ------ | ------------------------------ | --------------- | ------------- |
|        1 | Áp dụng Recursive Separator tối ưu cho Markdown bảng biểu (`|`, `\n## `) | Chunk chứa bảng biểu 7 loại sổ kế toán bị phân mảnh | Tăng Context Recall cho các câu hỏi tra cứu danh mục lên > 0.85 | Chạy lại test eval trên các câu hỏi liên quan đến Thông tư 88 |
|        2 | Triển khai Query Expansion (Mở rộng câu hỏi viết tắt như HĐĐT -> Hóa đơn điện tử) | Các query chứa từ viết tắt thường có điểm BM25 thấp hơn kỳ vọng | Tăng Context Precision thêm 5-8% | Đo lường độ tương đồng của danh sách top 5 retrieved chunks |
|        3 | Cải tiến Prompt hệ thống: Buộc câu trả lời ngắn gọn và tập trung đúng phạm vi đối tượng | Câu trả lời số 3 bị lan man sang quy định của doanh nghiệp cổ phần | Tăng Answer Relevance và Faithfulness lên > 0.95 | Kiểm thử mù (blind evaluation) trên 10 câu hỏi nghiệp vụ thực tế |

## Bonus experiments

| Experiment | Baseline | Metric delta | Latency/cost delta | Conclusion |
| ---------- | -------- | -----------: | -----------------: | ---------- |
| HyDE (Hypothetical Document Embeddings) | Hybrid + RRF | +0.035 Precision | +800ms / +$0.001 per query | Cải thiện tốt cho các câu hỏi mở, tuy nhiên latency tăng đáng kể do cần một lượt sinh trước của LLM. |
| Query Expansion (Synonym matching) | Hybrid + RRF | +0.040 Recall | +12ms / $0 cost | Rất hiệu quả đối với các thuật ngữ viết tắt trong ngành thuế (MST, CQT, GTGT, TNCN, HKD). |
