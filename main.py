# streamlit run main.py
import streamlit as st
from file_processing import (
    process_doc_to_str,
    process_docx_to_str,
    process_pdf_to_str,
    process_rtf_to_str,
)
from image_processing import read_image
from llm import create_messages, get_num_tokens
from openai import ChatCompletion

st.subheader("请将文件拖拽到此处或点击下方上传")
# File Uploader
uploaded_file = st.file_uploader(
    "Hidden label", type=["doc", "docx", "jpg", "pdf", "rtf"], label_visibility="hidden"
)
if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    if file_extension == "doc":
        resume_text = process_doc_to_str(uploaded_file)
    elif file_extension == "docx":
        resume_text = process_docx_to_str(uploaded_file)
    elif file_extension in ["jpg", "jpeg"]:
        with st.spinner("读取图片简历中..."):
            resume_text = read_image(uploaded_file)
    elif file_extension == "pdf":
        resume_text = process_pdf_to_str(uploaded_file)
    elif file_extension == "rtf":
        resume_text = process_rtf_to_str(uploaded_file)

    st.success("成功读取简历")
    # Add an element between file input and the parsed text
    st.subheader("规范化简历如下:")
    # Display llm output
    res_box = st.empty()

    messages, num_tokens = create_messages(resume_text)
    if num_tokens > 2000:
        model = "gpt-3.5-turbo-16k"
        print(f"提示词Token数: {num_tokens} > 2000, 使用{model}模型")
    else:
        model = "gpt-3.5-turbo"
        print(f"提示词Token数: {num_tokens}, 使用{model}模型")
    contents = []
    concat_response = ""
    retry_count = 0
    max_retries = 2
    while True:
        try:
            for resp in ChatCompletion.create(
                model=model,
                messages=messages,
                request_timeout=2,
                temperature=0,
                stream=True,
            ):
                delta = resp["choices"][0]["delta"]
                finish_reason = resp["choices"][0]["finish_reason"]
                if hasattr(delta, "content"):
                    contents.append(delta.content)
                if finish_reason == "stop":
                    num_tokens += get_num_tokens(concat_response)
                    print(f"总Token数: {num_tokens}")
                    break
                concat_response = "".join(contents)
                res_box.markdown(concat_response)
            break
        except Exception as e:
            retry_count += 1
            if retry_count > max_retries:
                st.error("服务器负载较高，请刷新页面重试")
                break
            else:
                st.warning("服务器响应缓慢，正在重连...")
                continue
