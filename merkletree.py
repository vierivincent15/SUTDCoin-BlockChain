# implement merkle tree class here

from transaction import *
import math
import hashlib

class MerkleTree():
    def __init__(self, transactions):
        self.transactions = transactions
        self.leaf_nodes = None
        self.nonleaf_nodes = None
        self.height = None
        self.build()

    def add(self, transaction):
        # Add entries to tree
        self.transactions.append(transaction)
        self.build()

    def build(self):
        # Build tree computing new root
        height = math.ceil(math.log(len(self.transactions), 2))
        self.height = height    # assign height
        leaf_nodes = [str.encode("")]*(2**height)

        for i in range(len(self.transactions)):
            to_hash = str.encode(self.transactions[i].serialize() + "leaf")     # different hashing
            m = hashlib.sha256()
            m.update(to_hash)
            leaf_nodes[i] = m.digest()
        self.leaf_nodes = leaf_nodes    # assign leaf nodes

        old_list = leaf_nodes
        nonleaf_nodes = []
        for i in range(height):
            new_list = []
            for i in range(0,len(old_list),2):
                to_hash = old_list[i] + old_list[i+1] + str.encode("nonleaf")   # different hashing
                m = hashlib.sha256()
                m.update(to_hash)
                new_list.append(m.digest())
            old_list = new_list.copy()
            new_list.extend(nonleaf_nodes)
            nonleaf_nodes = new_list.copy()
            new_list = []
        self.nonleaf_nodes = nonleaf_nodes      # assign non leaf nodes
        

    def get_proof(self, transaction):
        # Get membership proof for entry
        try:
            idx = self.transactions.index(transaction)
        except ValueError:
            print("Transaction not in MerkleTree")
            return
        
        tree_ls = self.nonleaf_nodes.copy()
        tree_ls.extend(self.leaf_nodes)
        final_idx = len(self.nonleaf_nodes) + idx
        if final_idx%2 == 0:
            final_idx = final_idx - 1
        else:
            final_idx = final_idx + 1

        proof = []
        proof_idx = []
        while final_idx >= 0:
            proof.append(tree_ls[final_idx])
            proof_idx.append(final_idx)
            if final_idx%2 == 0:
                result = int((final_idx - 2)/2)
                if result%2 == 0:
                    final_idx = result - 1
                else:
                    final_idx = result + 1
            else:
                result = int((final_idx - 1)/2)
                if result%2 == 0:
                    final_idx = result - 1
                else:
                    final_idx = result + 1
        return (proof_idx, proof)

    def get_root(self):
        # Return the current root
        return self.nonleaf_nodes[0]

def verify_proof(entry, proof, root):
    # Verify the proof for the entry and given root. Returns boolean.
    if proof is None:
        print("Transaction not in MerkleTree")
        return False

    proof_idx, proof_ls = proof
    to_hash = str.encode(entry + "leaf")
    m = hashlib.sha256()
    m.update(to_hash)
    hash_entry = m.digest()

    hash_value = hash_entry
    for i in range(len(proof_ls)):
        if proof_idx[i]%2 == 0:
            to_hash = hash_value + proof_ls[i] + str.encode("nonleaf")
        else:
            to_hash = proof_ls[i] + hash_value + str.encode("nonleaf")
        m = hashlib.sha256()
        m.update(to_hash)
        hash_value = m.digest()

    if(hash_value == root):
        return True
    else:
        return False


# to test implementation
if __name__ == "__main__":
    transactions = []
    amount = 1000
    comment = "COOL!"
    for i in range(4):
        sign_key_1 = SigningKey.generate()
        sender = sign_key_1.get_verifying_key()
        
        sign_key_2 = SigningKey.generate()
        receiver = sign_key_2.get_verifying_key()
        
        Tx = Transaction.new(sender, receiver, amount, comment, sign_key_1)
        transactions.append(Tx)
    

    sign_key_1 = SigningKey.generate()
    sender = sign_key_1.get_verifying_key()
    
    sign_key_2 = SigningKey.generate()
    receiver = sign_key_2.get_verifying_key()
    
    Tx = Transaction.new(sender, receiver, amount, comment, sign_key_1)

    print(transactions)
    print(transactions[2])
    transactions.remove(Tx)
    print(transactions)
    # tree = MerkleTree(transactions)
    # print(tree)
    # print(transactions[0].validate())