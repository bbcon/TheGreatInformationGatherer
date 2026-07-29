# Can Data Centres Play Nice With The Grid? | Ep249: Varun Sivaram & Steve Smith

**Guest:** Unknown Guest
**Channel:** Cleaning Up Podcast 
**Date Processed:** 2026-07-19
**Duration:** 3965 seconds
**URL:** https://www.youtube.com/watch?v=4kSrgRZUCwE

**Tags:** #energy-transition #climate #podcast

---

# Can Data Centres Play Nice With The Grid? | Cleaning Up Podcast Summary

## 1. Episode Overview

**Guest Background:**
- **Varun Sivaram**: CEO and founder of Emerald AI, former Chief Strategy Officer at Orsted, and former US diplomat running clean energy diplomacy under Secretary John Kerry
- **Steve Smith**: Group Chief Strategy Officer, UK External Affairs Officer, and President of National Grid Partners (the utility's $600M corporate venture capital arm)

**Main Topic:**
How to make AI data centers grid-friendly assets rather than liabilities through software-enabled flexibility, featuring results from a groundbreaking trial in the UK.

**Key Thesis:**
Data centers represent an unprecedented power demand challenge, but unlike traditional inflexible loads, they can be made **transformatively flexible** through software control—enabling faster grid connections, lower costs, and better grid stability without massive infrastructure buildout.

## 2. Major Themes Discussed

### The Data Center Power Challenge

**The Problem Framing:**
Steve explains that the electricity industry was built on the assumption that **demand was inflexible**. Engineers designed systems to handle massive sudden ramps (like "a million customers putting their kettle on" during football halftime). The solution was expensive infrastructure like pumped storage in Wales.

**Key Insights:**
- A single 1 GW data center represents roughly **1/42nd of UK peak transmission demand**—equivalent to a large city
- In the US, there's demand for **50 GW of data centers by 2028**, but only 25 GW can be connected—leaving "hundreds of billions, if not trillions" of investment stranded
- The bottleneck isn't cost sensitivity—it's **speed to power**. Data centers have relatively inelastic demand and desperately need fast connections

**The Opportunity:**
As Steve notes: "Networks are largely fixed cost businesses. So the more electrons you can throw at them, the lower the unit cost." Data centers could be **massive revenue opportunities** if utilities can connect them without prohibitive infrastructure costs.

### Why Traditional Approaches Fail

**Historical Context:**
Michael shares an anecdote from 5 years ago when an EU country imposed a **moratorium on new data centers** after a hyperscaler demanded millisecond latency and would only build in city centers—an "absurdly over-rigorous requirement."

**The Inflexibility Problem:**
Data centers traditionally demanded:
- Extremely low latency
- Zero risk of disruption  
- Critical customer loads that couldn't be interrupted
- Massive, inflexible power draws

**The Infrastructure Cost:**
Without flexibility, connecting large data centers requires:
- New substations and transformer bays (18-24 month buildout)
- Massive transmission upgrades to handle peak loads
- The system is only stressed **100-200 hours per year**, with average utilization around 30-35%
- Building for these peaks is extraordinarily expensive

### The Emerald AI Solution: Three Types of Flexibility

Varun introduces **three ways to achieve data center flexibility:**

1. **Temporal Flexibility**: Slowing down or pausing certain computations that can wait
2. **Spatial Flexibility**: Moving workloads between data centers (e.g., Virginia to Chicago) in tens of milliseconds
3. **Resource Flexibility**: Traditional approach using batteries or generators

**The Key Innovation:**
Emerald focuses on the first two, treating data centers **not as black boxes** but as software-controllable assets. The company performs a **"dual optimization"**—meeting grid needs while maintaining AI customer satisfaction.

**How It Works:**
- Customers label jobs by priority (0-100 scale)
- High-priority jobs (inference, time-sensitive training) run at 100% performance
- Lower-priority jobs (model fine-tuning for next month, video indexing) can be throttled
- **AI agents** autonomously make real-time decisions to balance grid demands with customer needs

### The Trial Results: Proof of Concept

**Trial Setup:**
- 96 Blackwell Ultra Nvidia GPUs (latest generation)
- 130 kW cluster (equivalent to 400 UK households)
- Dozens of representative production workloads (Meta, OpenAI, Alibaba models)
- **200 different power target events** simulated by National Grid and EPRI

**Four Top-Line Results:**

1. **Lightning Strike Response**: Reduced consumption by **35% in 30 seconds** autonomously (overnight, with team asleep)

2. **Football Match "Kettle Spike"**: Successfully modulated to offset the tea kettle demand spike at halftime and full-time

3. **Renewable Doldrums**: Maintained 10% reduction over 8+ hours during low wind periods—something **batteries couldn't do** (would run out after 4 hours)

4. **Carbon Intensity Following**: Tracked marginal carbon signals, increasing consumption when grid was clean, decreasing when dirty

**Performance Metrics:**
- High-priority tasks ran at **98.8-100% performance** (the 1.2% degradation occurred only when ALL running jobs were high-priority)
- The system "beautifully" followed National Grid's demand profiles in real-time
- Demonstrated response times from **milliseconds to hours**

**The "Chaos Graph":**
Varun describes three visualizations:
- **Grid view**: Clean trace showing perfect compliance with grid requests
- **Customer view**: All jobs performing to their labeled priority levels  
- **Under the hood**: "Utter chaos"—indecipherable complexity that "no human can solve"—only AI agents can optimize in real-time

## 3. Frameworks & Mental Models

### The Electrification Paradox
**Framework**: "The answer to high electricity costs is to use more of it—bigger denominator."

Michael and Steve agree that attracting large loads like data centers actually **reduces unit costs** for all customers by spreading fixed network costs over more consumption.

### The Flexibility Time Spectrum
**Framework**: Think about grid challenges across time horizons:

- **Milliseconds-seconds**: Harmonics, transients, voltage stability, frequency response
- **Seconds-minutes**: System contingencies (lightning strikes, generator trips)
- **Minutes-hours**: Peak demand management, renewable intermittency
- **Hours-days**: Renewable doldrums, seasonal patterns
- **Years-decades**: Infrastructure planning and siting

Different solutions work at different time scales. Emerald focuses primarily on the **seconds-to-hours** domain, though they've demonstrated millisecond-level capabilities in research.

### The "Menagerie of Workloads" Model
**Framework**: Not all AI workloads are created equal. Varun describes a spectrum:

- **Ultra-low latency** (milliseconds): World models, autonomous driving, gaming (40+ frames/second)
- **Low latency** (sub-second): Real-time inference like ChatGPT responses
- **Medium latency** (minutes): Agentic workflows preparing your daily schedule before you wake
- **High latency tolerance** (hours-days): Model pre-training, fine-tuning, video indexing, batch inference

**Application**: By understanding this diversity, you can create **differentiated service levels** and flex the tolerant workloads without impacting user experience.

### Carrots vs. Sticks in Regulation
**Framework**: Steve (drawing on his Ofgem experience) advocates for **incentive-based rather than mandate-based** approaches.

Rather than requiring flexibility through regulation (sticks), offer:
- Faster grid connections
- Lower connection costs  
- Priority access to capacity
- Revenue from grid services

This creates a **de facto standard** where everyone opts in because the benefits are so compelling.

## 4. Contrarian Takes

### Data Centers as Grid Assets, Not Liabilities
**Contrarian view**: The conventional wisdom treats data centers as problematic, inflexible loads that strain infrastructure. 

**Varun and Steve argue**: Data centers are actually **uniquely positioned to be the most flexible loads ever connected** because they're:
- Electronically controllable at software speed
- Large enough to matter (hundreds of MW to GW scale)
- Connected at the speed of light to other data centers globally
- Running diverse workloads with varying latency requirements

This is a **complete inversion** of the traditional problem.

### Speed Matters More Than Price
**Contrarian view**: Countries compete for data centers by offering cheap electricity.

**Michael and guests argue**: Data centers have **relatively inelastic demand** for power. What they desperately need is **speed to connection**. Countries should compete on regulatory efficiency and fast interconnection, not subsidized electricity.

**Evidence**: Despite the UK's relatively high electricity prices, there's enormous interest in building there due to universities, talent, and potential for fast connections.

### The Latency Myth
**Contrarian view**: Data centers require absolute minimal latency and can't tolerate any flexibility.

**Varun challenges this**: While some workloads genuinely need ultra-low latency, the **vast majority don't**. The industry has simply never been forced to differentiate because power was never a constraint. 

**Steve's anecdote**: He recalls Intel during the California energy crisis claiming "there is no economic price" at which they'd curtail chip production. "Turned out there was an economic price. It was pretty high, but they did find a point."

### Software Innovation Can Move Faster Than Hardware
**Contrarian view**: Energy innovation takes decades (Michael's usual position on technologies like perovskite solar).

**Varun's reframe**: By focusing on **software-based solutions**, Emerald went from incorporation to commercial-scale deployment in **16 months**—not the typical 20-year cleantech timeline.

This represents a fundamentally different innovation pathway for the energy transition.

## 5. Practical Implications

### For Data Center Developers
**Immediate actions:**
- Implement workload prioritization systems (0-100 scale)
- Consider locations near existing substations with spare capacity (like Blyth, Northumberland)
- Engage early with utilities on flexibility offerings to **accelerate interconnection queues**
- Budget for flexibility software as a **speed-to-market enabler**, not just a cost

**Strategic shift**: View power flexibility as a **competitive advantage** for faster deployment, not a compromise.

### For Utilities and Grid Operators
**Operational opportunities:**
- Data centers can provide **multiple grid services**: peak shaving, frequency response, renewable integration, carbon optimization
- Average transmission utilization is only 30-35%—there's **massive spare capacity** most of the year
- Flexibility enables connecting loads **without massive infrastructure upgrades**

**Commercial approach:**
- Develop **tiered interconnection products**: faster/cheaper for flexible loads, slower/expensive for inflexible
- Create certification standards for flexibility (working with EPRI, Nvidia)
- Think "carrot-based" incentives rather than mandates

**Cost savings**: National Grid spends "billions of pounds a year" on system balancing—flexible data centers provide a **new, potentially cheaper tool**.

### For Policymakers
**Framework development:**
- Support industry standards for data center flexibility (EPRI DC Flex initiative)
- Avoid blanket moratoria on data centers—instead create **smart incentive structures**
- Recognize that attracting data centers **lowers unit electricity costs** for all consumers
- Compete on **speed and regulatory efficiency**, not just subsidized power prices

**Geopolitical considerations**: Michael raises the Gulf attacks, noting that **stability and security** may become factors in data center location decisions alongside cost and speed.

### For Investors
**Market sizing**: Varun calculates that enabling one 200 MW data center to expand to 230 MW a year early creates **$2 billion in NPV**. With 50 GW of US demand, the total value creation is enormous.

**Business model**: Emerald positions as **"picks and shovels"**—enabling others to capture most of the value while taking a slice of a massive market.

**Risks to monitor**:
- Could hyperscalers (Google, Microsoft) build this capability in-house?
- Will Nvidia's control of GPU protocols create dependency?
- Could new chip architectures (Google TPUs, future competitors) disrupt the approach?
- Regulatory uncertainty around how flexibility is valued

### For Understanding Macro Trends
**The AI power crunch is real**: This isn't hype. There's **2x more demand than can be connected** in the US by 2028.

**Digitization enables demand flexibility**: Michael notes it's "incredibly lucky" that just as supply becomes variable (renewables), digitization enables demand control. **AI puts this on steroids.**

**The "agentic" future**: As AI agents run 24/7 enterprise processes, data center loads could grow even more dramatically than current projections.

**Infrastructure as bottleneck**: The limiting factor for AI deployment may not be chips or algorithms, but **grid capacity and speed of interconnection**.

## 6. Notable Quotes

**On the scale of the challenge:**
> "AI is the biggest new customer, I think, humanity has seen on the power grid... Give it 5 years, give it 10 years, and suddenly the pace of AI's power growth, I think, will be unprecedented." — Varun Sivaram

**On the paradigm shift:**
> "This industry was built on the idea that demand was inflexible... But in this new world, both on the residential side but now on the industrial side, you're realizing, well, actually with software and modern technology, it doesn't have to be like that. Demand could be super flexible." — Steve Smith

**On the business opportunity:**
> "Any sane business when it gets a sudden gold rush of customers coming to say 'I'd like to use a lot more of your product' would say 'Happy days, please do. Where can I sign?' And the problem we were seeing was that although we could see how helpful data centers could be and what great customers they could be, they were presenting these challenges." — Steve Smith

**On the lucky timing:**
> "It's incredibly lucky that just at the time when our supply is becoming variable, intermittent, digitization enables us to control the demand side. Because if that wasn't happening, we'd really be in trouble. And of course, I think AI puts that on steroids." — Michael Liebreich

**On creating value:**
> "There are billions of dollars of value to be created. You take one data center, 200 megawatts, expanded to 230 megawatts a year early, that's $2 billion of net present value... Our goal is to serve as this picks and shovels app that enables others to make lots and lots and lots of money." — Varun Sivaram

---

**Key Takeaway**: The data center power challenge isn't insurmountable—it requires rethinking fundamental assumptions about demand flexibility. By treating data centers as software-controllable assets rather than inflexible black boxes, we can connect them faster, cheaper, and in ways that actually **help** rather than harm grid stability. The trial results prove this isn't theoretical—it works at scale, today.

---

*Summary generated: 2026-07-19 14:55*
*Tokens: 17,346 input, 3,467 output | Cost: $0.10*
