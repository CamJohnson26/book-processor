from ollama_apis.prompts import COMPRESS_TEXT_PROMPT_V1, COMBINE_SUMMARIES_PROMPT_V1
from ollama_apis.run_prompt import chat

CHAR_LIMIT = 5000


def compress_long_text(text):
    result = ''
    for i in range(0, len(text), CHAR_LIMIT):
        print(f'Compression. Processing {i+1} of {len(text)}')
        subtext = text[i:i+CHAR_LIMIT]
        result += chat(COMPRESS_TEXT_PROMPT_V1 + '\n' + subtext)
    print(f'Compressed from {len(text)} to {len(result)}')
    return result


def summarize_long_text_recursive(text, prompt, char_limit=CHAR_LIMIT):
    summary = ''
    for i in range(0, len(text), char_limit):
        print(f'Summarize. Processing {i+1} of {len(text)}')
        subtext = text[i:i+char_limit]
        new_summary = chat(prompt + '\n' + subtext)
        summary += '\n' + new_summary
    if len(summary) > char_limit:
        print('Still too long, going again')
        summarize_long_text_recursive(summary, prompt, char_limit=char_limit)
    return summary


def summarize_long_text(text, prompt, char_limit=CHAR_LIMIT, compress=True):
    if compress:
        text = compress_long_text(text)
    summary = summarize_long_text_recursive(text, prompt, char_limit=char_limit)
    return chat(COMBINE_SUMMARIES_PROMPT_V1 + '\n' + summary)
