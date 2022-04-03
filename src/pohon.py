class TreeNode:
    id = 0
    def __init__(self, name, puzzle, distance, cost, path):
        self.name = name
        TreeNode.id += 1
        self.id = TreeNode.id
        self.children = []
        self.puzzle = puzzle
        self.distance = distance
        self.cost = cost + distance
        self.path = path
    
    def addChild(self, obj):
        self.children.append(obj)
