// 2×2 MATRIX MULTIPLICATION (much faster for testing)
// A: RAM[16..19] (2 rows × 2 cols)
// B: RAM[20..23]
// C: RAM[24..27]

// Initialize Matrix A = [[1,0],[0,1]] (identity)
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
@1
D=A
@19
M=D

// Initialize Matrix B = [[2,3],[4,5]]
@2
D=A
@20
M=D
@3
D=A
@21
M=D
@4
D=A
@22
M=D
@5
D=A
@23
M=D

// i = 0
@30
M=0

(LOOP_i)
@30
D=M
@2
D=D-A
@END_ALL
D;JGE  // if i>=2, end

// j=0
@31
M=0

(LOOP_j)
@31
D=M
@2
D=D-A
@END_j
D;JGE  // if j>=2 end j-loop

// sum=0
@33
M=0

// k=0
@32
M=0

(LOOP_k)
@32
D=M
@2
D=D-A
@END_k
D;JGE  // if k>=2 break

// compute addrA = 16 + (i*2) + k
@30
D=M      // D=i
D=D+M    // D=2*i
@16
D=D+A    // baseA + 2*i
@32
D=D+M    // + k
@35
M=D      // addrA

@35
A=M
D=M
@36
M=D      // A_val

// compute addrB = 20 + (k*2) + j
@32
D=M      // D=k
D=D+M    // D=2*k
@20
D=D+A    // baseB + 2*k
@31
D=D+M    // + j
@37
M=D      // addrB

@37
A=M
D=M
@38
M=D      // B_val

// product = A_val * B_val (repeated add)
@39
M=0      // product=0
@36
D=M
@40
M=D      // count=A_val

(LOOP_mult)
@40
D=M
@AFTER_mult
D;JEQ

@39
D=M
@38
D=D+M
@39
M=D      // product += B_val

@40
M=M-1

@LOOP_mult
0;JMP

(AFTER_mult)
// sum += product
@33
D=M
@39
D=D+M
@33
M=D

// k++
@32
M=M+1
@LOOP_k
0;JMP

(END_k)
// compute addrC = 24 + (i*2) + j
@30
D=M      // D=i
D=D+M    // D=2*i
@24
D=D+A
@31
D=D+M
@41
M=D      // addrC

@33
D=M      // D = sum
@41
A=M      // A = addrC
M=D      // RAM[addrC] = sum

// j++
@31
M=M+1
@LOOP_j
0;JMP

(END_j)
// i++
@30
M=M+1
@LOOP_i
0;JMP

(END_ALL)
@HALT
0;JMP

(HALT)
@HALT
0;JMP
