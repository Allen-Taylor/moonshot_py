# moonshot_py

Swap on Moonshot with Python. 

```
Notes so far:

Program - MoonCVVNZFSYkqNXP6bxHLPL6QQJiMagDL3qcqUQTrG

BUY - 66063d1201daebe, amount, collateralAmount, slippageBps

sender XXX Writable Signer Fee Payer

backendAuthority Cb8Fnhp95f9dLxB3sYkNCbN3Mjxuc3v2uQZ7uVeqvNGB Signer 

senderTokenAccount XXX Writable 

curveAccount XXX Writable 

curveTokenAccount XXX Writable 

dexFee 3udvfL24waJcLhskRAsStNMoNUvtyXdxrWQz4hgi953N Writable 

helioFee 5K5RtTWzzLp4P8Npi84ocf7F1vBsAu29N1irG4iiUnzt Writable 

mint XXX

configAccount 36Eru7v11oU5Pfrojyn5oY3nETA1a1iqsw2WUu6afkM9

associatedTokenProgram TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA

associatedTokenProgram ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL

systemProgram 11111111111111111111111111111111

-Buy transaction requires two signatures, the user keypair and the backendAuthority keypair.

```


-----------------------------------------------------------------------------

```
Last Update: 6/28/2024
Credit to Metalingus (Klaus) and Andrew Gryffin

Endpoint: https://ms.dexscreener.com/tx/v1/prepare

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

Endpoint: https://ms.dexscreener.com/tx/v1/submit

Payload:
{
direction: "buy",
token: "JSON Web Token (from prepared endpoint)", 
signedTransaction: "Serialized Signed Transaction"
}

Response

???

```
