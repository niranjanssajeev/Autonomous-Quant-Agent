## 🧠 System Architecture (The 4 Agents)

```mermaid
graph TD
    A[Autopilot Schedule] -->|16:00 IST| B(Agent 1: Data Harvester)
    B -->|yfinance API| C[(Master Database CSV)]
    C -->|Live Updates| D(Agent 2: Streamlit Visualizer)
    
    A -->|Triggers| E(Agent 3: Sentiment Analyst)
    E -->|Scrapes Web| F[Financial News]
    F -->|Headlines| E
    E -->|Gemini API Score| G(Agent 4: Predictive Quant)
    
    C -->|Historical Math| G
    G -->|Random Forest ML| H[(Audit Log CSV)]
