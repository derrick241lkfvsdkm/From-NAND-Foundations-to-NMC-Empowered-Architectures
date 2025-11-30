//p1
(CHECK)
@KBD
D=M
@PART3
D;JEQ
@PART2
D;JNE
@CHECK
0;JMP




//p2
(PART2)
@8192
D=A
@n
M=D
@i
M=0

(FILL)
//if i = n goto CHECK
@i
D=M
@n
D=D-M
@CHECK
D;JEQ
//ARM[i+SCREEN]=-1
@i
D=M
@SCREEN
A=D+A
M=-1
@i
M=M+1
@FILL
0;JMP

//p3
(PART3)
@8192
D=A
@n
M=D
@i
M=0

(CLEAR)
//if i = n goto CHECK
@i
D=M
@n
D=D-M
@CHECK
D;JEQ
//ARM[i+SCREEN]=0
@i
D=M
@SCREEN
A=D+A
M=0
M=0
@i
M=M+1
@CLEAR
0;JMP













