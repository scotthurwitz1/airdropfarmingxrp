#creates txt document with seeds

import xrpl
import pandas as pd
from xrpl.wallet import Wallet
seeds = []
addresses = []
num = 2650
filename = 'redacted'

for i in range(num):
    a = xrpl.core.keypairs.generate_seed()
    seeds.append(a)

for i in seeds:
    address = Wallet(seed=i, sequence=12).classic_address
    addresses.append(address)

df = pd.DataFrame()
df['Seeds']=seeds
df['Addresses']=addresses
print(df)

df.to_excel(f'redacted', index = False)


