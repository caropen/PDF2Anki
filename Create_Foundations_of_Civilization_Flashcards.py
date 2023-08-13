import PyPDF2
import openai
import os
import re
from dataclasses import dataclass
import math

openai.api_key = 'insert-api-key-here'

@dataclass
class Chapter:
    number: int
    title: str
    content: str

def read_chapters(file_path):
    with open(file_path):
        reader = PyPDF2.PdfReader(file_path)

    start_page = 12
    end_page = 224
    table_of_contents = {}
    lecture_num = 1

    for i in range(start_page, end_page):
        page = reader.pages[i]
        line2 = (page.extract_text().split('\n'))[1]
        print("page "+ str(i) + ": " + line2 + "\n")
        if line2.startswith("Lecture"):
            table_of_contents[lecture_num] = i
            lecture_num = lecture_num + 1

    chapters = []
    for lecture_num, lect_startpage in table_of_contents.items():
        if lecture_num == len(table_of_contents):
            lect_endpage = end_page+1
        else:
            lect_endpage = table_of_contents[lecture_num+1]

        line1 =  (reader.pages[lect_startpage].extract_text()).split('\n')[0]
        lines12 =  (reader.pages[lect_startpage].extract_text()).split('\n')[0:2]
        print(lines12)
        print("(n)")
        title = re.sub(r'^\d+', '', line1)
        if len(title) == 0:
            title = re.sub(r'^Lecture [0-9]+:', '', lines12[1])
            title = title[0:math.floor(len(title)/2)]

        CurrentChapter = Chapter(lecture_num, title.strip(), " ".join(page.extract_text() for page in reader.pages[lect_startpage:lect_endpage]))

        chapters.append(CurrentChapter)
    return chapters

def create_anki_cards(chapters):
    generated_flashcards = ''
    prompt = """
I want you to create a deck of up to 10 flashcards from the Lecture Text. Do not give an introduction in your answer. Only output the flashcards in the following format:
Question;Answer
Question;Answer
...

Instructions to create a deck of flashcards:
- Keep the flashcards simple, clear, and focused on the most important information.
- Answers should contain only a single key fact/name/concept/term.

Example Text:
The characteristics of the Dead Sea: Salt lake located on the border between Israel and Jordan. Its shoreline is the lowest point on the Earth's surface, averaging 396 m below sea level. It is 74 km long. It is seven times as salty (30% by volume) as the ocean. Its density keeps swimmers afloat. Only simple organisms can live in its saline waters.

Example Output:
Where is the Dead Sea located?;On the border between Israel and Jordan.
What is the lowest point on the Earth\'s surface?;The Dead Sea shoreline.

Lecture Text:
"""
    # print(prompt+chapters[0].content)

    for chapter in chapters:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt+chapter.content}
        ]

        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages, 
                temperature =0.7,
                max_tokens=1024
            )

        response_from_api = response['choices'][0]['message']['content']

        print(response_from_api)
        # Add lecture hints to each flashcard
        cards = response_from_api.split('\n')
        cards = [line + " (Lecture " + str(chapter.number) + ": " + str(chapter.title) + ")"  for line in cards]
        enhanced_response = '\n'.join(cards)

        generated_flashcards += enhanced_response
        generated_flashcards += "/n"

    # Save the cards to a text file
    with open("flashcards.txt", "w") as f:
        f.write(generated_flashcards)

    return generated_flashcards

if __name__ == "__main__":
    file_path = 'Foundations-of-Western-Civilization-370.pdf'
    chapters = read_chapters(file_path)
    #with open("book.txt", "w") as f:
    #    for chapter in chapters:
    #        f.write("Title: " + chapter.title + "\n")
    #        f.write("Content: " + chapter.content + "\n\n")
    generated_flashcards = create_anki_cards(chapters)
