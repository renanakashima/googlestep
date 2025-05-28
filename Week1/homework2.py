from anagram.score_checker import calculate_score
"""
Given a string, return the anagrams from the dictionary.
Not all the characters in the string need to be used.
"""

input = "anagram/large.txt"
dictionary_with_words = "anagram/words.txt"
output = "large_answer.txt"

def txt_to_list(txt_file):
    with open(txt_file) as f:
        lis = [line.rstrip() for line in f]
    return lis

def find_anagrams(random_strings, dictionary):
    with open(output, 'w') as file:
        file.write("")
    
    new_dict = []
    for word in dictionary:
        new_dict.append([int(calculate_score(word)),{char:(word.count(char)) for char in word}, word]) 
    new_dict = sorted(new_dict, reverse=True, key=lambda x: x[0])
    
    for s in random_strings:
        d = {char:(s.count(char)) for char in s}
    
        for i in range(len(new_dict)):
            chars = new_dict[i][1]
            word = new_dict[i][2]
            
            anagram = True
            for letter, count in chars.items():
                string_count = d.get(letter, 0)
                if string_count < count:
                    anagram = False
                    break 
            if anagram:
                with open(output, 'a') as file:
                    file.write(str(word) + '\n')
                break        
    return output

def main():
    find_anagrams(txt_to_list(input),txt_to_list(dictionary_with_words))

if __name__ == "__main__":
    main()
    
#time complexity

#space complexity
