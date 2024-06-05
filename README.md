# Vacuum Robot

'Bot545046.py' contains my code for a vacuum robot, which is tasked with cleaning a known amount of stains, in a variety of unknown maps with various obstacles.

I submitted this code in May 2023, for a programming assignment from my Premaster Data Science and Society at Tilburg University, where I received a grade 10, and an award for the best robot of the class. The other files in this repository are from this assignment, and are not my creation.

The robot uses the [A* pathfinding algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm) to find the fastest route towards an observed stain, or towards unexplored territory. This algorithm inherently finds an efficient path around obstacles.

Below is a visual demo of the robot. 

![til](https://github.com/rldekkers/msc-datascience-robot-assignment/blob/fb2aba4d5c5174bfabc612d9f854b31069c7bbb8/animation.gif)
