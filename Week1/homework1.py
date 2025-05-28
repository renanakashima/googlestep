from binary_search import binary_search

"""
Given a string, returns all the anagrams from the dictionary    
"""

test_cases = "testcases_hw1.txt"
dictionary_with_words = "anagram/words.txt"

def txt_to_list(txt_file):
    with open(txt_file) as f:
        lis = [line.rstrip() for line in f]
    return lis

def find_anagrams(random_strings, dictionary):
    strings = []
    for s in random_strings:
        strings.append(''.join(sorted(s)))
    
    new_dict = []
    for word in dictionary:
        new_dict.append([''.join(sorted(word)), word]) 
    new_dict.sort()
    
    '''
    full_list = []
    for i in range(len(strings)):
        anagram = []
        for j in range(len(new_dict)):
            if strings[i] == new_dict[j][0]:
                anagram.append(new_dict[j][1])
        full_list.append(anagram)
    '''    
        
    full_list = []
    for i in range(len(strings)):
        anagram = []
        for index in binary_search(strings[i],new_dict):
            anagram.append(new_dict[index][1])
        full_list.append(anagram)
        
    print(full_list)
    return full_list

def main():
    find_anagrams(txt_to_list(test_cases),txt_to_list(dictionary_with_words))

if __name__ == "__main__":
    main()
    
#time complexity

#space complexity