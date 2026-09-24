import streamlit as st
import snowflake_utils as sf
from components.helpers import extract_thinking_and_response

def render():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    selected_prompt = None

    # =========================================================================
    # EMPTY STATE: WELCOME BANNER, SUGGESTED QUICK INQUIRIES, EMPTY STATE GUIDE
    # =========================================================================
    if not st.session_state.messages:
        # Welcome Banner Header
        st.markdown("""
        <div class="chat-welcome-banner">
            <div style="display:flex; align-items:center; gap:16px;">
                <div style="font-size:32px; background:#EFF6FF; border:1px solid #BFDBFE; border-radius:12px; width:52px; height:52px; display:flex; align-items:center; justify-content:center;">💬</div>
                <div>
                    <h2>Welcome to Chat Assistant</h2>
                    <p style="margin-top:4px; color:#64748B;">Ask anything about your policies, claims, fraud analysis, or actuarial risk metrics. Attach an image to estimate insurance claims. Powered by live Snowflake Cortex AI.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card-panel" style="padding:16px 20px; margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="font-size:13px; font-weight:700; color:#334155;">💡 Suggested Quick Inquiries</div>
                <div style="font-size:11px; background:#F0FDF4; color:#166534; padding:3px 8px; border-radius:12px; font-weight:600;">Live Cortex Agent</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quick Question Buttons - Row 1
        q_col1, q_col2, q_col3 = st.columns(3)
        with q_col1:
            if st.button("🔍 Auto policies likely to churn?", use_container_width=True):
                selected_prompt = "Which of my auto policies are most likely to churn in the next 30 days?"

        with q_col2:
            if st.button("⚠️ Why was CLM-00381 flagged?", use_container_width=True):
                selected_prompt = "Show me why CLM-00381 was flagged for fraud"

        with q_col3:
            if st.button("💰 Estimate premium for 35yo $60k", use_container_width=True):
                selected_prompt = "Estimate premium for age 35, annual income $60000, credit score 700, coverage $250000"

        # Quick Question Buttons - Row 2
        q_col4, q_col5, q_col6 = st.columns(3)
        with q_col4:
            if st.button("📊 Show top 5 loss ratio policies", use_container_width=True):
                selected_prompt = "Show top 5 highest loss ratio policies"

        with q_col5:
            if st.button("🛡️ Summarize high risk fraud alerts", use_container_width=True):
                selected_prompt = "Summarize high risk fraud alerts"

        with q_col6:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

        # Quick Question Buttons - Row 3: Image-based (dynamic from stage)
        q_col7, q_col8, q_col9 = st.columns(3)
        stage_files = sf.list_stage_files()
        image_files = [f for f in stage_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        with q_col7:
            if st.button("📷 Analyze claim evidence photo", use_container_width=True):
                if image_files:
                    selected_prompt = (
                        f"The following image files are available in the claim evidence stage: {', '.join(image_files)}. "
                        f"Please analyze the first image '{image_files[0]}' and estimate the insurance claim amount. "
                        f"Show the image analysis, then query the database for comparison data, and justify every number."
                    )
                else:
                    selected_prompt = "No evidence images found in the claim evidence stage. Please upload images first."

        with q_col8:
            if st.button("📊 Compare all evidence images", use_container_width=True):
                if len(image_files) >= 2:
                    selected_prompt = (
                        f"Analyze EACH of these evidence images one by one: {', '.join(image_files)}. "
                        f"For each image, identify damage type and estimate costs. "
                        f"Then query the database for average claim amounts by damage type and compare. "
                        f"Provide a combined total claim estimate with full justification."
                    )
                elif image_files:
                    selected_prompt = f"Analyze the evidence image '{image_files[0]}' and estimate the claim with database comparison."
                else:
                    selected_prompt = "No evidence images found in stage. Please upload images first."

        with q_col9:
            if st.button("📄 Verify invoice against policy", use_container_width=True):
                invoice_files = [f for f in image_files if 'invoice' in f.lower()]
                if invoice_files:
                    selected_prompt = (
                        f"Analyze the invoice image '{invoice_files[0]}' and verify whether the amounts "
                        f"are consistent with actual policy coverage and claim amounts in the database. "
                        f"Query the semantic model for real coverage limits and deductibles to compare against."
                    )
                elif image_files:
                    selected_prompt = f"Analyze '{image_files[0]}' and compare the estimated damage costs with actual policy data from the database."
                else:
                    selected_prompt = "No evidence files found in stage. Please upload images first."

        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

        # Empty State Guide Box
        st.markdown("""
        <div style="background:#FFFFFF; border:1px dashed #CBD5E1; border-radius:12px; padding:32px 24px; text-align:center; margin-bottom:20px;">
            <div style="font-size:40px; margin-bottom:10px;">🤖❄️</div>
            <h4 style="margin:0 0 6px 0; font-size:16px; font-weight:700; color:#1E293B;">How can I assist your underwriting & claims team today?</h4>
            <p style="margin:0 auto; max-width:520px; font-size:13px; color:#64748B; line-height:1.5;">
                Connected to live insurance database. Click a quick inquiry button above, type a question below, or <b>attach a damage photo</b> to estimate a claim.
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        # =========================================================================
        # ACTIVE CHAT STATE: TOP HEADER WITH CLEAR BUTTON
        # =========================================================================
        header_c1, header_c2 = st.columns([3, 1])
        with header_c1:
            st.markdown("""
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:16px;">
                <div style="font-size:24px; background:#EFF6FF; border:1px solid #BFDBFE; border-radius:10px; width:42px; height:42px; display:flex; align-items:center; justify-content:center;">💬</div>
                <div>
                    <div style="font-weight:700; color:#0F172A; font-size:16px;">Insurance Intelligence Assistant</div>
                    <div style="font-size:12px; color:#64748B;">Connected to live insurance database</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with header_c2:
            if st.button("🗑️ Clear Chat History", key="active_clear_chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

    # =========================================================================
    # RENDER CHAT HISTORY (Chronological ChatGPT-style format)
    # =========================================================================
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                if msg.get("image"):
                    st.image(msg["image"], caption=msg.get("image_name"), width=320)
                if msg.get("content"):
                    st.markdown(msg["content"])
        else:
            with st.chat_message("assistant"):
                agent_title = msg.get("agent", "INSURANCE_INTELLIGENCE_ASSISTANT")
                thinking_text = msg.get("thinking", "")
                clean_content = msg.get("content", "")

                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:8px; font-weight:700; font-size:12px; text-transform:uppercase; letter-spacing:0.6px; color:#059669; margin-bottom:8px;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="#10B981">
                        <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2M7.5 13A2.5 2.5 0 0 0 5 15.5 2.5 2.5 0 0 0 7.5 18a2.5 2.5 0 0 0 2.5-2.5A2.5 2.5 0 0 0 7.5 13m9 0a2.5 2.5 0 0 0-2.5 2.5 2.5 2.5 0 0 0 2.5 2.5 2.5 2.5 0 0 0 2.5-2.5 2.5 2.5 0 0 0-2.5-2.5"/>
                    </svg>
                    <span>{agent_title}</span>
                </div>
                """, unsafe_allow_html=True)

                if thinking_text:
                    resp_tab, think_tab = st.tabs(["💬 Response", "🧠 Thinking Process"])
                    with resp_tab:
                        st.markdown(clean_content)
                    with think_tab:
                        thinking_formatted = thinking_text.replace("\n", "<br>")
                        st.markdown(f"""
                        <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-left:4px solid #0284C7; border-radius:8px; padding:12px 16px; font-family:'JetBrains Mono', monospace; font-size:12px; color:#334155; line-height:1.6;">
                            <div style="font-weight:700; color:#0284C7; margin-bottom:8px; text-transform:uppercase; font-size:11px; letter-spacing:0.5px;">⚙️ Execution & Reasoning Trace</div>
                            {thinking_formatted}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(clean_content)

    # =========================================================================
    # NATIVE STREAMLIT CHAT INPUT WITH FILE ATTACHMENT (+)
    # =========================================================================
    chat_input_val = st.chat_input(
        "Ask about policies, claims, fraud, risk, or attach a claim evidence photo...",
        accept_file=True,
        file_type=["jpg", "jpeg", "png"],
        key="main_chat_input"
    )

    prompt_to_process = None
    user_text_display = None
    image_bytes_to_store = None
    image_name_to_store = None

    if chat_input_val:
        user_text = ""
        uploaded_files = []
        if hasattr(chat_input_val, "text") and chat_input_val.text:
            user_text = chat_input_val.text.strip()
        elif isinstance(chat_input_val, dict) and chat_input_val.get("text"):
            user_text = chat_input_val.get("text", "").strip()

        if hasattr(chat_input_val, "files") and chat_input_val.files:
            uploaded_files = chat_input_val.files
        elif isinstance(chat_input_val, dict) and chat_input_val.get("files"):
            uploaded_files = chat_input_val.get("files", [])

        if uploaded_files:
            file_obj = uploaded_files[0]
            image_bytes_to_store = file_obj.getvalue()
            image_name_to_store = file_obj.name.replace(" ", "_")

            with st.spinner(f"Uploading {image_name_to_store} to Snowflake stage..."):
                upload_ok = sf.upload_image_to_stage(image_bytes_to_store, image_name_to_store)

            if upload_ok:
                user_msg = user_text if user_text else f"Analyze attached evidence image: {image_name_to_store}"
                user_text_display = user_msg
                prompt_to_process = (
                    f"{user_msg} "
                    f"The image file is named {image_name_to_store} and is in the claim evidence stage. "
                    f"Use the ANALYZE_CLAIM_IMAGE tool with IMAGE_FILENAME={image_name_to_store} to analyze it."
                )
            else:
                st.error(f"Failed to upload {image_name_to_store} to stage. Check stage permissions.")
        elif user_text:
            user_text_display = user_text
            prompt_to_process = user_text

    elif selected_prompt:
        user_text_display = selected_prompt
        prompt_to_process = selected_prompt

    # =========================================================================
    # PROCESS PROMPT & GENERATE ASSISTANT RESPONSE
    # =========================================================================
    if prompt_to_process:
        # 1. Append user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_text_display,
            "image": image_bytes_to_store,
            "image_name": image_name_to_store
        })

        # 2. Show thinking loader for assistant inside st.chat_message
        with st.chat_message("assistant"):
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:8px; font-weight:700; font-size:12px; text-transform:uppercase; letter-spacing:0.6px; color:#0284C7; margin-bottom:8px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="#0284C7">
                    <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2M7.5 13A2.5 2.5 0 0 0 5 15.5 2.5 2.5 0 0 0 7.5 18a2.5 2.5 0 0 0 2.5-2.5A2.5 2.5 0 0 0 7.5 13m9 0a2.5 2.5 0 0 0-2.5 2.5 2.5 2.5 0 0 0 2.5 2.5 2.5 2.5 0 0 0 2.5-2.5 2.5 2.5 0 0 0-2.5-2.5"/>
                </svg>
                <span>INSURANCE_INTELLIGENCE_ASSISTANT</span>
                <span style="font-size:11px; background:#E0F2FE; color:#0369A1; padding:2px 8px; border-radius:10px; font-weight:600; margin-left:auto;">Thinking...</span>
            </div>
            """, unsafe_allow_html=True)
            with st.spinner("Querying Insurance Master Agent..."):
                try:
                    raw_response = sf.ask_cortex_agent(prompt_to_process)
                    real_thinking = sf.parse_agent_thinking(raw_response)
                    thinking_process, clean_resp = extract_thinking_and_response(raw_response, prompt_to_process)
                    if real_thinking:
                        thinking_process = real_thinking
                    agent_name = "INSURANCE_INTELLIGENCE_ASSISTANT"
                except Exception as e:
                    thinking_process = f"Execution Error: {e}"
                    clean_resp = f"Snowflake Query Error: {e}"
                    agent_name = "SNOWFLAKE_ERROR"

        st.session_state.messages.append({
            "role": "assistant",
            "agent": agent_name,
            "thinking": thinking_process,
            "content": clean_resp
        })
        st.rerun()