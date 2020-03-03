### Question 1
Design and implement `Blockchain` and `Block` classes. A `Blockchain` object
contains `Block` object(s). Each `Block` object has

- set of transactions that form a hash tree
- header that includes
    - hash of the previous header
    - root of the hash tree
    - timestamp (Unix timestamp expressed as an integer)
    - nonce (a random number needed to generate PoW)

Follow the same interface as in the `Transaction` class from the last week
(there is no signing, thus do not implement `sign()`.)
You need to implement `add()` to add a new block to the blockchain.
Hash of every new block's header should be less than `TARGET` (a global parameter,
set now to `\x00\x00\x0f\xff\xff\xff...\xff`).

Test your implementation.
What checks have you implemented in `Blockchain`'s `validate()` ?


### Question 2

Introduce forks and their handling in your implementation.  Modify your
implementation, such that `add()` allows to anchor a new block to a given
arbitrary existing block.  Implement the `resolve()` method, that returns the
longest chain (e.g., it can return the latest block of the longest chain).  Test
your implementation.