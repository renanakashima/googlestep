from binary_search import binary_search

"""
Given a string, return all the anagrams from the dictionary    
"""

test_cases = "testcases_hw1.txt"
dictionary_with_words = "anagram/words.txt"

def txt_to_list(txt_file):
    with open(txt_file) as f:
        lis = [line.rstrip() for line in f]
    return lis


# n items in a list
# sorting: O(n * log n) time
# loop: O(n) time


def find_anagrams(string, dictionary):
    # O(1) constant time
    string = ''.join(sorted(string))

    new_dict = []
    # O(1 * n), where n is the number of words in dictionary
    # O(n) time
    for word in dictionary:
        # O(1)
        new_dict.append([''.join(sorted(word)), word]) 
    # O(n * log n)
    new_dict.sort()

    # binary search takes O(log n) time
    # worst cast: n matches, O(n) time
    # O(log n  + n) time => O(n) time
    for index in binary_search(string,new_dict):
        print(new_dict[index][1])

"""
def find_anagrams(random_strings, dictionary):
    strings = []
    for s in random_strings:
        strings.append(''.join(sorted(s)))
    
    new_dict = []
    for word in dictionary:
        new_dict.append([''.join(sorted(word)), word]) 
    new_dict.sort()
        
    full_list = []
    for i in range(len(strings)):
        anagram = []
        for index in binary_search(strings[i],new_dict):
            anagram.append(new_dict[index][1])
        full_list.append(anagram)
        
    print(full_list)
    return full_list
"""
def main():
    #find_anagrams(txt_to_list(test_cases),txt_to_list(dictionary_with_words))
    find_anagrams("board",txt_to_list(dictionary_with_words))
    
if __name__ == "__main__":
    main()
    
#time complexity

#space complexity