import tiktoken


def create_messages(resume_text: str) -> tuple[list[dict], int]:
    messages = []
    system_message_content = """
    You are a helpful assistant. 我会给你一份不规整的简历, 你需要将其规范化. 并至少返回以下信息:
    ```
    姓名
    性别
    民族
    出生年月
    联系方式
    教育背景
    工作经历
    自我评价
    ```
    格式要求如下: 
    1. 你需要将简历中的信息按照上述顺序依次填写, 并用空行分隔.
    2. 每个字段名使用markdown加粗, 字段名后加一个冒号, 然后是字段内容. 在字段内容后加一个换行符.
    3. 尽可能完善字段内容. 如果简历中没有某个字段, 请填写"无".
    以下是一个示例, 该示例中的信息是不完整的, 只是为了展示格式要求:
    ```
    **姓名:** 张三\n
    **性别:** 男\n
    **民族:** 汉\n
    **出生年月:** 1990年1月12日\n
    **联系方式:** 无\n
    ...省略...
    """
    messages.append({"role": "system", "content": system_message_content})
    messages.append({"role": "user", "content": resume_text})
    num_tokens = get_num_tokens(str(messages))
    return (messages, num_tokens)


def get_num_tokens(text: str) -> list[int]:
    enc = tiktoken.get_encoding("cl100k_base")
    tokenized_text = enc.encode(text)
    return len(tokenized_text)
