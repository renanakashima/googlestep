def sieve(n):
    """
    Return the smallest prime strictly greater than 2*n.
    We know by Bertrand's postulate that for n >= 1 there is
    at least one prime in (2n, 4n], so sieving up to 4*n suffices.
    """
    
    limit = 4 * n

    prime = [True] * (limit + 1)
    prime[0] = False
    prime[1] = False

    p = 2
    while p * p <= limit:
        if prime[p]:
            for i in range(p * p, limit + 1, p):
                prime[i] = False
        p += 1

    for i in range(2 * n, limit + 1):
        if prime[i]:
            return i