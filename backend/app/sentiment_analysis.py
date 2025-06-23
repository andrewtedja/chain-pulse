from .stringmatching.aho_corasick import AhoCorasick
from .stringmatching.fuzzy import FuzzyMatcher

keywords = {
    "positive": 
    [
        "bullish", "pump", "surge", "rally", "moon", "breakout", "ath", "all time high", "whale pumped", "support held", "uptrend", "rebound", "bounce", "recovery", "accumulation", "god candle", "parabolic", "demand zone", "double bottom", "consolidation", "higher low", "partnership", "listing", "airdrop", "upgrade", "adoption", "integration", "favor", "approval", "gains", "sparks", "increase", "extending", "inflow", "boost", "anticipated", "bull run", "green candle", "break resistance", "trend reversal", "ETF approved", "record high", "buy pressure", "new listing",
    ],

    "negative": 
    [
        "crash", "dump", "bearish", "rugpull", "decline", "bear market", "whale dumped", "resistance failed", "exit liquidity", "bleed", "correction", "plunge", "pampedak", "downtrend", "down", "fud", "doubt", "fear", "uncertainty", "war", "loss", "bleeds", "attack", "hacked", "fake", "decrease", "scam", "pressure", "liquidated", "market turmoil", "flash crash", "exploit", "lawsuit", "under investigation", "sell pressure",
    ]
}

matcher = AhoCorasick(keywords["positive"] + keywords["negative"])
fuzzy = FuzzyMatcher()

def analyze_sentiment(text):
    text_lower = text.lower()
    aho_result = matcher.search_words(text_lower)

    pos_keywords_found = set()
    neg_keywords_found = set()

    # EXACT
    for kw in keywords["positive"]:
        if kw in aho_result:
            pos_keywords_found.add(kw)
    for kw in keywords["negative"]:
        if kw in aho_result:
            neg_keywords_found.add(kw)

    # FUZZY (If exact not found)
    for kw in keywords["positive"]:
        if kw not in pos_keywords_found:
            count, _ = fuzzy.fuzzy_search(kw, text_lower)
            if count > 0:
                pos_keywords_found.add(kw)

    for kw in keywords["negative"]:
        if kw not in neg_keywords_found:
            count, _ = fuzzy.fuzzy_search(kw, text_lower)
            if count > 0:
                neg_keywords_found.add(kw)

    pos_count = len(pos_keywords_found)
    neg_count = len(neg_keywords_found)

    score = (pos_count - neg_count) / max(1, pos_count + neg_count)


    label = "neutral"
    if score > 0:
        label = "positive"
    elif score < 0:
        label = "negative"

    return {
        "score": round(score, 2),
        "sentiment": label,
        "positive": {"count": pos_count, "keywords": list(pos_keywords_found)},
        "negative": {"count": neg_count, "keywords": list(neg_keywords_found)},
    }




# TESTING
def test_analyze_sentiment():
    test_cases = [
        # format: (text, expected_pos_keywords, expected_neg_keywords, expected_pos_count, expected_neg_count)

        # === Exact matches only ===
        ("The market is bullish and there's a pump incoming", 
         ["bullish", "pump"], [], 2, 0),

        # === Exact multiword ===
        ("Analysts predict a bear market and potential dump", 
         [], ["bear market", "dump"], 0, 2),

        # === Mixed: exact + fuzzy ===
        ("Looks like a rallly and crssh are coming", 
         ["rally"], ["crash"], 1, 1),

        # === All fuzzy ===
        ("This is a moonn pumpy surgey rugpul market", 
         ["moon", "pump", "surge"], ["rugpull"], 3, 1),

        # === No match ===
        ("Nothing exciting here, just sideways motion", 
         [], [], 0, 0),

        # === Casing & plural tolerance ===
        ("We're entering bearish trends and rallies", 
         [], ["bearish"], 0, 1),
    ]

    for i, (text, expected_pos, expected_neg, exp_pos_count, exp_neg_count) in enumerate(test_cases, 1):
        result = analyze_sentiment(text)
        pos_result = result["positive"]["keywords"]
        neg_result = result["negative"]["keywords"]
        score = result["score"]

        pass_pos = set(pos_result) == set(expected_pos)
        pass_neg = set(neg_result) == set(expected_neg)
        pass_count = (
            result["positive"]["count"] == exp_pos_count and
            result["negative"]["count"] == exp_neg_count
        )

        status = "✅ PASS" if pass_pos and pass_neg and pass_count else "❌ FAIL"
        print(f"\n=== Test Case {i}: {status} ===")
        print(f"Text      : {text}")
        print(f"Expected  : +{expected_pos} ({exp_pos_count}) / -{expected_neg} ({exp_neg_count})")
        print(f"Got       : +{pos_result} ({result['positive']['count']}) / -{neg_result} ({result['negative']['count']})")
        print(f"Sentiment Score: {score}")
        print("-" * 50)


if __name__ == "__main__":
    test_analyze_sentiment()
