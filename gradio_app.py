import gradio as gr
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose.
What's in this image?. Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Donot say 'In the image I see' but say 'With what I see, I think you have ....'
Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_filepath, image_filepath):
    try:
        speech_to_text_output = transcribe_with_groq(audio_file_path=audio_filepath, stt_model="whisper-large-v3")

        if image_filepath:
            encoded_img = encode_image(image_filepath)
            doctor_response = analyze_image_with_query(
                query=system_prompt + speech_to_text_output,
                encoded_image=encoded_img,
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )
        else:
            doctor_response = "No image provided for me to analyze."

        voice_of_doctor = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="final.mp3")

        return speech_to_text_output, doctor_response, "final.mp3"
    except Exception as e:
        return f"Error: {e}", "", ""

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🩺 AI Doctor Assistant
        Welcome to your personal AI doctor assistant with **voice and vision** capabilities.
        Speak your symptoms, upload your image, and receive a caring, professional response instantly.
        """,
        elem_classes="text-center"
    )

    with gr.Row(equal_height=True):
        with gr.Column():
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Record Your Symptoms")
            image_input = gr.Image(type="filepath", label="🖼️ Upload Image (optional)")

            submit_btn = gr.Button("Analyze", variant="primary")

        with gr.Column():
            with gr.Accordion("📄 Speech to Text (What you said)", open=True):
                speech_output = gr.Textbox(label="Speech to Text", interactive=False)

            with gr.Accordion("🩺 Doctor's Response", open=True):
                doctor_output = gr.Textbox(label="Doctor's Response", interactive=False)

            with gr.Accordion("🔊 Voice Response", open=True):
                audio_output = gr.Audio(label="Doctor Speaking")

    submit_btn.click(fn=process_inputs, inputs=[audio_input, image_input], outputs=[speech_output, doctor_output, audio_output])

    gr.Markdown(
        "<center>Made with ❤️ by Komal | For learning and medical awareness purposes only.</center>"
    )

if __name__ == "__main__":
    demo.launch(debug=True)


