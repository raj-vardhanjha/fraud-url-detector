import re
import tldextract

def extract_features(url):

    features = []

    features.append(len(url))
    features.append(url.count("."))
    features.append(url.count("-"))
    features.append(url.count("/"))

    features.append(1 if "https" in url else 0)

    ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    features.append(1 if re.search(ip_pattern, url) else 0)

    suspicious_words = ["login","secure","update","bank","verify","free","account"]
    features.append(sum([1 for word in suspicious_words if word in url.lower()]))

    extracted = tldextract.extract(url)
    domain = extracted.domain

    features.append(len(domain))

    return features
