import gradio as gr
from dotenv import load_dotenv
from sugar_rehab_companion import SugarRehabCompanion

load_dotenv(override=True)

async def run_chat(message, history):
    async for chunk in SugarRehabCompanion().run(message):
        yield chunk
        

#with gr.Blocks(fill_width=False) as ui:
#    gr.Markdown("## Sugar Rehab Companion")
#    query_textbox = gr.Textbox(label="how are you feeling today?")
#    run_button = gr.Button("Run", variant="primary")
#    report = gr.Markdown(label="Response")
#    
#    run_button.click(fn=run_chat, inputs=query_textbox, outputs=report)
#    query_textbox.submit(fn=run_chat, inputs=query_textbox, outputs=report)
#    
#    ui.launch(inbrowser=True)
    
gr.ChatInterface(run_chat, title="Sugar Rehab Companion").launch(inbrowser=True)