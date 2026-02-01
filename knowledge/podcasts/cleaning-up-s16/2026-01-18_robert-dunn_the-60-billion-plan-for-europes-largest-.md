# The $60 Billion Plan For Europe’s Largest AI Data Centre | Ep235: Robert Dunn

**Guest:** Robert Dunn
**Channel:** Cleaning Up Podcast 
**Date Processed:** 2026-01-18
**Duration:** 3746 seconds
**URL:** https://www.youtube.com/watch?v=juAyLAUmU3w

**Tags:** #energy-transition #climate #podcast

---

# The $60 Billion Plan For Europe's Largest AI Data Centre

## 1. Episode Overview

**Guest:** Robert Dunn, CEO of Start Campus

**Background:** Rob has 20+ years of experience building data centers across Europe, previously spending a decade at Digital Realty developing facilities in major cloud markets (Frankfurt, London, Amsterdam, Paris, Dublin). He joined Start Campus in early 2022, moving to Portugal to lead what will become Europe's largest data center project.

**Main Topic:** The development of a massive 1.2 gigawatt data center campus in Sines, Portugal, on the site of a former coal-fired power station. The project represents a fundamental shift in data center strategy—moving from small urban facilities to enormous "green giants" in industrial locations with abundant renewable power.

**Key Thesis:** The future of European data centers lies not in traditional city locations but in massive, purpose-built facilities outside urban areas that can leverage renewable energy, innovative cooling solutions, and existing industrial infrastructure. This €60 billion project (€10B in infrastructure, €40-50B in customer IT equipment) exemplifies this transformation, accelerated by AI's explosive computational demands.

**Context:** Host Michael Liebreich was involved in this project's genesis, co-authoring the "Green Giants" white paper in 2021 (before ChatGPT) that advocated for exactly this model. The episode was recorded on-site in Portugal in October, with Microsoft subsequently announcing a $10 billion investment in the facility.

## 2. Major Themes Discussed

### The Scale and Economics of Hyperscale Data Centers

**The Question:** What does it actually take to build a facility of this magnitude, and what are the economics?

**Rob's Perspective:** The project operates on a staggering scale that was almost unimaginable even a few years ago. The first operational building (29 megawatts) represents just 2.5% of the eventual 1.2 gigawatt campus. 

**Key Insights:**
- **Cost metrics:** The industry standard is approximately €10 million per megawatt for physical infrastructure. At scale, Start Campus expects to achieve slightly better efficiency, targeting around €10 billion for the complete 1.2GW infrastructure.
- **Customer investment multiplier:** The IT equipment (GPUs, CPUs, servers) that customers install typically costs **four times** the infrastructure investment—adding €40 billion in equipment to the €10 billion facility cost.
- **Total envelope:** This creates a **€50-60 billion total investment** when fully built out.
- **Timeline:** From groundbreaking in early 2022 to full completion by 2030—an 8-year development cycle with staggered building phases every 6-9 months.

**Supporting Evidence:** Rob notes that individual racks now consume 60-130 kilowatts (equivalent to 60-130 one-bar electric heaters in a single rack), with next-generation equipment expected to reach 1-2 megawatts per rack. This exponential growth in power density drives the need for massive facilities.

### The Transformation of Data Center Location Strategy

**The Question:** Why build enormous data centers outside cities when conventional wisdom said they needed to be urban for latency reasons?

**Rob's Perspective:** The "FLAPD" markets (Frankfurt, London, Amsterdam, Paris, Dublin) dominated European data center development, with facilities typically ranging from 40-100 megawatts. The Green Giants thesis challenged this orthodoxy before the AI boom made it obvious.

**Key Mechanisms:**
- **Power availability:** Urban grids cannot support gigawatt-scale facilities. Industrial sites with existing transmission infrastructure can.
- **Cooling efficiency:** Access to seawater or other natural cooling resources dramatically reduces operational costs and environmental impact.
- **Renewable integration:** Large-scale renewable energy projects (solar, wind, hydro) can be co-located or directly connected more easily outside urban areas.
- **Cost structure:** Lower land costs, power costs, and cooling costs create a **20-30% reduction in total power expenses** compared to traditional facilities.

**The Sines Advantage:** The former coal power station site provided:
- Existing 400kV grid connection (previously serving a 3GW coal plant)
- Permitted seawater cooling infrastructure already in place
- Industrial zoning and community acceptance
- 64 hectares of available land

**Contrarian Element:** When the Green Giants paper launched at COP26 in November 2021, "people thought that data centers needed to be in cities because of latency." The AI training workload revolution proved this assumption wrong—these workloads can tolerate higher latency in exchange for massive scale and lower costs.

