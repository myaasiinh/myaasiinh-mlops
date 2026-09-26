import re
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUB = ROOT / "myaasiinh-submission"
EX_STRESS = ROOT / "contoh repo rilet" / "human-stress-prediction"
EX_ZENML = ROOT / "contoh repo rilet" / "MLOPS_11_RA"

PAIRS = [
    (SUB / "student_transform.py", EX_STRESS / "stress_transform.py"),
    (SUB / "student_trainer.py", EX_STRESS / "stress_trainer.py"),
    (SUB / "student_tuner.py", EX_STRESS / "stress_tuner.py"),
    (SUB / "ml-pipeline.ipynb", EX_STRESS / "ml-pipeline.ipynb"),
    (SUB / "Dockerfile", EX_STRESS / "Dockerfile"),
    (SUB / "requirements.txt", EX_STRESS / "requirements.txt"),
    (SUB / "run_pipeline.py", EX_ZENML / "main.py"),
    (SUB / "Dockerfile", EX_ZENML / "Dockerfile"),
    (SUB / "requirements.txt", EX_ZENML / "requirements.txt"),
]


def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"#VSC-[0-9a-fA-F-]+", "", text)
    text = re.sub(r"\"id\"\s*:\s*\"[^\"]+\"", '"id":""', text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def main() -> None:
    rows: list[tuple[str, str, float | None]] = []
    for a_path, b_path in PAIRS:
        if not a_path.exists() or not b_path.exists():
            rows.append((str(a_path), str(b_path), None))
            continue
        a = normalize(a_path.read_text(encoding="utf-8", errors="ignore"))
        b = normalize(b_path.read_text(encoding="utf-8", errors="ignore"))
        rows.append((str(a_path), str(b_path), similarity(a, b)))

    rows.sort(key=lambda t: (1 if t[2] is None else 0, 0 if t[2] is None else -t[2]))

    print("Similarity ratios (0..1, higher=more similar):")
    for a, b, r in rows:
        if r is None:
            print(f"- {Path(a).name} vs {Path(b).name}: missing")
        else:
            print(f"- {Path(a).name} vs {Path(b).name}: {r:.3f}")


if __name__ == "__main__":
    main()
