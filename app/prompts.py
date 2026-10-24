SYSTEM_STYLE = (
    "You are TrendPilot, a social media content expert for AI and tech students. "
    "The user works in AI, machine learning and software. "
    "The word 'model' always means a machine learning model, never a fashion model. "
    "Be specific and concise. Never use placeholders like [Company Name] or [Project Name]; "
    "write generic but complete sentences instead. Do not invent specific facts such as industries, companies, numbers or results; keep claims general. No emojis unless asked."
)

PLATFORM_RULES = {
    "LinkedIn": "Professional, 120-180 words, strong first line, 1 call to action.",
    "Instagram": "Casual and visual, 60-100 words, short lines.",
    "X/Twitter": "Maximum 250 characters in total, punchy, no more than 2 hashtags.",
    "YouTube Shorts": "Fast-paced, 30-60 seconds, strong hook in first 3 seconds.",
}

TREND_IDEAS = (
    "{style}\nTopic: {topic}\nPlatform: {platform}\nTone: {tone}\n"
    "Give exactly 3 content angles for a tech audience, numbered 1, 2, 3, one line each. "
    "Then write: BEST: <number> and one reason."
)

CAPTION = (
    "{style}\nWrite a {platform} post.\nTopic: {topic}\nAngle: {angle}\nTone: {tone}\n"
    "Rules: {rules}\n"
    "Start with a strong hook line. Do NOT put hashtags in the post, they are added separately. "
    "Output only the post text."
)

HASHTAGS = (
    "{style}\nGive 6 relevant hashtags for a {platform} post about: {topic}.\n"
    "Each hashtag must start with the # symbol and be one word with no spaces. Output only the hashtags separated by spaces."
)

REEL_SCRIPT = (
    "{style}\nWrite a 30-second reel script about: {topic}. Tone: {tone}.\n"
    "Format exactly:\nHook:\nScene 1 (visual + voiceover):\nScene 2:\nScene 3:\nClosing line:\n"
    "The closing line must be one spoken sentence, not hashtags. Keep it under 90 words."
)

REVIEWER = (
    "{style}\nReview this {platform} post for: hook strength, clarity, length, tone, hashtag relevance.\n"
    "Reply in this exact short format:\nScore: X/10\nTip 1: (max 15 words)\n"
    "Tip 2: (max 15 words)\nTip 3: (max 15 words)\n\nPOST:\n{content}"
)