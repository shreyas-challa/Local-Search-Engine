import os
import re
import ftfy
from sklearn.feature_extraction.text import TfidfVectorizer


PATH_TO_NOTES_FOLDER = "./files/"
data = [] # corpus to analyse and transform for fit and search


for filename in os.listdir(PATH_TO_NOTES_FOLDER):
    if filename.endswith(".md"): # Filter for mark down files
        path = os.path.join(PATH_TO_NOTES_FOLDER, filename)
        with open(path, 'r', encoding="utf-8") as f:
            file = f.read()
            fixed_text = ftfy.fix_text(file) #clean the unicode transformation errors

            pattern = r"\[\[(.*?)\]\]" # pattern for note links
            replacement = r"\1" # use inner text
            text = re.sub(pattern, replacement, fixed_text, flags=re.MULTILINE) # replace note links with inner text

            pattern = r'^!(?:\[\[|Pasted).*\n?' # regex pattern for images
            cleaned_text = re.sub(pattern, '', text, flags=re.MULTILINE)
            
            pattern = r'```.*?```'
            not_final = re.sub(pattern, '', cleaned_text, flags=re.DOTALL) # delete the code blocks from existence

            pattern = r"`([^`]*)`"
            replacement = r"\1"
            final = re.sub(pattern, replacement, not_final, flags=re.MULTILINE) # replace the fucking inline shit

            words = final.split()

            # print(final)
            # print(words)
            data.append(final) # append to corpus
            
print(data[0])

tfidf = TfidfVectorizer()
result = tfidf.fit_transform(data)
print(result.shape)

for ele1, ele2 in zip(tfidf.get_feature_names_out(), tfidf.idf_):
    print(ele1, ':', ele2)