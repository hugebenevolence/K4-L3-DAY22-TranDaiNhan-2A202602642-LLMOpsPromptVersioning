"""Small local checks for routing, evaluation data, and output guards."""

import importlib
import json
import os
import sys
import unittest
from pathlib import Path

os.environ.setdefault("OTEL_SDK_DISABLED", "true")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


class LabChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ab = importlib.import_module("02_prompt_hub_ab_routing")
        cls.ragas = importlib.import_module("03_ragas_evaluation")
        cls.guards = importlib.import_module("04_guardrails_validator")

    def test_routing_and_prompt_consistency(self):
        routes = [self.ab.get_prompt_version(f"req-{i:04d}") for i in range(50)]
        self.assertEqual(routes, [self.ab.get_prompt_version(f"req-{i:04d}") for i in range(50)])
        self.assertEqual(set(routes), {self.ab.PROMPT_V1_NAME, self.ab.PROMPT_V2_NAME})
        self.assertEqual(self.ab.SYSTEM_V1, self.ragas.SYSTEM_V1)
        self.assertEqual(self.ab.SYSTEM_V2, self.ragas.SYSTEM_V2)

    def test_ragas_dataset_keeps_each_context(self):
        item = {"question": "Q", "answer": "A", "reference": "R", "contexts": ["one", "two"]}
        sample = self.ragas.build_ragas_dataset([item]).samples[0]
        self.assertEqual(sample.retrieved_contexts, ["one", "two"])

    def test_pii_and_json_guards(self):
        from guardrails import Guard

        pii = Guard().use(self.guards.PIIDetector(on_fail=self.guards.OnFailAction.FIX))
        text = "Email a@example.com, call (555) 867-5309; SSN 123-45-6789; card 4532 1234 5678 9010."
        output = pii.validate(text).validated_output
        for label in ("EMAIL", "PHONE", "SSN", "CREDIT_CARD"):
            self.assertIn(f"[{label}_REDACTED]", output)
        self.assertNotIn("a@example.com", output)

        formatter = Guard().use(self.guards.JSONFormatter(on_fail=self.guards.OnFailAction.FIX))
        self.assertEqual(json.loads(formatter.validate("```json\n{'ok': true,}\n```").validated_output), {"ok": True})
        self.assertIn("error", json.loads(formatter.validate("invalid {]").validated_output))


if __name__ == "__main__":
    unittest.main()
