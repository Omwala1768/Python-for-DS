sentence = input("Enter a sentence: ")

word_count = len(sentence.split())
char_count = len(sentence)

lowercase_sentence = sentence.lower()
uppercase_sentence = sentence.upper()
underscore_sentence = sentence.replace(" ", "_")

print("\nNumber of words:", word_count)
print("Number of characters:", char_count)
print("Lowercase:", lowercase_sentence)
print("Uppercase:", uppercase_sentence)
print("With underscores:", underscore_sentence)
