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
    pass