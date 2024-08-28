import struct
from config import payer_keypair, client, PUB_KEY
from constants import *
from solana.rpc.types import TokenAccountOpts, TxOpts
from solana.transaction import AccountMeta
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price  # type: ignore
from solders.instruction import Instruction  # type: ignore
from solders.message import MessageV0  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from solders.transaction import VersionedTransaction  # type: ignore
from spl.token.instructions import create_associated_token_account, get_associated_token_address
from utils import get_token_balance, confirm_txn, derive_curve_accounts
import requests

def get_token_data(token_address):
    url = f"https://api.moonshot.cc/token/v1/solana/{token_address}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        token_data = response.json() 
        
        return token_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

def buy(mint_str: str, sol_in: float = 0.01, slippage_bps: int = 1500):
    try:
        token_data = get_token_data(mint_str)
        if token_data == None:
            return
            
        token_price = token_data['priceNative']
        tokens_out = sol_in / float(token_price)
        token_amount = int(tokens_out * 10**9)
        collateral_amount = int(sol_in * LAMPORTS_PER_SOL)
        print(f"Collateral Amount: {collateral_amount}, Token Amount: {token_amount}, Slippage (bps): {slippage_bps}")
        
        # Retrieve the public key of the owner
        SENDER = payer_keypair.pubkey()
        MINT = Pubkey.from_string(mint_str)
        
        # Attempt to retrieve token account, otherwise create associated token account
        token_account, token_account_instructions = None, None
        try:
            account_data = client.get_token_accounts_by_owner(SENDER, TokenAccountOpts(MINT))
            token_account = account_data.value[0].pubkey
            token_account_instructions = None
        except:
            token_account = get_associated_token_address(SENDER, MINT)
            token_account_instructions = create_associated_token_account(SENDER, SENDER, MINT)

        # Define account keys required for the swap
        CURVE_ACCOUNT, CURVE_TOKEN_ACCOUNT = derive_curve_accounts(MINT)
        SENDER_TOKEN_ACCOUNT = token_account

        # Build account key list 
        keys = [
            AccountMeta(pubkey=SENDER, is_signer=True, is_writable=True),
            AccountMeta(pubkey=SENDER_TOKEN_ACCOUNT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=CURVE_ACCOUNT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=CURVE_TOKEN_ACCOUNT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=DEX_FEE, is_signer=False, is_writable=True),
            AccountMeta(pubkey=HELIO_FEE, is_signer=False, is_writable=True),
            AccountMeta(pubkey=MINT, is_signer=False, is_writable=True), 
            AccountMeta(pubkey=CONFIG_ACCOUNT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=TOKEN_PROGRAM, is_signer=False, is_writable=True),
            AccountMeta(pubkey=ASSOC_TOKEN_ACC_PROG, is_signer=False, is_writable=False),
            AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False)
        ]

        # Construct the swap instruction
        data = bytearray()
        data.extend(bytes.fromhex("66063d1201daebea"))
        data.extend(struct.pack('<Q', token_amount))
        data.extend(struct.pack('<Q', collateral_amount))
        data.extend(struct.pack('<B', 0))
        data.extend(struct.pack('<Q', slippage_bps))
        data = bytes(data)
        swap_instruction = Instruction(MOONSHOT_PROGRAM, data, keys)

        # Create transaction instructions
        instructions = []
        instructions.append(set_compute_unit_price(UNIT_PRICE))
        instructions.append(set_compute_unit_limit(UNIT_BUDGET))
        
        # Add token account creation instruction if needed
        if token_account_instructions:
            instructions.append(token_account_instructions)
        
        # Add the swap instruction
        instructions.append(swap_instruction)

        # Compile message
        compiled_message = MessageV0.try_compile(
            payer_keypair.pubkey(),
            instructions,
            [],  
            client.get_latest_blockhash().value.blockhash,
        )

        # Create transaction
        transaction = VersionedTransaction(compiled_message, [payer_keypair])
        
        # Send the transaction and print the transaction signature
        txn_sig = client.send_transaction(transaction, opts=TxOpts(skip_preflight=False, preflight_commitment="confirmed")).value
        print(f"Transaction Signature: {txn_sig}")
        
        # Confirm transaction and print the confirmation result
        confirm = confirm_txn(txn_sig)
        print(f"Transaction Confirmation: {confirm}")
    except Exception as e:
        print(e)
        
