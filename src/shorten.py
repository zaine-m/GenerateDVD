import ollama

SYSTEM_PROMPT = """You label YouTube titles.

Turn the title into a 2-4 word topic label.

Rules:
- Describe the main subject of the video.
- Write in the same tone as the title
- Output only the label.
- Use 2-4 words.
- Remove filler and dramatic wording.
- Keep important names, brands, and topics.

Examples:


Input: We created the sport of the future | Unraveled
Output: Creating New Sport

Input: How to increase your stamina with terrible video game tactics
Output: Video Game Stamina Strategies

Input: The Right-Wing Pick-Me EPIDEMIC
Output: Right-Wing Pick-Mes

Input: How to make a perfect E3 press conference (or drinking game) | Unraveled
Output: Improving E3 Conference

Input: Dark Psychology "FACTS" Are Definitely Not Toxic
Output: Toxic Psychology Facts

Input: Your SON is NOT Your Husband
Output: Predator Mothers

Input: I Hope You Get EVICTED
Output: Terrible Roommates

Input: And THAT'S Why You're BANNED From the Movies
Output: Bad Movie Theater Etiquette

Input: Anyways... That's How I Lost My Medical License
Output: Horrible Nurses

Input: You Don’t Want A Wife… You Want a SERVANT
Output: Misogynic Men Trad Wives

Input: AI Schooling is the New UNSCHOOLING
Output: AI Unschooling

Input: Stop EXPLOITING Your Kids For Views
Output: Mommy Vloggers

Input: The QUEEN of TikTok Main Characters
Output: Main Character Syndrome

Input: I Got Hypnotized To See If It's Fake
Output: Investigating Hypnotism

Input: I Tried Walmart's Terrifying Metaverse Experience
Output: Terrifying Metaverse Walmart

Input: Stop Trying To Give Birth At Disneyland
Output: Weird Disneyland Behaviours

Input: I am the worst chef on youtube
Output: Cooking Stuff Badly

Input: I followed a bunch of tutorials on how to get taller
Output: Can I Get Taller?

Input: I ate like Tom Brady for a month
Output: Tom Brady Diet

Input: Learning the Most Pointless Life Lessons from Dhar Mann
Output: Dhar Mann Videos

Input: I bought every weird ad I saw for a month
Output: Trying Weird Ads
"""

def shortenTitles(videos):
    for video in videos:
        video['short title'] = shortenTitle(video['full title'])
    return videos

def shortenTitle(longTitle):
    result = ollama.generate(
        model='llama3.2:1b',
        system=SYSTEM_PROMPT,
        prompt=f"Title: {longTitle}\nLabel:"
    )

    print(result['response'].strip())
    return result['response'].strip()