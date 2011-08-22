__author__ = 'hector'


class TrieTree(object):

    root = {}

    def addWord(self,word):
        node = self.root
        for char in word:
            leaf = node.get(char)
            if not leaf:
                leaf = {}
                node[char] = leaf

            node = leaf
        node['cw'] = True


    def containsWord(self, word):
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




  