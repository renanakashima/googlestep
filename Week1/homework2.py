"""
Given a string, returns the anagrams from the dictionary.
Not all the characters in the string need to be used.
"""

input = "anagram/small.txt"
dictionary_with_words = "anagram/words.txt"
output = "small_answer.txt"

def txt_to_list(txt_file):
    with open(txt_file) as f:
        lis = [line.rstrip() for line in f]
    return lis

def find_anagrams(random_strings, dictionary):
    with open(output, 'w') as file:
        file.write("")
    
    new_dict = []
    for word in dictionary:
        new_dict.append([{char:(word.count(char)) for char in word}, word]) 
    
    for s in random_strings:
        d = {char:(s.count(char)) for char in s}
    
        anagram = []
        for i in range(len(dictionary)):
            chars = new_dict[i][0]
            word = new_dict[i][1]
            
            can_form_word = True
            for letter, count in chars.items():
                string_count = d.get(letter, 0)
                if string_count < count:
                    can_form_word = False
                #break
            
            if can_form_word:
                anagram.append(word)
            break
    
        with open(output, 'a') as file:
            file.write(str(anagram) + '\n')
    
    return output

#def score_check

def main():
    find_anagrams(txt_to_list(input),txt_to_list(dictionary_with_words))

if __name__ == "__main__":
    main()
    
#time complexity

#space complexity