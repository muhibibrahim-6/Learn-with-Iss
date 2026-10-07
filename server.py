import os
from datetime import datetime
from flask import Flask, render_template, jsonify, Response

app = Flask(__name__)

SITE_NAME = "Learn With Iss"
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "contact@example.com")  # Render > Environment এ নিজের ইমেইল দিন
OWNER = "Muhib Ibrahim"
TAGLINE = f"The Hacker Knowledge Hub By {OWNER}"
DESCRIPTION = (
    f"{SITE_NAME} — High-performance cybersecurity knowledge hub curated by {OWNER}. "
    "10 core domains, offensive roadmaps, 45+ tools, legal labs, and curated threat feeds."
)

NAV = [
    ("welcome", "Welcome"), ("knowledge", "Knowledge"), ("paths", "Roadmaps"),
    ("arsenal", "Tools"), ("practice", "Labs"), ("glossary", "Terms"),
    ("intel", "News Feeds"), ("rules", "Rules"), ("legal", "Legal"),
]

ETHOS = [
    ("🧠", "Curiosity first", "Ask how it works. Take it apart. The deepest understanding comes from breaking things in a place where breaking is safe."),
    ("🤝", "Share knowledge", "The best of this culture is open. Write-ups, tools, and teaching lift everyone. You were helped — pass it on."),
    ("🛡️", "Do no harm", "Power without ethics is just damage. Hack what you own or have permission to test. Disclose responsibly."),
    ("♾️", "Never stop", "The field moves daily. The hacker doesn't memorize answers — they learn how to learn, forever."),
]

