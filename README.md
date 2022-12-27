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
