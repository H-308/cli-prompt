import os
import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-3-flash-preview')

def load_system_prompt():
    with open("prompts/prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def convert_to_cli(prompt):
    if not prompt:
        return "Error: Missing prompt"

    try:
        system_prompt = load_system_prompt()
        full_content = f"{system_prompt}\n\nUser: {prompt}"

        completion = model.generate_content(
            full_content,
            generation_config={"temperature": 0}
        )

        reply = completion.text.strip()
        print(f"reply: {reply}")
        return reply

    except Exception as e:
        return f"Error: {str(e)}"

demo = gr.Interface(
    fn=convert_to_cli,
    inputs=gr.Textbox(label="Prompt"),
    outputs=gr.Textbox(label="Reply"),
    title="CLI Agent"
)

if __name__ == "__main__":
    demo.launch()