DOMAINS = [
    ("🕸️", "Web Application Security", "Where most of the action is. The browser is an attack surface and so is everything behind it.",
     ["Injection: SQLi, command, template (SSTI), LDAP", "XSS — stored, reflected, DOM; and CSP bypasses", "SSRF, IDOR, broken access control, auth flaws", "Request smuggling, deserialization, file upload abuse"],
     [("OWASP Top 10", "https://owasp.org/www-project-top-ten/"), ("PortSwigger Web Security Academy", "https://portswigger.net/web-security"), ("OWASP Cheat Sheets", "https://cheatsheetseries.owasp.org/")]),
    ("🌐", "Network & Infrastructure", "Map it, understand it, then find the soft spot. Protocols leak more than people think.",
     ["Recon & scanning: ports, services, versions", "Pivoting, tunneling, lateral movement", "MITM, ARP/DNS poisoning, protocol abuse", "Firewall / IDS evasion fundamentals"],
     [("Nmap Reference", "https://nmap.org/book/man.html"), ("HackTricks — Pentesting", "https://book.hacktricks.xyz/"), ("Wireshark Docs", "https://www.wireshark.org/docs/")]),
    ("🧬", "Binary Exploitation & RE", "Read the machine. Understand memory, then understand what breaks it.",
     ["Buffer overflows, ROP, format strings", "Heap exploitation, use-after-free", "Static & dynamic analysis, debugging", "Disassembly & decompilation workflows"],
     [("Nightmare (heap/pwn course)", "https://guyinatuxedo.github.io/"), ("Ghidra", "https://ghidra-sre.org/"), ("pwn.college", "https://pwn.college/")]),
    ("🔐", "Cryptography", "Don't roll your own. But absolutely learn how the real ones break.",
     ["Symmetric/asymmetric primitives & modes", "Padding oracles, length-extension, nonce reuse", "Hashing, password cracking, rainbow tables", "TLS, PKI, and where trust goes wrong"],
     [("Cryptopals Challenges", "https://cryptopals.com/"), ("Crypto 101", "https://www.crypto101.io/"), ("NIST CSRC", "https://csrc.nist.gov/")]),
    ("🔎", "OSINT & Recon", "The quietest phase and often the most powerful. Information wants to be found.",
     ["Domain, DNS, cert transparency, subdomain enum", "People & org footprinting, metadata", "Credential & breach data exposure", "Cloud asset & bucket discovery"],
     [("OSINT Framework", "https://osintframework.com/"), ("crt.sh — cert transparency", "https://crt.sh/"), ("Shodan", "https://www.shodan.io/")]),
    ("⬆️", "PrivEsc & Post-Exploitation", "Getting in is step one. Staying, escalating, and understanding the blast radius is the craft.",
     ["Linux & Windows privilege escalation", "Credential harvesting & token abuse", "Persistence, defense evasion (lab-only)", "Active Directory attack paths"],
     [("GTFOBins", "https://gtfobins.github.io/"), ("LOLBAS", "https://lolbas-project.github.io/"), ("PayloadsAllTheThings", "https://github.com/swisskyrepo/PayloadsAllTheThings")]),
    ("📡", "Wireless & Hardware", "Radio, firmware, and physical interfaces — the attack surface you can hold in your hand.",
     ["Wi-Fi (WPA2/3), capture & cracking", "Bluetooth, RFID/NFC, SDR basics", "Firmware extraction & analysis", "JTAG/UART & embedded debugging"],
     [("Hak5", "https://hak5.org/"), ("OpenWrt", "https://openwrt.org/"), ("Firmware Analysis (OWASP)", "https://owasp.org/www-project-firmware-security-testing-methodology/")]),
    ("☁️", "Cloud & Container Security", "The perimeter moved to IAM. Misconfigurations are the new open ports.",
     ["IAM misconfig, privilege escalation paths", "Storage exposure, metadata SSRF", "Container escape, K8s attack surface", "CI/CD & supply-chain risk"],
     [("HackTricks Cloud", "https://cloud.hacktricks.xyz/"), ("CIS Benchmarks", "https://www.cisecurity.org/cis-benchmarks"), ("Kubernetes Security", "https://kubernetes.io/docs/concepts/security/")]),
    ("🤖", "AI / LLM Security", "The newest frontier. Models are software — and software gets attacked.",
     ["Prompt injection (direct & indirect)", "Jailbreaks, data exfiltration, tool abuse", "Training-data & supply-chain poisoning", "Model & adversarial-input attacks"],
     [("OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/"), ("MITRE ATLAS", "https://atlas.mitre.org/"), ("LLM Security", "https://llmsecurity.net/")]),
    ("🎭", "Social Engineering", "The human is part of the system. Study it with consent, ethics, and a clear purpose.",
     ["Pretexting, phishing awareness & defense", "OSINT-driven targeting (authorized only)", "Physical security & tailgating concepts", "Building org-wide resilience & training"],
     [("SANS Security Awareness", "https://www.sans.org/security-awareness-training/"), ("NIST Phishing Guidance", "https://csrc.nist.gov/"), ("Social-Engineer.org", "https://www.social-engineer.org/")]),
]

PATHS = [
    ("Foundations", "Start here — no prior experience needed.", [
        "Learn Linux: the shell, files, permissions, processes", "Networking basics: TCP/IP, DNS, HTTP, ports",
        "Pick one language: Python for tooling, then a little C", "Set up a lab: a VM, Kali/Parrot, and a target box",
        "Play OverTheWire Bandit + TryHackMe Pre-Security"]),
    ("Core Offense", "Build real attacker skills, ethically.", [
        "Work through PortSwigger Web Security Academy end-to-end", "Learn recon: nmap, enumeration, OSINT",
        "Practice on Hack The Box / TryHackMe boxes", "Read OWASP Top 10 and reproduce each class in your lab",
        "Start documenting — write-ups make you 10x faster"]),
    ("Specialize", "Go deep where your curiosity pulls you.", [
        "Pick a track: web, binary, cloud, AI, or AD", "Compete in CTFs (watch CTFtime for events)",
        "Study MITRE ATT&CK to think like a real adversary", "Contribute: bug bounties, open-source tools, write-ups",
        "Learn the defense side too — it makes you dangerous"]),
]

