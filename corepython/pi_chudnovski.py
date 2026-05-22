import sys
import time
import argparse
import concurrent.futures
from tqdm import tqdm

# USE: C:\Users\loren\AppData\Local\Programs\Python\Python313\python.exe pi_chudnovski.py -d 100000000 -o pi_1b.txt -v pi-billion.txt


# required for Python 3.11 mybe?????
try:
    sys.set_int_max_str_digits(0)
except AttributeError:
    pass

# WOW!
try:
    import gmpy2
    from gmpy2 import mpz, isqrt
    HAS_GMP = True
except ImportError:
    import math
    print("=========================================================================")
    print("WARNING: 'gmpy2' not found. Falling back to Python's built-in integers.")
    print("For a billion digits, gmpy2 is STRONGLY recommended to finish in hours")
    print("rather than years. Please 'pip install gmpy2'.")
    print("=========================================================================\n")
    mpz = int
    isqrt = math.isqrt
    HAS_GMP = False

C1 = mpz(10939058860032000)
C2 = mpz(13591409)
C3 = mpz(545140134)

# High-performance integer constants for the base-case math (python native ints)
C1_int = 10939058860032000
C2_int = 13591409
C3_int = 545140134

class ProgressTracker:
    """A minimal wrapper to throttle tqdm updates and prevent recursion overhead."""
    def __init__(self, pbar, update_freq=10000):
        self.pbar = pbar
        self.count = 0
        self.update_freq = update_freq
        
    def advance(self, n=1):
        self.count += n
        if self.count >= self.update_freq:
            self.pbar.update(self.count)
            self.count = 0
            
    def flush(self):
        if self.count > 0:
            self.pbar.update(self.count)
            self.count = 0

def bs(a, b, tracker):
    """
    Recursive Binary Splitting of the Chudnovsky series.
    Computes terms from index 'a' to 'b-1'.
    """
    diff = b - a
    if diff == 1:
        a2 = a * a
        a3 = a2 * a
        P = 5 - 46*a + 108*a2 - 72*a3
        Q = C1_int * a3
        T = P * (C2_int + C3_int * a)
        tracker.advance(1)
        return mpz(P), mpz(Q), mpz(T)
    elif diff == 2:
        # Node 1
        a2 = a * a
        a3 = a2 * a
        P1 = 5 - 46*a + 108*a2 - 72*a3
        Q1 = C1_int * a3
        T1 = P1 * (C2_int + C3_int * a)
        
        # Node 2
        b1 = a + 1
        b2 = b1 * b1
        b3 = b2 * b1
        P2 = 5 - 46*b1 + 108*b2 - 72*b3
        Q2 = C1_int * b3
        T2 = P2 * (C2_int + C3_int * b1)
        
        # Combine using fast native Python ints, then cast to mpz
        P = P1 * P2
        Q = Q1 * Q2
        T = T1 * Q2 + P1 * T2
        
        tracker.advance(2)
        return mpz(P), mpz(Q), mpz(T)
        
    m = (a + b) // 2
    P1, Q1, T1 = bs(a, m, tracker)
    P2, Q2, T2 = bs(m, b, tracker)
    
    P = P1 * P2
    Q = Q1 * Q2
    T = T1 * Q2 + P1 * T2
    return P, Q, T

def calc_pi(digits):
    """Calculates Pi to the specified number of digits using Binary Splitting."""
    stats = {}
    
    D_calc = digits + 10
    
    N = int(D_calc / 14.181647462725477) + 1
    print(f"Target: {digits} digits | Guard digits: 10 | Series terms needed: {N}")
    
    print("Launching massive square root calculation in background thread...")
    # Hide latency by running square root concurrently with binary splitting
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future_sqrt = pool.submit(lambda: isqrt(mpz(10005) * (mpz(10)**(2 * D_calc))))
        
        start_time = time.time()
        with tqdm(total=N, desc="Binary Splitting", unit=" terms") as pbar:
            tracker = ProgressTracker(pbar)
            if N == 0:
                Q, T = mpz(1), mpz(0)
            else:
                _, Q, T = bs(1, N + 1, tracker)
                tracker.flush()
        stats['bs_time'] = time.time() - start_time
        
        print("Retrieving enormous square root (waiting if not finished)...")
        wait_start = time.time()
        sqrt_val = future_sqrt.result()
        C = mpz(426880) * sqrt_val
        stats['sqrt_time'] = time.time() - wait_start
    
    print("Performing final division... Can be slow")
    start_time = time.time()
    numerator = C * Q
    denominator = C2 * Q + T
    pi_int = numerator // denominator
    stats['div_time'] = time.time() - start_time
    
    print("Converting large integer to string representation....")
    start_time = time.time()
    pi_str_full = str(pi_int)
    pi_str = pi_str_full[0] + "." + pi_str_full[1:digits+1]
    stats['str_time'] = time.time() - start_time
    
    return pi_str, stats

