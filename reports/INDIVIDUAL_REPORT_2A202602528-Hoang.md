# Individual contribution report

## Thông tin

- Họ và tên: Vương Việt Hoàng
- Mã học viên: 2A202602528
- Nhóm: Nhóm Một
- Repository/branch: main

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Golden Dataset & A/B Evaluation | Soạn 16 cặp Q&A chuẩn thực tế, xác định câu hỏi, answer key và mục tiêu retrieval, sau đó chạy thử nghiệm A/B giữa Dense-only và Hybrid RRF để so sánh hiệu quả thực tế của mô hình | `group_project/evaluation/golden_dataset.json`, `reports/RESULT.md` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Dùng goldenset chuẩn hóa 16 cặp Q&A để đánh giá chất lượng retrieval thay vì chỉ kiểm tra output bằng mắt.  
   **Lý do/evidence:** Với domain pháp luật/thuế, đánh giá thủ công trực tiếp dễ bị thiên lệch và khó tái lặp. Golden dataset giúp định lượng hiệu năng thông qua Context Precision và Context Recall theo cùng một baseline cho mọi thử nghiệm.  
   **Trade-off:** Cần mất thời gian xây dựng câu hỏi/đáp án chất lượng cao và đảm bảo chúng phản ánh đúng thực tế người dùng; tuy nhiên, so với việc đánh giá cảm tính, độ tin cậy của kết quả tăng rõ rệt.

2. **Quyết định:** So sánh Dense-only với Hybrid + RRF như một thí nghiệm A/B có kiểm soát để chứng minh quyết định kỹ thuật.  
   **Lý do/evidence:** Khi chạy trên cùng golden dataset, Hybrid + RRF cho thấy cải thiện đáng kể: Context Precision từ 0.677 lên 0.822 và Context Recall từ 0.602 lên 0.692, chứng minh việc kết hợp semantic và lexical search mang lại độ chính xác cao hơn.  
   **Trade-off:** Quá trình đánh giá yêu cầu nhiều bước chạy query và lưu trữ số liệu, tăng thời gian kiểm thử nhưng mang lại bằng chứng thực nghiệm đủ mạnh để justify lựa chọn architecture.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: Golden dataset `group_project/evaluation/golden_dataset.json` với 16 câu hỏi thực tế và so sánh kết quả retrieval giữa Dense-only và Hybrid RRF; đồng thời đối chiếu trên `reports/RESULT.md`.
- Kết quả trước/sau nếu có:  
  - Dense-only: Context Precision 0.677, Context Recall 0.602.  
  - Hybrid + RRF: Context Precision 0.822, Context Recall 0.692.  
  - Kết luận: Hybrid RRF cải thiện rõ rệt độ phủ và độ chính xác của ngữ cảnh truy vấn.
- Lỗi đã phát hiện và cách xử lý: Một số câu hỏi trong golden set có độ mơ hồ về wording hoặc liên quan đến nhiều luật/điều kiện, dẫn tới sự chênh lệch giữa đầu vào người dùng và câu trả lời mong đợi. Tôi đã tinh chỉnh các cặp Q&A để sát tình huống thực tế, đồng thời thống nhất tiêu chí đánh giá theo phần nội dung được hỗ trợ bằng evidence thay vì đo bằng cảm nhận chủ quan.

## Điều còn hạn chế

- Một hạn lệch cụ thể của phần tôi làm: Golden dataset hiện có 16 cặp Q&A, khá hữu ích cho việc đánh giá ban đầu nhưng vẫn còn giới hạn về độ phủ các tình huống cực đoan hoặc truy vấn phức tạp hơn trong thực tế.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Mở rộng golden dataset theo từng nhóm nghiệp vụ rõ ràng (thuế, đăng ký doanh nghiệp, chính sách mới) và bổ sung các query khó hơn để đánh giá độ bền của hệ thống.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 25/09/2026
- Tên thành viên: Vương Việt Hoàng
