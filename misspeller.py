import sys
import random
from array import array
def duplicate_chars(word):
    result = []

    for index,char in enumerate(word):
        rand = int(random.uniform(1,3))
        result += char * rand
        if rand > 2:
            result += word[index:]
            break

    return ''.join(result)

def shuffle_bowels(word):
    aword = array('c',word)
    for index, char in enumerate(aword):
        if char in 'aeiou':
            replacement = random.choice('aeiou')
            if replacement != char:
                aword[index] = replacement
                break

    return ''.join(aword)

if __name__ == '__main__':

    #Generate at most distance 2 misspells and print them

    for word in sys.stdin:
        print shuffle_bowels(duplicate_chars(str.strip(word)))