### Innovative Cooling Technology and Efficiency

**The Question:** How do you keep facilities generating this much heat operational and efficient?

**Rob's Perspective:** Cooling represents one of the largest operational expenses and environmental impacts. Start Campus is pioneering **seawater cooling** as the primary system, with traditional air cooling only as backup.

**Key Metrics:**
- **PUE (Power Usage Effectiveness):** Seawater cooling achieves approximately **1.1 PUE** versus **1.3 PUE** for traditional chiller/cooling tower systems
- **Translation:** For every megawatt of IT load, seawater cooling uses only 100kW for cooling versus 300kW for traditional systems
- **Efficiency gain:** This represents **3-4x better efficiency** and roughly **20% reduction in total power costs**

**Technical Implementation:**
- Seawater passes through **titanium-plated heat exchangers** (titanium prevents corrosion)
- Process cooling water is chilled without direct contact with seawater
- The system leverages infrastructure originally built for the 3GW coal plant
- Future buildings will use shared heat exchanger infrastructure for the entire campus

**Future-Proofing Challenge:** As rack densities increase from 60-130kW to potentially 1-2 megawatts, **air cooling becomes insufficient**. The industry is transitioning to:
- **Liquid-to-chip cooling:** Water delivered directly to the back of racks
- **Higher operating temperatures:** Moving from 24-26°C to 27-32°C range (chips are being designed to handle this)
- **DC power delivery:** Future racks may use medium-voltage DC instead of 400V AC for efficiency

### The Business Model and Customer Dynamics

**The Question:** How does the business model work, and what are customers actually looking for?

**Rob's Perspective:** The data center operator (Start Campus) builds and operates the physical infrastructure, while customers (hyperscalers, neo-clouds) install and own their IT equipment. Revenue comes from long-term lease agreements.

**Customer Priorities (100-point allocation):**
- **Speed to market: ~50 points** - "Time to market is so important in this AI race at the moment"
- **Cost: ~25 points** - Total cost of ownership including rent, power, and cooling
- **Future-proofing: ~25 points** - Ability to support next-generation equipment

**Lease Structure Evolution:**
- **Traditional model:** 5-7 year leases for space in multi-tenant facilities
- **New hyperscale model:** 10+ year leases required when building dedicated facilities costing €1.5-2 billion
- **Financing requirement:** Cannot raise the necessary debt without long-term, creditworthy anchor tenants

**Customer Categories:**
1. **Hyperscalers:** Amazon, Google, Meta, Microsoft, Apple, Oracle, OpenAI—companies with strong balance sheets
2. **Neo-clouds:** Newer players like CoreWeave who need equity backing or three-party agreements
3. **Sovereign wealth funds:** Emerging as potential balance sheet providers

**The Spider-Man Meme Problem:** Rob acknowledges the circular dependency—everyone wants to use someone else's balance sheet rather than their own equity. The question of "who's actually standing behind this for long enough" remains fascinating and somewhat unresolved.

### Grid Integration and Community Relations

**The Question:** How do you ensure a gigawatt-scale facility plays nicely with the local grid and community?

**Rob's Perspective:** Transparency and genuine additionality are essential. Start Campus aims to be a net benefit, not a burden.

**Grid Strategy:**
- **100% renewable commitment:** All power will be from renewable sources
- **Additionality principle:** For every gigawatt of consumption, supplement the grid through new renewable projects via PPAs (Power Purchase Agreements) or direct wire connections
- **Flexibility:** Maintaining options for both purchasing from grid-connected renewables and developing private-wire solar/wind projects
- **TSO coordination:** Working closely with the transmission system operator to ensure adequate generation and transmission capacity

**Backup Power:**
- **24 hours of on-site fuel storage** using HVO (Hydrogenated Vegetable Oil—plant-based diesel alternative)
- **1.2GW of backup generators** (eventually), but working with customers to reduce this by identifying truly critical vs. non-critical loads
- **Resilience advantage:** During the April 28 Iberian blackout, being on HVO meant fuel was available when hospitals were scrambling for diesel

**Community Benefits:**
- **Job creation:** Peak construction will employ 3,000-4,000 people; operations will provide long-term skilled employment
- **Returning diaspora:** Portuguese engineers who left to build data centers globally are returning home
- **Housing development:** Private and public initiatives to build accommodation (visible construction cranes in Sines)
- **Industrial revitalization:** Transitioning from coal to AI, alongside other green industries like battery manufacturing
- **Skills development:** Partnering with local schools and universities to train workers

