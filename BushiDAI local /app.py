# app.py
# BushiDAI Local - Chat UI met streaming, upload, opslaan, instellingen

import streamlit as st
from bushidai_local_client import local
import io
import json
from datetime import datetime
from pathlib import Path

try:
    from pypdf import PdfReader
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

CHATS_DIR = Path("chats")
CHATS_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="BushiDAI Local",
    page_icon="⚔️",
    layout="centered"
)

st.title("⚔️ BushiDAI Local")
st.caption("TRUTH == TRUTH")

# --- Sessie state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_text" not in st.session_state:
    st.session_state.uploaded_text = ""
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = local.system_prompt

# --- Bestandsupload ---
with st.expander("📎 Bestand uploaden (PDF / TXT)", expanded=False):
    uploaded = st.file_uploader(
        "Kies een bestand om te gebruiken als context",
        type=["pdf", "txt", "md"],
        label_visibility="collapsed"
    )
    if uploaded is not None:
        if uploaded.type == "application/pdf" and HAS_PDF:
            reader = PdfReader(io.BytesIO(uploaded.read()))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            st.session_state.uploaded_text = text[:12000]
            st.success(f"PDF geladen ({len(reader.pages)} pagina's).")
        else:
            text = uploaded.read().decode("utf-8", errors="ignore")
            st.session_state.uploaded_text = text[:12000]
            st.success("Bestand geladen.")

    if st.session_state.uploaded_text:
        if st.button("Context wissen"):
            st.session_state.uploaded_text = ""
            st.rerun()

# --- Chatgeschiedenis ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Invoer ---
st.divider()
prompt = st.text_area("Je vraag", height=100, placeholder="Typ hier je vraag...", label_visibility="collapsed")

col1, col2 = st.columns([4, 1])
with col2:
    send = st.button("Verstuur", type="primary", use_container_width=True)

if send and prompt.strip():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    full_prompt = prompt
    if st.session_state.uploaded_text:
        full_prompt = (
            "Gebruik de volgende documenttekst als context:\n\n"
            + st.session_state.uploaded_text
            + "\n\n---\n\nVraag: "
            + prompt
        )

    # Zorg dat client de actuele system prompt gebruikt
    local.set_system_prompt(st.session_state.system_prompt)

    with st.chat_message("assistant"):
        def stream_response():
            for chunk in local.bushidai_query(full_prompt, stream=True):
                yield chunk
        full_response = st.write_stream(stream_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()

# --- Sidebar ---
with st.sidebar:
    st.header("Instellingen")

    # Modelkiezer
    models = local.get_available_models()
    if models:
        selected = st.selectbox("Model", models, index=models.index(local.model) if local.model in models else 0)
        if selected != local.model:
            local.model = selected

    # Temperatuur
    local.temperature = st.slider("Temperatuur", 0.0, 1.5, float(local.temperature), 0.05)

    st.divider()

    # Systeem prompt
    with st.expander("Systeem prompt", expanded=False):
        new_prompt = st.text_area(
            "Bewerk de systeem prompt",
            value=st.session_state.system_prompt,
            height=250,
            label_visibility="collapsed"
        )
        if st.button("Prompt opslaan", use_container_width=True):
            st.session_state.system_prompt = new_prompt
            local.set_system_prompt(new_prompt)
            st.success("Systeem prompt bijgewerkt")

    st.divider()
    st.header("Chat")

    if st.button("Nieuwe chat", use_container_width=True):
        st.session_state.messages = []
        local.clear_history()
        st.session_state.current_chat = None
        st.rerun()

    if st.session_state.messages:
        chat_name = st.text_input("Chatnaam", value=datetime.now().strftime("%Y-%m-%d %H:%M"))
        if st.button("Chat opslaan", use_container_width=True):
            path = CHATS_DIR / f"{chat_name}.json"
            path.write_text(json.dumps(st.session_state.messages, ensure_ascii=False, indent=2), encoding="utf-8")
            st.success(f"Opgeslagen: {chat_name}")

    saved = list(CHATS_DIR.glob("*.json"))
    if saved:
        choice = st.selectbox("Opgeslagen chats", ["— kies —"] + [p.stem for p in saved])
        if choice != "— kies —" and st.button("Chat laden", use_container_width=True):
            data = json.loads((CHATS_DIR / f"{choice}.json").read_text(encoding="utf-8"))
            st.session_state.messages = data
            st.session_state.current_chat = choice
            local.clear_history()
            st.rerun()

    st.divider()
    st.caption(f"Context: {local.num_ctx}")
    if st.session_state.uploaded_text:
        st.caption("📄 Context actief")