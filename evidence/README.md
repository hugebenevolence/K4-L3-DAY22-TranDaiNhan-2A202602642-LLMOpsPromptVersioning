# Day 22 evidence — Tran Dai Nhan

LangSmith project: [day22-lab](https://smith.langchain.com/o/c184d0e3-d29d-4c6c-832d-c1ca4b2ce5bd/projects/p/f4ac32ab-1725-4707-82f6-3af9ea710422). The LangSmith API confirmed 50 successful root `rag-query` traces and 50 successful root `ab-rag-query` traces. A sample `rag-query` trace contains the input question, retriever output, prompt, model run, and answer. Prompt Hub contains `tran-dai-nhan-rag-prompt-v1` and `tran-dai-nhan-rag-prompt-v2`; both were pulled successfully for A/B routing. The 409 messages in the routing log mean the prompt content was already on Hub, so there was no new commit to create.

`03_ragas_scores.png` is a real terminal capture displaying the values from `data/ragas_report.json`, which was saved by the completed evaluation run. `01_langsmith_traces.png` and `02_prompt_hub.png` are currently visual reports made from actual LangSmith API responses, **not screenshots of the LangSmith website**. They should be replaced with UI captures before grading if the course requires screenshots. The original score JSON and console logs remain unedited evidence of the executions.

| Metric | V1 | V2 |
|---|---:|---:|
| Faithfulness | 0.9570 | 0.9162 |
| Answer relevancy | 0.9090 | 0.8920 |
| Context recall | 1.0000 | 1.0000 |
| Context precision | 0.9417 | 0.9417 |

Both prompts pass the 0.8 faithfulness target and exceed 0.9. V1 scored 0.0409 higher on faithfulness and 0.0171 higher on answer relevancy. Its shorter answer instructions may have limited unsupported claims; this is an interpretation of the measured difference, not a causal proof. Recall and precision are equal because both versions used the same knowledge base, embedding model, retriever, and top-3 contexts.

The Guardrails logs cover six PII cases and five JSON cases. PII inputs are fictional. The JSON fallback remains parseable even when repair fails. Local regression checks passed with `python -m unittest discover -s tests -v`.
