hubs = {redacted}

import xrpl
from retrying import retry
from time import sleep
import pandas as pd
import decimal
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
from xrpl.models.requests import AccountLines
from xrpl.account import get_balance
from xrpl.utils import drops_to_xrp
from xrpl.utils import xrp_to_drops
from xrpl.models.amounts import IssuedCurrencyAmount

##### set the amount you want to keep in each line, needs to be higher than target

######fix filenames before running
filename_in = 'redacted'
df = pd.read_excel(f'redacted', 0)
seeds = df['Seeds'].tolist()

# Define the network client
JSON_RPC_URL = "https://xrplcluster.com/"
client = JsonRpcClient(JSON_RPC_URL)

#set params
hub_address = redacted

##get dest addresses
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


def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None

@retry(retry_on_result=retry_if_result_none)
def pay(originaddress, originwallet):
    account = originaddress
    try:
        # Look up info about your account
        acct_lines = AccountLines(
            account=account)
        response = client.request(acct_lines)
        result = response.result.get('lines')
        num_lines = len(result)

        balance = get_balance(account, client)
        balance_xrp = drops_to_xrp(str(balance))
        avail_bal = balance_xrp - (num_lines * 2) - 10

        diff = avail_bal - decimal.Decimal(4.011)
        print(diff)
        distro = xrpl.utils.xrp_to_drops(diff)
    except:
        pass

    if diff <= 0:
        return True

    # Prepare transaction ----------------------------------------------------------
    my_payment = xrpl.models.transactions.Payment(
        account=originaddress,
        amount=distro,
        destination=hub_address,
    )

    # Sign transaction -------------------------------------------------------------
    signed_tx = xrpl.transaction.safe_sign_and_autofill_transaction(
        my_payment, originwallet, client)
    max_ledger = signed_tx.last_ledger_sequence
    tx_id = signed_tx.get_hash()

    # Submit transaction -----------------------------------------------------------
    try:
        tx_response = xrpl.transaction.send_reliable_submission(signed_tx, client)
        sleep(13)
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        sleep(13)
        print(f"Submit failed: {e}")

    prev = get_transaction_from_hash(tx_id, client).result.get('validated', {})
    if prev == True:
        print('succeed')
        return True
    else:
        print('fail')
        return None

#run
count = 0

for i in origins:
    count += 1
    print(count)
    print(i[1])
    # if count >= 2272:
    #     break

    if i[1] == 'redacted':
        print('pass')
        continue

    # if i[1] in hubs.values():
    #     continue

    account = i[1]
    # Look up info about your account
    try:
        acct_lines = AccountLines(
            account=account)
        response = client.request(acct_lines)
        result = response.result.get('lines')
        num_lines = len(result)

        balance = get_balance(account, client)
        balance_xrp = drops_to_xrp(str(balance))
        avail_bal = balance_xrp - (num_lines * 2) - 10

        diff = avail_bal - decimal.Decimal(4.011)
        print(diff)
    except:
        continue

    if diff > 0:
        pay(i[1], i[0])
        continue
