// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(WHITE)  //Loop for turning the screen white.
@KBD
D=M
@BLACK
D;JGT
@x
D=M
@SCREEN
D=D+A
A=D-1
M=0
@x
M=M-1
@WHITE
0;JMP
(BLACK)  //Loop for turning the screen black.
@24575
D=M
@WHITE
D;JLT  //If screen gets filled, go to white.
@x
D=M
@SCREEN
D=D+A
A=D
M=-1
@x
M=M+1
@BLACK
0;JMP