import json
from pathlib import Path


ROOT = Path(__file__).parents[2]


def test_github_action_calls_the_reminder_hourly_from_19h10_to_23h10_vietnam() -> None:
    workflow = (
        ROOT / ".github" / "workflows" / "learning-reminder.yml"
    ).read_text(encoding="utf-8")

    assert "10 12-16 * * *" in workflow
    assert "https://hsk-learning-api.vercel.app/api/cron/learning-reminder" in workflow
    assert "secrets.CRON_SECRET" in workflow


def test_vercel_config_does_not_use_paid_hourly_cron() -> None:
    config = json.loads(
        (ROOT / "backend" / "vercel.json").read_text(encoding="utf-8")
    )

    assert "crons" not in config
