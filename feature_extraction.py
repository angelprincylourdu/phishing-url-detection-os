from urllib.parse import urlparse
import re


def extract_features(url):
    parsed = urlparse(url)

    host = parsed.hostname or ""

    # Dataset-style URL features
    url_length = len(url)

    domain_length = len(host)

    is_domain_ip = 1 if re.fullmatch(
        r"\d{1,3}(?:\.\d{1,3}){3}",
        host
    ) else 0

    tld_length = len(host.rsplit(".", 1)[-1]) if "." in host else 0

    no_subdomain = max(host.count(".") - 1, 0)

    obfuscated = re.findall(r"%[0-9A-Fa-f]{2}", url)

    no_obfuscated = len(obfuscated)

    has_obfuscation = 1 if no_obfuscated > 0 else 0

    obfuscation_ratio = (
        no_obfuscated / url_length
        if url_length else 0
    )

    letters = sum(c.isalpha() for c in url)

    digits = sum(c.isdigit() for c in url)

    letter_ratio = letters / url_length if url_length else 0

    digit_ratio = digits / url_length if url_length else 0

    other_special = sum(
        not c.isalnum()
        and c not in "/:."
        for c in url
    )

    special_ratio = (
        other_special / url_length
        if url_length else 0
    )

    return {
        "URLLength": url_length,
        "DomainLength": domain_length,
        "IsDomainIP": is_domain_ip,
        "TLDLength": tld_length,
        "NoOfSubDomain": no_subdomain,
        "HasObfuscation": has_obfuscation,
        "NoOfObfuscatedChar": no_obfuscated,
        "ObfuscationRatio": obfuscation_ratio,
        "NoOfLettersInURL": letters,
        "LetterRatioInURL": letter_ratio,
        "NoOfDegitsInURL": digits,
        "DegitRatioInURL": digit_ratio,
        "NoOfEqualsInURL": url.count("="),
        "NoOfQMarkInURL": url.count("?"),
        "NoOfAmpersandInURL": url.count("&"),
        "NoOfOtherSpecialCharsInURL": other_special,
        "SpacialCharRatioInURL": special_ratio,
        "IsHTTPS": 1 if parsed.scheme == "https" else 0
    }
