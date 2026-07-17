import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_script(relative_path: str) -> str:
    result = subprocess.run(
        [sys.executable, str(ROOT / relative_path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout


class ScaffoldTests(unittest.TestCase):
    def test_voice_pipeline_script_runs_and_supports_interrupt(self):
        output = run_script("examples/12-voice-pipeline/main.py")
        self.assertIn("用户打断", output)
        self.assertIn("MockTTS", output)
        self.assertIn("流水线结束", output)

    def test_project_scripts_run(self):
        scripts = [
            "projects/01-weather/main.py",
            "projects/02-search-agent/main.py",
            "projects/03-multi-agent/main.py",
            "projects/04-voice-assistant/main.py",
            "projects/05-enterprise-agent/main.py",
        ]
        for script in scripts:
            with self.subTest(script=script):
                output = run_script(script)
                self.assertTrue(output.strip(), f"{script} should print a demo transcript")


if __name__ == "__main__":
    unittest.main()
