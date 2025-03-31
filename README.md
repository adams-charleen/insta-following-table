# "Solidarity" Network Analysis

## Methods

### Scraping Instagram: Fetching Basic Metrics

I wrote a Python script `insta_scrape.py` to collect data from 37 hand-curated Instagram accounts by automating a web browser with a tool called Selenium. The script started by setting up a Chrome browser in a way that mimics a real user, either visibly or in the background (headless mode). It logged into Instagram using a provided username and password by navigating to the login page, entering the credentials, and clicking the login button, while also handling popups like "Save Login Info" and "Turn on Notifications" by clicking "Not Now" if they appeared. The script then visited the profile pages of a list of 37 specified Instagram handles, such as "harvardoop" and "jvpboston," to scrape data. For each account, it checked if the profile was private or nonexistent, and if accessible, it extracted the number of posts, followers, and accounts the user was following from the profile's header section. To avoid being blocked by Instagram, the script paused for 3 seconds between each account and restarted the browser every 5 accounts. The collected data was saved into a text file called instagram_results.txt

#### Formatting Basic Metrics Table 

I used the Python script `table.py` to create an HTML table from Instagram profile data stored in a text file named instagram_results.txt. The script read the file, which contained usernames and their associated data (posts, followers, and following counts), parsing each line into a dictionary by splitting the username and data, and converting the data string into a dictionary format. It then generated an HTML file with a styled table, using CSS to format the table with borders, alternating row colors, and hover effects for better readability. For each username, a row was added to the table, displaying the username, number of posts, followers, and accounts followed, with the html.escape function used to safely handle special characters in the data. The final HTML table was saved as instagram_results_table.html.

### Scraping Instagram: Fetching Who the 37 Accounts Follow

The data collection was carried out using the Python script `handles_scrape.py` that accessed Instagram data through direct web requests with the requests library, bypassing the need for a browser. The script first logged into Instagram by sending a login request with a provided username and password, mimicking a real user by including specific headers like a user agent and an Instagram app ID, and obtaining session cookies for authentication. Using these cookies, the script then retrieved the list of accounts followed by each of 37 specified Instagram handles, such as "harvardoop" and "jvpboston." For each handle, it accessed the user’s profile to get their user ID, then fetched their "following" list in batches of 100 accounts at a time, continuing until all followed accounts were collected. To avoid being blocked by Instagram, the script paused for a random duration between 1 to 3 seconds between batch requests and 2 to 4 seconds between different handles. The collected following lists were saved into a text file named instagram_following.txt in a designated folder for further analysis.

#### Formatting the "Follows" Data

I used the Python script `format_insta_following_table.py` to transform the Instagram following data into an HTML table for easy viewing. The script read data from instagram_following.txt, which contained a list of Instagram accounts and the accounts they follow, formatted as account-following pairs. Each line was parsed by splitting the account name and its following list, cleaning the list by removing brackets and quotes, and storing the data in a dictionary. The script then generated an HTML file with a styled table, including CSS to format the table with borders, alternating row colors, hover effects, and a scrollable column for the following lists. For each account, a row was added to the table with the account name in one column and the list of followed accounts in a scrollable div in the second column. The resulting HTML table was saved as instagram_following_table.html for viewing in a web browser, with a title indicating the data was processed on March 30, 2025: https://adams-charleen.github.io/insta-following-table/instagram_following_table.html

##### Note

Discrepancies exist between the “follows” reported in the basic metrics (instagram_results_table.html) and the data pulled for who specifically the  accounts follow (instagram_following_table.html). These inconsistencies are likely due to some accounts being set to private. It is reasonable to hypothesize that a significant number of Harvard students may have made their personal accounts private, while individuals outside the university, particularly in the broader community, may not have. In the subsequent network analysis, personal accounts are likely categorized under “Other.”


### Network Analyses

I performed etwork analyses with the Python script `deeper_network_dive.py` that processed Instagram following data from the file instagram_following.txt to construct a directed network graph, where nodes represent Instagram accounts and edges represent follow relationships. Using the NetworkX library, the script calculated several network metrics: in-degree centrality (to identify the most followed accounts), out-degree centrality (to find accounts following the most others), betweenness centrality (to detect key connectors), closeness centrality (to measure proximity to other accounts), and PageRank (to assess influence). The Louvain method was applied for community detection to identify clusters of accounts, and the largest communities (350–450 accounts) were categorized into University, Regional, Thematic, or Other based on account naming patterns. Visualizations were generated, including a community size distribution, bar plots for in-degree and out-degree centrality, a subgraph of the top 10 most followed accounts, and a circular layout of the network with communities.

## Results

The top 10 most followed accounts (in-degree centrality) included "harvardundergradpsc" (0.0056), "harvardoop" (0.0054), and "palestinianyouthmovement" (0.0054), while "jvpboston" (0.1892) and "hiddenpalestine" (0.1536) had the highest out-degree centrality, indicating they follow the most accounts. "jvpboston" also led in betweenness centrality (0.0010), marking it as a key connector, followed by "harvardoop" (0.0009). For closeness centrality, "harvardundergradpsc" (0.0058) and "palestinianyouthmovement" (0.0057) were the most central, and "harvardundergradpsc" had the highest PageRank (0.00027), indicating strong influence, followed by "harvardoop" (0.00027). 


### Top 10 Most Followed Accounts (In-Degree Centrality)

