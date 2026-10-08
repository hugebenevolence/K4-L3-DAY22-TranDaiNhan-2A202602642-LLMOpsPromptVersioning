# Day 22 evidence — Tran Dai Nhan

LangSmith project: [day22-lab](https://smith.langchain.com/o/c184d0e3-d29d-4c6c-832d-c1ca4b2ce5bd/projects/p/f4ac32ab-1725-4707-82f6-3af9ea710422). After the full rerun, the LangSmith API confirmed at least 100 root `rag-query` traces and 100 root `ab-rag-query` traces. A sample `rag-query` trace contains the input question, retriever output, prompt, model run, and answer. Prompt Hub contains `tran-dai-nhan-rag-prompt-v1` and `tran-dai-nhan-rag-prompt-v2`; both were pulled successfully for A/B routing. The 409 messages in the original routing log mean the prompt content was already on Hub, so there was no new commit to create.

`01_langsmith_traces.png` and `02_prompt_hub.png` are captures of the `day22-lab` tracing page and Prompt Hub listing in Edge Profile 1. The Prompt Hub screenshot shows both named prompts. `03_ragas_scores.png` is a terminal capture displaying the values from `data/ragas_report.json`, which was saved by the completed full rerun. The score JSON is an exact copy of that report; the routing and Guardrails logs are unedited excerpts from the same rerun.

| Metric | V1 | V2 |
|---|---:|---:|
| Faithfulness | 0.9652 | 0.9232 |
| Answer relevancy | 0.9092 | 0.8942 |
| Context recall | 1.0000 | 1.0000 |
| Context precision | 0.9450 | 0.9417 |

Both prompts pass the 0.8 faithfulness target and exceed 0.9. V1 scored 0.0420 higher on faithfulness, 0.0149 higher on answer relevancy, and 0.0033 higher on context precision. Its shorter answer instructions may have limited unsupported claims; this is an interpretation of the measured difference, not a causal proof. Recall is equal at 1.0. Both versions used the same knowledge base, embedding model, retriever, and top-3 contexts.

The Guardrails logs cover six PII cases and five JSON cases. PII inputs are fictional. The JSON fallback remains parseable even when repair fails. The full `run_all.py` rerun completed all four steps with PASS, and local regression checks passed with `python -m unittest discover -s tests -v`. Guardrails emitted a non-fatal telemetry export error after the PASS summary because its telemetry endpoint could not be resolved.
