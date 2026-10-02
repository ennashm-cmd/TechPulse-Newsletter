import streamlit as st
from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, LLM, Process
from crewai_tools import SerperDevTool

# Load environment variables from .env file
load_dotenv()

# Page configuration for a professional tech dashboard theme
st.set_page_config(
    page_title="TechPulse Newsletter Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Tech Theme CSS Styling (Dark/Neon accent modern dashboard)
st.markdown("""
    <style>
    .main-title { font-size: 2.3rem; font-weight: 800; color: #0F172A; letter-spacing: -0.025em; }
    .sub-desc { font-size: 1.05rem; color: #475569; margin-bottom: 25px; }
    .newsletter-card { background: #0F172A; color: #F8FAFC; padding: 25px; border-radius: 12px; border: 1px solid #334155; font-family: monospace; font-size: 1.05rem; line-height: 1.6; }
    .stButton>button { background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); color: white; font-weight: 600; border-radius: 8px; border: none; padding: 0.6rem 1.2rem; }
    .stButton>button:hover { background: linear-gradient(135deg, #1D4ED8 100%, #1E40AF 100%); }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# SIDEBAR: API Configurations & Quick Status
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ TechPulse Control")
    st.info("**Engine:** CrewAI Sequential Crew\n\n**Architecture:** Researcher + Writer Model")
    
    st.divider()
    
    st.markdown("### 🔑 API Credentials")
    openai_key_input = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    serper_key_input = st.text_input("Serper API Key", type="password", value=os.getenv("SERPER_API_KEY", ""))
    
    if st.button("Save & Secure Keys", use_container_width=True):
        if openai_key_input:
            os.environ["OPENAI_API_KEY"] = openai_key_input
        if serper_key_input:
            os.environ["SERPER_API_KEY"] = serper_key_input
        st.success("Credentials saved to environment!")

    st.markdown("---")
    st.caption("Tech Newsletter Engine v1.0 • Powered by CrewAI")

# -------------------------------------------------------------
# MAIN LAYOUT: Tech Newsletter Studio
# -------------------------------------------------------------
st.markdown('<p class="main-title">⚡ TechPulse Newsletter Studio</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-desc">Autonomous multi-agent pipeline: A web-scraping Researcher pinpoints today’s top 3 tech stories, and a dedicated Writer formats them into a high-impact, exact 5-line executive newsletter.</p>', unsafe_allow_html=True)

# Interactive Studio Layout
col_workspace, col_info = st.columns([2, 1], gap="large")

with col_workspace:
    st.markdown("#### 🚀 Dispatch Newsletter Agent Crew")
    
    # Configuration options for the newsletter run (using correct crewai provider paths)
    model_choice = st.selectbox("Select LLM Core Engine", ["openai/gpt-4o-mini", "openai/gpt-4o"])
    
    run_crew_btn = st.button("🔴 Run Tech News Crew", type="primary", use_container_width=True)

    if run_crew_btn:
        current_openai = os.getenv("OPENAI_API_KEY")
        current_serper = os.getenv("SERPER_API_KEY")
        
        if not current_openai or not current_serper:
            st.error("⚠️ Missing API Keys! Please configure OpenAI and Serper API keys in the sidebar.")
        else:
            try:
                # Initialize LLM & Web Search Tool
                llm = LLM(model=model_choice)
                search_tool = SerperDevTool()

                # 1. Define Agents (Researcher with tool, Writer with NO tools)
                researcher = Agent(
                    role="Lead Tech News Researcher",
                    goal="Search the web and find today's top 3 breakthrough technology news stories.",
                    backstory="You are an expert tech scout who scours live web data for major industry shifts, product launches, and breakthroughs.",
                    tools=[search_tool],
                    llm=llm,
                    verbose=True
                )

                writer = Agent(
                    role="Concise Newsletter Writer",
                    goal="Turn the provided research data into an engaging, punchy, exact 5-line newsletter summary.",
                    backstory="You are a master newsletter copywriter known for extreme brevity, impactful insights, and strict adherence to structural formatting.",
                    tools=[],  # Explicitly has no search tools
                    llm=llm,
                    verbose=True
                )

                # 2. Define Tasks with explicit sequential context passing
                research_task = Task(
                    description="Search the web and identify today's top 3 most important and trending technology news stories.",
                    expected_output="A detailed summary of today's top 3 tech news stories with key highlights and context.",
                    agent=researcher
                )

                write_task = Task(
                    description="Using the research output provided by the researcher, write a punchy tech newsletter that is formatted into exactly 5 lines.",
                    expected_output="An exact 5-line newsletter summary highlighting the top 3 tech stories.",
                    agent=writer,
                    context=[research_task]  # Explicitly passes researcher's result into the writer task
                )

                # 3. Assemble Crew with sequential process execution
                tech_crew = Crew(
                    agents=[researcher, writer],
                    tasks=[research_task, write_task],
                    process=Process.sequential,
                    verbose=True
                )

                with st.spinner("🛰️ Crew active: Researcher scouring live web -> Writer compiling exact 5-line dispatch..."):
                    # Execute crew kickoff
                    result = tech_crew.kickoff()

                st.success("✅ Newsletter Successfully Compiled!")
                st.markdown("### 📨 Your Final 5-Line Newsletter Output")
                
                # Render inside a sleek dark mode container
                st.markdown(f'<div class="newsletter-card">{result.raw}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Execution Error: {e}")

with col_info:
    st.markdown("### ⚙️ Architecture Specs")
    st.markdown("""
    * **Process:** Sequential (`Process.sequential`)
    * **Agent 1 (Researcher):** Equipped with `SerperDevTool` to pull live web updates.
    * **Agent 2 (Writer):** Isolated with zero tools; relies solely on passed context.
    * **Output Rule:** Strictly engineered for an exact 5-line dispatch.
    """)
    st.markdown("---")
    st.info("💡 **Tip:** Ensure your Serper API key has active request quotas for real-time web scraping.")