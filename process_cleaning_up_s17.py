#!/usr/bin/env python3
"""Batch-process Cleaning Up episodes 239-266 + specials into knowledge/podcasts/cleaning-up-s17."""

from process_knowledge import process_video, load_knowledge_config

EPISODES = [
    ("mQDxplrGkDA", "Trump, Venezuela & The Future Of Clean Energy | Ep239: Michael Liebreich & Bryony Worthington"),
    ("ibo4adr5cdk", "Is Clean Energy Actually Causing Higher Bills? | Ep240: Katie White MP"),
    ("urmP7zN6n04", "Is Africa Ready To Become A Clean Energy Powerhouse? | Ep241: Clemens Calice"),
    ("EzySrSD8vz8", "The State of the Climate 2026 | Ep242: Zeke Hausfather"),
    ("otaq3rGj0Cw", "The World Decides: Clean Energy or Oil & Gas? Ep243: Damilola Ogunbiyi"),
    ("YpddT8QDkcw", "Why Isn't Carbon Removal Working? | Ep244: Robert Hoglund"),
    ("5oL_XlZ8k_M", "Why Renewables Are Booming Despite the Politics | Ep245: Miguel Stilwell d'Andrade"),
    ("fRETqbABCFA", "Can a Transatlantic Electricity Cable Connect North America & Europe? | Ep246: Laurent Segalen"),
    ("Oh6ovfhIqhw", "How To Build Quickly In An Era of Fossil Fuel Shocks | Ep247: Hilde Tonne"),
    ("5Gh5PFkvcDU", "Iran Will Reshape Oil, Gas & Clean Energy For Years To Come | Special: Bryony Worthington & Michael Liebreich"),
    ("YL64XW5ZRBA", "Are Fossil Fuel Cars About to Have A Kodak Moment? Ep248: Fiona Howarth"),
    ("4kSrgRZUCwE", "Can Data Centres Play Nice With The Grid? | Ep249: Varun Sivaram & Steve Smith"),
    ("iRd9Qpd3Pag", "Do We Still Need Carbon Capture & Storage? | Ep250: Emmanouil Kakaras"),
    ("24zL93zf2XY", "Can We Cool The Planet, And Should We Try? | Ep251: Ricken Patel"),
    ("r2xS5e5EGEg", "The True Cost of Fossil Fuels | Ep252: Pierre Wunsch"),
    ("hmHIrtBZIAg", "The Mother of All Energy Crises | Ep253: Fatih Birol"),
    ("8bXWtW5lFE8", "The Era Of Fossil Fuel Unreliability Has Begun | Ep254: Jennifer Granholm"),
    ("lWGtsLK0W14", "Europe Needs Clean Tech More Than Ever | Ep255: Thomas Pellerin-Carlin"),
    ("MrV1E_QZgXo", "Electrify Everything You Can, Do The Rest Later: The Electrification Staircase | Ep256"),
    ("jUxdaHFJI68", "India's Solar Revolution Is Bringing Cheap Energy To Millions | Ep257: Harish Hande"),
    ("MikHMrLfUaQ", "Can Anyone Catch China's Clean Tech Lead? Ep258: Bryony Worthington & Michael Liebreich"),
    ("dUYjGT55g5A", "Why Flexible Power Is Suddenly So Valuable | Ep259: Hakan Agnevall"),
    ("EhVIZY9LUzo", "RCP8.5 Is Dead, What Comes Next? Ep260: Roger Pielke Jr."),
    ("0jSepnpmBBo", "How Wind Energy Overtook Nuclear in Just Two Decades | Ep261: Henrik Andersen"),
    ("xCUASv01bVY", "How China Became an Energy Superpower | Ep262: Professor Ning Li"),
    ("cH1qI2czwlM", "How the US Makes and Breaks Global Deals | Ep263: John Kerry"),
    ("iBhkBTZ9lSI", "How Australia Became The World's Battery Champion | Deep Dive Australia 01: Darren Miller"),
    ("Xvhd34i6YMk", "Can Asia Ever Move Beyond Coal? | Ep264: Ravi Menon"),
    ("OYtapcSdZOo", "Australia Loves Solar, So Why The Diesel Addiction? Deep Dive Australia 02: Chris Bowen"),
    ("RE2ZeGd8aaI", "Southeast Asia's Leapfrog to Clean Tech | Ep265: Marie Cheong"),
    ("1tKVSJcS_SI", "Are Solar And Batteries Undermining Australia's Grid? Deep Dive Australia 03: Marc England"),
    ("3y9bXPsHGyE", "Batteries Are The Killer Tech Of The Energy Transition | Ep266: Alex Shoer"),
    ("IVGL9vVTdeY", "Is Australia Finally Turning Its Back on Coal? Lily D'Ambrosio | Deep Dive Australia 04"),
]

if __name__ == "__main__":
    config = load_knowledge_config()
    results = []
    total_cost = 0.0

    for i, (video_id, title) in enumerate(EPISODES, 1):
        print(f"\n[{i}/{len(EPISODES)}] {title[:70]}...")
        try:
            result = process_video(
                video_id=video_id,
                title=title,
                content_type="podcast",
                output_folder="cleaning-up-s17",
                config=config,
            )
            if result:
                results.append(result)
                total_cost += result["cost"]
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

    print(f"\n{'='*60}")
    print(f"Processed {len(results)}/{len(EPISODES)} episodes")
    print(f"Total cost: ${total_cost:.2f}")
    print(f"{'='*60}")
