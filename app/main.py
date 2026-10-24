from agent import run_agent

PLATFORMS = {"1": "LinkedIn", "2": "Instagram", "3": "X/Twitter", "4": "YouTube Shorts"}
TONES = {
    "1": "Professional but exciting",
    "2": "Funny",
    "3": "Motivational",
    "4": "Short and catchy",
}
OUTPUTS = {"1": "Post", "2": "Reel Script", "3": "Post + Reel Script"}


def choose(title, options):
    print(f"\n{title}")
    for key, value in options.items():
        print(f"  {key}. {value}")
    while True:
        choice = input("Enter number: ").strip()
        if choice in options:
            return options[choice]
        print("Invalid choice, try again.")


def print_result(result):
    print("\n" + "=" * 50)
    print("Topic:", result["topic"])
    print("Platform:", result["platform"])
    print("Idea:", result["idea"])
    print("\nCaption:\n", result["caption"])
    print("\nHashtags:", result["hashtags"])
    if result["reel_script"]:
        print("\nReel Script:\n", result["reel_script"])
    print("\nReview:\n", result["review"])
    print("\nSaved file:", result["saved_file"])
    print(f"Total time: {result['seconds']} seconds")


def run_cli():
    print("=== TrendPilot: Local AI Agent for Viral Content Ideas ===")
    while True:
        topic = input("\nEnter your topic: ").strip()
        if not topic:
            print("Topic cannot be empty.")
            continue
        platform = choose("Choose platform:", PLATFORMS)
        tone = choose("Choose tone:", TONES)
        output_type = choose("Choose output type:", OUTPUTS)

        result = run_agent(topic, platform, tone, output_type)
        print_result(result)

        again = input("\nGenerate another? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    run_cli()