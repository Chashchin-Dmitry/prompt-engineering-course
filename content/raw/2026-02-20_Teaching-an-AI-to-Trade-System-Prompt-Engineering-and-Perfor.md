# Teaching an AI to Trade: System Prompt Engineering and Performance Monitoring

**Source:** https://medium.com/@kojott/teaching-an-ai-to-trade-system-prompt-engineering-and-performance-monitoring-9d55258cca06
**Author:** 
**Published:** None
**Scraped:** 2026-02-20

---

Teaching an AI to Trade: System Prompt Engineering and Performance Monitoring
Jiri George Dolejs
10 min read
·
Oct 27, 2025

Press enter or click to view image in full size
my dashboard from the bot paper trading
The Inspiration: Alpha Arena

In late 2025, nof1.ai launched Alpha Arena — the first benchmark designed to measure AI’s investing abilities in real markets. They gave six leading AI models $10,000 each of real capital, identical prompts, and set them loose on crypto perpetuals. The goal? Test whether LLMs could generate alpha, manage risk, and handle the adversarial, unpredictable nature of markets.

It was a brilliant concept: markets as the ultimate intelligence test. Static benchmarks can’t capture the chaos of real trading — order book dynamics, slippage, fees, psychological pressure of live capital. Alpha Arena confronted AI models with all of it.

The competition is still running (scheduled through November 2025), and the results are fascinating to watch in real-time. As of this writing, the leaderboard shows real performance differences between models — proof that prompt engineering and reasoning capabilities matter when trading real capital.

Watching Alpha Arena, I wanted to take the concept further. While their benchmark is groundbreaking, the system isn’t fully open-source, and the test duration is time-limited. I saw an opportunity to build something different: a completely transparent, open-source, community-driven version that anyone could run indefinitely, modify, and learn from.

Building an Open-Source AI Trading System

Building a trading bot powered by a large language model isn’t just about connecting APIs and letting the AI loose on markets. Without proper constraints and monitoring, an LLM will happily burn through capital while generating confident-sounding justifications for every bad trade.

In this post, I’ll break down the system prompt architecture that keeps my AI trading bot disciplined, explain the risk management framework that governs every decision, and show you how I monitor performance to ensure the bot is actually following the rules.

The goal isn’t just to replicate what Alpha Arena tested — it’s to create a platform where developers can experiment with prompt engineering, risk management strategies, and different AI approaches in a real market environment, all while learning from actual code and results.

The Core Problem: LLMs Don’t Understand Risk

Large language models are trained to generate plausible text based on patterns in their training data. Ask an LLM to analyze a Bitcoin chart, and it’ll give you a detailed technical analysis with entry points, targets, and reasoning that sounds completely legitimate. Ask it to manage a trading portfolio, and it’ll confidently open leveraged positions on everything that’s moving.

The problem? LLMs have no inherent concept of financial risk.

They don’t feel the pain of losing money. They don’t understand that a 50% drawdown requires a 100% gain to recover. They can’t intuitively grasp that protecting capital matters more than chasing returns. Without explicit constraints, an LLM trading bot optimizes for interesting-sounding trades rather than sustainable profitability.

This is why the system prompt isn’t just important — it’s everything.

Building a Risk-First System Prompt

The system prompt is the foundational instruction that shapes every decision the AI makes. It’s sent with every request, establishing the rules and philosophy that govern trading behavior. Here’s how I structured it:

1. Capital Preservation as the Foundation

“You are a top level crypto trader focused on multiplying the account while safeguarding capital.”

Notice the order: multiply while safeguarding. Not “safeguard while trying to multiply.” This subtle difference establishes priority. The bot needs to prioritize survival first. You can’t grow an account that’s blown up.

Key Insight: In trading, staying in the game is more important than winning any single trade. A bot that loses 2% twenty times can recover. A bot that loses 40% once might never come back.

2. The 1–2% Rule: Mathematical Position Sizing

“Never risk more than 1–2% of total capital on a single trade.”

This isn’t a suggestion — it’s the core risk management constraint. Here’s the math:

Risk 10% per trade → Six losses in a row = 46% drawdown → Need 85% gain to recover
Risk 2% per trade → Six losses in a row = 11.5% drawdown → Need 13% gain to recover

The bot calculates position size algorithmically based on the distance to the stop-loss. If entering BTC at $67,000 with a stop at $66,000 (1% account risk on a $10,000 account), the math is:

Risk per coin: $1,000 ($67k — $66k)
Maximum loss allowed: $100 (1% of $10,000)
Position size: 0.1 BTC ($100 ÷ $1,000)

