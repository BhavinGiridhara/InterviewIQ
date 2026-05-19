from random import choice
from app.models import InterviewQuestion


def q(id, role, topic, difficulty, question, expected, hints):
    return InterviewQuestion(
        id=id,
        role=role,
        topic=topic,
        difficulty=difficulty,
        question=question,
        expected_concepts=expected,
        hints=hints,
    )


QUESTION_BANK = [
    # -------------------- DATA STRUCTURES: EASY --------------------
    q("ds-array-vs-linkedlist-easy", "SWE Intern", "Data Structures", "Easy",
      "What is the difference between an array and a linked list? When would you use each?",
      ["array", "linked list", "indexing", "memory", "insert", "delete", "O(1)", "O(n)"],
      ["Compare random access.", "Mention insertion/deletion tradeoffs.", "Use Big-O." ]),
    q("ds-hashmap-easy", "SWE Intern", "Data Structures", "Easy",
      "What is a hash map, and why is average lookup usually O(1)?",
      ["hash function", "key", "value", "bucket", "collision", "O(1)"],
      ["Explain key-value storage.", "Mention hashing.", "Mention collisions." ]),
    q("ds-stack-easy", "SWE Intern", "Data Structures", "Easy",
      "What is a stack? Give one real-world or programming example where a stack is useful.",
      ["stack", "LIFO", "push", "pop", "call stack", "undo"],
      ["Define LIFO.", "Mention push/pop.", "Give a practical example." ]),
    q("ds-queue-easy", "SWE Intern", "Data Structures", "Easy",
      "What is a queue? How is it different from a stack?",
      ["queue", "FIFO", "enqueue", "dequeue", "stack", "LIFO"],
      ["Define FIFO.", "Compare to LIFO.", "Mention enqueue/dequeue." ]),
    q("ds-bst-easy", "SWE Intern", "Data Structures", "Easy",
      "What property makes a binary search tree searchable?",
      ["binary search tree", "left", "right", "ordering", "search", "O(log n)", "O(n)"],
      ["Describe left subtree vs right subtree.", "Mention balanced vs unbalanced.", "Discuss search path." ]),
    q("ds-set-easy", "SWE Intern", "Data Structures", "Easy",
      "What is a set data structure, and how is it different from a list?",
      ["set", "unique", "duplicates", "list", "membership", "hashing"],
      ["Mention uniqueness.", "Compare membership checks.", "Mention duplicates." ]),
    q("ds-heap-easy", "SWE Intern", "Data Structures", "Easy",
      "What is a heap, and what problem is it commonly used to solve?",
      ["heap", "priority queue", "min heap", "max heap", "root", "priority"],
      ["Mention priority queues.", "Explain min/max at root.", "Give scheduling as an example." ]),
    q("ds-graph-easy", "SWE Intern", "Data Structures", "Easy",
      "What is a graph in computer science? Explain nodes and edges with an example.",
      ["graph", "node", "edge", "directed", "undirected", "social network"],
      ["Define nodes and edges.", "Give a real example.", "Mention directed/undirected if possible." ]),
    q("ds-time-complexity-easy", "SWE Intern", "Data Structures", "Easy",
      "Why is searching an unsorted array usually O(n)?",
      ["linear search", "unsorted", "O(n)", "worst case", "scan"],
      ["Explain that there is no ordering clue.", "Mention checking elements one by one.", "Mention worst case." ]),
    q("ds-collision-easy", "SWE Intern", "Data Structures", "Easy",
      "What is a collision in a hash table, and how can it be handled?",
      ["collision", "hash table", "bucket", "chaining", "open addressing"],
      ["Define collision.", "Mention chaining.", "Mention probing/open addressing." ]),

    # -------------------- DATA STRUCTURES: MEDIUM --------------------
    q("ds-stack-queues-medium", "SWE Intern", "Data Structures", "Medium",
      "How would you implement a stack using two queues? Explain the tradeoffs.",
      ["stack", "queue", "LIFO", "FIFO", "push", "pop", "time complexity", "tradeoff"],
      ["Mention that stacks are LIFO while queues are FIFO.", "Explain whether push or pop will be expensive.", "Talk about time complexity." ]),
    q("ds-lru-cache-medium", "SWE Intern", "Data Structures", "Medium",
      "Design an LRU cache. What data structures would you combine and why?",
      ["LRU", "hash map", "doubly linked list", "O(1)", "eviction", "capacity"],
      ["Use a hash map for lookup.", "Use a doubly linked list for recency order.", "Mention eviction." ]),
    q("ds-min-stack-medium", "SWE Intern", "Data Structures", "Medium",
      "How would you design a stack that can return the minimum element in O(1)?",
      ["stack", "min stack", "O(1)", "auxiliary stack", "push", "pop"],
      ["Use a second stack.", "Store current minimums.", "Explain push/pop behavior." ]),
    q("ds-cycle-linkedlist-medium", "SWE Intern", "Data Structures", "Medium",
      "How would you detect whether a linked list has a cycle?",
      ["linked list", "cycle", "fast pointer", "slow pointer", "Floyd", "O(1) space"],
      ["Mention two pointers.", "Fast moves two steps.", "If they meet, there is a cycle." ]),
    q("ds-valid-parentheses-medium", "SWE Intern", "Data Structures", "Medium",
      "How would you check if a string of parentheses/brackets is valid?",
      ["stack", "parentheses", "matching", "push", "pop", "O(n)"],
      ["Use a stack for opening brackets.", "Pop when matching closing bracket appears.", "Check leftover stack." ]),
    q("ds-queue-stacks-medium", "SWE Intern", "Data Structures", "Medium",
      "How would you implement a queue using two stacks? Explain amortized complexity.",
      ["queue", "stack", "FIFO", "LIFO", "amortized", "O(1)", "transfer"],
      ["Use input and output stacks.", "Transfer only when needed.", "Explain amortized O(1)." ]),
    q("ds-top-k-medium", "SWE Intern", "Data Structures", "Medium",
      "How would you find the top K largest numbers in a huge list?",
      ["heap", "min heap", "top k", "O(n log k)", "memory"],
      ["Use a min heap of size k.", "Compare with sorting.", "Explain why it saves memory/time." ]),
    q("ds-trie-medium", "SWE Intern", "Data Structures", "Medium",
      "When would a trie be useful, and how would autocomplete use it?",
      ["trie", "prefix", "autocomplete", "children", "search", "words"],
      ["Mention prefix search.", "Each node stores characters.", "Autocomplete follows prefix path." ]),
    q("ds-graph-representation-medium", "SWE Intern", "Data Structures", "Medium",
      "Compare adjacency lists and adjacency matrices for representing graphs.",
      ["graph", "adjacency list", "adjacency matrix", "space", "edge lookup", "sparse", "dense"],
      ["Discuss space complexity.", "Mention sparse vs dense graphs.", "Compare edge lookup." ]),
    q("ds-bst-delete-medium", "SWE Intern", "Data Structures", "Medium",
      "How do you delete a node from a binary search tree? Explain the main cases.",
      ["BST", "delete", "leaf", "one child", "two children", "successor", "predecessor"],
      ["Handle leaf nodes.", "Handle one child.", "For two children, use successor/predecessor." ]),

    # -------------------- DATA STRUCTURES: HARD --------------------
    q("ds-median-stream-hard", "SWE Intern", "Data Structures", "Hard",
      "How would you continuously find the median from a stream of numbers?",
      ["median", "stream", "two heaps", "min heap", "max heap", "balance"],
      ["Use two heaps.", "Keep sizes balanced.", "Median comes from heap tops." ]),
    q("ds-union-find-hard", "SWE Intern", "Data Structures", "Hard",
      "Explain Union-Find. How do path compression and union by rank improve performance?",
      ["union find", "disjoint set", "path compression", "rank", "connected components"],
      ["Explain find and union.", "Mention flattening trees.", "Mention connected components." ]),
    q("ds-lfu-cache-hard", "SWE Intern", "Data Structures", "Hard",
      "Design an LFU cache. How is it different from an LRU cache?",
      ["LFU", "LRU", "frequency", "hash map", "linked list", "eviction", "tie breaker"],
      ["Track frequency counts.", "Handle ties by recency.", "Discuss O(1) target design." ]),
    q("ds-serialize-tree-hard", "SWE Intern", "Data Structures", "Hard",
      "How would you serialize and deserialize a binary tree?",
      ["serialize", "deserialize", "tree", "DFS", "BFS", "null markers", "reconstruction"],
      ["Pick DFS or BFS.", "Store null markers.", "Explain how to rebuild." ]),
    q("ds-word-search-hard", "SWE Intern", "Data Structures", "Hard",
      "How would you solve Word Search II efficiently on a board with many words?",
      ["trie", "DFS", "backtracking", "visited", "prefix pruning", "board"],
      ["Build a trie of words.", "DFS from board cells.", "Prune invalid prefixes." ]),
    q("ds-range-query-hard", "SWE Intern", "Data Structures", "Hard",
      "When would you use a segment tree or Fenwick tree? Explain a use case.",
      ["segment tree", "Fenwick tree", "range query", "update", "prefix sum", "log n"],
      ["Mention range sums/min/max.", "Discuss updates.", "Compare to recomputing each query." ]),
    q("ds-graph-shortest-hard", "SWE Intern", "Data Structures", "Hard",
      "How would you choose between BFS, Dijkstra, and A* for pathfinding?",
      ["BFS", "Dijkstra", "A*", "weighted graph", "unweighted graph", "heuristic"],
      ["BFS for unweighted.", "Dijkstra for nonnegative weights.", "A* uses a heuristic." ]),
    q("ds-persistent-structure-hard", "SWE Intern", "Data Structures", "Hard",
      "What is a persistent data structure, and why might immutable versions be useful?",
      ["persistent", "immutability", "structural sharing", "versions", "memory", "undo"],
      ["Explain keeping old versions.", "Mention structural sharing.", "Give undo/history as example." ]),

    # -------------------- ALGORITHMS: EASY --------------------
    q("alg-two-sum-easy", "SWE Intern", "Algorithms", "Easy",
      "Explain how you would solve Two Sum efficiently and why it is better than brute force.",
      ["hash map", "complement", "O(n)", "brute force", "nested loops"],
      ["Mention storing seen numbers.", "Mention complement = target - current.", "Compare O(n) and O(n^2)." ]),
    q("alg-binary-search-easy", "SWE Intern", "Algorithms", "Easy",
      "Explain binary search and why it requires sorted input.",
      ["binary search", "sorted", "middle", "left", "right", "O(log n)"],
      ["Mention halving the search space.", "Explain why order matters.", "Give complexity." ]),
    q("alg-linear-vs-binary-easy", "SWE Intern", "Algorithms", "Easy",
      "Compare linear search and binary search.",
      ["linear search", "binary search", "sorted", "O(n)", "O(log n)"],
      ["Mention sorted requirement.", "Compare Big-O.", "Mention simple scan vs halving." ]),
    q("alg-palindrome-easy", "SWE Intern", "Algorithms", "Easy",
      "How would you check if a string is a palindrome?",
      ["two pointers", "string", "palindrome", "left", "right", "O(n)"],
      ["Use left and right pointers.", "Move inward.", "Compare characters." ]),
    q("alg-duplicates-easy", "SWE Intern", "Algorithms", "Easy",
      "How would you check if an array contains duplicates?",
      ["set", "hashing", "duplicates", "O(n)", "space"],
      ["Use a set.", "If seen before, duplicate exists.", "Discuss time and space." ]),
    q("alg-reverse-string-easy", "SWE Intern", "Algorithms", "Easy",
      "How would you reverse a string or array in place?",
      ["two pointers", "swap", "in place", "O(n)", "O(1) space"],
      ["Use two pointers.", "Swap ends.", "Move inward." ]),

    # -------------------- ALGORITHMS: MEDIUM --------------------
    q("alg-sliding-window-medium", "SWE Intern", "Algorithms", "Medium",
      "When would you use a sliding window? Give an example problem.",
      ["sliding window", "subarray", "substring", "left", "right", "O(n)"],
      ["Mention contiguous ranges.", "Move left/right pointers.", "Avoid recomputing work." ]),
    q("alg-bfs-dfs-medium", "SWE Intern", "Algorithms", "Medium",
      "Compare BFS and DFS. When would you choose one over the other?",
      ["BFS", "DFS", "queue", "stack", "shortest path", "graph", "tree"],
      ["BFS explores level by level.", "DFS goes deep first.", "Mention shortest path in unweighted graphs." ]),
    q("alg-merge-intervals-medium", "SWE Intern", "Algorithms", "Medium",
      "How would you merge overlapping intervals?",
      ["intervals", "sort", "overlap", "merge", "O(n log n)"],
      ["Sort by start time.", "Track current interval.", "Merge when overlapping." ]),
    q("alg-topological-sort-medium", "SWE Intern", "Algorithms", "Medium",
      "What is topological sorting, and how could it be used for course prerequisites?",
      ["topological sort", "DAG", "prerequisites", "in-degree", "dependency", "cycle"],
      ["Mention directed acyclic graph.", "Prerequisites are dependencies.", "Cycles make it impossible." ]),
    q("alg-recursion-medium", "SWE Intern", "Algorithms", "Medium",
      "Explain recursion using tree traversal as an example.",
      ["recursion", "base case", "recursive case", "tree", "call stack", "traversal"],
      ["Mention base case.", "Mention recursive calls on children.", "Discuss call stack." ]),
    q("alg-dp-medium", "SWE Intern", "Algorithms", "Medium",
      "What is dynamic programming? Explain it using climbing stairs or Fibonacci.",
      ["dynamic programming", "overlapping subproblems", "memoization", "tabulation", "state"],
      ["Mention repeated subproblems.", "Use memoization or table.", "Define state." ]),
    q("alg-sorting-medium", "SWE Intern", "Algorithms", "Medium",
      "Compare quicksort and mergesort at a high level.",
      ["quicksort", "mergesort", "partition", "divide and conquer", "O(n log n)", "worst case"],
      ["Both are divide and conquer.", "Mention quicksort worst case.", "Mention mergesort extra memory." ]),

    # -------------------- ALGORITHMS: HARD --------------------
    q("alg-dijkstra-hard", "SWE Intern", "Algorithms", "Hard",
      "Explain Dijkstra's algorithm. What assumptions does it make about edge weights?",
      ["Dijkstra", "priority queue", "shortest path", "weighted graph", "nonnegative", "relaxation"],
      ["Use a priority queue.", "Mention nonnegative weights.", "Explain relaxing distances." ]),
    q("alg-bellman-ford-hard", "SWE Intern", "Algorithms", "Hard",
      "When would Bellman-Ford be preferred over Dijkstra's algorithm?",
      ["Bellman-Ford", "Dijkstra", "negative weights", "negative cycle", "shortest path"],
      ["Mention negative edges.", "Mention detecting negative cycles.", "Compare complexity." ]),
    q("alg-kmp-hard", "SWE Intern", "Algorithms", "Hard",
      "How does KMP improve string matching compared with checking every alignment?",
      ["KMP", "string matching", "prefix table", "LPS", "O(n+m)", "avoid rechecking"],
      ["Mention prefix/suffix table.", "Explain skipping repeated comparisons.", "Give complexity." ]),
    q("alg-backtracking-hard", "SWE Intern", "Algorithms", "Hard",
      "How would you solve N-Queens using backtracking?",
      ["backtracking", "N-Queens", "constraints", "columns", "diagonals", "recursion"],
      ["Place queens row by row.", "Track attacked columns/diagonals.", "Undo choices." ]),
    q("alg-dp-knapsack-hard", "SWE Intern", "Algorithms", "Hard",
      "Explain the 0/1 Knapsack problem and what the DP state represents.",
      ["knapsack", "dynamic programming", "state", "capacity", "choice", "optimal substructure"],
      ["Define dp[i][capacity].", "Choose take or skip.", "Mention optimal substructure." ]),
    q("alg-cycle-detection-hard", "SWE Intern", "Algorithms", "Hard",
      "How would you detect a cycle in a directed graph?",
      ["directed graph", "cycle", "DFS", "visiting", "visited", "recursion stack"],
      ["Use DFS states.", "Visiting means currently in recursion stack.", "Back edge means cycle." ]),

    # -------------------- SYSTEM DESIGN: EASY/MEDIUM/HARD --------------------
    q("sys-rest-easy", "Backend Intern", "System Design", "Easy",
      "What is a REST API? Explain GET vs POST with an example.",
      ["REST", "API", "GET", "POST", "resource", "request", "response"],
      ["GET reads data.", "POST creates/sends data.", "Use a simple endpoint example." ]),
    q("sys-status-codes-easy", "Backend Intern", "System Design", "Easy",
      "What do HTTP status codes like 200, 400, 404, and 500 mean?",
      ["HTTP", "200", "400", "404", "500", "client error", "server error"],
      ["Group by success/client/server.", "Give examples.", "Mention debugging value." ]),
    q("sys-api-medium", "Backend Intern", "System Design", "Medium",
      "Design a simple URL shortener. What APIs, database tables, and edge cases would you consider?",
      ["POST", "GET", "database", "unique code", "redirect", "collision", "expiration", "rate limiting"],
      ["Define create-short-url and redirect endpoints.", "Mention mapping short code to long URL.", "Consider collisions and abuse." ]),
    q("sys-rate-limit-medium", "Backend Intern", "System Design", "Medium",
      "How would you add rate limiting to an API?",
      ["rate limiting", "API", "user", "IP", "Redis", "token bucket", "sliding window"],
      ["Track requests by user/IP.", "Use Redis for shared state.", "Mention time windows." ]),
    q("sys-cache-medium", "Backend Intern", "System Design", "Medium",
      "Where would caching help in a web app, and what are the risks?",
      ["cache", "latency", "database", "stale data", "TTL", "invalidation"],
      ["Mention repeated reads.", "Discuss stale data.", "Mention TTL/invalidation." ]),
    q("sys-chat-hard", "Backend Intern", "System Design", "Hard",
      "Design a real-time chat system. What components would you need?",
      ["WebSocket", "database", "message queue", "scaling", "presence", "delivery", "persistence"],
      ["Use WebSockets for real time.", "Store messages.", "Discuss scaling multiple servers." ]),
    q("sys-feed-hard", "Backend Intern", "System Design", "Hard",
      "Design a social media feed. How would you generate and rank posts?",
      ["feed", "ranking", "fanout", "cache", "database", "pagination", "scaling"],
      ["Discuss pull vs push/fanout.", "Mention ranking signals.", "Mention caching/pagination." ]),

    # -------------------- OOP: EASY/MEDIUM/HARD --------------------
    q("oop-class-object-easy", "SWE Intern", "OOP", "Easy",
      "Explain the difference between a class and an object.",
      ["class", "object", "instance", "fields", "methods", "blueprint"],
      ["Class is blueprint.", "Object is instance.", "Give example." ]),
    q("oop-encapsulation-easy", "SWE Intern", "OOP", "Easy",
      "What is encapsulation, and why is it useful?",
      ["encapsulation", "private", "public", "methods", "data hiding", "validation"],
      ["Mention hiding internal state.", "Use methods to control access.", "Explain maintainability." ]),
    q("oop-library-medium", "SWE Intern", "OOP", "Medium",
      "Design classes for a library checkout system. What objects and relationships would you use?",
      ["class", "object", "Book", "User", "Checkout", "encapsulation", "relationship"],
      ["Identify core nouns.", "Separate data from behavior.", "Mention relationships between users and books." ]),
    q("oop-parking-medium", "SWE Intern", "OOP", "Medium",
      "Design classes for a parking lot system.",
      ["class", "ParkingLot", "Spot", "Vehicle", "Ticket", "inheritance", "composition"],
      ["Identify entities.", "Use composition.", "Think about spot types and vehicle types." ]),
    q("oop-solid-hard", "SWE Intern", "OOP", "Hard",
      "Explain one SOLID principle and show how it improves code design.",
      ["SOLID", "single responsibility", "open closed", "dependency inversion", "maintainability"],
      ["Pick one principle.", "Give before/after example.", "Tie to maintainability." ]),
    q("oop-elevator-hard", "SWE Intern", "OOP", "Hard",
      "Design an elevator control system using OOP. What classes and responsibilities would you define?",
      ["Elevator", "Floor", "Request", "Controller", "state", "queue", "responsibility"],
      ["Separate controller from elevator.", "Track direction/state.", "Discuss request queues." ]),

    # -------------------- DEBUGGING: EASY/MEDIUM/HARD --------------------
    q("debug-api-easy", "SWE Intern", "Debugging", "Easy",
      "A frontend receives a 500 error from the backend. How would you debug it step by step?",
      ["reproduce", "logs", "network tab", "request payload", "stack trace", "status code"],
      ["Start by reproducing the issue.", "Check browser Network tab.", "Check backend logs." ]),
    q("debug-null-easy", "SWE Intern", "Debugging", "Easy",
      "Your code throws a null/undefined error. What steps would you take to find the cause?",
      ["reproduce", "stack trace", "logs", "null", "input", "guard clause"],
      ["Read the stack trace.", "Find the variable that is null.", "Check assumptions/input." ]),
    q("debug-slow-medium", "SWE Intern", "Debugging", "Medium",
      "An endpoint suddenly becomes slow. How would you investigate?",
      ["latency", "logs", "database", "query", "profiling", "metrics", "cache"],
      ["Check when it started.", "Look at logs/metrics.", "Inspect DB queries." ]),
    q("debug-memory-medium", "SWE Intern", "Debugging", "Medium",
      "A web app's memory usage keeps growing. What might cause it and how would you debug it?",
      ["memory leak", "profiling", "references", "listeners", "cache", "cleanup"],
      ["Mention leaks from retained references.", "Use profiling tools.", "Check event listeners/caches." ]),
    q("debug-race-hard", "SWE Intern", "Debugging", "Hard",
      "A bug only happens sometimes in production but not locally. How would you debug it?",
      ["race condition", "logs", "observability", "reproduction", "feature flags", "concurrency"],
      ["Think about timing/concurrency.", "Add structured logs.", "Use production-safe diagnostics." ]),
    q("debug-distributed-hard", "Backend Intern", "Debugging", "Hard",
      "A request passes through multiple services and occasionally fails. How would you trace it?",
      ["distributed tracing", "correlation id", "logs", "metrics", "timeouts", "retries"],
      ["Use correlation IDs.", "Check traces/logs across services.", "Look for timeouts/retries." ]),
]


