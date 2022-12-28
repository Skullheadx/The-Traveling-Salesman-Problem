# The-Traveling-Salesman-Problem

My solutions to the Traveling Salesman Problem (TSP) inspired by video presented by Reducible on Youtube. 
(https://youtu.be/GiDsjIBOVoA)

--------------------------------------------------------------------------------------------------------------
**TSP Problem Definition**

_If a salesman starts at a town and wants to travel to every other town only once, what is the shortest path he should take such that he ends up in the town he started in?_

Assuming that:
1. Each town is connected by a direct edge
2. The distance between town A and town B is the same as the distance between town B and town A
3. The direct path to a town is always the shortest, i.e. going directly from town A to town C is faster than going from town A to town B and then town C

--------------------------------------------------------------------------------------------------------------
**Method 1: Brute Force**

By checking every single possibility and calculating the distance of each route, the shortest path can be determined. As **n**, the number of towns, increases, on the first turn, (starting at any town) there are n-1 towns to choose from, then on the second turn there are n-2 choices and so on until there is only one option left which is to return to the starting town. This means that there are `(n - 1)! / 2` total possibilities accounting for duplicates. This strategy while easy to implement, is not suited to calculating more than 20 nodes as the number possibilities that would be considered at _n=20_ is `(20-1)!/2 = 60,822,550,204,416,000`. 

--------------------------------------------------------------------------------------------------------------
**Method 2: Nearest Neighbor (NN) Heuristic**

If we start at any town and find the closest town that we haven't been to yet and continue this until all the cities have been visited, this creates a complete tour.

--------------------------------------------------------------------------------------------------------------
**Lower Bound and the Optimal Solution**

In the case of the TSP, finding the optimal solution for a large number of nodes can end up taking too much time to compute, meaning that we have nothing to compare our heuristic solutions to. 
This is where the **Minimum Spanning Tree (MST)** comes in. 
_The minimum spanning tree is the set of edges that connects all the nodes with the minimum cost (in the case of the TSP, the costs is the distance between nodes) and no cycles._  
**For example:** A graph with 4 nodes: A,B,C,D at (0,0), (0,10), (20,0), (20,10) respectively on the Cartesian Plane will have a MST of 40.0.
This is because the MST only needs to connect all the nodes in the shortest distance possible, which in this case would be the edges AB + BC + CD. There is also another MST that is equally good which is simply AB + AD + CD.

![img_1.png](img_1.png)

The usefulness of the MST lies in the fact that the optimal tour which in the case of the example above is highlighted in green, is always greater than the MST. 
`MST Cost < Optimal Tour Cost` Since we are not trying to find the optimal solution, but a solution that is good enough and that we can calculate within a reasonable amount of time (heuristic solution) we can compare our solution to the minimum spanning tree and get an approximation ratio.

Take this graph for instance. The grey circles represent nodes or towns in the TSP, the blue line represents the Nearest Neighbor heuristic solution and the red line represents the MST. 
![](NN_Heuristic+MST.png)

By calculating each of the distances in the MST, we can determine that the `MST Cost = 1360.299` and the `Tour Cost = 1,994.528`. We can now determine the approximation ratio by simply dividing the tour cost by the MST cost.

`Tour Cost / MST Cost = 1,994.528 / 1360.299 = 1.466`

`1.466 * 100% - 100% = 46.6% `

By manipulating the result, we can determine how much our solution overshot the lower bound.
Of course this value does not represent to a high degree of accuracy how much we overshot the optimal solution, but it does give us ballpark numbers.
In this case, the approximation ratio is `46.6%` of the MST.
(As an exercise to the reader, can you determine why this is the MST?)
