
from openai import OpenAI
from dotenv import load_dotenv
import gradio as gr
import os

# Завантажуємо API-ключ
load_dotenv()

# Підключення до Groq
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Особистість AI-планувальника
system_message = {
    "role": "system",
    "content": (
        "Ти — розумний персональний AI-планувальник. "
        "Твоя мета — допомагати користувачу організовувати день, "
        "планувати завдання, визначати пріоритети та ефективно "
        "розподіляти час. "
        "Відповідай українською мовою, дружньо, зрозуміло "
        "та структуровано. "
        "Надавай практичні поради та конкретні рекомендації."
    )
}


# Функція спілкування з AI

def chat_with_ai(message, history):

    history = history or []

    conversation = [system_message]

    conversation.extend(history)

    conversation.append({
        "role": "user",
        "content": message
    })

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=conversation,
        temperature=0.7,
        max_tokens=1000
    )

    answer = response.choices[0].message.content

    updated_history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": answer}
    ]

    return "", updated_history, updated_history



    history = history or []

    conversation = [system_message]

    for user_message, assistant_message in history:
        conversation.append({
            "role": "user",
            "content": user_message
        })

        conversation.append({
            "role": "assistant",
            "content": assistant_message
        })

    conversation.append({
        "role": "user",
        "content": message
    })

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=conversation,
        temperature=0.7,
        max_tokens=1000
    )

    answer = response.choices[0].message.content

    updated_history = history + [(message, answer)]

    return "", updated_history, updated_history


# Функція очищення історії
def clear_history():
    return [], []


# Створення інтерфейсу
with gr.Blocks(title="Smart Assistant AI") as demo:

    gr.Markdown(
        """
        # 🤖 Smart Assistant AI

        ### Твій персональний AI-планувальник

        Організовуй свій день, плануй завдання
        та ефективно розподіляй час!
        """,
        elem_id="main-title"
    )

    chatbot = gr.Chatbot(
        label="Спілкування з асистентом",
        height=400
    )

    message = gr.Textbox(
        placeholder="Напиши своє повідомлення...",
        label="Твоє повідомлення"
    )

    with gr.Row():
        send_btn = gr.Button("Надіслати", variant="primary")
        clear_btn = gr.Button("🗑️ Очистити історію")

    # Прихована історія розмови
    history = gr.State([])

    # Надсилання повідомлення
    send_btn.click(
        fn=chat_with_ai,
        inputs=[message, history],
        outputs=[message, history, chatbot]
    )

    # Очищення історії
    clear_btn.click(
        fn=clear_history,
        inputs=None,
        outputs=[chatbot, history]
    )


# Запуск
if __name__ == "__main__":
    demo.launch(
        theme=gr.themes.Soft(
            primary_hue="purple",
            secondary_hue="violet",
            neutral_hue="slate"
        ),
        css="""
        .gradio-container {
            max-width: 1000px !important;
            margin: auto !important;
        }

        #main-title {
            text-align: center;
            padding: 25px;
        }

        #main-title h1 {
            color: #8871cf;
            font-size: 36px;
        }

        #main-title p {
            color: #77718a;
            font-size: 16px;
        }
        """
    )
