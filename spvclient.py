from transaction import Transaction
from blockchain import Blockchain, validate
from block import Block
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
        for key, value in blockchain.chain.items():
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
    client1 = SPVClient.new('a')
    client2 = SPVClient.new('b')

    # build a test blockchain
    tx1 = Transaction('Alice', 'Bob', 10, "comment")
    tx2 = Transaction('Bob', 'Alice', 20, "comment")
    tx3 = Transaction('Alice', 'Bob', 30, "comment")
    transactions1 = [tx1, tx2, tx3]
    transactions2 = [tx2, tx1, tx3]
    transactions3 = [tx3, tx2, tx1]
    transactions4 = [tx1, tx2, tx3, tx1]
    block1 = Block(transactions1)
    block2 = Block(transactions2)
    block3 = Block(transactions3)
    block4 = Block(transactions4)
    blocks = [block1, block2, block3]
    blockchain = Blockchain()
    for b in blocks:
        blockchain.add(b)

    # Able to receive block headers (not full blocks)
    # client1.receive_block_header(blockchain)
    # print(client1.block_headers)

    # Able to receive transactions (with their presence proofs) and verify them
    # Able to send transactions
    UTXO = client1.send_transaction(client2.public_key, 100, 'comment')
    print("\nVerifiying Transaction")
    print("-" * 100)
    print(f"Result: {client1.verify_transaction(UTXO)}")
