import re
import ftfy
from sklearn.feature_extraction.text import TfidfVectorizer


path = "./Lecture 15- Dijkstra's algorithm.md"

pattern = r"\[\[(.*?)\]\]" # turning note links back into normal text
replacement = r"\1"

data = []

with open(path, 'r') as f:
  file = f.read()
  fixed_text = ftfy.fix_text(file) #clean the unicode transformation errors
  
  text = re.sub(pattern, replacement, fixed_text, flags=re.MULTILINE) # replace note links with inner text

  pattern = r'^!(?:\[\[|Pasted).*\n?' # regex pattern for images
  cleaned_text = re.sub(pattern, '', text, flags=re.MULTILINE)
  
  pattern = r'```.*?```'
  not_final = re.sub(pattern, '', cleaned_text, flags=re.DOTALL) # delete the code blocks from existence

  pattern = r"`([^`]*)`"
  replacement = r"\1"
  final = re.sub(pattern, replacement, not_final, flags=re.MULTILINE) # replace the fucking inline shit

  words = final.split()
  
  # data.append(words)
  # print(final)
  # print(words)


tfidf = TfidfVectorizer()
result = tfidf.fit_transform(words)

for ele1, ele2 in zip(tfidf.get_feature_names_out(), tfidf.idf_):
    print(ele1, ':', ele2)