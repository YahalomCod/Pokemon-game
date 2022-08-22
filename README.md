# Pokemon game as TSP problem

* Created by Yahalom Chasid and Guy Azoulay.

## About the assignment:
The given task was to build a runnable Pokemon game with a given sever that contians all the game data:
* Agents as players.
* Pokemons as Pokemons.

Our task was to assign each agent to the given pokemons and to catch 'em all while using our last graph project.
We used the same algorithms and improved the GUI so that the agents movement is shown the in the GUIץ

## The Algorithem:
We assigned pokemons to each agent depending on the distance between them and by using TSP and shortest Path algorithem we implemented on the last task,
this was used with threads- each thread to each agentץ

## How to run:
* open cmd in the main file(Ex4-OPP) and run this command: java -jar Ex4_Server_v0.0.jar 11 (or any case between 0-15)
* open cmd in the src file inside the main file(Ex4-OPP\src) and run this command: python student_code.py
