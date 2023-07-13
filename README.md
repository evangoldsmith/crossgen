# Cross - Gen (WIP)
### A Distinct Crossword Generator Built With Wave Function Collapse
[Wave function collapse](https://en.wikipedia.org/wiki/Wave_function_collapse) is a concept first originated to describe superpositions in quantum mechanics. It describes the process in which a quantum system is "observed" by the external world and collapses into a single measurable state. 
This idea has been used as an algorithm for procedural generation of complex images, audio, text, and other forms of media. In this project, I use a custom version of this algorithm written in python to automatically generate unique crosswords.
### How It Works
A square board of a user inputed size is instatiated with each cell starting with max "entropy" of 26 (for each potential letter in the alphabet).
![image info](.img/crossgen.jpg)
The board then goes through a series of "collapsing" where a random cell with minimum entropy is observed and collapsed to a random letter of it's potential options.

### Special Thanks
- Mark Diehl/Peter Broda 
	- [Word Database](https://www.facebook.com/groups/1515117638602016/permalink/2997721820341583/)
- The Coding Train on Youtube
	- [Introduction to wfc](https://www.youtube.com/watch?v=rI_y2GAlQFM&t=504s)