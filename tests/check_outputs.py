import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "tests", "test_results_final.md")
OUT = os.path.join(ROOT, "tests", "test_cases.md")
LIMITS = {"LinkedIn": (120, 180), "Instagram": (60, 100)}


def get_section(text, name):
    match = re.search(rf"## {name}\n(.*?)(?=\n## |\Z)", text, re.S)
    return match.group(1).strip() if match else ""


def parse_results():
    text = open(RESULTS, encoding="utf-8").read()
    blocks = re.split(r"\n## Test ", "\n" + text)[1:]
    tests = []
    for b in blocks:
        def field(label):
            m = re.search(rf"\*\*{label}:\*\* (.*)", b)
            return m.group(1).strip() if m else ""
        tests.append({
            "num": b.split("\n")[0].strip(),
            "input": field("Input"),
            "tools": field("Tools used"),
            "before": field("Score before rewrite"),
            "after": field("Score after rewrite"),
            "file": field("Saved file"),
            "time": field("Time"),
        })
    return tests


def check(test):
    parts = [p.strip() for p in test["input"].split("|")]
    platform, output_type = parts[1], parts[3]
    if not os.path.exists(test["file"]):
        return {"saved file exists": False}

    text = open(test["file"], encoding="utf-8").read()
    post = get_section(text, "Post")
    tags = get_section(text, "Hashtags").split()
    reel = get_section(text, "Reel Script")

    results = {}
    results["no placeholders"] = not re.search(r"\[[^\]]+\]", post + reel)
    results["hashtags start with #"] = bool(tags) and all(t.startswith("#") for t in tags)
    if platform == "X/Twitter":
        results[f"post max 250 chars (got {len(post)})"] = len(post) <= 250
    if platform in LIMITS:
        lo, hi = LIMITS[platform]
        words = len(post.split())
        results[f"post {lo}-{hi} words (got {words})"] = lo <= words <= hi
    if "reel" in output_type.lower() or "script" in output_type.lower():
        results["reel script present"] = len(reel) > 0
    return results


def main():
    tests = parse_results()
    lines = [
        "# Test Cases and Results\n",
        "Useful = Yes when all automatic checks pass, Partly when some fail.\n",
        "| # | Input (topic / platform / tone / output) | Tools used | Score before -> after | Time | Saved file | Failed checks | Useful? |",
        "|---|---|---|---|---|---|---|---|",
    ]
    yes = 0
    for t in tests:
        failed = [k for k, v in check(t).items() if not v]
        useful = "Yes" if not failed else "Partly"
        yes += useful == "Yes"
        lines.append(
            f"| {t['num']} | {t['input']} | {t['tools']} | {t['before']} -> {t['after']} | "
            f"{t['time']} | {os.path.basename(t['file'])} | {'; '.join(failed) or '-'} | {useful} |"
        )
        print(f"Test {t['num']}: {useful} | failed: {failed or 'none'}")
    lines.append(f"\n**{yes} of {len(tests)} tests passed all automatic checks.**")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nSaved: {OUT}")


if __name__ == "__main__":
    main()