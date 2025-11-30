#!/usr/bin/env python3
# init_matmul.py
# Initialize matrix data in RAM for testing MatMul

def create_matmul_init():
    """Create an assembly program that initializes matrices A and B"""
    asm_code = []
    
    # Matrix A: 4x4 identity-like matrix for easy verification
    # A = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]
    A = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    
    # Matrix B: simple values
    # B = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]]
    B = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]
    
    asm_code.append("// Initialize Matrix A at RAM[16..31]")
    for i in range(4):
        for j in range(4):
            addr = 16 + i * 4 + j
            val = A[i][j]
            asm_code.append(f"@{val}")
            asm_code.append("D=A")
            asm_code.append(f"@{addr}")
            asm_code.append("M=D")
    
    asm_code.append("\n// Initialize Matrix B at RAM[32..47]")
    for i in range(4):
        for j in range(4):
            addr = 32 + i * 4 + j
            val = B[i][j]
            asm_code.append(f"@{val}")
            asm_code.append("D=A")
            asm_code.append(f"@{addr}")
            asm_code.append("M=D")
    
    asm_code.append("\n// End initialization")
    asm_code.append("@END_INIT")
    asm_code.append("0;JMP")
    asm_code.append("(END_INIT)")
    
    return "\n".join(asm_code)

def create_matmul_with_init():
    """Create complete MatMul program with initialization"""
    init_code = create_matmul_init()
    
    with open("MatMul.asm", "r") as f:
        matmul_code = f.read()
    
    # Combine initialization with matrix multiplication
    full_program = init_code + "\n\n" + matmul_code
    
    with open("MatMul_Full.asm", "w") as f:
        f.write(full_program)
    
    print("Created MatMul_Full.asm with matrix initialization")
    print("\nExpected result (A * B where A is identity):")
    print("Matrix C should equal Matrix B:")
    B = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]
    for i, row in enumerate(B):
        print(f"  Row {i}: {row}")

if __name__ == "__main__":
    create_matmul_with_init()