**Local Acceptance:** The site is in an established industrial zone, making the transition from coal power to data centers more natural than placing such a facility in a residential area.

## 3. Frameworks & Mental Models

### The "Green Giants" Framework

**Core Concept:** Future data centers should be characterized by:
1. **Massive scale** (gigawatt-class rather than tens of megawatts)
2. **Out-of-town locations** with industrial infrastructure
3. **Renewable energy integration** as a primary design principle
4. **Innovative cooling** leveraging natural resources
5. **Repurposing existing assets** (transmission lines, cooling infrastructure, industrial sites)

**Application:** When evaluating data center projects, assess:
- Can the location support gigawatt-scale power delivery?
- What renewable resources are available or can be developed?
- What existing infrastructure can be repurposed?
- What natural cooling resources exist?
- Is the community/regulatory environment supportive of industrial development?

### The Power Density Evolution Model

**Framework:** Understanding data center economics requires tracking power density trends:
- **2005:** 24MW was "the biggest in Europe"
- **2015-2020:** 40-100MW became standard for cloud markets
- **2020-2025:** Gigawatt-scale facilities emerging
- **Rack level:** 2-3 tons → 60-130kW → 1-2MW (projected)

**Implication:** Infrastructure must be designed with **flexibility for 3-5x density increases** over facility lifetime. This means:
- Structural capacity for heavier equipment
- Electrical infrastructure that can be reconfigured
- Cooling systems that can scale
- Space allocation that anticipates equipment shrinking but support infrastructure expanding

### The PUE (Power Usage Effectiveness) Metric

**Definition:** PUE = Total Facility Power / IT Equipment Power

**Interpretation:**
- **1.1 PUE:** Only 10% overhead (100kW cooling per 1MW IT load)—excellent
- **1.3 PUE:** 30% overhead (300kW cooling per 1MW IT load)—traditional
- **Lower is better:** Directly translates to operational cost savings

**Application:** When comparing data center efficiency:
- Seawater cooling: ~1.1 PUE
- Modern air cooling: ~1.3 PUE
- Older facilities: 1.5-2.0 PUE

A 0.2 PUE improvement (1.3 to 1.1) represents approximately **20% reduction in power costs**—massive at gigawatt scale over decades.

### The N+1 Redundancy Principle

**Concept:** For any critical system, ensure that one component can fail (or be under maintenance) while maintaining 100% capacity.

**Application Examples:**
- Dual cooling systems (seawater + air chillers initially)
- Multiple UPS (Uninterruptible Power Supply) blocks
- Generator arrays where one can be offline
- Multiple transformers and electrical paths

**Economic Trade-off:** N+2 (two components can fail) provides more resilience but costs significantly more. The calculation depends on:
- Number of redundant units (more units may justify N+2)
- Criticality of the load
- Customer SLA requirements (typically 99.999% uptime—"five nines")

## 4. Contrarian Takes

### Speed Over Perfection (Sometimes)

**Contrarian View:** While Rob emphasizes building "the right way" with future-proofing, he acknowledges that **Meta's approach of "throwing up tents"** to deploy GPUs in months has validity.

**Reasoning:** In the current AI race, having compute capacity operational in 6-12 months may be more valuable than having a perfectly engineered 20-year facility in 24 months. The opportunity cost of delayed deployment can exceed the cost of suboptimal infrastructure.

**Rob's Nuance:** "There's space for both of us in the industry." Different customers have different priorities, and the market can support both rapid deployment and long-term sustainable infrastructure.

