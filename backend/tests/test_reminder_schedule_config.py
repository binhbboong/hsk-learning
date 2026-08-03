import json
from pathlib import Path


ROOT = Path(__file__).parents[2]


def test_local_scheduler_replaces_github_reminder_workflows() -> None:
    workflows = ROOT / ".github" / "workflows"

    assert not (workflows / "learning-reminder.yml").exists()
    assert not (workflows / "learning-reminder-v2.yml").exists()
    assert not (workflows / "learning-reminder-poller.yml").exists()


def test_vercel_config_does_not_use_paid_hourly_cron() -> None:
    config = json.loads(
        (ROOT / "backend" / "vercel.json").read_text(encoding="utf-8")
    )

    assert "crons" not in config
