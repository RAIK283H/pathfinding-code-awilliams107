# Pathfinding Starter Code

Random Pathing Algorithm:
The random pathing algorithm being implemented keeps track of a current node and a set of neighbors and visited nodes to try and create a path to both the target and exit node respectively
The tracking allows it to make only valid moves, and the visited nodes ensures that it cannot double back with a previous route
There is also an implemented retry method where the random generator will try around 40 times by default to create a valid path to ensure smoothness and limit failures, although there is
implementation to fail gracefully with a print message to the user and a returned empty list of nodes

New Statistic: 
I added a new Total Nodes Visited statistic so the user could track how many nodes a certain path has visited as it is happening, counting the starting but not the exit node
It appears at the bottom of the scoreboard and is updated and reset throughout the running, allowing people to count along with the path and help count any confusing graphs with tight nodes