def binary_search(word, dictionary):
    index = []
    start = 0
    end = len(dictionary) - 1
    
    while start <= end:
        mid = start + (end - start) // 2
        if word == dictionary[mid][0]:
            index.append(mid)
            left = mid - 1
            while left >= 0 and word == dictionary[left][0]:
                index.append(left)
                left -= 1
            right = mid + 1
            while right < len(dictionary) and word == dictionary[right][0]:
                index.append(right)
                right += 1
            break
        elif word < dictionary[mid][0]:
            end = mid - 1
        else:
            start = mid + 1
    index.sort()
    return index

'''
dictionary_with_words = "anagram/words.txt"

def txt_to_list(txt_file):
    with open(txt_file) as f:
        lis = [line.rstrip() for line in f]
    new_dict = []
    for word in lis:
        new_dict.append([''.join(sorted(word)), word]) 
    new_dict.sort()
    return new_dict


print(binary_search(''.join(sorted("an")), txt_to_list(dictionary_with_words)))
'''