TOOLS = {
    "Recon": ["nmap", "masscan", "amass", "subfinder", "theHarvester", "Shodan"],
    "Web": ["Burp Suite", "OWASP ZAP", "ffuf", "sqlmap", "nikto", "gobuster"],
    "Exploitation": ["Metasploit", "msfvenom", "searchsploit", "Impacket", "CrackMapExec"],
    "Reverse Eng.": ["Ghidra", "radare2 / Cutter", "x64dbg", "gdb + pwndbg", "IDA Free"],
    "Network": ["Wireshark", "tcpdump", "Bettercap", "mitmproxy", "Responder"],
    "Password": ["hashcat", "John the Ripper", "hydra", "Hashes.com"],
    "Forensics": ["Volatility", "Autopsy", "binwalk", "ExifTool", "CyberChef"],
    "Cloud": ["ScoutSuite", "Prowler", "Pacu", "kube-hunter", "trivy"],
}

PRACTICE = [
    ("PortSwigger Web Security Academy", "Free, world-class web hacking labs", "https://portswigger.net/web-security"),
    ("Hack The Box", "Live machines & pro labs", "https://www.hackthebox.com/"),
    ("TryHackMe", "Guided rooms, beginner-friendly", "https://tryhackme.com/"),
    ("picoCTF", "Beginner CTF by Carnegie Mellon", "https://picoctf.org/"),
    ("OverTheWire", "Classic terminal wargames", "https://overthewire.org/wargames/"),
    ("VulnHub", "Downloadable vulnerable VMs", "https://www.vulnhub.com/"),
    ("pwn.college", "Binary exploitation & systems", "https://pwn.college/"),
    ("Cryptopals", "Hands-on crypto attacks", "https://cryptopals.com/"),
    ("Root-Me", "Huge challenge catalogue", "https://www.root-me.org/"),
    ("CTFtime", "Find live CTF competitions", "https://ctftime.org/"),
]

GLOSSARY = [
    ("0-day", "A vulnerability with no available patch — defenders have had zero days to fix it."),
    ("CVE", "Common Vulnerabilities and Exposures — a unique ID for a publicly known flaw."),
    ("Payload", "The part of an exploit that performs the intended action after a vuln is triggered."),
    ("Pivot", "Using a compromised host to reach networks you couldn't reach directly."),
    ("Recon", "Reconnaissance — gathering information about a target before engaging."),
    ("RCE", "Remote Code Execution — running arbitrary code on a target over the network."),
    ("PrivEsc", "Privilege escalation — going from low-privilege access to admin/root."),
    ("C2", "Command & Control — infrastructure used to operate compromised systems."),
    ("Bug Bounty", "A program that pays researchers for responsibly reported vulnerabilities."),
    ("Responsible Disclosure", "Reporting a flaw privately to the owner and giving time to fix it."),
    ("Red Team", "Offensive security — simulating real adversaries to test defenses."),
    ("Blue Team", "Defensive security — detection, response, and hardening."),
]

