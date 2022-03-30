import xrpl
import pandas as pd
from xrpl.models.requests import AccountLines
from time import sleep
import random
from xrpl.account import get_balance

#### make sure value/rate is the norm
filename_in = 'redacted'

#randomness
delays = [13.0, 21.0, 34.0, 55.0, 89.0, 144.0, 233.0]
delays = [i/6.1 for i in delays]
# sleep()

##TL info
name = 'snub'
Issuer = "rNCRr79JC8YcA8pG4VAzhrshYxahKCodnX"
Currency = '534E554200000000000000000000000000000000'
Value = '77000999.99'

# Define the network client
from xrpl.clients import JsonRpcClient
JSON_RPC_URL = "https://xrplcluster.com/"
client = JsonRpcClient(JSON_RPC_URL)

 #import seeds
df = pd.read_excel(f'redacted', 0)
seeds = df['Seeds'].tolist()

# Create an index of wallet/classic address pairs
both = []
from xrpl.wallet import Wallet
for i in seeds:
    hold = []
    wallet = Wallet(seed=i, sequence=1)
    hold.append(wallet)
    address = str(Wallet(seed=i, sequence=1).classic_address)
    hold.append(address)
    both.append(hold)

print(both)
count = 0

runtime = [0,1,2, 3, 5]
for j in runtime:
    count = 0
    ##wallet is 0, address is 1
    for i in both:
        trust = False
        # Create an account str from the wallet
        count+=1
        wallet = i[0]
        account = i[1]
        print(count, account, name)

        # Look up info about your account
        acct_lines = AccountLines(
            account=account)
        try:
            balance = get_balance(account, client)
            response = client.request(acct_lines)
            result = response.result.get('lines')
            for i in result:
                if i.get('account') == Issuer:
                    trust = True

            if trust != True:
                print(random.choice(delays))
                sleep(random.choice(delays))
                # Prepare payment
                from xrpl.models.transactions import TrustSet
                from xrpl.models.amounts import IssuedCurrencyAmount
                b = IssuedCurrencyAmount(currency=Currency, issuer=Issuer, value=Value)
                a = TrustSet(account=account, limit_amount=b, fee='15', flags=131072)

                # Sign the transaction
                from xrpl.transaction import safe_sign_and_autofill_transaction
                my_tx_payment_signed = safe_sign_and_autofill_transaction(a, wallet, client, check_fee=False)

                # Submit and send the transaction
                from xrpl.transaction import send_reliable_submission
                tx_response = send_reliable_submission(my_tx_payment_signed, client)

                #sleep(.5)

        except xrpl.transaction.XRPLReliableSubmissionException as e:
            print(f"Submit failed: {e}")
            pass

        except:
            pass
