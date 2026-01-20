import re
import ftfy


path = "./Lecture 15- Dijkstra's algorithm.md"

pattern = r"\[\[(.*?)\]\]" # turning note links back into normal text
replacement = r"\1"


with open(path, 'r') as f:
  file = f.read()
  fixed_text = ftfy.fix_text(file) #clean the unicode transformation errors
  
  text = re.sub(pattern, replacement, fixed_text, flags=re.MULTILINE) # replace note links with inner text


  pattern = r'^!(?:\[\[|Pasted).*\n?' # regex pattern for images

  cleaned_text = re.sub(pattern, '', text, flags=re.MULTILINE)
  
  # words = file.split()
  print(cleaned_text)