def find_question(question_id: str) -> InterviewQuestion | None:
    for question in QUESTION_BANK:
        if question.id == question_id:
            return question
    return None


def _matches(question: InterviewQuestion, role: str, topic: str, difficulty: str) -> bool:
    role_lower = role.lower()
    return (
        question.topic.lower() == topic.lower()
        and question.difficulty.lower() == difficulty.lower()
        and (role_lower in question.role.lower() or question.role.lower() in role_lower or question.role == "SWE Intern")
    )


def select_question(role: str, topic: str, difficulty: str, exclude_ids: list[str] | None = None) -> InterviewQuestion:
    exclude_ids = set(exclude_ids or [])

    exact = [q for q in QUESTION_BANK if _matches(q, role, topic, difficulty)]
    available = [q for q in exact if q.id not in exclude_ids]
    if available:
        return choice(available)
    if exact:
        return choice(exact)

    topic_and_difficulty = [q for q in QUESTION_BANK if q.topic.lower() == topic.lower() and q.difficulty.lower() == difficulty.lower()]
    available = [q for q in topic_and_difficulty if q.id not in exclude_ids]
    if available:
        return choice(available)
    if topic_and_difficulty:
        return choice(topic_and_difficulty)

    same_difficulty = [q for q in QUESTION_BANK if q.difficulty.lower() == difficulty.lower()]
    available = [q for q in same_difficulty if q.id not in exclude_ids]
    if available:
        return choice(available)
    if same_difficulty:
        return choice(same_difficulty)

    return choice(QUESTION_BANK)
