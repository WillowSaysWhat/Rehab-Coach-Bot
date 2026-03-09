import gradio as gr
from dotenv import load_dotenv
from sugar_rehab_companion import SugarRehabCompanion

load_dotenv(override=True)

# =============================================================================
# COLOURS — dark mode (change these to redesign the UI)
# =============================================================================
COLOUR_PRIMARY = "#5B9BD5"              # Accent blue (buttons, links)
COLOUR_PRIMARY_HOVER = "#7AB3E8"        # Lighter blue on hover
COLOUR_BACKGROUND = "#1A1A1A"           # Page background
COLOUR_SURFACE = "#2D2D2D"              # Cards and input area
COLOUR_HEADER_BG = "#1E2A38"            # Header bar background
COLOUR_HEADER_TEXT = "#E8E8E8"          # Header title text
COLOUR_USER_BUBBLE = "#2E5A8C"          # User message bubble
COLOUR_BOT_BUBBLE = "#2D2D2D"           # Bot message bubble
COLOUR_BOT_TEXT = "#E8E8E8"             # Bot message text
COLOUR_INPUT_BORDER = "#404040"         # Textbox border
COLOUR_ACCENT_SOFT = "#2E5A8C"          # Focus ring
COLOUR_INPUT_BG = "#252525"             # Input background
COLOUR_INPUT_TEXT = "#E8E8E8"           # Input text
# =============================================================================

async def run_chat(message, history):
    # Gradio 6 Chatbot expects list of {"role": "user"|"assistant", "content": "..."}
    messages = list(history) if history else []
    if not message or not message.strip():
        yield messages, ""
        return
    messages = messages + [{"role": "user", "content": message}]
    full_reply = ""
    async for chunk in SugarRehabCompanion().run(message):
        full_reply += chunk
        yield messages + [{"role": "assistant", "content": full_reply}], ""  # "" clears the input


# Custom CSS using the colour variables above (so one place to edit)
CUSTOM_CSS = f"""
    /* Page and layout */
    .gradio-container {{ background: {COLOUR_BACKGROUND} !important; }}
    .main .wrap {{
        max-width: 720px;
        margin: auto;
        padding: 1rem;
    }}
    /* Header block */
    .header-bar {{
        background: {COLOUR_HEADER_BG} !important;
        color: {COLOUR_HEADER_TEXT} !important;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-weight: 600;
        font-size: 1.25rem;
    }}
    /* Primary button */
    .primary-btn {{
        background: {COLOUR_PRIMARY} !important;
        border-color: {COLOUR_PRIMARY} !important;
        color: white !important;
    }}
    .primary-btn:hover {{
        background: {COLOUR_PRIMARY_HOVER} !important;
        border-color: {COLOUR_PRIMARY_HOVER} !important;
    }}
    /* Chat bubbles: user */
    .message.user .message-body {{
        background: {COLOUR_USER_BUBBLE} !important;
        color: white !important;
    }}
    /* Chat bubbles: bot */
    .message.bot .message-body {{
        background: {COLOUR_BOT_BUBBLE} !important;
        color: {COLOUR_BOT_TEXT} !important;
    }}
    /* Input area */
    .input-wrap, .input-wrap input, .input-wrap textarea {{
        border-color: {COLOUR_INPUT_BORDER} !important;
        background: {COLOUR_INPUT_BG} !important;
        color: {COLOUR_INPUT_TEXT} !important;
        border-radius: 10px;
    }}
    .input-wrap:focus-within {{
        box-shadow: 0 0 0 2px {COLOUR_ACCENT_SOFT};
    }}
    /* Blocks and panels dark */
    .block, .form, .panel {{
        background: {COLOUR_SURFACE} !important;
    }}
"""

# Theme: Soft with blue primary; detailed colours come from CUSTOM_CSS above
theme = gr.themes.Soft(primary_hue="blue")

with gr.Blocks(title="Sugar Rehab Companion", fill_width=False) as ui:
    gr.HTML(
        f'<div class="header-bar">Sugar Rehab Companion</div>',
        elem_classes=["header-bar"],
    )
    chatbot = gr.Chatbot(
        label=None,
        height=400,
    )
    row = gr.Row()
    with row:
        query_textbox = gr.Textbox(
            placeholder="How are you feeling today?",
            label="",
            show_label=False,
            scale=9,
            container=False,
        )
        run_button = gr.Button("Send", variant="primary", scale=1, min_width=80)

    run_button.click(
        fn=run_chat,
        inputs=[query_textbox, chatbot],
        outputs=[chatbot, query_textbox],
    )
    query_textbox.submit(
        fn=run_chat,
        inputs=[query_textbox, chatbot],
        outputs=[chatbot, query_textbox],
    )

ui.launch(inbrowser=True, theme=theme, css=CUSTOM_CSS)
