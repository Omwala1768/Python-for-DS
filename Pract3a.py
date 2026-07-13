Input = input("Enter the text: ")

find_text = input("Enter the word to search for: ")

if find_text in Input:
    print(f"The word '{find_text}' was found in the text.")
else:
    print(f"The word '{find_text}' was NOT found in the text.")
