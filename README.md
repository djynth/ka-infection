An implentation of the Infection project for Khan Academy's application process. The official description of the parameters can be found [here](https://docs.google.com/a/khanacademy.org/document/d/1NiKv-MjULOFyyc8f5w8R_EqvuPJ10wJVJgZhtTK9VKc/edit#heading=h.24vvz52659j3). In brief, the challenge is to implement a graph of students and teachers who can be "infected" classroom-by-classroom by a new version of a piece of software. Classrooms are infected as a whole to make sure classmates are using the same version, and in the Limited Infection case, the goal is to infect only a specified potion of the population.

#### Implementation

I chose to complete this project in Python both because the majority of my portfolio is in a web-focused language (JavaScript, PHP, etc.) and so I wanted to highlight my ability in other environments, and because Python is high level enough to focus on the conceptual parts of the project and easily expand to, for example, a graphical interface.

#### Algorithm

The Limited Infection scenario is an example of the famous Subset Sum problem, where the goal is to choose a subset of a given set of numbers that sum to a certain target. If the goal is to infect `k` students and we have classrooms of sizes `a_1, a_2, a_3, ..., a_n` then we attempt to find a subset of these classrooms with size summing to `k`. The Subset Sum problem is known to be NP-complete, so a perfect polynomial time algorithm is beyond the scope of this project. Thus, we can either compromise on complexity (and implement a brute force, exponential time algorithm) and/or correctness (and implement an algorithm that finds a subset of classrooms with only approximately `k` total students).

#### Usage

Run `total_infection.py` to execute randomized correctness tests for the Total Infection scenario. (Use `-h` to see command-line options.) These tests simply create randomly-sized classrooms and then infect and/or disinfect them, checking along the way that the infection has spread properly.