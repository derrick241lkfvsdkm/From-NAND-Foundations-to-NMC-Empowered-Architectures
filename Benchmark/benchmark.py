#!/usr/bin/env python3
# benchmark.py
# Benchmark script to compare standard Hack CPU vs NMC-augmented CPU

import subprocess
import sys
import os

def run_benchmark(hack_file, test_name):
    """Run both simulators on a .hack file and compare results"""
    print(f"\n{'='*70}")
    print(f"Benchmarking: {test_name}")
    print(f"{'='*70}\n")
    
    # Run standard CPU
    print("Running Standard Hack CPU:")
    print("-" * 70)
    try:
        result_std = subprocess.run(
            ["python3", "hack_cpu.py", hack_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        print(result_std.stdout)
        if result_std.stderr:
            print("STDERR:", result_std.stderr)
    except subprocess.TimeoutExpired:
        print("ERROR: Standard CPU timed out!")
        return
    except Exception as e:
        print(f"ERROR running standard CPU: {e}")
        return
    
    print("\n")
    
    # Run NMC CPU
    print("Running NMC-Augmented Hack CPU:")
    print("-" * 70)
    try:
        result_nmc = subprocess.run(
            ["python3", "hack_cpu_nmc.py", hack_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        print(result_nmc.stdout)
        if result_nmc.stderr:
            print("STDERR:", result_nmc.stderr)
    except subprocess.TimeoutExpired:
        print("ERROR: NMC CPU timed out!")
        return
    except Exception as e:
        print(f"ERROR running NMC CPU: {e}")
        return
    
    print("\n" + "="*70 + "\n")

def main():
    """Main benchmark runner"""
    if len(sys.argv) > 1:
        # Run specific test
        hack_file = sys.argv[1]
        if not os.path.exists(hack_file):
            print(f"Error: File {hack_file} not found")
            sys.exit(1)
        test_name = os.path.basename(hack_file)
        run_benchmark(hack_file, test_name)
    else:
        # Run all .hack files in current directory
        hack_files = [f for f in os.listdir('.') if f.endswith('.hack')]
        if not hack_files:
            print("No .hack files found in current directory")
            print("Usage: python3 benchmark.py [file.hack]")
            sys.exit(1)
        
        for hack_file in sorted(hack_files):
            run_benchmark(hack_file, hack_file)

if __name__ == "__main__":
    main()
