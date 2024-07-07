# From https://algo.monster/liteproblems/425

# Given a list of words, find all word squares you can build from them. A sequence of words forms a word square if the kth row and column read the exact same string, where 0 ≤ k < max(numRows, numColumns).

class Trie:
    def __init__(self):
        # Each Trie node contains an array of 26 Trie nodes, representing the 26 lowercase English letters
        self.children = [None] * 26
        # 'values' is a list that holds the indices of words corresponding to the node path
        self.values = []

    def insert(self, word, index):
        # Insert a word into the Trie with corresponding index
        node = self
        for char in word:
            char_index = ord(char) - ord('a')
            if node.children[char_index] is None:
                node.children[char_index] = Trie()
            node = node.children[char_index]
            # Append the index of the word at every character's node
            node.values.append(index)

    def search(self, prefix):
        # Return a list of indices of words that start with the given prefix
        node = self
        for char in prefix:
            char_index = ord(char) - ord('a')
            if node.children[char_index] is None:
                return []  # Prefix not found
            node = node.children[char_index]
        return node.values


class Solution:
    def wordSquares(self, words):
        def dfs(square):
            # Depth-first search to build word squares
            if len(square) == len(words[0]):  # Base case: Square is complete
                squares.append(square[:])  # Add a deep copy of the current square to results
                return
            # Get the current prefix to be matched from all words in the square
            idx = len(square)
            prefix = [word[idx] for word in square]
            # Find all words in the Trie with the current prefix
            indices = trie.search(''.join(prefix))
            for index in indices:
                square.append(words[index])  # Add the matching word to the current square
                dfs(square)                 # Continue to build the square recursively
                square.pop()                # Backtrack to try another word

        trie = Trie()
        squares = []
        # Insert all words into the Trie along with their respective indices
        for i, word in enumerate(words):
            trie.insert(word, i)
      
        # Initialize the depth-first search with each word as a starting point
        for word in words:
            dfs([word])
            print(len(squares))
      
        return squares

def _read_words(fileName):
    words = []

    with open(fileName, 'r') as f:
        for line in f:
            if (len(line.strip()) == 3) and line.strip().isalpha():
                words.append(line.strip())
    return words

# words = _read_words('words.txt')
# print(words)
words = ["abc", "bca", "cab"]
sol = Solution().wordSquares(words)
print(sol)
# filter lists in sol that have the same words
# def remove_duplicate_arrays(arrays):
#     unique_arrays = {}
#     for array in arrays:
#         # Convert the list to a frozenset to normalize the order
#         normalized = frozenset(array)
#         # Store the original list in the dictionary with the frozenset as the key
#         unique_arrays[normalized] = array
#     # Extract the unique lists from the dictionary values
#     return list(unique_arrays.values())

# unique_arrays = remove_duplicate_arrays(sol)
# print(len(unique_arrays))
# print(sol)

# # print which arrays are in sol that arent in unique_arrays
# for array in sol:
#     if array not in unique_arrays:
#         print(array)

