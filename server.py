import anvil.server
from nucypher_core.ferveo import DkgPublicKey, Ciphertext
from nucypher.characters.lawful import Enrico as Enrico
from nucypher.characters.lawful import Ursula
from nucypher.characters.lawful import Bob
from nucypher.cli.utils import connect_to_blockchain
from nucypher.utilities.emitters import StdoutEmitter
from electora_keys import DKGkey, uplink_key
from nucypher.policy.conditions.lingo import ConditionLingo

anvil.server.connect(uplink_key)
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
    message = f'{proof}{vote}'.encode()
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
    

anvil.server.wait_forever()