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
Update: 6/27/2024

Endpoint: https://ms.dexscreener.com/tx/v1/prepare

Payload:
{
amount: "100000000000000"
creatorPK: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # public key
direction: "buy"
mintAddress: "5FaBJoqfPH5iv9NDFxgFfz9egBNNF5QPozMYuaBMmTvC"
slippageBps: 1500
}

Response:
{
    "transaction": "Serialized transaction base64",
    "token": "Some random generated hash ",
    "direction": "buy"
}

```
