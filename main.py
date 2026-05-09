from groq import Groq
from dotenv import load_dotenv
import os

from tools import (
    show_interfaces,
    show_bgp
)
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_llm(messages):

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        temperature=0
    )

    return completion.choices[0].message.content


SYSTEM_PROMPT = """
You are a network automation assistant.

You have access to the following tools:

1. show_interfaces
   - Shows interface status summary

2. show_bgp
   - Shows BGP neighbor summary

RULES:

- If the user asks about interfaces,
  return ONLY:
  TOOL:show_interfaces

- If the user asks about BGP,
  return ONLY:
  TOOL:show_bgp

- Do not explain.
- Do not add extra text.
"""


ANALYSIS_SYSTEM_PROMPT = """
You are an expert network engineer.

Analyze router command outputs carefully.

Rules:
- Be accurate
- Be concise
- Do not hallucinate
- Only use information present in output
"""


while True:

    user_input = input("\Ask Query: ")

    # Exit Optionz
    if user_input.lower() in ["exit", "quit"]:
        break

    tool_selection_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    llm_decision = ask_llm(
        tool_selection_messages
    )

    print(f"\nLLM Decision: {llm_decision}")

    tool_output = None

    if "TOOL:show_interfaces" in llm_decision:

        tool_output = show_interfaces()

    elif "TOOL:show_bgp" in llm_decision:

        tool_output = show_bgp()

    else:
        print("\nAssistant:")
        print(llm_decision)
        continue

    print("\nRaw Router Output:\n")
    print(tool_output)

    analysis_messages = [
        {
            "role": "system",
            "content": ANALYSIS_SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"""
User Question:
{user_input}

Router Output:
{tool_output}
"""
        }
    ]

    final_response = ask_llm(
        analysis_messages
    )

    print("\nAssistant:\n")
    print(final_response)