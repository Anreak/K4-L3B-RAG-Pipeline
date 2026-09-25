import streamlit as st
from dotenv import load_dotenv
from src.task10_generation import generate_with_citation, reorder_for_llm, format_context, call_llm, SYSTEM_PROMPT, retrieve

load_dotenv()

st.set_page_config(
    page_title="Trợ lý Pháp luật & Thuế Hộ Kinh Doanh",
    page_icon="⚖️",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("⚖️ Trợ lý Hộ Kinh Doanh")
    st.markdown(
        "Chatbot RAG thông minh hỗ trợ tra cứu chính sách pháp luật, đăng ký kinh doanh và nghĩa vụ thuế "
        "dành cho hộ và cá nhân kinh doanh."
    )
    st.divider()
    top_k = st.slider("Số lượng tài liệu truy xuất (top_k)", min_value=1, max_value=10, value=5)
    enable_memory = st.toggle("🧠 Ghi nhớ ngữ cảnh hội thoại (Multi-turn)", value=True, help="Cho phép hỏi nối tiếp dựa trên các câu trả lời trước đó.")
    
    st.divider()
    st.markdown("**Cấu hình hệ thống:**")
    st.markdown("- **Embedding:** `MiniLM-L12-v2` (384d)")
    st.markdown("- **Vector DB:** ChromaDB (Cosine)")
    st.markdown("- **Search:** Dense + BM25Okapi")
    st.markdown("- **Fusion:** Reciprocal Rank Fusion (k=60)")
    st.markdown("- **LLM Provider:** Google Gemini Flash")
    
    st.divider()
    if st.button("🗑️ Xóa lịch sử trò chuyện", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("⚖️ Trợ lý Tra cứu Pháp luật & Thuế cho Hộ Kinh Doanh")
st.caption(
    "Dữ liệu được chuẩn hoá từ Sổ tay thuế, Nghị định 01/2021/NĐ-CP, Thông tư 88/2021/TT-BTC "
    "và các cổng thông tin pháp luật chính thống."
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander(f"📚 Nguồn tham khảo & Trích dẫn ({len(message['sources'])} tài liệu) - Phương pháp: {message.get('method', 'hybrid').upper()}"):
                for idx, src in enumerate(message["sources"], 1):
                    meta = src.get("metadata", {})
                    score = src.get("score", 0.0)
                    method = src.get("retrieval_method", "hybrid")
                    title = meta.get("title", meta.get("source", f"Tài liệu {idx}"))
                    url = meta.get("url")
                    
                    st.markdown(
                        f"""
                        <div style="background-color: rgba(30, 64, 175, 0.08); border-left: 4px solid #2563eb; padding: 10px 14px; border-radius: 6px; margin: 8px 0;">
                            <span style="font-weight: 600; color: #1e3a8a;">[{idx}] {title}</span> 
                            &nbsp;<span style="background-color: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 12px; font-size: 0.85em; font-weight: 500;">{method.upper()}</span>
                            &nbsp;<span style="background-color: #f1f5f9; color: #475569; padding: 2px 8px; border-radius: 12px; font-size: 0.85em;">Score: {score:.4f}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if url:
                        st.markdown(f"🔗 **Liên kết nguồn:** [{url}]({url})")
                    st.markdown(f"> *{src.get('content', '').strip()[:400]}...*")
                    st.divider()

query = st.chat_input("Nhập câu hỏi về thủ tục đăng ký, thuế, hóa đơn...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Đang tìm kiếm tài liệu và tổng hợp câu trả lời..."):
            # Multi-turn conversation context handling
            history_context = ""
            if enable_memory and len(st.session_state.messages) > 1:
                recent_messages = st.session_state.messages[-3:-1]
                history_lines = [f"{m['role'].capitalize()}: {m['content']}" for m in recent_messages]
                history_context = "\nLịch sử hội thoại trước đó:\n" + "\n".join(history_lines) + "\n\n"

            # Execute RAG generation with conversation context if active
            chunks = retrieve(query, top_k=top_k)
            if not chunks:
                answer = "Tôi không thể xác minh thông tin này từ nguồn hiện có."
                sources = []
                method = "none"
            else:
                reordered = reorder_for_llm(chunks)
                context = format_context(reordered)
                user_message = (
                    f"{history_context}"
                    f"Context tài liệu:\n{context}\n\n"
                    f"Câu hỏi: {query}\n\n"
                    f"Trả lời câu hỏi trên dựa vào Context. Nêu rõ tài liệu hoặc nguồn tham chiếu tương ứng."
                )
                try:
                    answer = call_llm(SYSTEM_PROMPT, user_message)
                    if not answer or not answer.strip():
                        answer = "Tôi không thể xác minh thông tin này từ nguồn hiện có."
                except Exception as e:
                    answer = f"Tôi không thể xác minh thông tin này từ nguồn hiện có. (Chi tiết: {e})"
                sources = chunks
                method = chunks[0].get("retrieval_method", "hybrid")

            st.markdown(answer)

            if sources:
                with st.expander(f"📚 Nguồn tham khảo & Trích dẫn ({len(sources)} tài liệu) - Phương pháp: {method.upper()}"):
                    for idx, src in enumerate(sources, 1):
                        meta = src.get("metadata", {})
                        score = src.get("score", 0.0)
                        src_method = src.get("retrieval_method", "hybrid")
                        title = meta.get("title", meta.get("source", f"Tài liệu {idx}"))
                        url = meta.get("url")
                        
                        st.markdown(
                            f"""
                            <div style="background-color: rgba(30, 64, 175, 0.08); border-left: 4px solid #2563eb; padding: 10px 14px; border-radius: 6px; margin: 8px 0;">
                                <span style="font-weight: 600; color: #1e3a8a;">[{idx}] {title}</span> 
                                &nbsp;<span style="background-color: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 12px; font-size: 0.85em; font-weight: 500;">{src_method.upper()}</span>
                                &nbsp;<span style="background-color: #f1f5f9; color: #475569; padding: 2px 8px; border-radius: 12px; font-size: 0.85em;">Score: {score:.4f}</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        if url:
                            st.markdown(f"🔗 **Liên kết nguồn:** [{url}]({url})")
                        st.markdown(f"> *{src.get('content', '').strip()[:400]}...*")
                        st.divider()

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "method": method,
    })
