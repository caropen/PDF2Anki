This is a toy script to explore how large language models can be used to create flashcards for ANKI. [ANKI](https://apps.ankiweb.net/) is an open-source flashcard program relying on spaced repetition to aid memorization of text.

Aiming to improve my general knowledge I listened to "Foundations of Western Civilization" By Great Courses in Audible and realized just listening was not enough to retain all the facts. The corresponding learning material can be found as a PDF online. 

This script takes that PDF, extracts the chapters' text, passes it to GPT to generate pairs of questions and answers that can be imported into ANKI. The results are okayish and need some polishing, so time is not really saved compared to writing flashcards yourself. Maybe further prompt engineering can improve the output. 