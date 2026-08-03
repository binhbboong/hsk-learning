import json
from pathlib import Path


ROOT = Path(__file__).parents[2]


def test_new_github_action_polls_every_five_minutes_during_the_evening_window() -> None:
    workflows = ROOT / ".github" / "workflows"
    workflow = (workflows / "learning-reminder-poller.yml").read_text(encoding="utf-8")

    assert not (workflows / "learning-reminder.yml").exists()
    assert not (workflows / "learning-reminder-v2.yml").exists()
    assert "*/5 12-16 * * *" in workflow
    assert "https://hsk-learning-api.vercel.app/api/cron/learning-reminder" in workflow
    assert "secrets.CRON_SECRET" in workflow


def test_vercel_config_does_not_use_paid_hourly_cron() -> None:
    config = json.loads(
        (ROOT / "backend" / "vercel.json").read_text(encoding="utf-8")
    )

    assert "crons" not in config
