# SUTDCoin-BlockChain
SUTDCoin: Blockchain Implementation

We are going to design and implement a simple cryptocurrency during the
following 6 weeks, according to the following schedule:

* Week1 - Cryptography intro, coding, encoding, Merkle trees
* Week2 - SUTDcoin blockchain – basic design and implementation, forks handling
* Week3 - SUTDcoin blockchain – PoW, mining, transactions, and SPV
* Week4 - SUTDcoin networking – propagation, discovery, mining competition,
  interactions
* Week5 - SUTDcoin attacks – double-spending and selfish-mining attacks
* Week6 - SUTDcoin – shaping up and early grading

Use Python3 by default, the following packages may be helpful:
base58, ecdsa, flask, hashlib, cbor, sqlite3, and matplotlib.

**Note:** You do not have to configure your personal computer. At
[https://bit.ly/2Pjw2VE](https://bit.ly/2Pjw2VE), you can download a
virtual machine image for VirtualBox hypervisor with Linux that has most of the
packages and tools needed.  It requires minimum 2GB RAM, 20GB Disk, and 2 CPUs.

---

## Week 1

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

---

## Week 2

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

---

## Week 3

### Question 1
Design and implement a `Miner` class realizing miner's functionalities.  Then,
implement a simple simulator with miners running Nakamoto consensus and making
transactions:

- Adjust the `TARGET` (global and static) parameter, such that on average new
  blocks arrive every few (2-5) seconds.
- A miner who found a new block should be rewarded with 100 SUTDcoins.
- Introduce random transactions, such that miners (with coins) can send
  transactions to other miners.
- Make sure that coins cannot be double-spent.
    - consider the `addr:balance` model and the UTXO model. What are pros and
      cons?
    - do you need to modify (why, if so) the transaction format introduced in the
      first week?  *Hint:* yes, you need.
- Extend the verification checks.
- Simulate miners competition.

---

## Week 4

### Question 1
Design and implement an `SPVClient` class.  SPV clients should implement a
simple SPV logic, i.e., they should:
- have their key pairs associated
- be able to receive block headers (not full blocks)
- be able to receive transactions (with their presence proofs) and verify them
- be able to send transactions

Integrate your implementation with your simulator from the previous exercise.
Test your implementation.


### Question 2
Move actors of your protocol (i.e., miners and SPV clients) to stand-alone
applications.  For their communication, design and implement a simple network
protocol.  Your protocol should be able to handle different kind of messages
(e.g., SPV clients need only headers, miners need to synchronize entire
blocks, ...).

To implement the network protocol you can use your favorite tools (e.g., the
HTTP protocol and Flask).  You can simplify some functionalities (but ask
before) like node discovery (e.g., a file with participants' addresses is good
enough).

---

## Week 5

### Question 1
Implement and demonstrate double-spending via the 51% attack.

### Question 2
Implement and demonstrate the selfish-mining attack.

---

## Week 6

### Question 1
Prepare your code for a demonstration including:
- mining and coin creation
- fork resolution
- transaction resending protection
- payments between miners and SPV clients
    - transaction validation (for miners and SPV clients)
- the attacks from the previous week

Conduct a demonstration and prepare a document reporting on it.  In your report
please also document how to reproduce your demonstration and highlight major
differences between Bitcoin and your SUTDcoin.


### Early Grading