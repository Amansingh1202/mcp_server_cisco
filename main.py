from groq import Groq
from dotenv import load_dotenv
import os

from tools import (
    get_interfaces,
    show_bgp,
    get_interfaces_all,
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

1. get_interfaces(device_name)
   - Gets interface status summary for specific device

2. show_bgp(device_name)
   - Shows BGP neighbor summary for specific device

3. get_interfaces_all
   - Gets interface status summary for all devices

RULES:

- If the user asks about interfaces for specific device,
Return EXACTLY in this format:

TOOL:<tool_name>:<device_name>

Examples:
TOOL:get_interfaces:R2

Do not add extra text.

- If the user asks about interfaces without specific device,
Return EXACTLY in this format:

TOOL:<tool_name>:None

Examples:
TOOL:get_interfaces_all:None

Do not add extra text.

- If the user asks about BGP,
  Return EXACTLY in this format:

TOOL:<tool_name>:<device_name>

Examples:
TOOL:show_bgp:R1

Do not add extra text.

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
    print(f"\nLLM Response: {llm_decision}")
    parts = llm_decision.strip().split(":")
    tool_name = parts[1]
    device_name = parts[2]

    tool_output = None

    if tool_name == "get_interfaces":
        tool_output = get_interfaces(device_name)
    elif tool_name == "show_bgp":
        tool_output = show_bgp(device_name)
    elif tool_name == "get_interfaces_all":
        tool_output = get_interfaces_all()
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