// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.
@x  //This will be set to 0 so that it could help the program know when to stop adding.
M=0
@R2
M=0
(loop)
@x
D=M
@R0
D=D+M  //This is x(0) + the value given to R0, needed because later we will decrement x until x+R0=0.
@END
D;JEQ
@R1
D=M
@R2
M=M+D
@x
M=M-1
@loop
0;JMP
(END)
0;JMP