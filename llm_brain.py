from groq import Groq
import json

client = Groq(api_key="API_KEY")

conversation_history = [
    {
        "role": "system",
        "content": """
You are Jarvis, an intelligent, calm, precise AI assistant.

You may either:
1. Respond normally.
2. Or request to use a tool.

If you need to use a tool, respond ONLY in pure JSON format:

{
  "action": "tool_name",
  "argument": optional_argument
}

Do NOT add explanations before or after JSON.

If the user asks to see photos, images, pictures, or show visuals,
you MUST use the tool:

{
  "action": "search_google",
  "argument": "<person name> photos"
}

Do NOT generate image URLs manually.

Available tools:
- search_google
- open_first_result
- open_nth_result
- go_back
- close_browser
- scroll_down
- scroll_up
- copy_text
- paste_text
- save_file
- find_word
- replace_word
- save_code_file
- run_python_file
- run_java_file
- open_terminal

Use tools only when necessary.
If no tool is required, respond normally.
"""
    }
]


def ask_llm(user_input):
    global conversation_history

    conversation_history.append(
        {"role": "user", "content": user_input}
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=conversation_history,
        temperature=0.3
    )

    reply = response.choices[0].message.content.strip()

    conversation_history.append(
        {"role": "assistant", "content": reply}
    )

    return reply