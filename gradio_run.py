import gradio as gr
import filmr




def greet(topic, topia):
    output = filmr.create_film(topic, topia)

    return output


filmr_gui = gr.Interface(
    fn=greet,
    inputs=["text", "text"],
    outputs=["download_button"],
    title="Filmr",
    description="Create a film with the help of GPT4",
)

filmr_gui.launch(allowed_paths=["D:\repos\filmr"])
