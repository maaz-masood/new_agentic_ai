from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DebateConfigSmokeTest(unittest.TestCase):
    def test_debate_configs_and_entrypoint_are_aligned(self):
        agents_text = (ROOT / "src" / "my_crew" / "config" / "agents.yaml").read_text(encoding="utf-8")
        tasks_text = (ROOT / "src" / "my_crew" / "config" / "tasks.yaml").read_text(encoding="utf-8")
        crew_text = (ROOT / "src" / "my_crew" / "crew.py").read_text(encoding="utf-8")
        main_text = (ROOT / "src" / "my_crew" / "main.py").read_text(encoding="utf-8")
        readme_text = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("Expert Debate Moderator", agents_text)
        self.assertIn("Debate Judge and Adjudicator", agents_text)
        self.assertIn("Round winner", tasks_text)
        self.assertIn("Overall debate winner", tasks_text)
        self.assertIn("debate_judgment.md", crew_text)
        self.assertIn("Should advanced AI systems be regulated before public deployment?", main_text)
        self.assertIn("debate_judgment.md", readme_text)


if __name__ == "__main__":
    unittest.main()
