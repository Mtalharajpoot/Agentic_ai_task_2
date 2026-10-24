# TrendPilot: A Local Agentic AI Assistant Using Ollama

TrendPilot is a local agentic AI assistant that turns a topic into a complete social media content plan. It runs fully offline on a laptop using Ollama and **Gemma 3:4B**.

You give it a topic, platform, tone and output type. The agent plans the work, calls tools, reviews its own output, saves the result to a file and remembers previous runs.

## Features
- Local LLM through Ollama (`gemma3:4b`), no cloud API
- Agent workflow: plan, tool calls, self-review, rewrite, save
- 6 tools + a memory tool, every call is logged as `[Tool Called]: ...`
- Platform rules for LinkedIn, Instagram, X/Twitter and YouTube Shorts
- JSON memory of previous topics and saved file paths
- CLI demo, 10 test cases and an automatic output checker

## Agent workflow
```
User input (topic, platform, tone, output type)
-> Plan
-> Trend Idea Generator -> pick best angle
-> Caption Writer -> Hashtag Generator -> Reel Script Generator (if requested)
-> Content Reviewer
-> if score < 8: rewrite the post, then review again
-> File Saver (3 folders) -> Memory Tool -> final answer
```

## Tools
| Tool | Purpose |
|---|---|
| Trend Idea Generator | 3 content angles, picks the best one |
| Caption Writer | Platform-specific post |
| Hashtag Generator | 6 relevant hashtags |
| Reel Script Generator | 30-second script (hook, 3 scenes, closing line) |
| Content Reviewer | Score out of 10 and 3 improvement tips |
| File Saver | Saves results as Markdown files |
| Memory Tool | Stores previous topic, platform, tone and file path |

## Project structure
```
agentic_ai_task_2/
  app/            main.py, agent.py, tools.py, memory.py, prompts.py
  outputs/        generated_posts, generated_scripts, saved_results, memory.json
  tests/          run_tests.py, check_outputs.py, test_cases.md, test_results_*.md
  screenshots/    ollama_running, demo_output, saved_file_output, ...
  report/         final_report.pdf
  demo.py         CLI entry point
  requirements.txt
```

## Setup
1. Install Ollama from https://ollama.com and pull the model:
   ```
   ollama pull gemma3:4b
   ```
2. Create a virtual environment and install requirements:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Make sure the Ollama app is running, then start the demo:
   ```
   python demo.py
   ```

## Testing
```
python tests\run_tests.py          # all 10 test cases (or e.g. "4 6" for selected ones)
python tests\check_outputs.py      # rule checks, writes tests/test_cases.md
```
The checker tests: no placeholders, hashtags start with `#`, X/Twitter posts are at most 250 characters, LinkedIn and Instagram word limits, and reel script present when requested.

## Results
- 10 test cases, all completed without errors and all passed the automatic rule checks.
- Average time per run: about 3 minutes on a CPU-only laptop with Gemma 3:4B (30.4 minutes for all 10 tests).
- The model's own review score is noisy (it scored 7/10 in 9 of 10 tests), so it is not used as an accuracy measure.

## Error analysis (summary)
| Problem found | Cause | Fix |
|---|---|---|
| "Model" understood as a fashion model | Ambiguous word, no domain context | Added AI/ML context to the system prompt |
| Placeholders like [Company Name] | Not forbidden in the prompt | Added a no-placeholders rule |
| Review text cut off | Token limit too low | Raised the limit and used a short fixed review format |
| Hashtags broken or repeated inside the post | No strict format rules | One-word hashtags starting with #, no hashtags in the post |
| Invented facts (industry, results) | Model fills gaps | Added a "do not invent facts" rule |
| Rewrite did not improve the score | Small model reviewing its own work | Re-review after rewrite; see future improvements |

## Limitations
- Small 4B model on CPU: slow, and humor is hit and miss.
- Self-review by the same model is unreliable; rewrites improved the score in 0 of 9 cases.
- The agent does not know the user's real experience, so posts stay generic.

## Future improvements
- Keep the rewrite only if the review score improves, otherwise keep the original
- Code-based validation (character counts, hashtag format)
- Few-shot examples in prompts, especially for funny and meme styles
- Streamlit interface, web search tool, user feedback loop
- A larger local model or GPU

## Tech stack
Python, Ollama, Gemma 3:4B, requests, JSON memory, Markdown file saving.