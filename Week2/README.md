Question 2:
The complexity of searching / adding / removing an element is mostly O(1) with a hash table, whereas the complexity is O(log N) with a tree. This means that a hash table is more efficient than a tree. However, real-world large-scale database systems tend to prefer a tree to a hash table. Why? List as many reasons as possible.

- Knowing the right table size 
- Cost of re-hashing
- The worst case of hash table is O(N): trees guarantee O(logN)
- Trees enable searching for nearby objects as well (aware of relations)

Question 3:
Design a cache that achieves the following operations with mostly O(1)
When a pair of <URL, Web page> is given, find if the given pair is contained in the cache or not
If the pair is not found, insert the pair into the cache after evicting the least recently accessed pair
- Doubly Linked List combined with Hash Tables

