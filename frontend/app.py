import requests
import streamlit as st
import time
# Set page config
st.set_page_config(page_title="Fraud URL/Malware File Detector", layout="centered")

# Custom CSS for a red cyber look and techy background
custom_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://src.n-ix.com/uploads/2023/06/13/42a66e04-88c6-43f4-9b41-5d5ac941508a.png");
    background-size: cover;
    background-position: center;
    color: #ff4c4c;
    font-family: 'Courier New', Courier, monospace;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(10, 10, 10, 0.85);
    z-index: -1;
}

h1, h2, h3 {
    color: #FF0000;
}

input, textarea,
.stTextInput input {
    background-color: #1e1e1e !important;
    color: #ffffff !important;
    border: 1px solid #ff4c4c !important;
    border-radius: 5px !important;
    padding: 8px !important;
    font-family: 'Courier New', Courier, monospace;
}

button:hover {
    background-color: #ff1a1a !important;
    transform: scale(1.03);
    transition: 0.2s ease-in-out;
}

.blink {
    animation: blinker 2.5s linear infinite;
}

@keyframes blinker {
    50% { opacity: 0; }
}

.terminal {
    background-color: #000000;
    color: #ff4c4c;
    font-family: 'Courier New', Courier, monospace;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #ff4c4c;
    margin-top: 20px;
    white-space: pre-wrap;
}
</style>
"""

# Inject CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Title and subheader
st.markdown('<h1 class="blink">🚨Fake URL/Malware File Detector</h1>', unsafe_allow_html=True)
st.subheader("This is a fake URL/Malware file detector website")
st.markdown("---")

# URL Input
url = st.text_input("🔗 Enter the suspected URL")

# Scan Button and Terminal-style output
if st.button("Scan URL"):
    if not url:
        st.error("Please enter the URL.")
    else:
        try:
            response = requests.post("http://127.0.0.1:8000/predict/", json={"url": url})
            if response.status_code == 200:
                result = response.json()
                prediction = result.get("prediction", "Unknown").strip().lower()

                if prediction == "phishing":
                    threat_msg = "⚠ This URL is identified as Phishing! Stay safe."
                    alert = "[!] Threat Detected: PHISHING"
                elif prediction in ["legitimate", "benign"]:
                    threat_msg = "✅ This URL appears to be Legitimate."
                    alert = "[✓] No threat detected: LEGITIMATE"
                else:
                    threat_msg = "❓ Unable to determine the threat level."
                    alert = "[!] Threat Detected: Unknown"

                terminal_output = f"""
[INFO] Scanning URL...
[✓] URL submitted: {url}
{alert}
[✓] Report generated.
"""
                st.success("Scan completed successfully.")
                st.info(f"Report generated for: {url}")
                st.markdown("### Terminal Output 🖥")
                st.markdown(f'<div class="terminal">{terminal_output}</div>', unsafe_allow_html=True)
                st.markdown(f"### Result:\n*{threat_msg}*")
            else:
                st.error("Failed to get a response from the backend.")
        except Exception as e:
            st.error(f"Error: {e}")

# --------------------------------------------------------------------------------------------------------------------
API_KEY = "a7a9249020137a19b4589984ef093c97542f2c93120642100e03f5c591afe01d"  # 🔑 Replace with your actual API key

# Submit URL to VirusTotal for scanning
def submit_url_to_virustotal(file_url):
    headers = {"x-apikey": API_KEY}
    data = {"url": file_url}
    response = requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data=data)

    if response.status_code == 200:
        return response.json()["data"]["id"]
    else:
        st.error(f"Error submitting URL: {response.text}")
        return None

# Get the scan result after some delay
def get_url_analysis(analysis_id):
    headers = {"x-apikey": API_KEY}
    analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"

    time.sleep(5)  # wait for scan to complete

    response = requests.get(analysis_url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        stats = result["data"]["attributes"]["stats"]
        verdict = "Malicious" if stats["malicious"] > 0 else "Benign"
        return stats, verdict
    else:
        st.error(f"Error fetching analysis: {response.text}")
        return None, None
# --- Malware File URL Scanner ---
st.markdown("---")
file_url = st.text_input("🗂 Enter Malware File URL") #input

if st.button("Scan File URL"):
    if file_url:
        with st.spinner("Analyzing..."):
            analysis_id = submit_url_to_virustotal(file_url)
            if analysis_id:
                stats, verdict = get_url_analysis(analysis_id)
                if verdict:
                    st.subheader("Results:")
                    # st.write(stats)
                    if verdict == "Malicious":
                        st.error("🚨Malicious file")
                    else:
                        st.success("✅Safe")
    else:
        st.warning("Please enter a valid URL.")