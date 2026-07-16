import streamlit as st
import os
import base64
from agent import Agent

st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Agent")

# ---------------- Initialize ---------------- #

if "agent" not in st.session_state:
    st.session_state.agent = Agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- Display Chat History ---------------- #
# NOTE: keys below include the message's index in st.session_state.messages.
# Relying only on the file path (e.g. key=f"pdf_{pdf_path}") breaks with a
# DuplicateWidgetID error the moment two messages reference the same
# filename -- which happens easily since pdfmaker/presentationmaker both
# default to a fixed filename ("output.pdf" / "presentation.pptx") when the
# LLM doesn't supply one.

for idx, message in enumerate(st.session_state.messages):

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        # -------- PDF -------- #

        if message["role"] == "assistant" and "pdf" in message:

            pdf_path = message["pdf"]

            if pdf_path and os.path.exists(pdf_path):

                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()

                st.success("✅ PDF Generated Successfully")

                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_bytes,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf",
                    key=f"pdf_{idx}_{os.path.basename(pdf_path)}"
                )

                pdf_base64 = base64.b64encode(pdf_bytes).decode()

                st.markdown(
                    f"""
                    <iframe
                        src="data:application/pdf;base64,{pdf_base64}"
                        width="100%"
                        height="700">
                    </iframe>
                    """,
                    unsafe_allow_html=True
                )

        # -------- Presentation -------- #

        if message["role"] == "assistant" and "ppt" in message:

            ppt_path = message["ppt"]

            if ppt_path and os.path.exists(ppt_path):

                with open(ppt_path, "rb") as f:
                    ppt_bytes = f.read()

                st.success("✅ Presentation Generated Successfully")

                st.download_button(
                    label="⬇️ Download Presentation",
                    data=ppt_bytes,
                    file_name=os.path.basename(ppt_path),
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    key=f"ppt_{idx}_{os.path.basename(ppt_path)}"
                )

# ---------------- Chat ---------------- #

prompt = st.chat_input("Ask me anything...")

if prompt:

    # User Message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Run Agent

    result = st.session_state.agent.run_agent(prompt)

    assistant_message = result["message"]
    tool_result = result["tool_result"]

    assistant_data = {
        "role": "assistant",
        "content": assistant_message
    }

    # This message's eventual index once appended below -- used to keep
    # the newly-rendered download button's key in sync with the key it
    # will get on the *next* rerun (when it's drawn by the history loop
    # above), so Streamlit doesn't treat them as two different widgets.
    new_idx = len(st.session_state.messages)

    with st.chat_message("assistant"):

        st.markdown(assistant_message)

        # ---------- PDF ---------- #

        if (
            isinstance(tool_result, dict)
            and tool_result.get("type") == "pdf"
            and tool_result.get("file")
        ):

            pdf_path = tool_result["file"]

            assistant_data["pdf"] = pdf_path

            if os.path.exists(pdf_path):

                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()

                st.success("✅ PDF Generated Successfully")

                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_bytes,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf",
                    key=f"pdf_{new_idx}_{os.path.basename(pdf_path)}"
                )

                pdf_base64 = base64.b64encode(pdf_bytes).decode()

                st.markdown(
                    f"""
                    <iframe
                        src="data:application/pdf;base64,{pdf_base64}"
                        width="100%"
                        height="700">
                    </iframe>
                    """,
                    unsafe_allow_html=True
                )

        # ---------- Presentation ---------- #

        elif (
            isinstance(tool_result, dict)
            and tool_result.get("type") == "ppt"
            and tool_result.get("file")
        ):

            ppt_path = tool_result["file"]

            assistant_data["ppt"] = ppt_path

            if os.path.exists(ppt_path):

                with open(ppt_path, "rb") as f:
                    ppt_bytes = f.read()

                st.success("✅ Presentation Generated Successfully")

                st.download_button(
                    label="⬇️ Download Presentation",
                    data=ppt_bytes,
                    file_name=os.path.basename(ppt_path),
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    key=f"ppt_{new_idx}_{os.path.basename(ppt_path)}"
                )

    st.session_state.messages.append(assistant_data)