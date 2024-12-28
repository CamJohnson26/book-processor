
TEXT_SUMMARY_PROMPT_V2 = '''
Only perform this task, don't comment or say anything other than the raw answer.
Summarize the following text following these rules.
Keep the summary compact and void of emotion.
Follow the provided format exactly.
Only provide the summary, give no intro or other information:
BEGIN SUMMARY:
1. People.
List the major people or organizations mentioned, in order of relative importance to the text, with their full known name
2. Context. 
List the key events or ideas presented and summarize compactly
The text to summarize:
'''

COMPRESS_TEXT_PROMPT_V1 = '''
Only perform this task, don't comment or say anything other than the raw answer.
Compress the following text by removing any noise or unnecessary information:
'''

COMBINE_SUMMARIES_PROMPT_V1 = '''
Only perform this task, don't comment or say anything other than the raw answer.
Clean up and combine these summaries:
'''

SUMMARIZE_TEXT_PROMPT_V1 = '''
Only perform this task, don't comment or say anything other than the raw answer.
Extract the major news events into a ranked list of all major events mentioned in the following text.
Remove the noise, irrelevant information amd any editorializing
'''

CREATE_NEWS_STORY_PROMPT_V1 = '''
Only perform this task, don't comment or say anything other than the raw answer.
You will summarize today's news into a one page, executive summary.
Write a detailed, informative paragraph on each of these topics, using the raw information provided below:
Global Issues, Economy, Science and Technology, Sports & Entertainment.
Separate paragraphs with 3 blank lines.
'''