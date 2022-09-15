from rbt import *
import pickle

if __name__ == "__main__":
    bst = RedBlackTree()
    bst.insert(("/folder1/folder2/test1.jij","32fb249f42f82a4f924fc2f40df4"))
    bst.insert(("/folder1/yes.aaa","afdddhf982ed2f9debf92ebf29d"))
    bst.insert(("/folder1/folder3/folder4/wops.aab","afueb92ebf2fb2e2e9ijbf92ebf29d"))
    bst.insert(("/wips.aab","afdfjbf792ebf2fb2e2e9ijbf92ebf29d"))


#https://algorithmtutor.com/Data-Structures/Tree/Red-Black-Trees/
#https://github.com/Bibeknam/algorithmtutorprograms/blob/master/data-structures/red-black-trees/red_black_tree.py


bst.pretty_print()

with open('prueba', 'wb') as f:
    pickle.dump(bst,f)

