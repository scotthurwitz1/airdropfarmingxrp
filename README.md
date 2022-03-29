# airdropfarmingxrp
scripts for farming airdrops on the xrp ledger. 

I noticed the opportunity to earn a return on xrp tokens by
creating a "staking" type bundle of scripts that lock xrp tokens into "trustlines" over the 
span of a large number of wallets in exchange for marketing airdrops from token creators. 

Here are a selection of examples of my experience using my data science skills and the xrpl-py package to coordinate
and manage actions on the ledger for a cluster of several thousand individual accounts in order to facilitate
the airdrop farming process. 

account data export- generating new wallets and exporting their data

harvest xrp- collecting profits from each account to a hub, a similar process was used
to initially populate the accounts with funds for "staking"

trust add- adding trust lines for each account

offer create- executing sell orders on the ledger for each account

There were a few challenges that arose. For example, the need for verifying
transactions on the ledger after executing them, and fee adjustments as activity on the
ledger expanded, were two emergent behaviors that I dealt with specific to the xrpl's 
style of execution. As a result I have a moderate level of comfort navigating the xrpl-py codebase. 

Any potentially sensitive data has been redacted 
