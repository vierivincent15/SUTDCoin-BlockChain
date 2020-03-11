# implement transaction class here
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
import json

class Transaction:
    
    def __init__(self, sender=None, receiver=None, amount=None, comment=None, signature=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.comment = comment
        self.signature = signature
        
    @classmethod
    def new(cls, sender, receiver, amount, comment):
        # Instantiates object from passed values
        Tx = cls(sender,receiver,amount,comment)
        
        return Tx

    def serialize(self, sign_mode=True):
        # Serializes object to CBOR or JSON string
        data = {
            'sender': self.sender.to_string().hex(),
            'receiver': self.receiver.to_string().hex(),
            'amount': self.amount,
            'comment': self.comment
        }
        if sign_mode:
            data['signature'] = self.signature.hex()
        return json.dumps(data)
        

    @classmethod
    def deserialize(cls, json_string):
        # Instantiates/Deserializes object from CBOR or JSON string
        data = json.loads(json_string)
        sender = VerifyingKey.from_string(bytes.fromhex(data['sender']))
        receiver = VerifyingKey.from_string(bytes.fromhex(data['receiver']))
        amount = data['amount']
        comment = data['comment']
        signature = bytes.fromhex(data['signature'])
        
        return cls(sender,receiver,amount,comment,signature)

    def sign(self, sign_key):
        # Sign object with private key passed
        # That can be called within new()
        s = self.serialize(False)
        sig = sign_key.sign(s.encode())
        self.signature = sig

    def validate(self):
        # Validate transaction correctness.
        # Can be called within from_json()
        sig = self.signature
        s = self.serialize(False)
        return self.sender.verify(sig, s.encode())

    def __eq__(self, other):
        # Check whether transactions are the same
        return self.serialize(False) == other.serialize(False)

# to test implementation
if __name__ == "__main__":
    pass