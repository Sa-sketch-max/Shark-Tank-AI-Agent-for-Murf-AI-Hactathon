

# 🦈 **Venture Scrutinizer: The Opportunistic Investor**

**Submission for:** *Murf AI Voice Agent Hackathon — IIT Bombay Techfest*

<img width="1860" height="902" alt="Image" src="https://github.com/user-attachments/assets/3f6deaed-632d-45f0-8829-08098c24c1e2" />

## 🎯 **Project Goal**

To build a high-stakes, multi-tool **AI voice agent** that behaves like a demanding, interrogative venture capitalist.
The agent conducts a structured **financial interrogation**, evaluates the pitch across multiple dimensions, and outputs an **auditable investment decision** using JSON.

---

# 🌟 **Core Innovation: Agentic Decision-Making Pipeline**

Unlike simple Q&A bots, this system executes a **4-stage autonomous reasoning chain** known as **The Interrogation Chain**, powered by LiveKit Agents.

Each stage feeds into the next using tool outputs, enabling realistic VC-style scrutiny and decision-making.

---

# ⚙️ **Technical Stack**

### **Voice & Agent Orchestration**

* **LiveKit Agents (Python SDK)** for real-time agent workflows
* **Deepgram** for Speech-to-Text
* **Murf AI** for Text-to-Speech to generate a demanding investor persona
* **Google Gemini 2.5 Flash** for tool orchestration, reasoning, and decision logic

### **Frontend**

* **React + TypeScript + Tailwind CSS**
* Styled as a *Shark Tank-themed* interactive pitch interface

---

# 🔑 **Key Features**

### ✅ **1. Multi-Tool Chaining**

The LLM controls four custom tools, each dependent on the output of the previous one—demonstrating advanced agent autonomy.

### ✅ **2. Financial Scrutiny**

Extracts and validates:

* Profit
* Revenue
* Valuation
* Founder ask
* Equity offered

### ✅ **3. Market & Product Defense**

Challenges:

* IP defensibility
* Market moat
* Scalability of solution

### ✅ **4. Qualitative Founder Assessment**

Scores the founder based on:

* Passion
* Experience
* Communication quality

### ✅ **5. Structured JSON Verdict**

Final output is a strict, machine-readable **Investment Decision Report**, not plain text.

### ✅ **6. Opportunistic Investment Logic**

Risk-tolerant VC behavior:

* Will invest despite weak numbers **if IP or Founder Passion is high**
* Generates **Invest, Pass, or Counter-Offer** decisions

---

# 🎥 **Demo Video (Important)**

🔗 **Demo Video:**
`https://drive.google.com/file/d/1COtkj9DjbLkVM_xYLe4rEUJc0i0hMoZe/view?usp=drive_link`

---

# 🧠 **The Interrogation Chain — Tool Workflow**

1. **gather_financial_metrics**
   Extracts raw financials: Profit, Valuation, Ask, Equity.

2. **assess_product_and_market**
   Evaluates defensibility, strategy, competition, and scalability.

3. **judge_pitch_and_team_fit**
   Scores founder’s passion, clarity, and operational competence.

4. **render_final_decision_json**
   Outputs final structured verdict (Invest / Pass / Counter-Offer).

---

# ▶️ **Setup & Run Instructions**

## 📦 **Install Dependencies**

```bash
pip install livekit-agents livekit-plugins[google,deepgram,murf,silero,turn_detector] python-dotenv
```

---

## 🔑 **Environment Setup**

Create `.env.local` and add:

```
LIVEKIT_URL=
LIVEKIT_API_KEY=
LIVEKIT_SECRET_KEY=
GEMINI_API_KEY=
DEEPGRAM_API_KEY=
MURF_API_KEY=
```

---

## 🚀 **Run Backend Agent**

```bash
python agent.py
```

---

## 🖥️ **Run Frontend**

```bash
npm install
npm run dev
```

---

# 📚 **Repository Structure (Suggested)**

```
/agent
  ├── agent.py
  ├── tools/
  └── utils/

/frontend
  ├── src/
  ├── components/
  └── pages/

README.md
.env.example
```

---

# 🏁 **Final Notes**

This project demonstrates a **realistic venture-capital interrogation workflow**, combining:

* autonomous agents
* multimodal LLM reasoning
* voice interactivity
* professional TTS persona
* structured programmatic decisions

A perfect fit for the **Murf AI Voice Agent Hackathon**.

## 🏷️ Tags
- Murf AI
- Voice AI
- Shark Tank AI Agent