This removes discretion entirely. The bot can’t “feel confident” and size up — the math is immutable.

3. Mandatory Stop-Loss Orders

“Stop-loss orders are mandatory safeguards against emotional decisions.”

Every position includes a stop-loss price determined before entry. In live trading on Hyperliquid, these attach as reduce-only triggers that execute automatically. In paper trading mode, the bot checks stop conditions every iteration.

LLMs don’t have emotions, but they do rationalize holding losing positions. “The setup is still valid,” “it’s just a temporary pullback,” “the trend is intact on higher timeframes.” Sound familiar? The stop-loss removes this rationalization cycle. The price either hits the stop or it doesn’t — no debate, no hope, no averaging down.

4. Trend-Following Only

“Buy rising coins and sell falling ones; the market is always right.”

This constraint prevents the bot from trying to catch falling knives or fade strong trends. Counter-trend trading requires market intuition that LLMs simply don’t possess. By restricting the bot to trend-following setups, we play to its strengths: pattern recognition in indicator data across multiple timeframes.

The bot receives market data including:

3-minute candles for short-term momentum
4-hour candles for longer-term context
EMA relationships, RSI levels, MACD crossovers
Volume patterns and funding rates

When everything aligns in one direction, that’s a signal worth considering.

5. Stay Inactive Most of the Time

“Trade only when high-probability setups emerge. Avoid overtrading.”

This might be the hardest rule for both humans and AI. There’s a psychological pull to “do something” when watching markets. Prices are moving, opportunities seem to appear constantly, and inaction feels like missing out.

The reality? Most market movement is noise. High-probability setups — where indicators align, risk/reward is favorable, and the edge is legitimate — are rare. Trading every signal slowly bleeds accounts through fees and small losses.

The bot can output “hold” for every asset if nothing looks compelling. That’s not failure — that’s discipline.

6. Cut Losses Quickly, Let Profits Run

“Close losing trades decisively; exit weak performers without hesitation. Let winning trades develop when they show early profit.”

Stop-losses handle the first part automatically. The second part is where strategy design matters. The bot sets profit targets, but I’m experimenting with how aggressively to take profits versus trailing stops to capture larger moves.

This is an area where live trading data will inform optimization. The system prompt provides the philosophy; actual execution parameters evolve with empirical results.

7. Leverage Control with Risk Caps

“Use leverage responsibly; ensure even worst-case loss stays within the 1–2% risk cap.”

Leverage multiplies both gains and losses. The bot can use up to 10x leverage, but position sizing ensures that if the stop-loss triggers, the loss stays within tolerance.

Example with 10x leverage:

$10,000 account, 1% risk = $100 max loss
Entry: BTC at $50,000, Stop: $49,000
Position: 0.1 BTC ($5,000 notional, $500 margin at 10x)
Loss if stopped: $1,000 move × 0.1 BTC = $100 (exactly 1%)

Without this constraint, leverage becomes a death trap. With it, leverage is a tool for capital efficiency while maintaining strict risk limits.

8. Probabilistic Thinking

“Treat trading like a probability game with positive expectancy over many trades. Shift from needing to be right to managing outcomes.”

This mental model separates professionals from gamblers. You don’t need to win every trade — you need a system where wins outweigh losses over time.

45% win rate with 2:1 reward/risk ratio = profitable
60% win rate with 1:1 reward/risk ratio = profitable
80% win rate with 0.5:1 reward/risk ratio = unprofitable

The system prompt emphasizes this because LLMs naturally want to be “right” — they’re trained to generate accurate predictions. Trading isn’t about being right; it’s about making money.

Why These Rules Matter for AI Trading

Human traders can rely on intuition, gut feelings, and years of pattern recognition. LLMs don’t have intuition — they have statistical associations from training data. The system prompt compensates by encoding decades of trading wisdom into explicit constraints.

Get Jiri George Dolejs’s stories in your inbox

Join Medium for free to get updates from this writer.

Without these rules, the AI would:

Open 10 positions simultaneously because “they all look interesting”
Risk 20% on a “high-confidence” setup
Hold losing positions because “the fundamentals are strong”
Chase pumps and try to catch falling knives
Overtrade to “stay active”

With these rules, the bot behaves like a disciplined trader who’s read the classic books, blown up an account, learned the lessons, and now follows a proven process — just at machine speed without emotional attachment.

Monitoring: The Dashboard Architecture

A trading bot without proper visibility is a black box burning through capital. My Streamlit dashboard shows three categories of information that answer the critical questions:

