# implement transaction class here
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
import json
import uuid


class Transaction:

    def __init__(self, tid=None, sender=None, receiver=None, amount=None, comment=None, signature=None):
        if tid is None:
            self.tid = uuid.uuid4().hex
        else:
            self.tid = tid
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.comment = comment
        self.signature = signature

    @classmethod
    def new(cls, sender, receiver, amount, comment, sign_key):
        # Instantiates object from passed values
        Tx = cls(sender=sender, receiver=receiver,
                 amount=amount, comment=comment)
        if sender is not None:
            Tx.sign(sign_key)
        return Tx

    def serialize(self, sign_mode=True):
        # Serializes object to CBOR or JSON string
        data = {
            'tid': self.tid,
            'sender': self.sender.to_string().hex() if self.sender is not None else self.sender,
            'receiver': self.receiver.to_string().hex(),
            'amount': self.amount,
            'comment': self.comment
        }
        if sign_mode and not self.sender is None:
            data['signature'] = self.signature.hex()
        return json.dumps(data)

    @classmethod
    def deserialize(cls, json_string):
        # Instantiates/Deserializes object from CBOR or JSON string
        data = json.loads(json_string)
        tid = data['tid']
        if data['sender'] is None:
            sender = data['sender']
        else:
            sender = VerifyingKey.from_string(bytes.fromhex(data['sender']))
            signature = bytes.fromhex(data['signature'])
        receiver = VerifyingKey.from_string(bytes.fromhex(data['receiver']))
        amount = data['amount']
        comment = data['comment']

        return cls(tid, sender, receiver, amount, comment, signature if data['sender'] is not None else None)

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
