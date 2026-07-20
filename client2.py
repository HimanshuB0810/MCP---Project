import asyncio
import json
import streamlit as st
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage

load_dotenv()

SERVERS = {
    "maths": {
        "transport": "stdio",
        "command": "/home/himanshu-borikar/.local/bin/uv",
        "args": [
            "run",
            "fastmcp",
            "run",
            "/home/himanshu-borikar/Desktop/Himanshu/GENERATIVE AI & AGENTIC AI/MCP/Maths-MCP_Server_Local/main.py"
        ]
    },
    "expense": {
        "transport": "stdio",
        "command": "/home/himanshu-borikar/.local/bin/uv",
        "args": [
            "run",
            "fastmcp",
            "run",
            "/home/himanshu-borikar/Desktop/Himanshu/GENERATIVE AI & AGENTIC AI/MCP/Expense_Tracker_MCP_Server/main.py"
        ]
    },
    "manim-server": {
        "transport": "stdio",
        "command": "/home/himanshu-borikar/Desktop/Himanshu/GENERATIVE AI & AGENTIC AI/MCP/venv/bin/python",
        "args": [
            "/home/himanshu-borikar/Desktop/Himanshu/GENERATIVE AI & AGENTIC AI/MCP/manim-mcp-server/src/manim_server.py"
        ],
        "env": {
            "MANIM_EXECUTABLE": "/home/himanshu-borikar/Desktop/Himanshu/GENERATIVE AI & AGENTIC AI/MCP/venv/bin/manim"
        }
    }
}

SYSTEM_PROMPT = (
    "You have access to tools, but you should only use them when the user's "
    "request actually needs one (e.g. math calculations). For general knowledge "
    "questions you already know the answer to, just answer directly without "
    "calling a tool."
)


async def dispatch(prompt: str, model_choice: str, log: list):
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()

    named_tools = {}
    for tool in tools:
        named_tools[tool.name] = tool

    log.append(("info", f"tools online: {', '.join(named_tools.keys())}"))

    if model_choice == "Groq · llama-3.3-70b-versatile":
        llm = ChatGroq(model="llama-3.3-70b-versatile")
    else:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    llm_with_tools = llm.bind_tools(tools)

    response = await llm_with_tools.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ])

    if not getattr(response, "tool_calls", None):
        log.append(("final", response.content))
        return response.content

    tool_messages = []
    final_response = None
    for tc in response.tool_calls:

        selected_tool = tc['name']
        selected_tool_args = tc['args']
        tool_call_id = tc["id"]

        log.append(("call", f"{selected_tool}  ({json.dumps(selected_tool_args)})"))

        tool_result = await named_tools[selected_tool].ainvoke(selected_tool_args)
        log.append(("result", str(tool_result)))

        tool_messages.append(ToolMessage(content=json.dumps(tool_result), tool_call_id=tool_call_id))

        final_response = await llm.ainvoke(([prompt, response, *tool_messages]))
        log.append(("final", final_response.content))

    return final_response.content if final_response else None


st.set_page_config(page_title="⚙ The Toolbench", page_icon="🛠️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background-color: #0B1D33;
    background-image:
        linear-gradient(#132a45 1px, transparent 1px),
        linear-gradient(90deg, #132a45 1px, transparent 1px);
    background-size: 34px 34px;
    background-position: -1px -1px;
    color: #EDEFF2;
}

section[data-testid="stSidebar"] {
    background-color: #0E2138;
    border-right: 1px solid #1E3A57;
}

.rack-title {
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 3px;
    font-size: 0.7rem;
    color: #7E93A8;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.rack-unit {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #122A44;
    border: 1px solid #1E3A57;
    border-radius: 4px;
    padding: 10px 12px;
    margin-bottom: 8px;
}

.led {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #E8A33D;
    box-shadow: 0 0 6px 2px rgba(232, 163, 61, 0.55);
    flex-shrink: 0;
}

.led.idle {
    background: #3A5068;
    box-shadow: none;
}

.rack-unit-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #D9E2EA;
}

.rack-unit-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #5E7690;
    margin-left: auto;
}

h1.console-header {
    font-weight: 700;
    font-size: 2.1rem;
    letter-spacing: -0.5px;
    margin-bottom: 0px;
}

.console-sub {
    font-family: 'JetBrains Mono', monospace;
    color: #6F88A3;
    font-size: 0.85rem;
    margin-top: -6px;
    margin-bottom: 22px;
}

.panel {
    background: #0E2138;
    border: 1px solid #1E3A57;
    border-radius: 6px;
    padding: 18px 20px;
}

.trace-line {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    padding: 6px 0;
    border-bottom: 1px dashed #1E3A57;
    display: flex;
    gap: 10px;
}

.trace-tag {
    flex-shrink: 0;
    font-size: 0.68rem;
    padding: 2px 6px;
    border-radius: 3px;
    height: fit-content;
    letter-spacing: 1px;
}

