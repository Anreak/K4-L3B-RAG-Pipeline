# Individual contribution report

Mỗi thành viên copy template này thành:

```text
reports/<student-id>-<short-name>.md
```

Giới hạn khuyến nghị: 1 trang, không chép lại README hoặc mô tả lý thuyết chung. Báo cáo không phải một bài pipeline cá nhân; mục đích là ghi nhận ownership và bằng chứng đóng góp trong sản phẩm nhóm.

---

## Thông tin

- Họ và tên: Nguyễn Minh Quyền
- Mã học viên: 2A202602438
- Nhóm: Nhóm một
- Repository/branch: main

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Chuẩn hóa dữ liệu sang Markdown | Sử dụng MarkItDown để chuyển đổi tài liệu PDF/DOCX và đọc dữ liệu JSON, sau đó lưu thành Markdown theo cấu trúc thư mục `legal/` và `news/`; giữ metadata nguồn như `Source` và `Crawled` ở đầu file Markdown. | `src/task3_convert_markdown.py` | Done |
| Chunking, Embedding & ChromaDB | Phân đoạn tài liệu bằng Recursive Character Text Splitter với `chunk_size=500`, `chunk_overlap=60`; nhúng vector đa ngôn ngữ phù hợp tiếng Việt bằng `paraphrase-multilingual-MiniLM-L12-v2`; lưu các chunk và embedding vào ChromaDB theo cosine distance. | `src/task4_chunking_indexing.py` | Done |

Chỉ kê khai công việc có thể đối chiếu bằng file, commit, pull request, test hoặc kết quả evaluation.

## Quyết định kỹ thuật quan trọng

Mô tả tối đa hai quyết định mà bạn trực tiếp tham gia:

1. **Quyết định:**  
   Chọn chiến lược recursive với kích thước chunk 500 ký tự và overlap 60 ký tự.  
   **Lý do/evidence:** Ưu tiên giữ cấu trúc đoạn và ngữ cảnh lân cận khi chia các tài liệu Markdown có độ dài khác nhau.  
   **Trade-off:** Overlap 60 giúp bảo toàn thêm ngữ cảnh ở ranh giới chunk nhưng làm tăng số lượng ký tự lặp lại và chi phí embedding so với overlap nhỏ hơn.

2. **Quyết định:**  
   Dùng `paraphrase-multilingual-MiniLM-L12-v2` và ChromaDB với cosine distance.  
   **Lý do/evidence:** Model hỗ trợ nhiều ngôn ngữ, trong đó có tiếng Việt; ChromaDB hỗ trợ lưu trữ bền vững và truy hồi vector theo độ tương đồng cosine.  
   **Trade-off:** Model nhẹ, embedding có 384 chiều và phù hợp triển khai cục bộ, nhưng chất lượng ngữ nghĩa có thể thấp hơn các model lớn hơn.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: Chạy `convert_all()` trong `src/task3_convert_markdown.py` để chuẩn hóa dữ liệu landing, đồng thời kiểm tra cấu hình `CHUNK_SIZE=500`, `CHUNK_OVERLAP=60` và chạy `run_pipeline()` trong `src/task4_chunking_indexing.py`.
- Kết quả trước/sau nếu có: Tài liệu PDF/DOC/DOCX được MarkItDown chuyển thành Markdown; bài viết JSON được chuyển thành Markdown có tiêu đề, `Source`, `Crawled` và nội dung. Các chunk sau đó được gán ID ổn định theo dạng `<document>::chunk-<index>` và được upsert theo batch 250 phần tử.
- Lỗi đã phát hiện và cách xử lý: Chưa ghi nhận lỗi trong phần triển khai này.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Embedding được tạo cục bộ nên thời gian khởi tạo model và chi phí bộ nhớ có thể tăng khi chạy lần đầu hoặc xử lý tập dữ liệu lớn.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Bổ sung kiểm thử tự động để xác nhận kích thước, overlap 60, số lượng chunk và tính ổn định của ID sau mỗi lần chạy pipeline.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 25/09/2026
- Tên thành viên: Nguyễn Minh Quyền
