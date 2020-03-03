### Question 1

Get the hash value of `"Blockchain Technology"` using SHA2-256, SHA2-512,
SHA3-256, and SHA3-512.

**Note:** throughout the rest of this course use SHA2-256 as the default hash
function.


### Question 2

Let us define a hash function `H(n, msg)` that computes SHA2-512 over `msg` and
outputs the first `n` bytes of the hash.

- Find a collision of `H(1, msg)`, `H(2, msg)`, `H(3, msg)`, `H(4, msg)`, and
  `H(5, msg)`.  Measure how long it takes to find a collision.
- For `H(1, msg)`, `H(2, msg)`, `H(3, msg)`, `H(4, msg)` and `H(5, msg)`
  find a preimage of the corresponding hashes: `b"\x00"`, `b"\x00"*2`, `b"\x00"*3`,
  `b"\x00"*4`, and `b"\x00"*5`.  Measure how long it takes to find a preimage.
- Compare times of finding a collision and a preimage.


### Question 3

Generate key pairs for ECDSA and sign the string `"Blockchain Technology"`
using this signature scheme with the generated key. Then verify the obtained
signature.

**Note:** the `ecdsa` package uses NIST192p as the default elliptic curve, but in
real applications a longer/more secure curve should be considered.


### Question 4
Design and implement a `Transaction` class that includes the following fields

- sender (a public key of sender)
- receiver (a public key of receiver)
- amount (transaction amount, an integer >0)
- comment (arbitrary text, can be empty)
- signature (sender's signature protecting the transaction)

The class should provide the following interface

<pre>
class Transaction(...):
    ...

    @classmethod
    def new(...):
        # Instantiates object from passed values
        ...

    def serialize(...):
        # Serializes object to CBOR or JSON string
        ...

    @classmethod
    def deserialize(...):
        # Instantiates/Deserializes object from CBOR or JSON string
        ...

    def sign(...):
        # Sign object with private key passed
        # That can be called within new()
        ...

    def validate(...):
        # Validate transaction correctness.
        # Can be called within from_json()
        ...

    def __eq__(...):
        # Check whether transactions are the same
        ...
</pre>
(**Note:** this interface, maybe w/o `sign()`, will be useful for other future
classes.)

Test your implementation.
- Do you think it makes sense to add any other fields?
- What checks are you going to include within `validate()` ?
- Do you see any challenges in implementing `sign()` and `verify()`?


### Question 5

Develop a full Merkle tree implementation.  Your implementation should
implement the following methods and functions
<pre>
class MerkleTree(...):
    ...

    def add(...):
        # Add entries to tree
        ...

    def build(...):
        # Build tree computing new root
        ...

    def get_proof(...):
        # Get membership proof for entry
        ...

     def get_root(...):
        # Return the current root
        ...

def verify_proof(entry, proof, root):
    # Verify the proof for the entry and given root. Returns boolean.
    ...
</pre>

(Make sure you distinguish leaf nodes from non-leaf node.)

Populate the tree with a random number (between 100-1000) of random
transactions, compute a root, get proofs for 10 random entries and verify them.