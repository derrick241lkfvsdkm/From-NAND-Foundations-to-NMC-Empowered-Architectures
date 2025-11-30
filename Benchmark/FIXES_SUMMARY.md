# Summary of Fixes Applied to Hack CPU Benchmark Code

## Overview
The uploaded code had several critical bugs that prevented the benchmark from completing successfully. All issues have been identified and fixed.

## Critical Bugs Fixed

### 1. **Matrix Multiplication Address Calculation Bug**
**Location**: MatMul.asm and MatMul2x2.asm  
**Problem**: The code for computing `i*4` and `k*4` was incorrect.

**Original Code** (WRONG):
```assembly
@65
D=M      // D=i
@73
M=D      // temp = i
@73
D=M
@73
D=D+M    // D = i + i = 2*i
@73
D=D+M    // D = 2*i + i = 3*i (WRONG!)
```

**Fixed Code** (CORRECT):
```assembly
@65
D=M      // D=i
@73
M=D      // temp = i
D=D+M    // D = i + i = 2*i
@73
M=D      // temp = 2*i
D=D+M    // D = 2*i + 2*i = 4*i (CORRECT!)
```

**Impact**: This bug caused incorrect memory addresses to be calculated, resulting in wrong matrix elements being accessed and stored.

---

### 2. **Indirect Memory Write Bug**
**Location**: MatMul.asm line 164-168, MatMul2x2.asm line 170-174  
**Problem**: The A register was overwritten before the indirect write could complete.

**Original Code** (WRONG):
```assembly
@76
A=M      // A = RAM[76] = addrC (e.g., 48)
@68
D=M      // A is now 68! (overwrites previous A)
M=D      // Writes to RAM[68] instead of RAM[48]
```

**Fixed Code** (CORRECT):
```assembly
@68
D=M      // D = sum (load data first)
@76
A=M      // A = addrC (set address)
M=D      // RAM[addrC] = sum (write to correct location)
```

**Impact**: This bug caused all computed sums to be written to the wrong memory location, resulting in an all-zero output matrix.

---

### 3. **CPU Simulator - Signed Arithmetic**
**Location**: hack_cpu.py and hack_cpu_nmc.py  
**Problem**: The original code used `eval()` which doesn't properly handle 16-bit two's complement arithmetic.

**Fix**: Implemented proper signed/unsigned conversion functions:
```python
def to_signed(val):
    """Convert 16-bit unsigned to signed (two's complement)"""
    if val & 0x8000:
        return val - 0x10000
    return val

def to_unsigned(val):
    """Convert signed to 16-bit unsigned"""
    return val & 0xFFFF
```

**Impact**: Ensures correct behavior for negative numbers and overflow conditions.

---

### 4. **CPU Simulator - Halt Detection**
**Location**: hack_cpu.py and hack_cpu_nmc.py  
**Problem**: Programs with infinite halt loops (`@HALT; 0;JMP`) would run forever.

**Fix**: Added PC history tracking to detect when execution is stuck in a small loop:
```python
pc_history = []
while 0 <= PC < len(instrs) and instr_count < max_cycles:
    if len(pc_history) > 20:
        pc_history.pop(0)
    pc_history.append(PC)
    if len(pc_history) >= 20 and len(set(pc_history[-20:])) <= 2:
        break  # Stuck in a loop of 1-2 instructions
```

**Impact**: Programs now terminate correctly instead of hitting the max cycle limit.

---

### 5. **Assembler - Error Handling**
**Location**: assembler.py  
**Problem**: No validation of comp/dest/jump mnemonics.

**Fix**: Added explicit error checking:
```python
if comp not in self.comp:
    raise ValueError(f"Unknown comp mnemonic: {comp} in line: {line}")
```

**Impact**: Provides clear error messages for invalid assembly code.

---

## Test Results

### Before Fixes:
- **MatMul_Full.hack**: Hit 10M instruction limit, output all zeros
- **MatMul2x2.hack**: Hit 10M instruction limit, output all zeros

### After Fixes:
- **MatMul_Full.hack**: Completes in 5,223 instructions, correct output
- **MatMul2x2.hack**: Completes in 721 instructions, correct output

### Benchmark Results:
```
4×4 Matrix Multiplication:
- Standard CPU: 5,223 instructions
- NMC CPU: 5,223 instructions, 5,164.20 weighted cycles
- Speedup: 1.01x

2×2 Matrix Multiplication:
- Standard CPU: 721 instructions
- NMC CPU: 721 instructions, 708.40 weighted cycles
- Speedup: 1.02x
```

## Files Modified

1. **assembler.py** - Added error handling
2. **hack_cpu.py** - Fixed signed arithmetic, added halt detection
3. **hack_cpu_nmc.py** - Fixed signed arithmetic, added halt detection
4. **MatMul.asm** - Fixed address calculations and indirect writes
5. **MatMul2x2.asm** - Fixed address calculations and indirect writes

## Verification

All test programs now produce correct results:
- **Add.asm**: RAM[2] = RAM[0] + RAM[1] ✓
- **SimpleStore.asm**: Indirect addressing works ✓
- **MatMul2x2.asm**: 2×2 matrix multiplication ✓
- **MatMul_Full.asm**: 4×4 matrix multiplication ✓

Matrix C correctly equals Matrix B (since A is the identity matrix):
```
Matrix C (RAM[48..63]):
  Row 0: [1, 2, 3, 4]
  Row 1: [5, 6, 7, 8]
  Row 2: [9, 10, 11, 12]
  Row 3: [13, 14, 15, 16]
```
