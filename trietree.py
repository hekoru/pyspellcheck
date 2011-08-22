__author__ = 'hector'


class TrieTree(object):
    """ Dead simple Trie tree implementation using maps """

    root = {}

    def addWord(self,word):
        """Adds a new word to the trie tree"""
        node = self.root
        for char in word:
            leaf = node.get(char)
            if not leaf:
                leaf = {}
                node[char] = leaf

            node = leaf
        node['cw'] = True


    def containsWord(self, word):
        """Return True if the word is contained in the trie tree"""
        node = self.root
        found = True
        for char in word:
            leaf = node.get(char)
            if leaf is None:
                found = False
                break
            else:
                node = leaf

        return found and node.get('cw') is True

    def containsPrefix(self, prefix):
        """ Return a (prefix, subtree) tuple if the searched subtree contains the given prefix """
        node = self.root
        found = True
        for char in prefix:
            leaf = node.get(char)
            if leaf is None:
                found = False
                break
            else:
                node = leaf
        if found:
            tree = TrieTree()
            tree.root = node
            return prefix, tree
        else:
            return None




  