import gradio as gr

from app.services.vision import analyze_image
from app.services.llm import answer_question


# ============================================================
# IMAGE INSPECTION
# ============================================================

def inspect_image(image):

    if image is None:
        return (
            "No image uploaded.",
            None,
            "Please upload an equipment image."
        )

    image_path = "uploads/demo.jpg"
    image.save(image_path)

    result = analyze_image(image_path)

    detections = result["detections"]

    if detections:

        detection_text = "\n".join(
            [
                f"{item['object']} — "
                f"{item['confidence'] * 100:.1f}%"
                for item in detections
            ]
        )

        detected_component = detections[0]["object"]

        status = "Automatic component detection completed."

    else:

        detection_text = (
            "No supported component was detected automatically.\n\n"
            "Please select the component manually."
        )

        detected_component = None

        status = "Automatic detection was inconclusive."


    return (
        detection_text,
        detected_component,
        status
    )


# ============================================================
# QUESTION ANSWERING
# ============================================================

def ask_question(question, component):

    if not question or not question.strip():

        return "Please enter a technical question."

    answer = answer_question(
        question,
        component
    )

    return answer


# ============================================================
# APPLICATION
# ============================================================

with gr.Blocks(
    title="SnapAssist"
) as demo:

    gr.Markdown(
        """
        # SnapAssist

        **Engineering inspection and technical assistance**

        Upload equipment → identify the component → ask a technical question.
        """
    )

    # --------------------------------------------------------
    # IMAGE + DETECTION
    # --------------------------------------------------------

    with gr.Row():

        # IMAGE COLUMN

        with gr.Column():

            image = gr.Image(
                type="pil",
                label="Equipment image"
            )

            inspect_button = gr.Button(
                "Analyze equipment"
            )


        # RESULTS COLUMN

        with gr.Column():

            detections = gr.Textbox(
                label="Detection results",
                lines=7
            )

            component = gr.Dropdown(
                choices=[
                    "MCB",
                    "Circuit Breaker",
                    "Contactor",
                    "Relay"
                ],
                label="Component",
                value=None,
                allow_custom_value=True
            )

            status = gr.Textbox(
                label="Status"
            )


    # --------------------------------------------------------
    # CONNECT IMAGE BUTTON
    # --------------------------------------------------------

    inspect_button.click(
        fn=inspect_image,
        inputs=image,
        outputs=[
            detections,
            component,
            status
        ]
    )


    # --------------------------------------------------------
    # QUESTION SECTION
    # --------------------------------------------------------

    gr.Markdown(
        """
        ## Ask SnapAssist

        Ask a technical question about the selected component.
        """
    )


    question = gr.Textbox(
        label="Technical question",
        placeholder=(
            "Example: What should I check if this component keeps tripping?"
        ),
        lines=3
    )


    ask_button = gr.Button(
        "Get engineering guidance"
    )


    answer = gr.Textbox(
        label="Engineering guidance",
        lines=10
    )


    # --------------------------------------------------------
    # CONNECT QUESTION BUTTON
    # --------------------------------------------------------

    ask_button.click(
        fn=ask_question,
        inputs=[
            question,
            component
        ],
        outputs=answer
    )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    demo.launch()