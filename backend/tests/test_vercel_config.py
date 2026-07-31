import tomllib
import json
from pathlib import Path


def test_vercel_has_an_explicit_fastapi_entrypoint() -> None:
    pyproject = tomllib.loads(
        (Path(__file__).parents[1] / "pyproject.toml").read_text(encoding="utf-8")
    )

    assert pyproject["tool"]["vercel"]["entrypoint"] == "hsk_api.main:app"


def test_vercel_function_runs_near_the_singapore_database() -> None:
    config = json.loads(
        (Path(__file__).parents[1] / "vercel.json").read_text(encoding="utf-8")
    )

    assert config["regions"] == ["sin1"]
