from utils.transaction import Transaction
from utils.blockchain import Blockchain
from utils.block import Block
from ecdsa import SigningKey
import hashlib
import time


class SPVClient(object):

    @classmethod
    def new(cls, client_id=''):
        newClient = cls()
        # Associated key pairs
        newClient.private_key = SigningKey.generate()
        newClient.public_key = newClient.private_key.get_verifying_key()
        newClient.block_headers = []
        newClient.id = client_id
        newClient.balance = 0
        return newClient

    def receive_block_header(self, blockchain):
        for key, value in blockchain.blockchains.items():
            self.block_headers.append(value.to_json())

    def send_transaction(self, receiver, amount, comment):
        # TODO: check balance
        UTXO = Transaction(self.public_key, receiver, amount, comment)
        signature = UTXO.sign(self.private_key)
        UTXO.signature = signature
        self.balance -= amount
        return UTXO

    def receive_transaction(self, transaction):
        UTXO = Transaction(transaction.sender, transaction.receiver,
                           transaction.amount, transaction.comment)
        self.balance += transaction.amount

    def verify_transaction(self, transaction):
        return transaction.validate()


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

    # # Able to receive block headers (not full blocks)
    # # client1.receive_block_header(blockchain)
    # # print(client1.block_headers)

    # # Able to receive transactions (with their presence proofs) and verify them
    # # Able to send transactions
    # UTXO = client1.send_transaction(client2.public_key, 100, 'comment')
    # print("\nVerifiying Transaction")
    # print("-" * 100)
    # print(f"Result: {client1.verify_transaction(UTXO)}")