def verify_pi(calculated_pi_str, filepath):
    """Compares the calculated Pi string with a reference text file."""
    print(f"Verifying against reference file: '{filepath}'...")
    start_time = time.time()
    
    calc_clean = calculated_pi_str.replace(".", "").strip()
    
    try:
        with open(filepath, 'r') as f:
            ref_str = f.read().replace(".", "").replace("\n", "").replace(" ", "").strip()
            
        compare_len = min(len(calc_clean), len(ref_str))
        
        if len(ref_str) < len(calc_clean):
            print(f"Warning: Reference file has fewer digits ({len(ref_str)}) than requested ({len(calc_clean)}).")

        if calc_clean[:compare_len] == ref_str[:compare_len]:
            print(f"\n[✓] SUCCESS: All {compare_len} digits match perfectly!")
        else:
            print(f"\n[X] FAILURE: Mismatch detected.")
            for i in range(compare_len):
                if calc_clean[i] != ref_str[i]:
                    print(f"First mismatch at index {i} (Digit {i+1} after the '3'):")
                    start_idx = max(0, i - 5)
                    end_idx = min(compare_len, i + 5)
                    print(f"Calculated : ...{calc_clean[start_idx:end_idx]}...")
                    print(f"Reference  : ...{ref_str[start_idx:end_idx]}...")
                    break
    except FileNotFoundError:
        print(f"\n[!] Error: Verification file '{filepath}' not found.")
        
    return time.time() - start_time

def main():
    parser = argparse.ArgumentParser(description="Lightning Fast Pi Calculator (Chudnovsky / Binary Splitting)")
    parser.add_argument("-d", "--digits", type=int, default=1000000, 
                        help="Number of digits of Pi to calculate (e.g., 1000000000 for a billion).")
    parser.add_argument("-v", "--verify", type=str, default="", 
                        help="Optional: Path to a reference .txt file containing Pi for validation.")
    parser.add_argument("-o", "--output", type=str, default="pi_output.txt", 
                        help="Path to save the calculated digits of Pi.")
    args = parser.parse_args()

    total_start = time.time()
    
    pi_str, stats = calc_pi(args.digits)
    
    write_start = time.time()
    print(f"Saving output to '{args.output}'...")
    with open(args.output, "w") as f:
        f.write(pi_str)
    stats['write_time'] = time.time() - write_start
    
    stats['ver_time'] = 0.0
    if args.verify:
        stats['ver_time'] = verify_pi(pi_str, args.verify)
        
    total_time = time.time() - total_start

    print("\n" + "="*40)
    print(f"{'--- COMPUTATION STATISTICS ---':^40}")
    print("="*40)
    print(f"Binary Splitting       : {stats['bs_time']:>9.3f} seconds")
    print(f"Root Calculation       : {stats['sqrt_time']:>9.3f} seconds")
    print(f"Final Division         : {stats['div_time']:>9.3f} seconds")
    print(f"String Conversion      : {stats['str_time']:>9.3f} seconds")
    print(f"File Save IO           : {stats['write_time']:>9.3f} seconds")
    if args.verify:
        print(f"File Verification      : {stats['ver_time']:>9.3f} seconds")
    print("-" * 40)
    print(f"TOTAL WALL TIME        : {total_time:>9.3f} seconds")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()