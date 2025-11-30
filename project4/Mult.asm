//Define Variables
@i
M=0
@2
M=0
@1
D=M
@n
M=D

(LOOP)
@i
D=M
@n
D=D-M
D=D+1
@END
D;JGT
@2
D=M
@0
D=D+M
@2
M=D
@i
D=M
D=D+1
@i
M=D
@LOOP
0;JMP

(END)
@END
0;JMP