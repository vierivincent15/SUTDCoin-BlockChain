# implement transaction class here
from ecdsa import SigningKey, VerifyingKey, BadSignatureError
import json


class Transaction(object):

    def __init__(self, sender=None, receiver=None, amount=None, comment=None, signature=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.comment = comment
        self.signature = signature

    @classmethod
    def new(cls, sender, receiver, amount, comment, signing_key):
        # Instantiates object from passed values

        tx = cls(sender, receiver, amount, comment)
        tx.signature = tx.sign(signing_key)

        return tx

    def serialize(self, signature=True):
        # Serializes object to CBOR or JSON string
        
        to_json = {}
        to_json["sender"] = self.sender.to_string().hex() 
        to_json["receiver"] = self.receiver.to_string().hex()
        to_json["amount"] = self.amount
        to_json["comment"] = self.comment
        if signature:
            to_json["signature"] = self.signature.hex()
        output = json.dumps(to_json)

        return output

    @classmethod
    def deserialize(cls, json_obj):
        # Instantiates/Deserializes object from CBOR or JSON string
        from_json = json.loads(json_obj)
        sender = VerifyingKey.from_string(bytes.fromhex(from_json["sender"]))
        receiver = VerifyingKey.from_string(bytes.fromhex(from_json["receiver"]))
        amount = from_json["amount"]
        comment = from_json["comment"]
        signature = bytes.fromhex(from_json["signature"])

        return cls(sender, receiver, amount, comment, signature)


    def sign(self, signing_key):
        # Sign object with private key passed
        # That can be called within new()

        to_sign = self.serialize(signature=False)
        signature = signing_key.sign(to_sign.encode())

        return signature

    def validate(self):
        # Validate transaction correctness.
        # Can be called within from_json()
        orig_serialize = self.serialize(signature=False)
        try:
            validate = self.sender.verify(self.signature, orig_serialize.encode())
            return validate
        except BadSignatureError:
            return False

    def __eq__(self, other):
        # Check whether transactions are the same
        
        return (self.sender == other.sender) and (self.receiver == other.receiver) and (self.amount == other.amount) and (self.comment == other.comment)


# to test implementation
if __name__ == "__main__":
    print("="*25)
    print("Creating Sender and Receiver")
    ppl_1_private = SigningKey.generate() # uses NIST192p
    ppl_1_public = ppl_1_private.verifying_key
    ppl_2_private = SigningKey.generate() # uses NIST192p
    ppl_2_public = ppl_2_private.verifying_key

    print("="*25)
    print("Testing new() & sign()")
    t1 = Transaction.new(sender=ppl_1_public, receiver=ppl_2_public, amount=100, comment="Hello World", signing_key=ppl_1_private)
    print("sender", t1.sender)
    print("receiver", t1.receiver)
    print("amount", t1.amount)
    print("comment", t1.comment)
    print("signature", t1.signature)

    print("="*25)
    print("Testing serialize()")
    t1_serialize = t1.serialize()
    print(t1_serialize)

    print("="*25)
    print("Testing deserialize()")
    t1_ = Transaction.deserialize(t1_serialize)
    print("sender", t1_.sender)
    print("receiver", t1_.receiver)
    print("amount", t1_.amount)
    print("comment", t1_.comment)
    print("signature", t1_.signature)

    print("="*25)
    print("Testing validate()")
    print("If someone didn't change the message...")
    print(t1_.validate())
    print("If someone did change the message...")
    t1_.comment = "Hello Hello World"
    print(t1_.validate())
    
    print("="*25)
    print("Testing __eq__")
    t2 = Transaction.new(ppl_1_public, ppl_2_public, 100, "Hello World", ppl_1_private)
    print(t1 == t2)
    t3 = Transaction.new(ppl_1_public, ppl_2_public, 200, "Hello World", ppl_1_private)
    print(t1 == t3)