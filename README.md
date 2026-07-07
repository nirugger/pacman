*This project has been created as part of the 42 curriculum by fbertozz and nirugger*

# Description
The main goal of the project is to recreate our own version of the famous arcade game called "Pacman". The game is a
maze chase video game developed and released by Namco in 1980. The player controls Pac-Man, who must eat all the dots
inside an enclosed maze while avoiding four colored ghosts. Eating large dots allows Pac-Man to eat the ghosts, which
will return to their corners and will start chasing you again. The game is structured in ten levels, and it will end
either when the players lose all their lives or when they complete all the levels. A simple high score system is
implemented: at the end of the game, if the player's score is within the top 10, the player will be prompted to enter 
their name and the score will be saved and displayed in the high score list.
The game is implemented using Python language and the pygame library. It is designed to be played on a computer with a 
keyboard, where arrows keys are used to control Pac-Man's movement.

# Instructions
To run the game, you need to have Python and UV installed on your computer. When you have them installed, you can run
the game by executing the following command in your terminal:

```bash
make
```
This command will install all the needed dependencies and run the game.
Once the game is launched, you will be shown the main menu, which can be navigated using the arrow keys and the Enter
key, or using the mouse. The main menu has the following options:
- Continue: This option will allow you to continue a game you previously started and paused. If there is no such game,
this option will simply start a new game.
- New Game: This option will start a new game, resetting the score and lives.
- High Scores: This option will display the high score list, showing the top 10 scores.
- Instructions: This option will display the instructions on how to play the game.
- Reset: This option will reset the high score list, clearing all saved scores.
- Quit: This option will exit the game.

# Resources
The following resources were used to create this project:
- [Pygame](https://www.pygame.org/news): The library used to create the game and handle graphics and input.
- Maze-Generator: A tool provided by 42 to generate the maze for the game.
- Google: Used to find information and resources related to Pacman features and mechanics, and related to Pygame.
- Google Fonts: Used to find and download fonts for the game.

## Artificial Intelligence Usage:
The following operations during the game were assisted by AI:
- Color palettes generation.
- Game architecture and design: before starting to code, we asked Claude AI to summarize the good practices normally
used by expert game designers to have control of such a big project. Based on this, we got an idea in advance of the 
classes we needed to have control of the schema.

# Configuration
The subject of the project requested us to use a configuration file to store the game setting. More specifically, the
configuration file must be a JSON file, and it can contain comments.
There were no particular constraints on the content of the configuration file, and we realized that putting settings
related to the score would have been a terrible idea, as it would have allowed players to cheat by changing the
configuration file. Therefore, we decided to include only the following keys:
- "highscore_file: The name of the file where the high scores will be saved."
- "resolution": The resolution of the game window, in the format "width x height".
- "seed": The seed used to generate the maze for the first level. This allows to get a deterministic maze as the setup
of the first level. The seed must be an integer number.

# Highscore
The high score list is stored in a JSON file, which is specified in the configuration file. The high score list is a
list of dictionaries, where each dictionary contains the following keys:
- "name": The name of the player.
- "score": The score of the player.
- "date": The date such score was set.

When a game is terminated, the application will check whether the registered score is within the top 10 and, in case,
it will prompt the player to save their score. While saving the score, the system knows already your positioning in the
top 10, so that your name will be shown in real time upon completion in the high scores windows.

# Maze Generation
42 school provided us a package we needed to use to generate the maze and the whole game has to adapt to the maze
generation. The package generates a list of lists of integer number: each number, from 0 to 15, represents a
configuration for a cell in the maze. Every cell is intended as a quadruple if bits, where 0 stands for open wall and 1 
for closed wall.
At the beginning of each level we generated a new maze: maze for level one is deterministic, as the seed is determined
in advance, while any other level is randomly generated.
After we got such list of lists of integer, we transformed each valued into a Cell object, which has as attributes its 
value and many other useful information. For instance, each cell contains a pygame rect which will be used for
rendering, the presence of pac_gums and so on and so forth.
Afterward, we created a dictionary, whose keys and values are the tuple, representing the discrete position of the cell
in the maze, and the Cell object, respectively. We used this dictionary to save many game relevant information, such 
as the player of each entity at any turn of the level.
Moreover, to make the game more enjoyable, we decided to slightly modify the maze generated by the package: 
unfortunately the maze came with many dead ends, therefore we looped through all the cells of the maze, and, where
applicable, we destroyed the wall forming a dead end.
Finally, the package also provided a method to find the shortest path from one cell to another, which we used to
implement ghosts' strategies.

# Implementation
The game is implemented using Python and pygame.
There is a unique main loop which starts the app and within the same loop all the different functions and method are
called.
At the beginning, the main menu is shown. Navigating through it, the user can start all the different functionalities
of the game as described above.

## Control system
The menu can be navigated by mouse and keyboard, while the game can be played just by keyboard.
Arrow keys are used to move the character as follows:
Pressing a direction key, the player will select their next direction and when that direction is finally available, 
Pac-Man will turn that way. This is managed through a dictionary, which is an attribute of the players that contains
the current x and y directions and the future ones. At each frame of the game, the program checks whether the next
directions are available and, in case they are, it substitutes the current ones with the new ones, resetting the new
ones to zero, while waiting for the next input to update them.

## Collectible system
Collectibles are just boolean attributes of the cell. They're generated randomly at the start of each level and there
is a counter to determine whether the player got all of them. When this is the case, the level is considered won and
the game progresses to the new one. In case all the levels are completed, the game ends in a congratulatory window and 
asks to save the player's score.
There are three kinds of collectibles:
- "pac_gums": small dots inside a cell, they do nothing but collecting them increases your score.
- "super pac_gums": large dots placed in the four corners of the maze. When collected they increase your score and send
ghosts to 'frightened mode' for 15 seconds.
- "fruit": a collectible which appears twice per level and increases your score if you collect it. 