// 4×4 MATRIX MULTIPLICATION - Optimized Version
// A: RAM[16..31] (4 rows × 4 cols)
// B: RAM[32..47]
// C: RAM[48..63]
// Registers:
// R15 (65): i
// R14 (66): j
// R13 (67): k
// R12 (68): sum
// R11 (69): product
// R10 (70): A_val
// R9 (71): B_val
// R8 (72): count (for multiplication)
// R7 (73): temp
// R6 (74): addrA
// R5 (75): addrB
// R4 (76): addrC

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

// --- Optimized Address Calculation for A[i][k] ---
// addrA = 16 + (i*4) + k
// D = i
@65
D=M
// D = 4*i
@4
@R7
M=0
(MUL_4i)
@4
D=D-A
@END_MUL_4i
D;JLT
@65
D=M
@R7
M=M+D
@MUL_4i
0;JMP
(END_MUL_4i)
@R7
D=M
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

// --- Optimized Address Calculation for B[k][j] ---
// addrB = 32 + (k*4) + j
// D = k
@67
D=M
// D = 4*k
@4
@R7
M=0
(MUL_4k)
@4
D=D-A
@END_MUL_4k
D;JLT
@67
D=M
@R7
M=M+D
@MUL_4k
0;JMP
(END_MUL_4k)
@R7
D=M
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
M=M-1
@LOOP_mult
0;JMP

(AFTER_mult)
// sum += product
@68
M=M+D    // Use M=M+D (D=product) to save a D=M instruction
// The original code was:
// @68
// D=M
// @69
// D=D+M
// @68
// M=D
// The new code is:
// @69
// D=M
// @68
// M=M+D  // M=sum, D=product

// k++
@67
M=M+1
@LOOP_k
0;JMP

(END_k)
// --- Optimized Address Calculation for C[i][j] ---
// addrC = 48 + (i*4) + j
// D = i
@65
D=M
// D = 4*i
@4
@R7
M=0
(MUL_4i_C)
@4
D=D-A
@END_MUL_4i_C
D;JLT
@65
D=M
@R7
M=M+D
@MUL_4i_C
0;JMP
(END_MUL_4i_C)
@R7
D=M
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
