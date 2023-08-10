import anvil.server
from nucypher.characters.lawful import Bob, Ursula
from nucypher.characters.lawful import Enrico as Enrico
from nucypher.cli.utils import connect_to_blockchain
from nucypher.policy.conditions.lingo import ConditionLingo
from nucypher.utilities.emitters import StdoutEmitter
from nucypher_core.ferveo import Ciphertext, DkgPublicKey

DKGkey = b"\xa1o\xf0\xbb\xefl\xb0\xb1\xbd?E\xf4\xbek\xe6P\xc2\xd2N\xc8\xb0\xbd\x0c\xc1\xd5e\x83R\xdf\\\nY\x06\x04\xe5\x1cX\x99\xdaI\xeb\xb8\xca\xb70\xbfi\xaf"
goerli_uri = "https://goerli.infura.io/v3/663d60ae0f504f168b362c2bda60f81c"

connect_to_blockchain(eth_provider_uri=goerli_uri, emitter=StdoutEmitter())
enrico = Enrico(encrypting_key=DkgPublicKey.from_bytes(DKGkey))
# bob = Bob(
#     eth_provider_uri=goerli_uri,
#     domain='lynx',
#     known_nodes=[Ursula.from_teacher_uri('https://lynx.nucypher.network:9151', provider_uri=goerli_uri, min_stake=0)]
# )
# bob.start_learning_loop(now=True)
# print("Bob has finished learning")


def get_conditions(timestamp):
    time_condition = {
        "method": "blocktime",
        "chain": 5,
        "returnValueTest": {"comparator": ">=", "value": timestamp},
    }
    conditions = {
        "version": ConditionLingo.VERSION,
        "condition": time_condition,
    }
    return conditions


@anvil.server.callable
def encrypt_vote(proof, vote, timestamp):
    message = f"{proof}{vote}".encode()
    conditions = get_conditions(timestamp)
    ciphertext = enrico.encrypt_for_dkg(
        plaintext=message,
        conditions=conditions,
    )
    print(conditions)

    return bytes(ciphertext).hex()


@anvil.server.callable
def decrypt_vote(ciphertext, timestamp):
    cleartext = bob.threshold_decrypt(
        ritual_id=0,
        ciphertext=Ciphertext.from_bytes(bytes.fromhex(ciphertext)),
        conditions=get_conditions(timestamp),
    )
    return bytes(cleartext).decode()