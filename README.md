# moonshot_py
Swap on Moonswap with Python. 

**If you can - please support my work and donate to: 3pPK76GL5ChVFBHND54UfBMtg36Bsh1mzbQPTbcK89PD**

### Swap Layout

Do not change the hard-coded values as they are part of the actual buy/sell instructions for the moonswap program. 

**discriminator_as_int = 16927863322537952870**

**discriminator_as_int = 12502976635542562355**

### Contact

My services are for **hire**. Contact me if you need help integrating the code into your own project. 

Telegram: Allen_A_Taylor (AL THE BOT FATHER)

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
buy(mint_str=mint_str, collateral_amount=0.01, slippage_bps=500)

```
```
from moonshot import sell
from utils import get_token_balance
from config import PUB_KEY

# SELL EXAMPLE
mint_str = "token_to_sell"
token_balance = get_token_balance(PUB_KEY, mint_str)
sell(mint_str=mint_str, token_balance=token_balance, slippage_bps=500)

```
