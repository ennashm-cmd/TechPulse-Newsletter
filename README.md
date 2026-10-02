# Build Your Own Autonomous AI Tech Newsletter with Streamlit and CrewAI

### Introduction

Staying on top of the rapidly evolving tech landscape can feel like a full-time job. Between daily breakthrough announcements, product launches, and industry shifts, keeping a pulse on the industry takes hours of manual scrolling and research.

What if you could automate the entire process?

In this tutorial, we will explore how to build **TechPulse Newsletter Studio**—an autonomous multi-agent web application powered by **CrewAI** and **Streamlit**. With just a single click, an AI researcher agent scours the live web for top tech stories, and a dedicated writer agent condenses them into a punchy executive newsletter.

### What is CrewAI?

**CrewAI** is a cutting-edge framework designed for orchestrating role-playing autonomous AI agents. By breaking down complex workflows into collaborative roles (such as researchers, writers, and editors), agents can delegate tasks, share context through sequential pipelines, and execute complex workflows autonomously.

In our **TechPulse** architecture:

* **The Lead Tech News Researcher:** Equipped with the `SerperDevTool`, this agent crawls real-time web search results to isolate major technology breakthroughs.
* **The Concise Newsletter Writer:** An isolated copywriter agent with zero tools, relying strictly on the research passed down through the pipeline to format a clean, concise executive summary.

### How to Run Your Application

1. **Clone or Save the Script:** Save the code above into a file named `app.py`.
2. **Install Dependencies:**
pip install streamlit crewai crewai-tools python-dotenv

3. **Launch the Streamlit App:**
streamlit run app.py

4. **Input Your Keys:** Open the sidebar, enter your OpenAI API key and Serper API key, and hit **Run Tech News Crew** to generate your automated brief!
