try:
    from transaction import Transaction
    from blockchain import Blockchain
    from block import Block
    from merkletree import verify_proof
except:
    from utils.transaction import Transaction
    from utils.blockchain import Blockchain
    from utils.block import Block
    from utils.merkletree import verify_proof
from ecdsa import SigningKey
import hashlib
import time
import json
   

class SPVClient(object):

    @classmethod
    def new(cls, client_id='', balance=0):
        newClient = cls()
        # Associated key pairs
        newClient.private_key = SigningKey.generate()
        newClient.public_key = newClient.private_key.get_verifying_key()
        newClient.block_headers = []
        newClient.id = client_id
        newClient.balance = balance
        newClient.headers = [[]]
        return newClient

    def send_transaction(self, receiver, amount, comment="COOL!"):
        if (self.balance < amount):
            raise ValueError

        UTXO = Transaction.new(self.public_key, receiver,
                               amount, comment, self.private_key)
        return UTXO

    def add_header(self, header):
        idxs = self.trace_prev_header(header["prev_header"])
        hc_idx, h_idx = 0, 0
        if idxs != -1:
            hc_idx, h_idx = idxs
        if (h_idx == len(self.headers[hc_idx]) - 1) or h_idx == 0:
            self.headers[hc_idx].append(header)
        else:
            temp_header = self.headers[hc_idx][:h_idx+1].copy()
            temp_header.append(header)
            self.headers.append(temp_header)

    def trace_prev_header(self, prev_header):
        for i in range(len(self.headers)):
            for j in range(len(self.headers[i])):
                if self.headers[i][j] == prev_header:
                    return (i, j)

        # meaning prev_header not found in chain
        return -1

    def identify_longest_header(self):
        chain_length = [len(chain) for chain in self.headers]
        max_index = chain_length.index(max(chain_length))

        return max_index

    def deserialize_proof(self, serialization):
        serialization = json.loads(serialization)
        proof_idx = serialization['proof_idx']
        proof = [bytes.fromhex(proof) for proof in serialization['proof']]
        root = bytes.fromhex(serialization['root'])
        return ([proof_idx, proof], root)
   
    def validate_transaction(self, transaction, proof, tree_root):
        longest_idx = self.identify_longest_header()
        merkle_roots = [header["tree_root"]
                        for header in self.headers[longest_idx]]
        if tree_root not in merkle_roots:
            return False
        return verify_proof(transaction, proof, tree_root)


if __name__ == "__main__":
    print("Testing SPVClient")
    print("-" * 100)
    client1 = SPVClient.new('1')
    client2 = SPVClient.new('2')

    # build a test blockchain
    alice_priv = SigningKey.generate()
    alice_pub = alice_priv.get_verifying_key()
    bob_priv = SigningKey.generate()
    bob_pub = alice_priv.get_verifying_key()
    tx1 = Transaction.new(alice_pub, bob_pub, 10, "comment", alice_priv)
    tx2 = Transaction.new(bob_pub, alice_pub, 20, "comment", bob_priv)
    tx3 = Transaction.new(alice_pub, bob_pub, 30, "comment", alice_priv)
    transactions1 = [tx1, tx2, tx3]
    transactions2 = [tx2, tx1, tx3]
    transactions3 = [tx3, tx2, tx1]
    transactions4 = [tx1, tx2, tx3, tx1]
    block1 = Block.new(transactions1, None)
    block2 = Block(transactions2, block1.header)
    block3 = Block(transactions3, block2.header)
    block4 = Block(transactions4, block3.header)
    blocks = [block1]
    blockchain = Blockchain()
    # for b in blocks:
    #     blockchain.add_block(b)

    # # Able to receive transactions (with their presence proofs) and verify them
    # # Able to send transactions
    # UTXO = client1.send_transaction(client2.public_key, 100, 'comment')
    # print("\nVerifiying Transaction")
    # print("-" * 100)
    # print(f"Result: {client1.verify_transaction(UTXO)}")
