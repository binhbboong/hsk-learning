import json
from pathlib import Path


ROOT = Path(__file__).parents[2]


def test_github_action_calls_the_reminder_at_half_past_each_hour_from_18h_to_23h_vietnam() -> None:
    workflow = (
        ROOT / ".github" / "workflows" / "learning-reminder.yml"
    ).read_text(encoding="utf-8")

    assert "30 11-16 * * *" in workflow
    assert "https://hsk-learning-api.vercel.app/api/cron/learning-reminder" in workflow
    assert "secrets.CRON_SECRET" in workflow


def test_vercel_config_does_not_use_paid_hourly_cron() -> None:
    config = json.loads(
        (ROOT / "backend" / "vercel.json").read_text(encoding="utf-8")
    )

    assert "crons" not in config