def sell(mint_str: str, token_balance=None, slippage_bps: int=1500):
    try:
        # Retrieve token balance if not provided
        if token_balance is None:
            pubkey_str = str(payer_keypair.pubkey())
            token_balance = get_token_balance(pubkey_str, mint_str)
        
        print(f"Token Balance: {token_balance}")
        
        # Check if the token balance is zero
        if token_balance == 0:
            return
        
        sol_decimal = 10**9
        token_decimal = 10**9
        token_data = get_token_data(mint_str)
        
        if token_data == None:
            return
        
        token_price = token_data['priceNative']
        token_value = float(token_balance) * float(token_price)
        collateral_amount = int(token_value * sol_decimal)
        token_amount = int(token_balance * token_decimal)
        
        print(f"Collateral Amount: {collateral_amount}, Token Amount: {token_amount}, Slippage (bps): {slippage_bps}")
        
        # Define account keys required for the swap
        MINT = Pubkey.from_string(mint_str)
        CURVE_ACCOUNT, CURVE_TOKEN_ACCOUNT = derive_curve_accounts(MINT)
        SENDER = payer_keypair.pubkey()
        SENDER_TOKEN_ACCOUNT = get_associated_token_address(SENDER, MINT)

        # Build account key list 
        keys = [
            AccountMeta(pubkey=SENDER, is_signer=True, is_writable=True),
            AccountMeta(pubkey=SENDER_TOKEN_ACCOUNT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=CURVE_ACCOUNT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=CURVE_TOKEN_ACCOUNT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=DEX_FEE, is_signer=False, is_writable=True),
            AccountMeta(pubkey=HELIO_FEE, is_signer=False, is_writable=True),
            AccountMeta(pubkey=MINT, is_signer=False, is_writable=True), 
            AccountMeta(pubkey=CONFIG_ACCOUNT, is_signer=False, is_writable=True),
            AccountMeta(pubkey=TOKEN_PROGRAM, is_signer=False, is_writable=True),
            AccountMeta(pubkey=ASSOC_TOKEN_ACC_PROG, is_signer=False, is_writable=False),
            AccountMeta(pubkey=SYSTEM_PROGRAM, is_signer=False, is_writable=False)
        ]

        # Construct the swap instruction
        token_data = bytearray()
        token_data.extend(bytes.fromhex("33e685a4017f83ad"))
        token_data.extend(struct.pack('<Q', token_amount))
        token_data.extend(struct.pack('<Q', collateral_amount))
        token_data.extend(struct.pack('<B', 0))
        token_data.extend(struct.pack('<Q', slippage_bps))
        token_data = bytes(token_data)
        swap_instruction = Instruction(MOONSHOT_PROGRAM, token_data, keys)
        
        # Create the swap instruction
        swap_instruction = Instruction(MOONSHOT_PROGRAM, token_data, keys)

        # Create transaction instructions
        instructions = []
        instructions.append(set_compute_unit_price(UNIT_PRICE))
        instructions.append(set_compute_unit_limit(UNIT_BUDGET))
        instructions.append(swap_instruction)

        # Compile message
        compiled_message = MessageV0.try_compile(
            payer_keypair.pubkey(),
            instructions,
            [],  
            client.get_latest_blockhash().value.blockhash,
        )

        # Create transaction
        transaction = VersionedTransaction(compiled_message, [payer_keypair])
        
        # Send the transaction and print the transaction signature
        txn_sig = client.send_transaction(transaction, opts=TxOpts(skip_preflight=False, preflight_commitment="confirmed")).value
        print(f"Transaction Signature: {txn_sig}")

        # Confirm transaction and print the confirmation result
        confirm = confirm_txn(txn_sig)
        print(f"Transaction Confirmation: {confirm}")
    except Exception as e:
        print(e)


