# CryptoAgent
AI-Powered solution to identify which altcoin might pump in between 5%-10%
🪙 𝗣𝗿𝗼𝗷𝗲𝗰𝘁 𝗗𝗲𝗳𝗶𝗻𝗶𝘁𝗶𝗼𝗻
An autonomous crypto research agent built with Python + LLM tooling.

💻 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝘂𝗿𝗲
The software scrapes 6 different data points, mainly from Binance and Coinbase, for around 20 cryptocurrencies.

You can see how the scraping pipeline works in the “Data Execution” folder in the GitHub repository.

After collecting and organizing a large amount of data, the system sends the outputs to 6 different AI agents, each performing its own analysis.
I designed these agents based on OpenAI API logic with a strict JSON input/output workflow. Therefore, if you want to integrate other LLM APIs, you may need to modify some agent structures depending on the outputs you receive. These agents can be found in the “Agents” folder.

In the “Master” folder, you can find Main py which orchestrates both the AI agents and the data scraping flow.

I also developed a very ugly — but surprisingly useful — interface to run the software, which is also located in the “Master” folder 🙂

💾 𝗢𝘂𝘁𝗽𝘂𝘁
The software attempts to predict which coin(s) might pump by approximately 5–10% within:
1 day
3 days
7 days
It also provides a short reasoning analysis to justify each prediction.

🔴 𝗜𝗺𝗽𝗿𝗼𝘃𝗲𝗺𝗲𝗻𝘁 𝗣𝗼𝗶𝗻𝘁𝘀
1) Data scraping reliability
 Scraping can occasionally become unstable because some endpoints may identify the software as a bot and limit data transfer.
The scraping logic could likely be improved through:
- better API optimization
- smarter request scheduling
- reduced overload during data collection

2) AI agent stability
Depending on the clustered data volume, some AI agents may malfunction or produce inconsistent outputs. I believe certain agents become unstable when the context/data becomes too large.

3) Limited cryptocurrency coverage
Currently, the system only tracks around 20 cryptocurrencies in order to:
- reduce data overload
- minimize token/API costs

With better optimization, the structure could likely scale to support many more assets.

Hope you enjoy reviewing something coded in a very amateur — but highly experimental — way.
