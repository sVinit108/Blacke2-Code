from typing import List
from functools import reduce
from operator import xor

# Constants for Blake2b
BLAKE2B_BLOCK_SIZE = 128
BLAKE2B_ROUNDS = 12
BLAKE2B_IV = [
    0x6a09e667f3bcc908, 0xbb67ae8584caa73b,
    0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
    0x510e527fade682d1, 0x9b05688c2b3e6c1f,
    0x1f83d9abfb41bd6b, 0x5be0cd19137e2179,
]

h = [
    0x6a09e667f3bcc908, 0xbb67ae8584caa73b,
    0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
    0x510e527fade682d1, 0x9b05688c2b3e6c1f,
    0x1f83d9abfb41bd6b, 0x5be0cd19137e2179,
]

m = [
    0x6162636465666768, 0x6263646566676869,
    0x636465666768696a, 0x6465666768696a6b,
    0x65666768696a6b6c, 0x666768696a6b6c6d,
    0x6768696a6b6c6d6e, 0x68696a6b6c6d6e6f,
    0x696a6b6c6d6e6f70, 0x6a6b6c6d6e6f7071,
    0x6b6c6d6e6f707172, 0x6c6d6e6f70717273,
    0x6d6e6f7071727374, 0x6e6f707172737475,
    0x7071727374757677, 0x7172737475767778,
]

t = 16 * BLAKE2B_BLOCK_SIZE

f = 0xFFFFFFFFFFFFFFFF


# Rotate left and right operations
def rol(x: int, n: int) -> int:
    return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF

def ror(x: int, n: int) -> int:
    return ((x >> n) | (x << (64 - n))) & 0xFFFFFFFFFFFFFFFF

# Blake2b compression function
def blake2b_compress(h: List[int], m: List[int], t: int, f: int) -> List[int]:
    v = h + BLAKE2B_IV
    v[12] ^= t & 0xFFFFFFFFFFFFFFFF
    v[13] ^= t >> 64
    v[14] ^= f
    v[15] ^= 0xFFFFFFFFFFFFFFFF

    for r in range(BLAKE2B_ROUNDS):
        # Column step
        v[0] = (v[0] + v[4]) % 0xFFFFFFFFFFFFFFFF ^ (v[4] >> 64) % 0xFFFFFFFFFFFFFFFF
        v[4] = rol(v[4] ^ v[12], 32)
        v[8] = (v[8] + v[0]) % 0xFFFFFFFFFFFFFFFF ^ (v[0] >> 64) % 0xFFFFFFFFFFFFFFFF
        v[12] = rol(v[12] ^ v[8], 24)
        v[1] = (v[1] + v[5]) % 0xFFFFFFFFFFFFFFFF ^ (v[5] >> 64) % 0xFFFFFFFFFFFFFFFF
        v[5] = rol(v[5] ^ v[13], 16)
        v[9] = (v[9] + v[1]) % 0xFFFFFFFFFFFFFFFF ^ (v[1] >> 64) % 0xFFFFFFFFFFFFFFFF
        v[13] = rol(v[13] ^ v[9], 63)
        v[2] = (v[2] + v[6]) % 0xFFFFFFFFFFFFFFFF ^ (v[6] >> 64) % 0xFFFFFFFFFFFFFFFF
        v[6] = rol(v[6] ^ v[14], 32)
        v[10] = (v[10] + v[2]) % 0xFFFFFFFFFFFFFFFF ^ (v[2] >> 64) % 0xFFFFFFFFFFFFFFFF
        v[14] = rol(v[14] ^ v[10], 24)
        v[3] = (v[3] + v[7]) % 0xFFFFFFFFFFFFFFFF ^ (v[7] >> 64) % 0xFFFFFFFFFFFFFFFF
        v[7] = rol(v[7] ^ v[15], 16)
        
        # Diagonal step
        v[0] = (v[0] + v[5]) % 0xFFFFFFFFFFFFFFFF ^ (v[5] >> 64) % 0xFFFFFFFFFFFFFFFF
        v[5] = rol(v[5] ^ v[10], 32)
        v[10] = (v[10] + v[15]) % 0xFFFFFFFFFFFFFFFF ^ (v[15] >> 64) % 0xFFFFFFFFFFFFFFFF
        v[15] = rol(v[15] ^ v[4], 24)
        v[1] = (v[1] + v[6]) % 0xFFFFFFFFFFFFFFFF ^ (v[6] >> 64) % 0xFFFFFFFFFFFFFFFF
        v[6] = rol(v[6] ^ v[11], 16)
        v[11] = (v[11] + v[12]) % 0xFFFFFFFFFFFFFFFF ^ (v[12] >> 64) % 0xFFFFFFFFFFFFFFFF
        v[12] = rol(v[12] ^ v[7],16)
        
        return [v[i] ^ v[i + 8] for i in range(8)] + h

print(blake2b_compress(h,m,t,f))