import json
import time
import requests
from solana.transaction import Signature
from config import RPC, client
from solders.pubkey import Pubkey  # type: ignore
from spl.token.instructions import get_associated_token_address

def derive_curve_accounts(mint: Pubkey):
    try:
        MOONSHOT_PROGRAM = Pubkey.from_string("MoonCVVNZFSYkqNXP6bxHLPL6QQJiMagDL3qcqUQTrG")
        SEED = "token".encode()

        curve_account, _ = Pubkey.find_program_address(
            [SEED, bytes(mint)],
            MOONSHOT_PROGRAM
        )

        curve_token_account = get_associated_token_address(curve_account, mint)
        return curve_account, curve_token_account
    except Exception:
        return None, None

def find_data(data, field):
    if isinstance(data, dict):
        if field in data:
            return data[field]
        else:
            for value in data.values():
                result = find_data(value, field)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_data(item, field)
            if result is not None:
                return result
    return None

def get_token_balance(pub_key: str, token: str):
    try:

        headers = {"accept": "application/json", "content-type": "application/json"}

        payload = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "getTokenAccountsByOwner",
            "params": [
                pub_key,
                {"mint": token},
                {"encoding": "jsonParsed"},
            ],
        }
        
        response = requests.post(RPC, json=payload, headers=headers)
        ui_amount = find_data(response.json(), "uiAmount")
        return float(ui_amount)
    except Exception as e:
        return None

def confirm_txn(txn_sig, max_retries=20, retry_interval=3):
    retries = 0
    if isinstance(txn_sig, str):
        txn_sig = Signature.from_string(txn_sig)
    while retries < max_retries:
        try:
            txn_res = client.get_transaction(txn_sig, encoding="json", commitment="confirmed", max_supported_transaction_version=0)
            txn_json = json.loads(txn_res.value.transaction.meta.to_json())
            if txn_json['err'] is None:
                print("Transaction confirmed... try count:", retries+1)
                return True
            print("Error: Transaction not confirmed. Retrying...")
            if txn_json['err']:
                print("Transaction failed.")
                return False
        except Exception as e:
            print("Awaiting confirmation... try count:", retries+1)
            retries += 1
            time.sleep(retry_interval)
    print("Max retries reached. Transaction confirmation failed.")
    return None
