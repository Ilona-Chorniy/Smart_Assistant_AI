from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import os

# Завантажуємо API-ключ
load_dotenv()

# Підключаємо Groq
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Особистість асистента
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

# Історія розмови
conversation = [system_message]


# Функція спілкування з асистентом
def ask_ai(prompt):
    conversation.append({
        "role": "user",
        "content": prompt
    })

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=conversation,
        temperature=0.7,
        max_tokens=1000
    )

    answer = response.choices[0].message.content

    conversation.append({
        "role": "assistant",
        "content": answer
    })

    return answer


# Запуск асистента
print("AI-планувальник запущений!")
print("Напиши 'вихід', щоб завершити програму.")
print("Напиши '/reset', щоб очистити історію розмови.")
print("Напиши '/time', щоб дізнатися поточний час.")
print("Напиши '/help', щоб переглянути всі команди.")

while True:
    prompt = input("\nТи: ")

    if prompt.lower() == "вихід":
        print("До зустрічі!")
        break

    if prompt.lower() == "/reset":
        conversation.clear()
        conversation.append(system_message)
        print("Історію розмови очищено!")
        continue

    if prompt.lower() == "/time":
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        print("Поточна дата і час:", current_time)
        continue

    if prompt.lower() == "/help":
        print("\nДоступні команди:")
        print("вихід - завершити роботу асистента")
        print("/reset - очистити історію розмови")
        print("/time - показати поточну дату та час")
        print("/help - показати список команд")
        continue

    answer = ask_ai(prompt)
    print("\nАсистент:", answer)