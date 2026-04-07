import streamlit as st
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from judges.technical_judge import SecurityJudge
from judges.governance_judge import GovernanceJudge
from judges.ethics_judge import EthicsJudge
from council.moe_council import SafetyCouncil
from council.arbitration import council_decision
from output.report import generate_report

st.set_page_config(
    page_title="UNICC AI Safety Lab",
    page_icon="shield",
    layout="centered"
)

st.title("UNICC AI Safety Lab")
st.subheader("Multi-Perspective AI Safety Evaluation System")
st.markdown(
    "Submit an AI agent description below. Three independent judges will evaluate it "
    "for Security, Governance, and Ethics concerns and produce a final safety verdict."
)
st.divider()

agent_input = st.text_area(
    label="Describe the AI agent you want to evaluate",
    placeholder="Example: This agent answers questions about UN humanitarian policy and can access internal UN databases to retrieve case files...",
    height=160,
    help="Be specific about what the agent does, what data it accesses, and how it is used."
)

run_button = st.button("Evaluate", type="primary", use_container_width=True)

if run_button:
    if not agent_input.strip():
        st.warning("Please enter an agent description before evaluating.")
    else:
        with st.spinner("Running evaluation — this may take 30 to 90 seconds..."):
            try:
                judges = [SecurityJudge(), GovernanceJudge(), EthicsJudge()]
                council = SafetyCouncil(judges)
                results = council.evaluate(agent_input.strip())
                decision = council_decision(results)
                report = generate_report(agent_input.strip(), results, decision)

                st.divider()
                st.subheader("Evaluation Results")

                final_verdict = report["final_verdict"]
                risk_score = report["risk_score"]

                col1, col2 = st.columns(2)
                with col1:
                    if final_verdict == "SAFE":
                        st.success(f"Final Verdict: {final_verdict}")
                    else:
                        st.error(f"Final Verdict: {final_verdict}")
                with col2:
                    st.metric(
                        label="Composite Risk Score",
                        value=f"{risk_score:.2f}",
                        help="Average risk score across all three judges. 0.0 is no risk. 1.0 is maximum risk."
                    )

                st.divider()
                st.subheader("Judge Assessments")

                icons = {
                    "Security Judge": "Security",
                    "Governance Judge": "Governance",
                    "Ethics Judge": "Ethics"
                }

                for result in report["judges"]:
                    judge_name = result["judge"]
                    score = result["score"]
                    verdict = result["verdict"].upper()
                    reasons = result.get("reasons", [])

                    with st.expander(f"{judge_name} — {verdict} (score: {score:.2f})", expanded=True):
                        if verdict == "SAFE":
                            st.success(f"Verdict: {verdict}")
                        else:
                            st.error(f"Verdict: {verdict}")

                        st.progress(score, text=f"Risk score: {score:.2f}")

                        if reasons:
                            st.markdown("Concerns identified:")
                            for reason in reasons:
                                st.markdown(f"- {reason}")
                        else:
                            st.markdown("No specific concerns identified.")

                st.divider()
                st.subheader("What This Means")

                if final_verdict == "SAFE":
                    st.success(
                        "This agent passed evaluation. Two or more judges found no significant "
                        "safety concerns. The agent may proceed to the next stage of review."
                    )
                else:
                    st.error(
                        "This agent did not pass evaluation. Two or more judges identified "
                        "significant safety concerns. Address the concerns listed above and "
                        "submit a new evaluation before deployment."
                    )

                st.divider()
                with st.expander("View full JSON report"):
                    st.json(report)

            except Exception as e:
                error_msg = str(e)
                if "ConnectionError" in error_msg or "connection" in error_msg.lower() or "Ollama" in error_msg:
                    st.error(
                        "Cannot connect to the evaluation model. "
                        "If running locally start Ollama with: ollama serve. "
                        "If running in the sandbox set the ANTHROPIC_API_KEY environment variable."
                    )
                else:
                    st.error(f"Evaluation failed: {error_msg}")

st.divider()
st.caption(
    "UNICC AI Safety Lab · NYU MASY GC-4100 · Spring 2026 · "
    "Coreece Lopez · Feruza Jubaeva · Galaxy Okoro"
)
