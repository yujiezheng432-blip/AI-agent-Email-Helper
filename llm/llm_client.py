from ollama import chat


MODEL_NAME = "qwen3:8b"


def ask_llm(user_prompt: str, system_prompt: str = None) -> str:
    """
    普通模式：一次性返回完整结果
    """
    messages = []

    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    messages.append({
        "role": "user",
        "content": user_prompt
    })

    response = chat(
        model=MODEL_NAME,
        messages=messages
    )

    return response.message.content


def ask_llm_stream(user_prompt: str, system_prompt: str = None) -> str:
    """
    流式模式：终端中一个 token 一个 token 输出
    """
    messages = []

    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    messages.append({
        "role": "user",
        "content": user_prompt
    })

    full_text = ""

    stream = chat(
        model=MODEL_NAME,
        messages=messages,
        stream=True
    )

    for chunk in stream:
        token = chunk["message"]["content"]
        print(token, end="", flush=True)
        full_text += token

    print()
    return full_text