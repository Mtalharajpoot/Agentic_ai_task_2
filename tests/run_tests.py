import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "app"))

from agent import run_agent

TEST_CASES = [
    ("YOLOv8 helmet detection", "LinkedIn", "Professional but exciting", "Post"),
    ("AI internship experience", "LinkedIn", "Motivational", "Post"),
    ("Python learning journey", "Instagram", "Funny", "Reel Script"),
    ("Machine learning project", "X/Twitter", "Short and catchy", "Post"),
    ("Data annotation struggles", "LinkedIn", "Funny", "Post"),
    ("Model failed in production", "Instagram", "Funny", "Reel Script"),
    ("Final year project", "LinkedIn", "Professional but exciting", "Post"),
    ("Computer vision project", "YouTube Shorts", "Professional but exciting", "Reel Script"),
    ("Debugging FastAPI", "X/Twitter", "Funny", "Post"),
    ("Open-source contribution", "LinkedIn", "Motivational", "Post"),
]

LOG_FILE = os.path.join(ROOT, "tests", "test_results_v2.md")


def main():
    # Example: python tests\run_tests.py 4 6 2   (runs only tests 4, 6 and 2)
    if len(sys.argv) > 1:
        numbers = [int(n) for n in sys.argv[1:]]
    else:
        numbers = list(range(1, len(TEST_CASES) + 1))

    start_all = time.time()
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("# Test Results (version 2, after prompt fixes)\n\n")

    for n in numbers:
        topic, platform, tone, output_type = TEST_CASES[n - 1]
        print(f"\n########## TEST {n}: {topic} ##########")
        try:
            r = run_agent(topic, platform, tone, output_type)
            entry = (
                f"## Test {n}\n"
                f"- **Input:** {topic} | {platform} | {tone} | {output_type}\n"
                f"- **Tools used:** {', '.join(r['tools_used'])}\n"
                f"- **Score before rewrite:** {r['score_before']}\n"
                f"- **Score after rewrite:** {r['score']}\n"
                f"- **Saved file:** {r['saved_file']}\n"
                f"- **Time:** {r['seconds']} seconds\n"
                f"- **Useful? (fill in manually):** \n\n"
            )
        except Exception as e:
            entry = (f"## Test {n}\n- **Input:** {topic} | {platform} | {tone} | "
                     f"{output_type}\n- **ERROR:** {e}\n\n")
            print("ERROR:", e)

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry)

    total = (time.time() - start_all) / 60
    print(f"\nAll selected tests finished in {total:.1f} minutes. Results: {LOG_FILE}")


if __name__ == "__main__":
    main()