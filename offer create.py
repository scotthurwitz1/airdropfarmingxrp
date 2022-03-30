import xrpl
from retrying import retry
from time import sleep
import pandas as pd
from xrpl.models.requests import AccountLines
from xrpl.account import get_next_valid_seq_number
from xrpl.ledger import get_latest_validated_ledger_sequence
from xrpl.transaction import safe_sign_and_autofill_transaction, send_reliable_submission
from xrpl.utils import xrp_to_drops
from xrpl.models.transactions import Payment
import json
from xrpl.account import get_latest_transaction
from xrpl.transaction import get_transaction_from_hash
from xrpl.wallet import Wallet
from xrpl.clients import JsonRpcClient
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.requests import AccountLines
from xrpl.models.transactions import OfferCreate
import random


##### update count to limit number of lines, drop, order limit, and tl info
lines = 20000
limit = 1151
loop = True

#randomness
delays = [13.0, 21.0, 34.0, 55.0, 89.0, 144.0, 233.0]
delays = [i/2.33 for i in delays]

######fix filenames before running
filename_in = redacted
df = pd.read_excel(f'redacted', 0)
seeds = df['Seeds'].tolist()


# Define the network client
JSON_RPC_URL = "https://xrplcluster.com/"
client = JsonRpcClient(JSON_RPC_URL)

#set params
drop = 172
#name = 'fedos'
Issuer = "rwbV9h75Tqvr629o5tGVWbdmMzU9aqhUi3"
Currency = '4665646F73000000000000000000000000000000'


##get origin addresses
origins = []
for i in seeds:
    hold = []
    wallet = Wallet(seed=i, sequence=1)
    hold.append(wallet)
    address = str(Wallet(seed=i, sequence=1).classic_address)
    hold.append(address)
    origins.append(hold)

print(origins)


#------------------------------------------------------------------------------------------------------------------


# def retry_if_result_none(result):
#     """Return True if we should retry (in this case when result is None), False otherwise"""
#     return result is None
#
# @retry(retry_on_result=retry_if_result_none)
def sell(origin_address, origin_wallet):
    account = origin_address

    print('selling', account)
    xrp = drop / limit
    tp = xrp_to_drops(xrp)
    print('tp')

    # Prepare transaction ----------------------------------------------------------
    my_payment = xrpl.models.transactions.OfferCreate(
        account=origin_address,
        fee='15',
        taker_gets=to_harvest,
        taker_pays=str(tp),
        flags=131072
    )

    # Sign transaction -------------------------------------------------------------
    signed_tx = xrpl.transaction.safe_sign_and_autofill_transaction(
        my_payment, origin_wallet, client, check_fee=False)
    max_ledger = signed_tx.last_ledger_sequence
    tx_id = signed_tx.get_hash()
    print('hi3')
    # Submit transaction -----------------------------------------------------------
    try:
        tx_response = xrpl.transaction.send_reliable_submission(signed_tx, client)
        sleep(1)
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        sleep(4)
        print(f"Submit failed: {e}")
        pass
    except:
        pass

    # Look up info about your account
    acct_lines = AccountLines(
        account=account)
    try:
        response = client.request(acct_lines)
        result = response.result.get('lines')
        for j in result:
            # print(j)
            if j.get('account') == Issuer:
                Value = j.get('balance')
    except:
        pass
    if Value != '0':
        return None
    else:
        return True

#run
count = 0
succeed = 0
for i in origins:
    sleep(1)
    if succeed >= lines:
        break
    count += 1
    print(count, limit)
    account = i[1]

    if account == 'redacted':
        continue

    # Look up info about your account
    acct_lines = AccountLines(
        account=account
    )
    try:
        response = client.request(acct_lines)
        result = response.result.get('lines')
        for j in result:
            #print(j)
            if j.get('account') == Issuer:
                if float(j.get('balance')) >= drop:
                    print(random.choice(delays))
                    sleep(random.choice(delays))
                    succeed += 1
                    print(succeed)
                    to_harvest = IssuedCurrencyAmount(currency=Currency, issuer=Issuer, value=str(drop))
                    sell(i[1], i[0])
                    pass
    except:
        pass

sold = (drop/limit)*succeed
print('sold =', sold, lines)
