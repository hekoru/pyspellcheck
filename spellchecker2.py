__author__ = 'hector'

__author__ = 'hector'

from trietree import TrieTree
from itertools import groupby
from itertools import combinations
from array import array
from itertools import islice
import sys


VOWELS = 'aeiou'
NO_SUGGESTION = 'NO_SUGGESTION'

class SpellChecker(object):
    """
    Spell checker class. On init it will read /usr/share/dict/words. The method correct will offer a correction.
    A good improvement would be to teach the tree which are the most common words, and choose based on ocurrence instead
    of picking the first valid candidate, but that's out of the scope of the exercise. Other possible optimization is
    multithreaded generation of combinations and discard of prefixes.
    """
    trie = TrieTree()

    def __init__(self):
        """Reads the file and generates the trie tree"""
        file = open('/usr/share/dict/words')
        for word in file:
            self.trie.addWord(str.strip(str.lower(word)))

            #self.trie.addWord('concurrency')

    def _shuffle_vowels(self, word):
        sflist = []

        for index, character in enumerate(word):
            if character in VOWELS:
                sflist.append([word[:index] + vowel for vowel in VOWELS])

                sflist += self._shuffle_vowels(word[index + 1:])
                break

        if not sflist:
            sflist.append([word])

        return sflist

    def _split_duplicates(self, word, findex, tree):
        """
        Will generate a series of prefixes on duplicated consonant. For example adddress would be split in ((ad,add)
        ,(r,rr),(es,ess))
        """
        sflist = []
        index = findex

        word2 = word[findex:]
        wlen = len(word)

        for name, group in groupby(word2):
            size = len(list(group))
            size2 = size
            if size > 1:
                #There are no words with more than three repeated characters

                #if size > 2:
                #if index == findex and name in VOWELS:
                #    size -= 1

                #sflist.append(word[findex:index + 1])
                for x in range(1, min(3,size + 1)):
                    pref = word[findex:index + x]
                    preftocheck = pref[1:]
                    #if index == findex and x > 1:
                    #    preftocheck = pref[1:]

                    if tree.containsPrefix(preftocheck):
                        sflist.append(pref)


                #else:
                #    sflist.append(word[findex:index + 1])
                #    sflist.append(word[findex:index + 2])

                if index + size2 != wlen and sflist:
                    sflist = [w1 + w2 for w1 in sflist for w2 in self._split_duplicates_no_tree(word[index + size:], 0)]

                break

            index += size

        if not sflist:
            sflist.append(word)
        elif findex:
            sflist = [word[:findex] + w1 for w1 in sflist]

        return sflist

    def _split_duplicates_no_tree(self, word, findex):
        """
        Will generate a series of prefixes on duplicated consonant. For example adddress would be split in ((ad,add)
        ,(r,rr),(es,ess))
        """
        sflist = []
        index = findex

        wlen = len(word)

        for name, group in groupby(word[findex:]):
            size = len(list(group))
            if size > 1:

                #There are no words with more than three repeated characters
                if size > 2:
                    sflist.append(word[findex:index+1])
                    sflist.append(word[findex:index + 2])
                    sflist.append(word[findex:index+3])
                else:
                    sflist.append(word[findex:index+1])
                    sflist.append(word[findex:index + 2])


                if index + size != wlen:
                    sflist = [w1 + w2 for w1 in sflist for w2 in self._split_duplicates_no_tree(word[index + size:],0)]

                break


            index += size

        if not sflist:
            sflist.append(word)
        elif findex:
            sflist = [word[:findex] + w1 for w1 in sflist]



        return sflist

    def correct(self, word):
        word = str.lower(word)

        if self.trie.containsWord(word):
            return word

        units = self._shuffle_vowels(word)
        combined_units = []

        for unitlist in units:
            combs = []

            for unit in unitlist:
                if not combined_units:
                    if len(unit) > 1:
                        duplicates = self._split_duplicates(unit, 0, self.trie)
                    else:
                        duplicates = (unit,)

                    combs += [tuple for tuple in self._check_suffix(self.trie, duplicates) if tuple]
                else:
                    combs += self.combine_and_remove_duplicates(combined_units, unit)

                    #combs += [(w[0] + tuple[0], tuple[1]) for w in combined_units for tuple in self.generate_combinations(duplicates, w[1]) if tuple]

            combined_units = combs

        for w, t in combined_units:
            if self.trie.containsWord(w):
                return w

        return NO_SUGGESTION

    def _check_suffix(self, tree, words):
        for word in words:
            yield tree.containsPrefix(word)

    def combine_and_remove_duplicates(self, combined_units, unit):
        combs = []

        for word, dups, tree in [(word, self._split_duplicates(word + unit, len(word) - 1, tree), tree) for word, tree in
                                                                                                  combined_units]:
            for dup in dups:
                if len(dup) == len(word):
                    combs.append((word, tree))
                else:
                    tuple = tree.containsPrefix(dup[len(word):])
                    if tuple:
                        combs.append((dup, tuple[1]))
        return combs


if __name__ == '__main__':
    sc = SpellChecker()

    #for word in ['eabbaanddooneeee']:
    for word in sys.stdin:
        word = str.strip(word)
        #print "Correcting %s"%word
        correction = sc.correct(word)
        print correction
        if correction is NO_SUGGESTION:
            sys.exit(-1)