FEEDS = {
    "Threat Intel": [
        ("The Hacker News", "Breaking infosec news & incidents", "https://thehackernews.com/"),
        ("BleepingComputer", "Vulns, malware, ransomware reporting", "https://www.bleepingcomputer.com/news/security/"),
        ("GBHackers", "Daily cyber news & pentesting", "https://gbhackers.com/"),
        ("Dark Reading", "Enterprise security journalism", "https://www.darkreading.com/"),
        ("Krebs on Security", "Investigative deep dives", "https://krebsonsecurity.com/"),
        ("The Record", "Recorded Future intel desk", "https://therecord.media/"),
        ("SecurityWeek", "Daily security news", "https://www.securityweek.com/"),
        ("Infosecurity Magazine", "Industry magazine", "https://www.infosecurity-magazine.com/"),
        ("Schneier on Security", "Bruce Schneier commentary", "https://www.schneier.com/"),
        ("WIRED Security", "Security & policy", "https://www.wired.com/category/security/"),
        ("Hacker News", "Community front page", "https://news.ycombinator.com/"),
        ("Cisco Talos", "Threat research", "https://talosintelligence.com/"),
        ("Palo Alto Unit 42", "Threat intelligence & IR", "https://unit42.paloaltonetworks.com/"),
    ],
    "Nation-State & Government": [
        ("CISA Advisories", "US cyber advisories", "https://www.cisa.gov/news-events/cybersecurity-advisories"),
        ("CISA Home", "US Cybersecurity & Infrastructure Security Agency", "https://www.cisa.gov/"),
        ("CISA Stop Ransomware", "Ransomware alerts", "https://www.cisa.gov/stopransomware/official-alerts-statements-cisa"),
        ("NSA Cybersecurity Guidance", "NSA advisories", "https://www.nsa.gov/press-room/cybersecurity-advisories-guidance/"),
        ("FIRST.org", "Global incident response forum", "https://www.first.org/"),
        ("CERT/CC Vuln Notes", "Coordinated disclosure notes", "https://www.kb.cert.org/vuls/"),
        ("NIST CSRC", "Computer security standards", "https://csrc.nist.gov/"),
    ],
    "CVEs & Zero-Days": [
        ("NVD", "National Vulnerability Database", "https://nvd.nist.gov/"),
        ("NVD CVE Search", "Search every CVE", "https://nvd.nist.gov/vuln/search"),
        ("MSRC", "Microsoft patches & advisories", "https://msrc.microsoft.com/"),
        ("Huntr", "AI/ML bug bounty", "https://huntr.com/"),
    ],
    "Cloud Security": [
        ("AWS Security Blog", "Amazon cloud security", "https://aws.amazon.com/blogs/security/"),
        ("Azure Security Blog", "Microsoft cloud security", "https://azure.microsoft.com/en-us/blog/category/security/"),
        ("Google Cloud Security", "GCP identity & security", "https://cloud.google.com/blog/products/identity-security"),
        ("Cloudflare Security", "Edge & DDoS", "https://blog.cloudflare.com/tag/security/"),
        ("Microsoft Security Blog", "MSFT security research", "https://www.microsoft.com/en-us/security/blog/"),
        ("Google Security Blog", "Google security research", "https://security.googleblog.com/"),
        ("Apple Security Research", "Apple platform security", "https://security.apple.com/"),
    ],
    "AI & Offensive Tradecraft": [
        ("MITRE ATT&CK", "Adversary TTP knowledge base", "https://attack.mitre.org/"),
        ("MITRE ATLAS", "Adversarial threats to AI systems", "https://atlas.mitre.org/"),
        ("OWASP LLM Top 10", "LLM app security risks", "https://owasp.org/www-project-top-10-for-large-language-model-applications/"),
        ("LLM Security", "Prompt injection research", "https://llmsecurity.net/"),
        ("NIST AI RMF", "AI Risk Management Framework", "https://airc.nist.gov/"),
        ("AI Village", "DEF CON AI security community", "https://aivillage.org/"),
        ("Anthropic Research", "AI safety & alignment", "https://www.anthropic.com/research"),
        ("OpenAI Safety", "AI safety & alignment", "https://openai.com/safety"),
        ("Google DeepMind Safety", "AI safety research", "https://deepmind.google/safety/"),
        ("NIST AI", "AI standards & trustworthiness", "https://www.nist.gov/artificial-intelligence"),
    ],
}

RULES = [
    "Only test systems you own or have explicit, written permission to test.",
    "Unauthorized access is a crime in most of the world. Know your local law (e.g. CFAA, Computer Misuse Act).",
    "Found a real vulnerability? Disclose it responsibly to the owner — don't exploit, don't sell, don't sit on it.",
    "Everything here is for education, defense, authorized testing, and CTF. Use it to protect, not to harm.",
    "Be the kind of hacker the next generation is proud to learn from.",
]


@app.context_processor
def inject_globals():
    return dict(contact_email=CONTACT_EMAIL, year=datetime.now().year, site_name=SITE_NAME, owner=OWNER, tagline=TAGLINE, description=DESCRIPTION, nav=NAV)


@app.route("/")
def index():
    return render_template(
        "index.html", ethos=ETHOS, domains=DOMAINS, paths=PATHS, tools=TOOLS,
        practice=PRACTICE, glossary=GLOSSARY, feeds=FEEDS, rules=RULES,
    )


@app.route("/healthz")
def healthz():
    return jsonify(status="ok")


@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nAllow: /\n", mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
