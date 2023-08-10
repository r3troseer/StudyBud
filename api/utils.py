from decouple import config
from nltk import word_tokenize, sent_tokenize
import json
import openai

openai.api_key = config("OPENAI_API_KEY")


# def break_large_text(text, max_token_limit, overlap):
#     paragraphs = text.split("\n\n")  # Split text into paragraphs
#     chunks = []

#     for paragraph in paragraphs:
#         tokens = nltk.word_tokenize(paragraph)
#         if len(tokens) > max_token_limit:
#             # Split paragraph into smaller chunks based on max_token_limit
#             start = 0
#             while start < len(tokens):
#                 end = min(start + max_token_limit, len(tokens))
#                 chunk = " ".join(tokens[start:end])
#                 chunks.append(chunk)
#                 start += max_token_limit - overlap
#         else:
#             chunks.append(paragraph + "\n")
#     return chunks


def break_large_text(text, max_token_limit):
    # Split text into paragraphs
    # paragraphs = text.split("\n\n")
    chunks = []

    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    current_chunk = ""
    current_chunk_length = 0

    for sentence in sentences:
        # Tokenize the sentence into words
        tokens = word_tokenize(sentence)
        sentence_length = len(tokens)

        # Check if adding the current sentence will exceed the max_token_limit
        if current_chunk_length + sentence_length + 1 <= max_token_limit:
            if current_chunk:
                current_chunk += " "
            current_chunk += sentence
            current_chunk_length += sentence_length + 1
        else:
            # If the current_chunk is not empty, add it to the chunks list
            if current_chunk:
                chunks.append(current_chunk)
            # Start a new chunk with the current sentence
            current_chunk = sentence
            current_chunk_length = sentence_length + 1

    # Add the last remaining chunk, if any
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def generate_summary(text):
    summ = [{"role": "system", "content": "You are an extractive document summarizer."}]
    summ.append(
        {
            "role": "user",
            "content": f"Provide a concise summary of the following text:\n\n-----\n\n{text}\n\n note: Your summary should capture the main points and key ideas of the document.",
        }
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=summ,
        temperature=0.5,
    )
    # print(response)
    # p = str(p)  # coverts OpenAIObject into string to prepare for json to dictionary conversion
    # pjson = json.loads(response)  # converts json to dict
    # # Extract the generated questions and options from the response
    # pdata = pjson["choices"][0]["message"]["content"]

    # Extract the generated summary from the API response
    summary = response.choices[0].message.content
    print(response.usage)
    return summary


def generate_summary_vinci(self):
    prompt = f""
    response = openai.Completion.create(
        model="",
        messages=prompt,
        temperature=0.9,
    )
    summary = response.choices[0].text
    return summary


def generate_question(text):
    prompt = f"generate '10' multi-choice questions on this with 4 option including an answer and 3 distractors based on the following text:\n\n-----\n\n{text} \n\n note: do not perfom text completion, ignore references and the 10 questions should be in the format:\n\n 'question:\n options:\na\nb\nc\nd \nanswer:' "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.1,
        max_tokens=1500,
    )
    print(response)
    question = response.choices[0].text
    pjson = json.loads(str(response))
    pdata = pjson["choices"][0]["text"]
    return str(pdata)


def quest_parser(response):
    questions = []
    response_parts = response.strip().split(
        "\n\n"
    )  # Split response into individual questions

    for qa in response_parts:
        lines = qa.split("\n")
        print(f"all:\n {lines}")

        print(f"first:\n {lines[0]}")
        try:
            question = lines[0].split(": ")[1]
        except IndexError:
            question = lines[0].split(". ")[1]

        choices = []
        for line in lines[1:-1]:
            if line.startswith("   Options") or line.startswith("Options"):
                continue  # skip lines starting with 'Options'

            choices.append(line)

        answer = lines[-1].split(": ")[1]

        answer = qa.split("\n")[-1].split(": ")[1]
        questions.append(
            (question, choices, answer)
        )  # Append the parsed question to the list

    return questions