**Implication:** The **$15 billion valuation of Fermy** (Rick Perry's company) for data centers that are "less real" than Start Campus reflects market appetite for speed. Rob views this with "bemusement" but acknowledges the demand is real.

### The AI Bubble Question

**Contrarian Framing:** Rob carefully navigates the question of whether we're in an AI bubble, noting "there's clearly elements of both" boom and bubble.

**His Position:** Even if AI demand moderates:
- **Cloud computing continues growing** regardless of AI hype
- **Large-scale data centers remain necessary** for efficiency reasons
- **The Green Giants thesis predates AI** and remains valid for traditional workloads
- **This facility will adapt:** "This place will end up running as a combination—AI training, AI inference, other cloud products"

**Risk Mitigation:** Future-proofing isn't just about next-generation AI chips—it's about ensuring the facility remains economically viable across multiple technology cycles and use cases.

### Generators May Not Be Needed

**Contrarian Take:** Despite planning for 1.2GW of backup generators, Rob suggests **"we would like not to have to install all the generators."**

**Reasoning:** 
- Not all AI workloads require 100% uptime—training jobs can be interrupted and restarted
- Customers are increasingly willing to **designate critical vs. non-critical loads**
- **Battery storage** may become economically viable for backup power as costs decline
- Generators represent significant capex and environmental permitting challenges

**Current Reality:** The 24-hour HVO fuel storage provides resilience, but the goal is to minimize generator dependency through load management and alternative backup strategies.

### European Data Center Wave Still Coming

**Contrarian View:** Despite the hype and numerous announcements, Rob argues **"I don't even think we've seen the big wave in Europe yet. I think it's coming."**

**Reasoning:**
- Most AI infrastructure investment has focused on the US
- European data sovereignty concerns will drive local capacity
- Renewable energy abundance in Europe (Iberian solar/wind, Nordic hydro) creates competitive advantage
- Regulatory environment increasingly favors sustainable infrastructure

**Implication:** Current valuations and project announcements may not be bubble peaks but rather early indicators of sustained growth.

## 5. Practical Implications

### For Data Center Development

**Key Takeaways:**
1. **Location selection should prioritize:**
   - Existing transmission infrastructure (ideally 400kV connections)
   - Access to natural cooling resources (seawater, ambient air in cold climates)
   - Renewable energy availability or development potential
   - Industrial zoning and community acceptance
   - Available land for gigawatt-scale expansion

2. **Design for flexibility:**
   - Structural capacity for 3-5x current rack weights
   - Electrical infrastructure that can be reconfigured as power density increases
   - Space allocation anticipating equipment miniaturization but support infrastructure expansion
   - Cooling systems that can transition from air to liquid-to-chip

3. **Timeline expectations:**
   - 2-3 years of planning, permitting, and design before groundbreaking
   - 18-24 months construction for first building
   - 6-9 month staggered starts for subsequent buildings
   - 8-10 years total for gigawatt-scale campus buildout

4. **Cost benchmarks:**
   - €10 million per megawatt for infrastructure (target: slightly below at scale)
   - Customer IT equipment: 4x infrastructure cost
   - Total investment: €50-60 billion for 1.2GW facility

### For Investors and Financial Analysis

**Investment Considerations:**

1. **Revenue model requires long-term commitments:**
   - 10+ year leases necessary to finance new construction
   - Creditworthy anchor tenants essential
   - Balance sheet strength matters more than ever

2. **Operational efficiency drives returns:**
   - 20% power cost reduction from seawater cooling compounds over decades
   - PUE improvements directly impact competitiveness
   - Location advantages (renewable power costs, cooling efficiency) create sustainable moats

3. **Valuation framework questions:**
   - How much premium for speed vs. sustainability?
   - What discount rate for projects with 8-year buildouts?
   - How to value optionality and future-proofing?
   - The Fermy $15B valuation suggests market values concepts highly—but execution risk is real

4. **Risk factors:**
   - AI demand sustainability (though cloud growth provides downside protection)
   - Technology evolution (liquid cooling, DC power, quantum computing)
   - Regulatory changes (environmental, energy, data sovereignty)
   - Grid capacity and renewable energy availability
   - Customer concentration and balance sheet strength

### For Understanding Macro Trends

**Energy Transition Implications:**

1. **Data centers as renewable energy drivers:**
   - Gigawatt-scale facilities provide **anchor demand for new renewable projects**
   - PPAs enable financing of solar/wind developments
   - 24/7 baseload demand creates different profile than residential/commercial
   - Potential for data centers to provide **grid flexibility services** (though not yet implemented at Start Campus)

2. **Industrial site repurposing:**
   - Coal-to-AI transition demonstrates **"just transition" pathway**
   - Existing transmission infrastructure has enormous value
   - Cooling infrastructure can be repurposed
   - Community acceptance easier in established industrial zones

3. **Geographic shifts:**
   - **Renewable energy abundance becomes location determinant** (not just proximity to users)
   - Iberian Peninsula, Nordics, other renewable-rich regions gain advantage
   - Urban data centers may become legacy infrastructure
   - Industrial policy implications: countries with renewable resources and grid capacity can attract massive investment

**Labor Market Effects:**

1. **Skilled labor demand:**
   - 3,000-4,000 construction workers at peak
   - Hundreds of permanent operational staff
   - Specialized skills: electrical engineering, HVAC, IT infrastructure
   - **Diaspora return phenomenon:** Portuguese engineers coming home

2. **Training and education:**
   - Partnerships with local schools and universities essential
   - Transition training for workers from legacy industries (coal, LNG)
   - Long-term career paths in growing industry

### For Technology Strategy

**Compute Infrastructure Evolution:**

1. **Power density trajectory:**
   - Current: 60-130kW racks
   - Near-term: 1MW racks
   - Future: 2MW+ racks
   - **Implication:** Cooling and power delivery, not compute, become the constraints

2. **Cooling technology roadmap:**
   - Air cooling: Legacy for low-density applications
   - Liquid-to-chip: Current generation for high-density
   - Immersion cooling: Potential future for extreme density
   - **Natural cooling resources** (seawater, ambient air) provide sustainable advantage

3. **Power delivery evolution:**
   - Current: 400V AC
   - Emerging: Medium-voltage DC
   - **Efficiency gains:** Reducing conversion losses
   - **Infrastructure implications:** Requires different electrical design

4. **Workload differentiation:**
   - **AI training:** Can tolerate interruption, doesn't need 100% generator backup
   - **AI inference:** More latency-sensitive, may need urban edge locations
   - **Traditional cloud:** Continues growing regardless of AI hype
   - **Future flexibility:** Facilities must support multiple workload types

### Actionable Takeaways

**For Entrepreneurs/Operators:**
1. **Focus on execution over concepts:** The market values speed, but sustainable competitive advantage comes from operational excellence
2. **Secure power and cooling first:** These are the true constraints, not land or buildings
3. **Build relationships with TSOs and renewable developers early:** Grid capacity and renewable PPAs have long lead times
4. **Design for 2x current requirements:** Technology evolution will exceed expectations

**For Policymakers:**
1. **Streamline permitting for repurposed industrial sites:** These offer fastest path to sustainable data center development
2. **Coordinate grid planning with data center development:** Gigawatt-scale facilities require years of transmission planning
3. **Incentivize renewable energy co-location:** Data centers can anchor renewable project financing
4. **Support workforce training:** Transition workers from legacy industries while attracting returning diaspora

**For Corporate IT/Cloud Buyers:**
1. **Evaluate provider sustainability claims carefully:** PUE, renewable energy additionality, and cooling efficiency vary dramatically
2. **Consider workload requirements:** Not all applications need five-nines uptime or urban locations
3. **Long-term partnerships matter:** 10+ year commitments enable better infrastructure
4. **Geographic diversification:** European capacity will grow; consider data sovereignty implications

## 6. Notable Quotes

1. **On scale and investment:** "We're looking at €10 billion just for the physical infrastructure of the data center...and then we expect our customers to bring in their GPUs, their CPUs, their IT equipment. That's generally around four times as much. So we're looking at €40-50 billion of IT equipment going in to add on to the €10 billion that we're spending." 
   - *Illustrates the staggering capital intensity of modern AI infrastructure*

2. **On customer priorities:** "Time to market is so important in this AI race at the moment. If you can deliver a data center within 18 months, then you're in a much better position than someone that has only just started their design."
   - *Captures the urgency driving current market dynamics*

3. **On efficiency gains:** "Our primary and future-facing technology is the seawater cooling...it's doing it at about a 1.1 PUE which basically means it's about 3 to 4 times more efficient than these old chillers and cooling towers that we have."
   - *Quantifies the competitive advantage of innovative cooling*

4. **On the AI bubble question:** "Yes, there's a lot of hype around AI at the moment and we'll see where that goes. But I still think the growth in demand for data centers isn't going to go anywhere...this place will end up running as a combination—AI training, AI inference, other cloud products."
   - *Provides measured perspective on sustainability of demand*

5. **On building philosophy:** "Our business model is a little bit different. We're building for the investors for the long term. So we're here to support the next 5, 10 years of AI deployments, but in 10, 15, 20 years, this building also needs to be ready to support cloud and other IT services."
   - *Articulates the tension between speed and sustainability in current market*

---

**Final Reflection:** This episode captures a pivotal moment in technology infrastructure development. Rob Dunn and Start Campus represent a bet that sustainable, well-engineered, gigawatt-scale facilities will ultimately win over rapid-deployment approaches—but they're making that bet while moving fast enough to capture the AI wave. The €60 billion scale, Microsoft's subsequent $10B investment, and the transformation of a coal power station into Europe's largest data center embody both the opportunities and uncertainties of the current moment. Whether we're witnessing the foundation of critical 21st-century infrastructure or an overbuilt response to temporary AI hype remains to be seen—but Rob's focus on flexibility and multiple use cases suggests Start Campus is hedging intelligently.

---

*Summary generated: 2026-01-18 11:38*
*Tokens: 15,447 input, 5,779 output | Cost: $0.13*
