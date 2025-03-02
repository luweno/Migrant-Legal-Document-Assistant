import gradio as gr
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# Load API key from environment variables
def createAPI():
    load_dotenv()
    api_key = os.getenv("api_key")
    genai.configure(api_key=api_key)

# Function to call API
def callAPI(user_input):
    createAPI()
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
        f"""
        Goal
        Provide legal information in the specified language, referencing and citing the provided legal documents. Where appropriate, connect these references to relevant external legal sources or known standards. The information should be geared toward individuals who are not native to the United States, so do not assume they are familiar with US legal or cultural norms.

        Return Format
        Your answer must have two parts:

        Plain Legal Format (Concise)
        Answer the question concisely and then clearly state the legal information, citing the provided documents.
        Include relevant external references if they apply. Use precise, professional language suitable for a legal context, but keep it direct and succinct.
        Answer this again if another language has been requested and answer in that language.

        8th-Grade Reading Level Explanation
        Translate the above legal points into simpler language, at roughly an 8th-grade level.
        Explain or define any US‐specific terms, practices, or norms.
        Use short, clear sentences that are easily understood by someone with limited background in US law.
        Answer this again if another language has been requested and answer in that language.

        Warnings
        Do not include flowery or overly lengthy wording. Stay focused on clarity.
        Verify the correctness of legal references and citations.
        Do not assume the reader knows US cultural or legal norms; define or clarify as needed.
        Remember that this is informational only—include a disclaimer that formal legal counsel may be necessary.: {user_input}
        
        User Request: {user_input}
        """
    )
    return response.text


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        bot_message = callAPI(message)
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": bot_message})
        time.sleep(2)
        return message, chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch()