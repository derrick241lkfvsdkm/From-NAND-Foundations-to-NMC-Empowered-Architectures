// Initialize Matrix A at RAM[16..31]
@1
D=A
@16
M=D
@0
D=A
@17
M=D
@0
D=A
@18
M=D
@0
D=A
@19
M=D
@0
D=A
@20
M=D
@1
D=A
@21
M=D
@0
D=A
@22
M=D
@0
D=A
@23
M=D
@0
D=A
@24
M=D
@0
D=A
@25
M=D
@1
D=A
@26
M=D
@0
D=A
@27
M=D
@0
D=A
@28
M=D
@0
D=A
@29
M=D
@0
D=A
@30
M=D
@1
D=A
@31
M=D

// Initialize Matrix B at RAM[32..47]
@1
D=A
@32
M=D
@2
D=A
@33
M=D
@3
D=A
@34
M=D
@4
D=A
@35
M=D
@5
D=A
@36
M=D
@6
D=A
@37
M=D
@7
D=A
@38
M=D
@8
D=A
@39
M=D
@9
D=A
@40
M=D
@10
D=A
@41
M=D
@11
D=A
@42
M=D
@12
D=A
@43
M=D
@13
D=A
@44
M=D
@14
D=A
@45
M=D
@15
D=A
@46
M=D
@16
D=A
@47
M=D

// End initialization
@END_INIT
0;JMP
(END_INIT)

// 4×4 MATRIX MULTIPLICATION
// A: RAM[16..31] (4 rows × 4 cols)
// B: RAM[32..47]
// C: RAM[48..63]

// i = 0
@65
M=0

(LOOP_i)
@65
D=M
@4
D=D-A
@END_ALL
D;JGE  // if i>=4, end

// j=0
@66
M=0

(LOOP_j)
@66
D=M
@4
D=D-A
@END_j
D;JGE  // if j>=4 end j-loop

// sum=0
@68
M=0

// k=0
@67
M=0

(LOOP_k)
@67
D=M
@4
D=D-A
@END_k
D;JGE  // if k>=4 break

// compute addrA = 16 + (i*4) + k
@65
D=M      // D=i
@73
M=D      // temp = i
// D=2*i
D=D+M    // D = i + i = 2*i
@73
M=D      // temp = 2*i
// D=4*i
D=D+M    // D = 2*i + 2*i = 4*i
@16
D=D+A    // baseA + 4*i
@67
D=D+M    // + k
@74
M=D      // addrA

@74
A=M
D=M
@70
M=D      // A_val

// compute addrB = 32 + (k*4) + j
@67
D=M      // D=k
@73
M=D      // temp = k
// D=2*k
D=D+M    // D = k + k = 2*k
@73
M=D      // temp = 2*k
// D=4*k
D=D+M    // D = 2*k + 2*k = 4*k
@32
D=D+A    // baseB + 4*k
@66
D=D+M    // + j
@75
M=D      // addrB

@75
A=M
D=M
@71
M=D      // B_val

// product = A_val * B_val (repeated add)
@69
M=0      // product=0
@70
D=M
@72
M=D      // count=A_val

(LOOP_mult)
@72
D=M
@AFTER_mult
D;JEQ

@69
D=M
@71
D=D+M
@69
M=D      // product += B_val

@72
D=M
D=D-1
@72
M=D

@LOOP_mult
0;JMP

(AFTER_mult)
// sum += product
@68
D=M
@69
D=D+M
@68
M=D

// k++
@67
M=M+1
@LOOP_k
0;JMP

(END_k)
// compute addrC = 48 + (i*4) + j
@65
D=M      // D=i
@73
M=D      // temp = i
// D=2*i
D=D+M    // D = i + i = 2*i
@73
M=D      // temp = 2*i
// D=4*i
D=D+M    // D = 2*i + 2*i = 4*i
@48
D=D+A
@66
D=D+M
@76
M=D      // addrC

@68
D=M      // D = sum
@76
A=M      // A = addrC
M=D      // RAM[addrC] = sum

// j++
@66
M=M+1
@LOOP_j
0;JMP

(END_j)
// i++
@65
M=M+1
@LOOP_i
0;JMP

(END_ALL)
@HALT
0;JMP

(HALT)
@HALT
0;JMP
