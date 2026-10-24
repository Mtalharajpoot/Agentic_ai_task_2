import re
import time

from tools import (
    ask_ollama, trend_idea_generator, caption_writer, hashtag_generator,
    reel_script_generator, content_reviewer, file_saver,
)
from memory import save_to_memory, get_last_entry
from prompts import SYSTEM_STYLE, PLATFORM_RULES

IMPROVE = (
    "{style}\nImprove this {platform} post using the review tips. "
    "Keep the same topic and tone. Rules: {rules}\n"
    "Do not add hashtags or placeholders. Output only the improved post.\n\n"
    "POST:\n{post}\n\nREVIEW TIPS:\n{review}"
)


def make_plan(wants_reel):
    steps = [
        "Understand the topic, platform and tone",
        "Generate content angles (Trend Idea Generator)",
        "Select the best angle",
        "Write the post (Caption Writer)",
        "Generate hashtags (Hashtag Generator)",
    ]
    if wants_reel:
        steps.append("Create a reel script (Reel Script Generator)")
    steps += [
        "Review the output (Content Reviewer)",
        "Improve the post if the score is low, then review again",
        "Save the final result (File Saver)",
        "Update memory (Memory Tool)",
    ]
    return steps


def pick_best_angle(ideas):
    lines = [l.strip() for l in ideas.splitlines() if l.strip()]
    angles = [l for l in lines if re.match(r"^\W*\d[\.\)]", l)]
    match = re.search(r"BEST:\s*\**\s*(\d)", ideas)
    if match and angles:
        idx = int(match.group(1)) - 1
        if 0 <= idx < len(angles):
            return angles[idx].replace("*", "")
    if angles:
        return angles[0].replace("*", "")
    return lines[0] if lines else "General angle"


def parse_score(review):
    match = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", review)
    return float(match.group(1)) if match else None


def run_agent(topic, platform, tone, output_type):
    start = time.time()
    wants_reel = any(w in output_type.lower() for w in ("reel", "script", "video"))
    tools_used = []

    last = get_last_entry()
    if last:
        print(f"[Memory] Previous topic: {last['topic']} | platform: "
              f"{last['platform']} | tone: {last['tone']}")

    plan = make_plan(wants_reel)
    print("\nPlan:")
    for i, step in enumerate(plan, 1):
        print(f"{i}. {step}")
    print()

    ideas = trend_idea_generator(topic, platform, tone)
    tools_used.append("Trend Idea Generator")
    angle = pick_best_angle(ideas)

    caption = caption_writer(topic, platform, tone, angle)
    tools_used.append("Caption Writer")

    hashtags = hashtag_generator(topic, platform)
    tools_used.append("Hashtag Generator")

    reel = ""
    if wants_reel:
        reel = reel_script_generator(topic, tone)
        tools_used.append("Reel Script Generator")

    review = content_reviewer(platform, caption + "\n\n" + hashtags)
    tools_used.append("Content Reviewer")
    score_before = parse_score(review)
    score = score_before

    improved = False
    if score_before is not None and score_before < 8:
        print(f"[Agent] Score {score_before}/10 is low, rewriting the post...")
        print("[Tool Called]: Self-Improve (rewrite)")
        rules = PLATFORM_RULES.get(platform, "Clear and concise.")
        caption = ask_ollama(IMPROVE.format(style=SYSTEM_STYLE, platform=platform,
                                            rules=rules, post=caption, review=review), 250)
        tools_used.append("Self-Improve (rewrite)")
        improved = True

        review_after = content_reviewer(platform, caption + "\n\n" + hashtags)
        tools_used.append("Content Reviewer (re-check)")
        new_score = parse_score(review_after)
        if new_score is not None:
            score = new_score
        review = review_after

    final_text = (
        f"# TrendPilot Result\n\n"
        f"**Topic:** {topic}\n\n**Platform:** {platform}\n\n"
        f"**Tone:** {tone}\n\n**Output type:** {output_type}\n\n"
        f"## Content Angles\n{ideas}\n\n"
        f"## Selected Idea\n{angle}\n\n"
        f"## Post\n{caption}\n\n"
        f"## Hashtags\n{hashtags}\n\n"
    )
    if wants_reel:
        final_text += f"## Reel Script\n{reel}\n\n"
    final_text += f"## Review (score: {score})\n{review}\n"
    if improved:
        final_text += (f"\n_Note: the post was rewritten. Score before rewrite: "
                       f"{score_before}, after rewrite: {score}._\n")

    saved_file = file_saver(topic, platform, final_text, "saved_results")
    tools_used.append("File Saver")
    file_saver(topic, platform, caption + "\n\n" + hashtags, "generated_posts")
    if wants_reel:
        file_saver(topic, platform, reel, "generated_scripts")

    save_to_memory(topic, platform, tone, output_type, saved_file)
    tools_used.append("Memory Tool")

    return {
        "topic": topic, "platform": platform, "tone": tone,
        "idea": angle, "caption": caption, "hashtags": hashtags,
        "reel_script": reel, "review": review, "score": score,
        "score_before": score_before, "tools_used": tools_used,
        "saved_file": saved_file, "seconds": round(time.time() - start, 1),
    }


if __name__ == "__main__":
    result = run_agent(
        "YOLOv8 helmet detection project",
        "LinkedIn",
        "Professional but exciting",
        "Post + Reel Script",
    )
    print("\n" + "=" * 50)
    print("Topic:", result["topic"])
    print("Platform:", result["platform"])
    print("Idea:", result["idea"])
    print("\nCaption:\n", result["caption"])
    print("\nHashtags:", result["hashtags"])
    print("\nReel Script:\n", result["reel_script"])
    print("\nReview:\n", result["review"])
    print("\nSaved file:", result["saved_file"])
    print(f"Total time: {result['seconds']} seconds")