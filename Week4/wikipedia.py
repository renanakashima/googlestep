import sys
import collections
from collections import deque

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
    # BFS に工夫を入れて最短経路を出せるようにする
    # collections.deque を使うとスタックやキューが作れます
    # 30 行程度で書けます😀
        # Find the page IDs for start and goal titles
        start_id = None
        goal_id = None
        for page_id, title in self.titles.items():
            if title == start:
                start_id = page_id
            if title == goal:
                goal_id = page_id
        
        if start_id is None or goal_id is None:
            return "Page not found"
        
        if start_id == goal_id:
            return [self.titles[start_id]]
        
        queue = deque()
        # a simple list / set (faster) is better
        visited = {}
        #prev is better
        parent = {}  
        
        visited[start_id] = True
        queue.append(start_id)
        parent[start_id] = None
        
        while len(queue) != 0:
            node = queue.popleft()
            
            #this is where we find a goal; therefore we construct a path
            if node == goal_id:
                path = []
                current = goal_id
                while current is not None:
                    path.append(self.titles[current])
                    #parent points back from the current node to parent node
                    current = parent[current]
                path.reverse() 
                return path
                
            for child in self.links[node]:
                if child not in visited:
                    visited[child] = True
                    parent[child] = node  
                    queue.append(child)
        
        return "Not Found"


    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
    #return the top 10 pages  
    # 正しさの確認方法
    #  ページランクの分配と更新を何回繰り返しても「全部のノードのページランクの合計値」が一定に保たれることを確認してください
    #  一定にならない場合何かが間違ってます！

    # Large のデータセットで動かすためには O(N + E) のアルゴリズムが必要です
    #  ページ数：N = 2215900
    #  リンク数：E = 119006494 
    
    # ページランクの更新が「完全に」収束するのは時間がかかりすぎるので、更新が十分少なくなったら止める
    # 収束条件の作り方の例：
    # ∑(new_pagerank[i] - old_pagerank[i])^2 < 0.01
        damping = 0.85
        tol = 0.01
        N = len(self.titles)
        ranks = {pid: 1.0 / N for pid in self.titles}
        out_deg = {pid: len(self.links[pid]) for pid in self.titles}
        
        while True:
            # 1 0.5   => 0.075 / 3
            # 2 0.3   => 0.045 / 3
            # 3 0.2   => 0.03 / 3

            # 1 (0.075 / 3) + (0.045 / 3) + (0.03 / 3)
            # 2 (0.075 / 3) + (0.045 / 3) + (0.03 / 3)
            # 3 (0.075 / 3) + (0.045 / 3) + (0.03 / 3)

            # for each ind node, allocate 15% of the rank in every single node
            # compute_rank = 
            # for src1 in self.links:
            #     compute_rank = {pid: new_ranks[pid] + (1.0 - damping) * ranks[src1] / N }
            # new_ranks = {pid: compute_rank for pid in self.titles}



            new_ranks = {pid: 0 for pid in self.titles}
            for src1 in self.links:
            #for src1 in self.links.keys():
                compute_rank = new_ranks[pid] + (1.0 - damping) * ranks[src1] / N
            new_ranks = {pid: compute_rank for pid in self.titles}

            for src, dsts in self.links.items():
                if out_deg[src] == 0:
                    contrib = damping * ranks[src] / N
                    for pid in new_ranks:
                        new_ranks[pid] += contrib
                else:
                    contrib = damping * ranks[src] / out_deg[src]
                    for dst in dsts:
                        new_ranks[dst] += contrib
    
            delta = sum((new_ranks[pid] - ranks[pid])**2 for pid in ranks)
            ranks = new_ranks

            if delta < tol:
                break
                
        top10 = sorted(ranks.items(), key=lambda x: x[1], reverse=True)[:10]
        print("Top 10 pages by PageRank:")
        for pid, score in top10:
            print(f"{self.titles[pid]}: {score:.6f}")

        return [(self.titles[pid], score) for pid, score in top10]

    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])
        visited = {}
        for node in path:
            assert(node not in visited)
            visited[node] = True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    wikipedia.find_longest_titles()
    # Example
    wikipedia.find_most_linked_pages()
    # Homework #1
    result1 = wikipedia.find_shortest_path("A", "F")
    if result1:
        print("Result 1: ", result1)
    result2 = wikipedia.find_shortest_path("渋谷", "パレートの法則")
    if result2:
        print("Result 2: ", result2)
    result3 = wikipedia.find_shortest_path("新宿", "スイス")
    if result2:
        print("Result 3: ", result3)
    # test case where the goal is not reachable
    # doesn't go through an infinite loop
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")