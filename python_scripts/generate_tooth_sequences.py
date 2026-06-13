from fractions import Fraction

def compute_teeth_sequences(max_r, max_N):
    """
    Compute T(r, N) = [q^N] h_r(q) for 1 <= r <= max_r, r <= N <= max_N.
    
    Uses the recurrence:
    (1 - q^r) h_r(q) = 2q h_{r-1}(q) - q^2 h_{r-2}(q)
    
    Represents each h_r(q) as a list of coefficients, where h[i] = [q^i] h_r(q).
    """
    # h_0(q) = 1
    # h_1(q) = q/(1-q) = q + q^2 + q^3 + ...
    
    h = {}
    
    # h_0: constant 1
    h[0] = [Fraction(1)] + [Fraction(0)] * max_N
    
    # h_1: q/(1-q), coefficients are 0,1,1,1,...
    h[1] = [Fraction(0)] + [Fraction(1)] * max_N
    
    for r in range(2, max_r + 1):
        coeffs = [Fraction(0)] * (max_N + 1)
        
        # (1 - q^r) h_r(q) = 2q h_{r-1}(q) - q^2 h_{r-2}(q)
        # so h_r(q) = [2q h_{r-1}(q) - q^2 h_{r-2}(q)] / (1 - q^r)
        
        # Compute rhs = 2q h_{r-1} - q^2 h_{r-2}, coefficient by coefficient
        # Then solve for h_r using (1 - q^r) h_r = rhs
        # i.e. h_r[n] = rhs[n] + q^r h_r[n], so h_r[n] = rhs[n] + h_r[n-r]
        
        for n in range(max_N + 1):
            # rhs[n] = 2 * h_{r-1}[n-1] - h_{r-2}[n-2]
            rhs_n = Fraction(0)
            if n >= 1:
                rhs_n += 2 * h[r-1][n-1]
            if n >= 2:
                rhs_n -= h[r-2][n-2]
            
            # h_r[n] = rhs[n] + h_r[n-r]
            if n >= r:
                coeffs[n] = rhs_n + coeffs[n-r]
            else:
                coeffs[n] = rhs_n
        
        h[r] = coeffs
    
    return h

def print_sequences(h, max_r, max_N):
    print("Triangle T(r, N) = [q^N] h_r(q):")
    print()
    
    # Header
    header = "r\\N  " + "  ".join(f"{N:4d}" for N in range(1, max_N + 1))
    print(header)
    print("-" * len(header))
    
    for r in range(1, max_r + 1):
        row = f"{r:3d}  " + "  ".join(f"{int(h[r][N]):4d}" for N in range(1, max_N + 1))
        print(row)
    
    print()
    print("Individual sequences (starting from N=r):")
    print()
    for r in range(1, max_r + 1):
        seq = [int(h[r][N]) for N in range(r, max_N + 1)]
        print(f"r={r}: {seq}")

if __name__ == "__main__":
    max_r = 7
    max_N = 30  # extend well beyond the paper's table
    
    h = compute_teeth_sequences(max_r, max_N)
    print_sequences(h, max_r, max_N)
    
    # Verify against paper's Table 2
    print()
    print("Verification against Table 2 (N=1 to 15):")
    table2 = {
        1: [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        2: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
        3: [0,0,1,3,5,8,12,16,21,27,33,40,48,56,65],
        4: [0,0,0,1,4,7,12,20,30,42,58,77,100,127,158],
        5: [0,0,0,0,1,5,9,16,28,45,68,98,137,188,251],
        6: [0,0,0,0,0,1,6,11,20,36,60,95,144,208,296],
        7: [0,0,0,0,0,0,1,7,13,24,44,75,122,191,286],
    }
    
    all_ok = True
    for r in range(1, 8):
        for idx, N in enumerate(range(1, 16)):
            computed = int(h[r][N])
            expected = table2[r][idx]
            if computed != expected:
                print(f"MISMATCH at r={r}, N={N}: computed {computed}, expected {expected}")
                all_ok = False
    if all_ok:
        print("All values match Table 2.")