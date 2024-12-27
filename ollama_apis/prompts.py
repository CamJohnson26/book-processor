
TEXT_SUMMARY_PROMPT_V1 = '''
Summarize the following text following these rules.
Keep the summary compact and void of emotion.
Only provide the summary, give no intro or other information.:
1. Heading: People.List the major people or organizations mentioned, in order of relative importance to the text, with their full known name
2. Heading: Context. List key contextual information provided, such as dates, locations, historical context etc.
3. Heading: Key. List the key events or ideas presented and summarize compactly
4. Heading: Final. Give final notes on tone or anything else notable about the passage
5. Heading: Ref. Any references
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
Write a detailed, informative paragraph on each of these topics, using the raw information provided below.
Separate paragraphs with 3 blank lines.
Topics: Global Issues, Economy, Science and Technology, Sports & Entertainment.
'''