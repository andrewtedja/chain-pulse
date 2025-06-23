COIN_KEYWORDS = {
    "BTC": ["bitcoin", "btc"],
    "ETH": ["ethereum", "eth", "ether"],
    "BNB": ["bnb", "binance coin"],
    "SOL": ["solana", "sol"],
    "XRP": ["ripple", "xrp"],
    "RENDER": ["Render", "render"],
    "WLD": ["Worldcoin", "wld"],
    "ADA": ["cardano", "ada"],
    "AVAX": ["avalanche", "avax"],
    "HYPE": ["Hyperliquid", "hype"],
    "DOT": ["polkadot", "dot"],
    "TON": ["Toncoin", "ton"],
    "TRX": ["tron", "trx"],
    "MATIC": ["polygon", "matic"],
    "NEAR": ["near protocol", "near"],
    "ATOM": ["cosmos", "atom"],
    "FTM": ["fantom", "ftm"],
    "ONDO": ["ondo"],
    "DOGE": ["dogecoin", "doge"],
    "SUI": ["Sui", "sui"],
    "SHIB": ["shiba inu", "shib"],
    "PEPE": ["pepe"],
    "BOME": ["bome"],
    "WIF": ["dogwifhat", "wif"],
    "FLOKI": ["floki"],
    "BONK": ["bonk"],
    "UNI": ["uniswap", "uni"],
    "LINK": ["chainlink", "link"],
    "AAVE": ["aave"],
    "LDO": ["lido", "ldo"],
    "MKR": ["maker", "mkr"],
    "CRV": ["curve dao", "crv"],
    "SUSHI": ["sushiswap", "sushi"],
    "DYDX": ["dydx"],
    "BITGET": ["bitget", "bgb"],
    "OP": ["optimism", "op"],
    "ARB": ["arbitrum", "arb"],
    "IMX": ["immutable x", "imx"],
    "QNT": ["Quant", "qnt"],
    "MANA": ["decentraland", "mana"],
    "AXS": ["axie infinity", "axs"],
    "GALA": ["gala"],
    "LTC": ["litecoin", "ltc"],
    "BCH": ["bitcoin cash", "bch"],
    "XLM": ["stellar", "xlm"],
    "XMR": ["monero", "xmr"],
    "ETC": ["ethereum classic", "etc"],
    "FIL": ["filecoin", "fil"],
    "ICP": ["internet computer", "icp"],
    "VET": ["vechain", "vet"],
    "HBAR": ["hedera", "hbar"]
}

def identify_coins_in_text(text):
    found_coins = set()
    text_lower = text.lower()
    for ticker, keywords in COIN_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                found_coins.add(ticker)
                break # Lanjut ke ticker berikutnya jika sudah ketemu
    return list(found_coins)


# TESTING
if __name__ == '__main__':
    print("Unit Test untuk identify_coins_in_text")
    
    test_cases = [
        ("Great news for bitcoin (BTC) investors!", ["BTC"]),
        ("Ethereum and Ripple are soaring, but Solana faces issues.", ["ETH", "XRP", "SOL"]),
        ("What is the future of dogecoin?", ["DOGE"]),
        ("This article is about general market trends.", []),
        ("ETH's new upgrade is live!", ["ETH"])
    ]

    for i, (text, expected) in enumerate(test_cases, 1):
        result = identify_coins_in_text(text)
        # Urutkan untuk perbandingan yang konsisten
        result.sort()
        expected.sort()
        
        status = "V PASS" if result == expected else "X FAIL"
        print(f"\nTest Case #{i}: {status}")
        print(f"  - Text: '{text}'")
        print(f"  - Expected: {expected}")
        print(f"  - Got: {result}")