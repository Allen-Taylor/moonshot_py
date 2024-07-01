# moonshot_py

Swap on Moonshot with Python. 

```

Contact me if you would like early access to the code base.

The code base will be free in the future. 

Telegram: Allen_A_Taylor (AL THE BOT FATHER)

```
-----------------------------------------------------------------------------

```
HOW TO SWAP:

Credit to Metalingus (Klaus) and Andrew Gryffin

First Endpoint: https://ms.dexscreener.com/tx/v1/prepare

Payload:
{
amount: "",
collateralAmount: "", 
creatorPK: "" # public key, not priv key
direction: "buy"
mintAddress: ""
slippageBps: 1500
}

Response:
{
    "transaction": "Serialized Transaction Base64",
    "token": "JSON Web Token",
    "direction": "buy"
}

Decode (Base 64) the prepared transaction into a versioned txn and sign it.
Encode (Base 64) the signed versioned txn.

Second Endpoint: https://ms.dexscreener.com/tx/v1/submit

Payload:
{
direction: "buy",
token: "JSON Web Token (from prepared endpoint)", 
signedTransaction: "Serialized Signed Transaction"
}

Response
{
direction: "buy", 
transactionSignature: "xxx",
statusToken: "xxx",
status: "xxx"
}

```