| Account                        | In-Degree Centrality |
|--------------------------------|----------------------|
| harvardundergradpsc            | 0.005575             |
| harvardoop                      | 0.005383             |
| palestinianyouthmovement        | 0.005383             |
| harvardgs4p                     | 0.004614             |
| lsfpnational                    | 0.004229             |
| bdsboston                       | 0.003845             |
| jvpboston                       | 0.003845             |
| bu_sjp                          | 0.003845             |
| harvj4p                         | 0.003652             |
| harvafro                        | 0.003652             |


### Top 10 Accounts Following the Most (Out-Degree Centrality)

| Account                          | Out-Degree Centrality |
|----------------------------------|-----------------------|
| jvpboston                        | 0.189158              |
| hiddenpalestine                  | 0.153595              |
| nationalsjp                      | 0.131296              |
| healthcareworkersforpalestine    | 0.120915              |
| mitg4p                            | 0.100538              |
| harvardundergradpsc              | 0.094963              |
| m1t_caa                          | 0.091696              |
| pal_legal                        | 0.083622              |
| harvj4p                          | 0.080161              |
| harvardoop                        | 0.071126              |

### Top 10 Key Connectors (Betweenness Centrality)

| Account                        | Betweenness Centrality |
|--------------------------------|------------------------|
| jvpboston                      | 0.000999               |
| harvardoop                      | 0.000878               |
| harvardundergradpsc            | 0.000862               |
| hiddenpalestine                 | 0.000829               |
| harvardgs4p                     | 0.000745               |
| healthcareworkersforpalestine  | 0.000654               |
| nationalsjp                     | 0.000650               |
| pal_legal                       | 0.000472               |
| mitg4p                          | 0.000469               |
| m1t_caa                         | 0.000404               |


### Top 10 Accounts by Closeness Centrality

| Account                        | Closeness Centrality |
|--------------------------------|----------------------|
| harvardundergradpsc            | 0.005794             |
| palestinianyouthmovement        | 0.005721             |
| harvardoop                      | 0.005662             |
| harvardgs4p                     | 0.005190             |
| lsfpnational                    | 0.005061             |
| bu_sjp                          | 0.004873             |
| bdsboston                       | 0.004791             |
| jvpboston                       | 0.004791             |
| harvj4p                         | 0.004701             |
| mondoweiss                      | 0.004699             |


### Top 10 Accounts by PageRank

| Account                        | PageRank  |
|--------------------------------|-----------|
| harvardundergradpsc            | 0.000272  |
| harvardoop                      | 0.000269  |
| harvardgs4p                     | 0.000259  |
| palestinianyouthmovement        | 0.000248  |
| harvj4p                         | 0.000247  |
| lsfpnational                    | 0.000231  |
| harvafro                        | 0.000224  |
| right2edu                       | 0.000223  |
| bostonpsl                       | 0.000220  |
| nouraerakat                     | 0.000218  |


Community detection identified 16 communities, with sizes ranging from 152 to 622 accounts. The largest communities (350–450 accounts) were analyzed for composition: Community 4 (432 accounts) had 7 University, 7 Regional, 218 Thematic, and 200 Other accounts; Community 11 (413 accounts) had 10 University, 9 Regional, 55 Thematic, and 339 Other accounts; Community 6 (399 accounts) had 13 University, 25 Regional, 35 Thematic, and 326 Other accounts; Community 12 (391 accounts) had 9 University, 8 Regional, 94 Thematic, and 280 Other accounts; and Community 13 (357 accounts) had 22 University, 2 Regional, 111 Thematic, and 222 Other accounts.


### Community Sizes

| Community ID | Size |
|--------------|------|
| 2            | 622  |
| 15           | 578  |
| 5            | 456  |
| 4            | 432  |
| 11           | 413  |
| 6            | 399  |
| 12           | 391  |
| 13           | 357  |
| 7            | 241  |
| 8            | 230  |
| 3            | 227  |
| 14           | 194  |
| 1            | 187  |
| 9            | 164  |
| 0            | 160  |
| 10           | 152  |

### Composition of Largest Communities

| Community ID | Size | University | Regional | Thematic | Other |
|--------------|------|------------|----------|----------|-------|
| 4            | 432  | 7          | 7        | 218      | 200   |
| 11           | 413  | 10         | 9        | 55       | 339   |
| 6            | 399  | 13         | 25       | 35       | 326   |
| 12           | 391  | 9          | 8        | 94       | 280   |
| 13           | 357  | 22         | 2        | 111      | 222   |


Please go here for an interactive network plot of nodes and edges: https://adams-charleen.github.io/insta-following-table/interactive_network.html

## Conclusions and Interpretations 

The Instagram following network highlights a structure where accounts like "harvardundergradpsc" and "harvardoop" are highly influential, as they are the most followed, have high influence (PageRank), and are well-connected (closeness centrality), likely acting as central hubs within the network. "jvpboston" stands out as a key connector (high betweenness centrality) and is highly active in following others (out-degree centrality), suggesting it bridges different parts of the network. The community analysis shows 16 distinct clusters, with the largest communities (350–450 accounts) predominantly consisting of "Other" accounts (200–339), followed by "Thematic" accounts (35–218), indicating a diverse network with a strong presence of accounts focused on specific themes, such as activism (e.g., Palestine-related, given names like "palestinianyouthmovement" and "bdsboston"). University and Regional accounts are less dominant in these large communities, suggesting that while university-affiliated accounts (e.g., Harvard-related) are influential, the broader network is driven by thematic and diverse affiliations, likely centered around shared social or activist causes. The community size distribution further indicates a skewed structure, with a few large communities and many smaller ones, reflecting a network where certain clusters have significant reach while others are more niche.

