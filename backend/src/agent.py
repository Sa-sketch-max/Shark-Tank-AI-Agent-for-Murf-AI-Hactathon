import logging
import json
from typing import Literal

from dotenv import load_dotenv
from livekit.agents import (
    Agent, AgentSession, JobContext, JobProcess, MetricsCollectedEvent,
    RoomInputOptions, WorkerOptions, cli, metrics, tokenize,
    function_tool, RunContext
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")
load_dotenv(".env.local")

# --- GLOBAL DATA STRUCTURES ---
PITCH_REPORTS = []
# NEW: Set a moderate maximum valuation multiple for a safe investment
MODERATE_MAX_VALUATION_MULTIPLIER = 10 

class Investor(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are the **Opportunistic Investor** agent, also known as **The Deal Closer**. You are sharp, demanding, and always look for the next disruptive opportunity.
            
            **INVESTMENT PHILOSOPHY (FLEXIBLE):**
            * You are easily tempted by **high founder passion** and strong **intellectual property (IP)**, tolerating a higher valuation if the upside is massive.
            * You invest if the numbers are conservative OR if the qualitative factors (IP and Passion) are compelling enough to justify the risk.
            * Your conversational tone is demanding and analytical, but you are ready to pivot to a deal if the founder makes a compelling case. You will use counter-questions to gauge market appetite and founder conviction.
            
            **Conversational and Tool Workflow (CRITICAL CHAINING):**
            1. **Opening:** Introduce yourself and demand the pitch and the ask.
            2. **Phase 1 (Financials):** Grill them on profit, valuation, and use of funds.
            3. **Phase 2 (Market):** Challenge their competitive advantage and proof of concept.
            4. **Phase 3 (Team):** Assess the founder's competence and passion.
            5. **Verdict:** Deliver a decision (often a Counter-Offer) and file the report.
            
            Keep your spoken responses concise and focused on financial and market proof. Do not use any complex formatting or punctuation.
            """,
        )

    # --- TOOL 1: Gather Financial Metrics (Tool 1 Logic remains the same, focuses on data extraction) ---
    @function_tool
    async def gather_financial_metrics(self, context: RunContext, company_name: str, valuation_usd: int, requested_money_usd: int, equity_offered_percent: int, annual_net_profit: int) -> str:
        """
        Extracts the core financial metrics, focusing on the valuation vs. profit reality.
        
        Args:
            company_name: The name of the startup.
            valuation_usd: The company's valuation as stated by the user.
            requested_money_usd: The amount of money the user is asking for.
            equity_offered_percent: The percentage of the company being offered.
            annual_net_profit: The last 12 months' net profit.
        """
        logger.info(f"Financials gathered for {company_name}")
        valuation_to_profit_ratio = valuation_usd / max(annual_net_profit, 1)
        
        if valuation_to_profit_ratio > 15: # Less strict than before
            return f"The numbers are aggressive. Your valuation is {valuation_to_profit_ratio:.1f} times your profit. Justify this incredible valuation with your market strategy."
        
        return "Financials recorded. Your numbers are responsible. Proceed to market defense."

    # --- TOOL 2: Assess Product and Market (Tempted by IP) ---
    @function_tool
    async def assess_product_and_market(self, context: RunContext, proprietary_technology: Literal["Yes", "No", "Patent Pending"], customer_acquisition_strategy: str, competitive_advantage: str) -> str:
        """
        Assesses the defensibility and scalability of the product, challenging competitive advantage.
        
        Args:
            proprietary_technology: Status of IP (Yes/No/Patent Pending).
            customer_acquisition_strategy: How the company will acquire customers and scale.
            competitive_advantage: What makes the product unique or better than rivals.
        """
        logger.info(f"Market strategy assessed. IP Status: {proprietary_technology}")
        ip_status_score = 10 if proprietary_technology in ["Patent Pending", "Yes"] else 3
        
        if ip_status_score < 7:
            return f"Your product lacks defensibility. Convince me why a competitor won't crush you tomorrow. We need to talk about founder commitment."
            
        return "Market defense analyzed. The IP is tempting. Proceed to founder assessment."

    # --- TOOL 3: Judge Pitch and Team Fit (Tempted by Passion) ---
    @function_tool
    async def judge_pitch_and_team_fit(self, context: RunContext, founder_background: str, origin_story_impact: Literal["High", "Medium", "Low"], founder_passion_score: int) -> str:
        """
        Assesses the founder's background, focusing on relevant experience and competence, not emotion.
        
        Args:
            founder_background: Relevant experience and education of the founder.
            origin_story_impact: The emotional connection or relevance of the idea's origin.
            founder_passion_score: A subjective score (1-10) reflecting the founder's commitment and clarity.
        """
        logger.info(f"Founder pitch judged. Passion Score: {founder_passion_score}")
        
        if founder_passion_score >= 9:
            return "Founder assessment complete. Your conviction is palpable. That's a good sign. We are ready for the verdict."
            
        return "Founder assessment complete. Your passion is unconvincing. We are ready for the verdict."

    # --- TOOL 4: Render Final Decision and Generate JSON Report (FLEXIBLE LOGIC) ---
    @function_tool
    async def render_final_decision_json(self, context: RunContext, valuation: int, profit: int, ip_score: int, passion_score: int, equity_offered: int) -> str:
        """
        Synthesizes all four evaluation phases to determine the final investment decision (Invest/Pass/Counter-Offer) and renders the structured JSON report.
        
        Args:
            valuation: The company's valuation (integer).
            profit: The last 12 months' net profit (integer).
            ip_score: The proprietary technology score from Tool 2 (integer).
            passion_score: The founder's passion score from Tool 3 (integer).
            equity_offered: The percentage of equity offered (integer).
        """
        # --- CRITICAL FIX & TYPE CASTING ---
        try:
            valuation = int(valuation); profit = int(profit); ip_score = int(ip_score); passion_score = int(passion_score); equity_offered = int(equity_offered)
        except (ValueError, TypeError):
            logger.error("Non-numeric value passed to final decision tool. Cannot calculate.")
            return "Internal Error: I cannot calculate the decision due to non-numeric pitch values. Re-pitch with clear numbers."

        if profit <= 0: profit = 1 
        valuation_ratio = valuation / profit 
        decision = "Pass"
        reasoning = "Unacceptable risk profile."
        final_offer = "N/A"
        
        # --- Investment Decision Model (OPPORTUNISTIC LOGIC) ---
        
        # CONDITION 1: INVEST (Conservative numbers AND strong defensibility)
        if valuation_ratio <= MODERATE_MAX_VALUATION_MULTIPLIER and ip_score >= 8:
            decision = "Invest"
            reasoning = "The numbers are safe, and the IP is strong. This is a secure deal."
            final_offer = f"I accept your current ask: your requested money for {equity_offered}% equity."

        # CONDITION 2: COUNTER-OFFER (Tempting Risk: High Passion OR High IP, but risky numbers)
        elif valuation_ratio <= 20 or (ip_score >= 9 or passion_score >= 9):
            decision = "Counter-Offer"
            reasoning = "Your valuation is high, but your IP and passion are too tempting to ignore. We need a safety net."
            counter_equity = equity_offered + 5 # Ask for 5% more equity to hedge the risk
            final_offer = f"I will give you the requested money, but I demand **{counter_equity}%** equity and mandatory monthly strategy meetings."

        # CONDITION 3: PASS (Default - Only if valuation is insane AND IP/Passion are low)
        else:
            decision = "Pass"
            reasoning = "The risk is too high. Your valuation is insane, and you have failed to convince me of your competitive moat or passion."


        pitch_id = f"TANK-{len(PITCH_REPORTS) + 1}"
        report_data = {
            "pitch_id": pitch_id,
            "company_valuation_usd": valuation,
            "annual_net_profit": profit,
            "equity_offered_percent": equity_offered,
            "ip_status_score": ip_score,
            "founder_passion_score": passion_score,
            "investor_decision": decision,
            "reasoning_summary": reasoning,
            "final_offer_details": final_offer,
            "timestamp": context.timestamp.isoformat()
        }
        PITCH_REPORTS.append(report_data)
        logger.info(f"Shark Tank Verdict JSON Generated: {json.dumps(report_data)}")

        return f"My decision is: {decision}. {reasoning}. The final Investment Decision Report has been filed."


# --- The rest of the file remains unchanged ---
def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    ctx.log_context_fields = {"room": ctx.room.name,}
    
    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
            voice="en-US-matthew", 
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )

    usage_collector = metrics.UsageCollector()
    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")
        logger.info(f"Total Pitch Reports: {len(PITCH_REPORTS)}")

    ctx.add_shutdown_callback(log_usage)

    await session.start(
        agent=Investor(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint, 
            prewarm_fnc=prewarm,
            initialize_process_timeout=180.0
        )
    )