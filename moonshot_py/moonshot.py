import struct
from config import payer_keypair, client, PUB_KEY
from constants import *
from curve import get_tokens_by_collateral_amount, get_collateral_amount_by_tokens, derive_curve_accounts, TradeDirection
from solana.rpc.types import TokenAccountOpts, TxOpts
from solana.transaction import AccountMeta
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price  # type: ignore
from solders.instruction import Instruction  # type: ignore
from solders.message import MessageV0  # type: ignore
from solders.pubkey import Pubkey  # type: ignore
from solders.transaction import VersionedTransaction  # type: ignore
from spl.token.instructions import create_associated_token_account, get_associated_token_address
from utils import get_token_balance, confirm_txn

def buy(mint_str: str, collateral_amount: float = 0.01, slippage_bps: int = 500):
    try:
        # Calculate the amount of tokens to buy with the given collateral amount
        amount = get_tokens_by_collateral_amount(mint_str, collateral_amount, TradeDirection.BUY)
        
        # Convert collateral amount to integer representation in lamports
        collateral_amount = int(collateral_amount * LAMPORTS_PER_SOL)

        print(f"Collateral Amount (in lamports): {collateral_amount}, Amount: {amount}, Slippage (bps): {slippage_bps}")
        
        # Check if the amount calculation was successful
        if not amount:
            print("Failed to get tokens by collateral amount...")
            return

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

        # Define integer values
        discriminator_as_int = 16927863322537952870
        integers = [
            discriminator_as_int,
            amount,
            collateral_amount,
            slippage_bps
        ]
        
        # Pack integers into binary segments
        binary_segments = [struct.pack('<Q', integer) for integer in integers]
        data = b''.join(binary_segments)  
        
        # Create the swap instruction
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
        txn_sig = client.send_transaction(transaction, opts=TxOpts(skip_preflight=True, preflight_commitment="confirmed")).value
        print(f"Transaction Signature: {txn_sig}")
        
        # Confirm transaction and print the confirmation result
        confirm = confirm_txn(txn_sig)
        print(f"Transaction Confirmation: {confirm}")
    except Exception as e:
        print(e)
        
def sell(mint_str: str, token_balance: float=None, slippage_bps: int=500):
    try:
        # Retrieve token balance if not provided
        if token_balance is None:
            token_balance = get_token_balance(PUB_KEY, mint_str)
        
        print(f"Token Balance: {token_balance}")
        
        # Check if the token balance is zero
        if token_balance == 0:
            return
        
        # Calculate the collateral amount by tokens and convert token balance to lamports
        collateral_amount = get_collateral_amount_by_tokens(mint_str, token_balance, TradeDirection.SELL)
        amount = int(token_balance * LAMPORTS_PER_SOL)
        
        print(f"Collateral Amount: {collateral_amount}, Amount (in lamports): {amount}, Slippage (bps): {slippage_bps}")
        
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

        # Define integer values
        discriminator_as_int = 12502976635542562355
        integers = [
            discriminator_as_int,
            amount,
            collateral_amount,
            slippage_bps
        ]
        
        # Pack integers into binary segments
        binary_segments = [struct.pack('<Q', integer) for integer in integers]
        data = b''.join(binary_segments)  
        
        # Create the swap instruction
        swap_instruction = Instruction(MOONSHOT_PROGRAM, data, keys)

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
        txn_sig = client.send_transaction(transaction, opts=TxOpts(skip_preflight=True, preflight_commitment="confirmed")).value
        print(f"Transaction Signature: {txn_sig}")

        # Confirm transaction and print the confirmation result
        confirm = confirm_txn(txn_sig)
        print(f"Transaction Confirmation: {confirm}")
    except Exception as e:
        print(e)