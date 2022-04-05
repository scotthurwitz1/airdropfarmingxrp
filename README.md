# airdropfarmingxrp
scripts for farming airdrops on the xrp ledger. 

I noticed the opportunity to earn a return on xrp tokens by
creating a "staking" type bundle of scripts that lock xrp tokens into "trustlines" over the 
span of a large number of wallets in exchange for marketing airdrops from token creators. 

To do this, I combined my data science skills with tools from the xrpl-py library to coordinate
and manage actions on the ledger for a cluster of several thousand accounts.

scripts: 

account data export- generating new wallets and exporting their data

harvest xrp- collecting profits from each account to a hub, a similar process was used
to initially populate the accounts with funds for "staking"

trust add- adding trust lines for each account

offer create- executing sell orders on the ledger for each account

There were a few challenges that arose while working on the XRPL. 
These included the need to: continually verify transactions/retry failed transactions, 
process partial payments, and make fee adjustments. In the future I would be interested increasing
the speed of the scripts by running multiple iterations in parallel
on the cloud. 

Any potentially sensitive data has been redacted