Press enter or click to view image in full size
full trade history

Is it making money?

Available balance (uninvested cash)
Total equity (balance + position value)
Total return percentage
Realized vs unrealized PnL

Is it taking appropriate risk?

Margin allocated to leveraged positions
Maximum theoretical loss if all stops trigger
Portfolio heat (percentage of capital at risk)

Is the edge real?

Sharpe ratio (return per unit of total volatility)
Sortino ratio (return per unit of downside volatility)
Win rate and average profit per trade
Comparison to BTC buy-and-hold benchmark
Why Sortino Matters More Than Sharpe

The Sharpe ratio treats all volatility as risk. Big wins and big losses both penalize the score. But in trading, upside volatility isn’t a problem — that’s called “making money.”

The Sortino ratio only penalizes downside volatility. It answers the question: “Am I being compensated for the actual risk I’m taking (losing money), or just for price movement in general?”

For a trading bot, Sortino is more meaningful. If the equity curve goes up sharply, Sharpe ratio drops because of high volatility. Sortino doesn’t care — rapid gains aren’t risk.

The BTC Benchmark: Does Complexity Add Value?

The dashboard plots the bot’s equity curve against BTC buy-and-hold performance using the same starting capital and timeframe. This answers the most important question: Would I be better off just buying Bitcoin and doing nothing?

If the bot can’t outperform this simple benchmark over time, all the complexity is just adding fees and stress for no benefit. It’s a reality check that keeps you honest about whether active management provides value.

Press enter or click to view image in full size
all messaging visible
The Feedback Loop

This creates a complete system:

System prompt defines constraints
Bot enforces constraints algorithmically
Dashboard makes outcomes visible
Analysis reveals what’s working
Refinements improve the system
Repeat

Without visibility (step 3), the feedback loop breaks. You’re trusting that the LLM is behaving responsibly when it might be doing anything.

What Success Looks Like

The goal isn’t to beat the market every day. It’s to build a system that:

Survives long enough to learn from real market execution
Provides transparent visibility into every decision
Enforces risk management that protects capital
Generates positive expectancy over many trades
Improves through data-driven iteration

Paper trading looked promising. Now the bot is transitioning to live execution with minimal capital to validate these concepts against real market conditions, real slippage, real fees, and the psychological pressure of actual money on the line.

Transparency as Philosophy

Notice how much this post exposes about the system’s internals. This is intentional. A trading bot that hides its logic is untrustworthy by default. You should be able to answer fundamental questions about any automated system:

What rules govern its behavior?
How does it manage risk?
What does success look like?
How do you know it’s working?
What happens when it fails?

If you can’t answer these clearly, the system isn’t production-ready.

Why Open Source?

Alpha Arena demonstrated that AI can trade in real markets — but the real learning happens when you can see how it’s done. That’s why this project is completely open-source and community-driven:

Transparency: Every line of code, every prompt, every risk management rule is visible and documented.

Education: Learn by examining actual trading bot architecture, not just reading about theory.

Experimentation: Clone the repo, modify the system prompt, test different strategies, and share your results.

Community-Driven: The roadmap evolves based on what the community wants to see. Multi-LLM comparison? Advanced backtesting? Portfolio-level risk management? These features develop as the community supports them.

Learn More & Follow Along

Explore the Code: The complete implementation is available on GitHub at github.com/kojott/LLM-trader-test. Clone it, run it locally, modify the prompts, experiment with different strategies. Everything is documented.

Watch Live Performance: A real-time dashboard runs at llmtest.coininspector.pro showing the bot’s current equity curve, open positions, and trade history. See how the system performs in real markets soon with real capital.

Support Development: This project evolves through community sponsorship. If you want to see specific features developed, consider supporting on Patreon. The roadmap includes 10 tiers of capabilities (smart position sizing, emergency controls, strategy voting systems, Monte Carlo backtesting, etc.) that unlock as funding goals are reached. Supporters get early access, weekly updates, and input on priorities.

Questions or Feedback?

GitHub: github.com/kojott/LLM-trader-test
Twitter: @kojott
Telegram: @kojottchorche
Patreon: patreon.com/cw/llmtrader

⚠️ Disclaimer: This bot is experimental and educational. Trading involves substantial risk. Past performance does not indicate future results. The system prompt provides constraints but cannot eliminate trading risk. Never trade with money you can’t afford to lose. The bot is currently tested with minimal capital for precisely this reason. Do your own research and consult a financial advisor before trading.

---
*Auto-collected for Prompt Engineering Course*
