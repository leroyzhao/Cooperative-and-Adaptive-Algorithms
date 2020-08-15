class Node:
  def __init__(self, coords, parent):
    self.location = coords
    self.parent = parent
    if parent == None:
      self.cost = 1
    else:
      self.cost = parent.cost + 1

def printPath(endNode):
  n = endNode
  pathTaken = []
  while n!=None:
    pathTaken.append(n.location)
    n = n.parent
  
  #BFS
  print("Path Taken:")
  [print(pathTaken[i]) for i in range(len(pathTaken)-1, -1, -1)]

  #DFS
  # pathTaken.reverse()
  # print("Path Taken:\n", pathTaken)

  print("\nCost:", endNode.cost)

no_go = {(4,24),(5,24),(17,24),(18,24),
(0,23),(1,23),(2,23),(3,23),(4,23),(5,23),(6,23),(7,23),(8,23),(9,23),
(0,22),(1,22),(2,22),(3,22),(4,22),(8,22),(14,22),(15,22),(16,22),(17,22),(18,22),(19,22),(20,22),
(3,21),(4,21),(5,21),(8,21),(14,21),(15,21),(16,21),(17,21),(18,21),(19,21),(20,21),
(3,20),(4,20),(5,20),(8,20),(9,20),(10,20),(14,20),(15,20),(16,20),(17,20),(18,20),(19,20),(20,20),
(8,19),(9,19),(10,19),
(8,18),(9,18),(10,18),(14,18),(15,18),(16,18),(17,18),(18,18),(19,18),(20,18),
(0,17),(1,17),(2,17),(3,17),(4,17),(5,17),(6,17),(8,17),
(10,16),(24,16),
(10,15),(23,15),(24,15),
(8,14),(9,14),(10,14),(11,14),(12,14),(15,14),(16,14),(22,14),(23,14),(24,14),
(10,13),(15,13),(16,13),(21,13),(22,13),(23,13),(24,13),
(10,12),(15,12),(16,12),(18,12),(21,12),(24,12),
(4,11),(15,11),(16,11),(18,11),(21,11),
(15,10),(16,10),(18,10),(21,10),
(18,9),(21,9),
(2,8),(3,8),(4,8),(18,8),(21,8),
(2,7),(3,7),(4,7),(6,7),(7,7),(10,7),(11,7),(12,7),(18,7),
(2,6),(6,6),(7,6),(10,6),(11,6),(12,6),(18,6),(19,6),(20,6),(21,6),(22,6),(23,6),
(0,5),(1,5),(2,5),(6,5),(7,5),(10,5),(11,5),(12,5),(18,5),(19,5),(20,5),(21,5),
(0,4),(1,4),(2,4),(6,4),(7,4),(10,4),(11,4),(12,4),(18,4),(19,4),
(6,3),(7,3),(10,3),(11,3),(12,3),(18,3),(19,3),
(10,2),(11,2),(12,2),(18,2),(19,2),
(18,1),(19,1),
}

# S, E1
s = Node((2,11), None)
g = Node((23,19), None)
# S, E2
# s = Node((2,11), None)
# g = Node((2,21), None)
# (0,0), (24,24)
# s = Node((0,0), None)
# g = Node((24,24), None)

fringe = []
fringe.append(s)
expanded = set()

while len(fringe) != 0:
  u = fringe.pop()
  if u.location==g.location:
    printPath(u)
    break
  if u.location not in expanded:
    expanded.add(u.location)

    stepOptions = [
      (u.location[0],u.location[1]+1),
      (u.location[0]+1,u.location[1]),
      (u.location[0],u.location[1]-1),
      (u.location[0]-1,u.location[1])
    ]    

    for option in stepOptions:
      if ((option not in expanded) and (option not in no_go) and (max(option[0], option[1]) < 25) and (min(option[0], option[1]) > -1)):

        #BFS
        fringe.insert(0, Node(option, u))
        #DFS
        # fringe.append(Node(option, u))

print("Number of expanded nodes:", len(expanded))