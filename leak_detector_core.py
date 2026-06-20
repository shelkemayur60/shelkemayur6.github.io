"""
Core logic for the Data Leak Detector.
Handles password breach checking (via HIBP k-anonymity API) and
password strength analysis.
"""

import hashlib
import re
import requests

HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/{}"


def check_password_breach(password: str) -> int:
    """
    Check if a password has appeared in known data breaches.
    Uses the k-anonymity model: only the first 5 characters of the
    SHA-1 hash are sent to the API — the real password never leaves
    your machine.

    Returns:
        int: number of times this password was seen in breaches.
             0 means it was not found in any known breach.
    """
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]

    response = requests.get(HIBP_RANGE_URL.format(prefix), timeout=10)
    response.raise_for_status()

    for line in response.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)

    return 0


def analyze_password_strength(password: str) -> dict:
    """
    Analyze password strength based on common security criteria.

    Returns:
        dict with 'score' (0-5), 'label', and 'issues' (list of strings)
    """
    issues = []
    score = 0

    if len(password) >= 12:
        score += 1
    else:
        issues.append("Kiman 12 characters asayla pahije")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        issues.append("Kiman ek CAPITAL letter add kara")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        issues.append("Kiman ek small letter add kara")

    if re.search(r"\d", password):
        score += 1
    else:
        issues.append("Kiman ek number add kara")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        issues.append("Kiman ek special character (!@#$ etc.) add kara")

    labels = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Good",
        4: "Strong",
        5: "Very Strong",
    }

    return {
        "score": score,
        "label": labels[score],
        "issues": issues,
    }
