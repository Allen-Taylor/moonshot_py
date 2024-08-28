# moonshot_py 
Swap on Moonswap with Python. Updated: 8/29/2024

### Contact

My services are for **hire**. Contact me if you need help integrating the code into your own project. 

Telegram: @AL_THE_BOT_FATHER

### FAQS

**What format should my private key be in?** 

The private key should be in the base58 string format, not bytes. 

**Why are my transactions being dropped?** 

You get what you pay for. If you use the public RPC, you're going to get rekt. Spend the money for Helius or Quick Node. Also, play around with the compute limits and lamports.

**What format is slippage in?** 

Slippage is in bps format. 500bps equals 5% slippage. 

### Example

```
from moonshot import buy

# BUY EXAMPLE
mint_str = "token_to_buy"
buy(mint_str=mint_str, sol_in=0.01, slippage_bps=500)

```
```
from moonshot import sell
from utils import get_token_balance
from config import payer_keypair

# SELL EXAMPLE
mint_str = "token_to_sell"
pubkey_str = str(payer_keypair.pubkey())
token_balance = get_token_balance(pubkey_str, mint_str)
sell(mint_str=mint_str, token_balance=token_balance, slippage_bps=500)

```