.tag-call { background: rgba(232, 163, 61, 0.15); color: #E8A33D; border: 1px solid rgba(232,163,61,0.4); }
.tag-result { background: rgba(79, 176, 165, 0.15); color: #4FB0A5; border: 1px solid rgba(79,176,165,0.4); }
.tag-info { background: rgba(126, 147, 168, 0.15); color: #7E93A8; border: 1px solid rgba(126,147,168,0.35); }
.tag-final { background: rgba(237, 239, 242, 0.1); color: #EDEFF2; border: 1px solid rgba(237,239,242,0.3); }

.ticket {
    font-family: 'JetBrains Mono', monospace;
    background: #122A44;
    border-left: 3px solid #E8A33D;
    padding: 16px 18px;
    border-radius: 2px;
    line-height: 1.55;
    color: #EDEFF2;
}

div[data-testid="stTextArea"] textarea {
    background: #0E2138 !important;
    color: #EDEFF2 !important;
    border: 1px solid #2A4A6B !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.stButton > button {
    background: #E8A33D;
    color: #0B1D33;
    font-weight: 700;
    border: none;
    border-radius: 4px;
    letter-spacing: 1px;
    padding: 0.6rem 1.4rem;
}

.stButton > button:hover {
    background: #F2B85B;
    color: #0B1D33;
}

.stSelectbox label, .stTextArea label { 
    font-family: 'JetBrains Mono', monospace;
    color: #7E93A8 !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

if "log" not in st.session_state:
    st.session_state.log = []
if "answer" not in st.session_state:
    st.session_state.answer = None
if "busy" not in st.session_state:
    st.session_state.busy = False

with st.sidebar:
    st.markdown('<div class="rack-title">Connected servers</div>', unsafe_allow_html=True)
    unit_meta = {
        "maths": "arithmetic · stdio",
        "expense": "ledger · stdio",
        "manim-server": "animation · stdio",
    }
    for name in SERVERS:
        lit = "led" if st.session_state.busy else "led idle"
        st.markdown(f"""
        <div class="rack-unit">
            <div class="{lit}"></div>
            <div class="rack-unit-name">{name}</div>
            <div class="rack-unit-sub">{unit_meta.get(name, "stdio")}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="rack-title" style="margin-top:22px;">Model</div>', unsafe_allow_html=True)
    model_choice = st.selectbox(
        "Model",
        ["Groq · llama-3.3-70b-versatile", "Gemini · 2.5-flash"],
        label_visibility="collapsed",
    )

st.markdown('<h1 class="console-header">⚙ The Toolbench</h1>', unsafe_allow_html=True)
st.markdown('<div class="console-sub">local mcp servers · groq / gemini</div>', unsafe_allow_html=True)

col_input, col_gap = st.columns([3, 1])
with col_input:
    prompt = st.text_area(
        "Request",
        placeholder="e.g. Add an expense of Rs 9000 for shopping on 18 July 2026",
        height=100,
        label_visibility="collapsed",
    )
    send = st.button("SEND →", disabled=st.session_state.busy)

if send and prompt.strip():
    st.session_state.busy = True
    st.session_state.log = []
    st.session_state.answer = None
    with st.spinner("routing request through the rack…"):
        try:
            result = asyncio.run(dispatch(prompt, model_choice, st.session_state.log))
            st.session_state.answer = result
        except Exception as e:
            st.session_state.log.append(("info", f"error: {e}"))
    st.session_state.busy = False

st.write("")
left, right = st.columns([1.1, 1])

with left:
    st.markdown('<div class="rack-title">Trace</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        if not st.session_state.log:
            st.markdown('<span style="color:#4A6280; font-family: JetBrains Mono, monospace; font-size:0.82rem;">nothing dispatched yet</span>', unsafe_allow_html=True)
        else:
            tag_map = {"call": "tag-call", "result": "tag-result", "info": "tag-info", "final": "tag-final"}
            label_map = {"call": "CALL", "result": "RESULT", "info": "INFO", "final": "DONE"}
            for kind, text in st.session_state.log:
                text_display = text if len(str(text)) < 300 else str(text)[:300] + " …"
                st.markdown(
                    f'<div class="trace-line"><span class="trace-tag {tag_map.get(kind, "tag-info")}">{label_map.get(kind, "LOG")}</span>'
                    f'<span>{text_display}</span></div>',
                    unsafe_allow_html=True,
                )
        st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="rack-title">Response</div>', unsafe_allow_html=True)
    if st.session_state.answer:
        st.markdown(f'<div class="ticket">{st.session_state.answer}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="panel" style="color:#4A6280; font-family: JetBrains Mono, monospace; font-size:0.82rem;">awaiting a request</div>', unsafe_allow_html=True)