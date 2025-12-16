// Simple test: store value 42 at address stored in RAM[10]
// RAM[10] = 20 (address)
// RAM[20] should become 42

// Set RAM[10] = 20
@20
D=A
@10
M=D

// Set value = 42
@42
D=A

// Load address from RAM[10] into A, then store
@10
A=M
M=D

// Halt
@END
0;JMP
(END)
@END
0;JMP
