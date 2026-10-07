import os
from flask import Flask, render_template, jsonify, Response

app = Flask(__name__)

SITE_NAME = "Learn With Iss"
OWNER = "Muhib Ibrahim"
TAGLINE = f"Your Cybersecurity Study Hub, curated by {OWNER}"
DESCRIPTION = (
    f"{SITE_NAME} brings together ten core security domains, clear learning roadmaps, key tools, "
    f"safe practice labs and reliable news sources, curated by {OWNER}."
)

NAV = [
    ("welcome", "Welcome"), ("knowledge", "Knowledge"), ("paths", "Roadmaps"),
    ("arsenal", "Tools"), ("practice", "Labs"), ("glossary", "Terms"),
    ("intel", "News Feeds"), ("rules", "Rules"),
]

ETHOS = [
    ("🔭", "Explore with curiosity", "Every strong security professional begins by asking how something actually works. Investigate, test and dismantle systems in spaces designed for safe experimentation."),
    ("🤝", "Pass knowledge forward", "This field advances because people publish write-ups, release tools and mentor others. Take what helps you and contribute back."),
    ("🛡️", "Work with integrity", "Technical ability without ethics becomes a liability. Assess only what you own or have permission to examine, and disclose issues responsibly."),
    ("🚀", "Never stop growing", "Attack techniques change constantly. Real expertise comes from a habit of ongoing study rather than from remembering fixed answers."),
]

DOMAINS = [
    ("🌐", "Web Application Security", "Web apps and APIs are the most visible part of any organization. Learn how weaknesses appear in the browser, the server and the data layer.",
     ["Injection bugs such as SQL, command, template and LDAP injection", "XSS in its stored, reflected and DOM forms, plus ways around CSP", "SSRF, IDOR and flaws in login and permission checks", "HTTP request smuggling, unsafe deserialization and risky upload handling"],
     [("OWASP Top 10", "https://owasp.org/www-project-top-ten/"), ("PortSwigger Web Security Academy", "https://portswigger.net/web-security"), ("OWASP Cheat Sheets", "https://cheatsheetseries.owasp.org/")]),
    ("🛰️", "Network & Infrastructure", "Knowing how data moves across a network shows you where it can be intercepted or abused. Many protocols reveal more than their operators realize.",
     ["Discovering hosts, open ports and running service versions", "Traffic tunneling, pivoting and moving between systems", "Interception attacks, ARP and DNS poisoning, protocol misuse", "Fundamentals of bypassing firewalls and intrusion detection"],
     [("Nmap Reference", "https://nmap.org/book/man.html"), ("HackTricks — Pentesting", "https://book.hacktricks.xyz/"), ("Wireshark Docs", "https://www.wireshark.org/docs/")]),
    ("⚙️", "Binary Exploitation & Reverse Engineering", "Look at software the way the processor does. Learn how memory works and how errors in handling it can be turned into security flaws.",
     ["Buffer overflows, return-oriented programming and format strings", "Heap bugs and use-after-free conditions", "Analyzing programs statically and while running, using debuggers", "Working with disassemblers and decompilers"],
     [("Nightmare (heap/pwn course)", "https://guyinatuxedo.github.io/"), ("Ghidra", "https://ghidra-sre.org/"), ("pwn.college", "https://pwn.college/")]),
    ("🔑", "Cryptography", "Writing your own encryption is a mistake. A better investment is understanding how respected algorithms break when they are used poorly.",
     ["How symmetric and public-key systems and their modes of operation work", "Padding oracle attacks, length extension and reused nonces", "Hashing, password recovery and precomputed tables", "TLS, public-key infrastructure and where trust fails"],
     [("Cryptopals Challenges", "https://cryptopals.com/"), ("Crypto 101", "https://www.crypto101.io/"), ("NIST CSRC", "https://csrc.nist.gov/")]),
    ("🔍", "OSINT & Reconnaissance", "Collecting information is the quiet stage that often decides the outcome. Much of what you need to know about a target is openly available.",
     ["Mapping domains, DNS records, certificate logs and subdomains", "Profiling organizations and individuals, reading file metadata", "Finding leaked credentials and data from breaches", "Locating cloud resources and open storage"],
     [("OSINT Framework", "https://osintframework.com/"), ("crt.sh — cert transparency", "https://crt.sh/"), ("Shodan", "https://www.shodan.io/")]),
    ("🔓", "Privilege Escalation & Post-Exploitation", "Gaining a foothold is just the first step. The craft is in learning how much more access can be gained and what is at risk once inside.",
     ["Raising privileges on Linux and Windows hosts", "Harvesting credentials and abusing access tokens", "Maintaining access and avoiding detection (lab use only)", "Common attack routes through Active Directory"],
     [("GTFOBins", "https://gtfobins.github.io/"), ("LOLBAS", "https://lolbas-project.github.io/"), ("PayloadsAllTheThings", "https://github.com/swisskyrepo/PayloadsAllTheThings")]),
    ("📶", "Wireless & Hardware Security", "Wireless signals, device firmware and exposed ports create a physical attack surface that is easy to overlook.",
     ["Analyzing Wi-Fi security, WPA2 and WPA3 captures", "Bluetooth, RFID and NFC, along with SDR fundamentals", "Pulling and examining firmware images", "Debugging devices through UART and JTAG"],
     [("Hak5", "https://hak5.org/"), ("OpenWrt", "https://openwrt.org/"), ("Firmware Analysis (OWASP)", "https://owasp.org/www-project-firmware-security-testing-methodology/")]),
    ("☁️", "Cloud & Container Security", "In cloud environments, the boundary is defined by who holds which permissions, and the typical failure is a setting that was configured wrongly.",
     ["Wrong IAM settings and routes to higher privileges", "Publicly exposed storage and SSRF against metadata services", "Escaping containers and the attack surface of Kubernetes", "Weak points in build pipelines and the software supply chain"],
     [("HackTricks Cloud", "https://cloud.hacktricks.xyz/"), ("CIS Benchmarks", "https://www.cisecurity.org/cis-benchmarks"), ("Kubernetes Security", "https://kubernetes.io/docs/concepts/security/")]),
    ("🤖", "AI & LLM Security", "Machine-learning models are programs too, and they introduce a fresh set of weaknesses that the industry is still cataloguing.",
     ["Prompt injection, both direct and through external content", "Jailbreaking, data extraction and misuse of connected tools", "Poisoned training data and compromised AI components", "Stealing models and crafting adversarial inputs"],
     [("OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/"), ("MITRE ATLAS", "https://atlas.mitre.org/"), ("LLM Security", "https://llmsecurity.net/")]),
    ("🎭", "Social Engineering", "Every system includes human beings. Explore these methods only with permission, a clear scope and the aim of improving defenses.",
     ["Recognizing and resisting pretexting and phishing", "Using open-source research to profile targets (authorized work only)", "Physical access ideas such as tailgating", "Running awareness programs that make organizations more resilient"],
     [("SANS Security Awareness", "https://www.sans.org/security-awareness-training/"), ("NIST Phishing Guidance", "https://csrc.nist.gov/"), ("Social-Engineer.org", "https://www.social-engineer.org/")]),
]

PATHS = [
    ("Foundations", "Where complete newcomers should begin.", [
        "Become comfortable with Linux, including the shell, permissions and processes", "Learn how networks work: TCP/IP, DNS, HTTP and ports",
        "Pick Python for building tools, then add some C", "Set up a lab with a virtual machine, Kali or Parrot, and a target to practice on",
        "Work through OverTheWire Bandit and the TryHackMe Pre-Security path"]),
    ("Core Offense", "Build hands-on attacking skills while staying ethical.", [
        "Complete the entire PortSwigger Web Security Academy", "Practice reconnaissance using nmap, enumeration and OSINT",
        "Take on Hack The Box and TryHackMe machines", "Read about the OWASP Top 10 and recreate every category in your own lab",
        "Document your work and write it up; this makes you learn much faster"]),
    ("Specialize", "Choose a direction and go deeper.", [
        "Decide on a track: web, binary, cloud, AI or Active Directory", "Enter CTF contests (CTFtime lists upcoming ones)",
        "Use MITRE ATT&CK to see how actual threat actors operate", "Get involved through bug bounties, open-source projects and published write-ups",
        "Study defense too, because it sharpens your offensive thinking"]),
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
    ("PortSwigger Web Security Academy", "Excellent free labs for web security", "https://portswigger.net/web-security"),
    ("Hack The Box", "Hosted machines and professional-level labs", "https://www.hackthebox.com/"),
    ("TryHackMe", "Step-by-step rooms that welcome beginners", "https://tryhackme.com/"),
    ("picoCTF", "Beginner-friendly CTF run by Carnegie Mellon", "https://picoctf.org/"),
    ("OverTheWire", "Traditional wargames played in the terminal", "https://overthewire.org/wargames/"),
    ("VulnHub", "Vulnerable virtual machines you can download", "https://www.vulnhub.com/"),
    ("pwn.college", "Learn systems security and exploitation", "https://pwn.college/"),
    ("Cryptopals", "Exercises that teach real crypto attacks", "https://cryptopals.com/"),
    ("Root-Me", "A wide range of security challenges", "https://www.root-me.org/"),
    ("CTFtime", "Schedule of CTF competitions worldwide", "https://ctftime.org/"),
]

GLOSSARY = [
    ("0-day", "A security hole the vendor does not know about yet, so no fix exists and defenders have had no time to respond."),
    ("CVE", "Common Vulnerabilities and Exposures: the shared ID system used to name known vulnerabilities."),
    ("Payload", "The portion of an exploit that performs the attacker's chosen action once the flaw is triggered."),
    ("Pivot", "Taking over one machine and using it to access networks you could not otherwise reach."),
    ("Recon", "Short for reconnaissance, the work of gathering information about a target ahead of time."),
    ("RCE", "Remote Code Execution: running code of your choice on another system across a network."),
    ("PrivEsc", "Privilege escalation: gaining administrator or root rights from a lower-level account."),
    ("C2", "Command and Control: the servers and tooling used to direct compromised machines."),
    ("Bug Bounty", "A scheme in which companies pay researchers who report vulnerabilities responsibly."),
    ("Responsible Disclosure", "Telling the affected owner about a flaw in private and giving them time to correct it."),
    ("Red Team", "The attacking group, which imitates genuine adversaries to evaluate defenses."),
    ("Blue Team", "The defending group, responsible for detection, response and system hardening."),
]

FEEDS = {
    "Threat Intel": [
        ("The Hacker News", "Up-to-date security news and incidents", "https://thehackernews.com/"),
        ("BleepingComputer", "Coverage of vulnerabilities, malware and ransomware", "https://www.bleepingcomputer.com/news/security/"),
        ("GBHackers", "Everyday cyber news and penetration-testing content", "https://gbhackers.com/"),
        ("Dark Reading", "Detailed reporting aimed at enterprise security", "https://www.darkreading.com/"),
        ("Krebs on Security", "Investigations into cybercrime", "https://krebsonsecurity.com/"),
        ("The Record", "Reporting from the Recorded Future newsroom", "https://therecord.media/"),
        ("SecurityWeek", "Security news published daily", "https://www.securityweek.com/"),
        ("Infosecurity Magazine", "Industry stories and analysis", "https://www.infosecurity-magazine.com/"),
        ("Schneier on Security", "Opinion and insight from Bruce Schneier", "https://www.schneier.com/"),
        ("WIRED Security", "Security stories with a policy angle", "https://www.wired.com/category/security/"),
        ("Hacker News", "Tech discussion driven by its community", "https://news.ycombinator.com/"),
        ("Cisco Talos", "Published threat research", "https://talosintelligence.com/"),
        ("Palo Alto Unit 42", "Threat intelligence and response work", "https://unit42.paloaltonetworks.com/"),
    ],
    "Government & Official Advisories": [
        ("CISA Advisories", "Cybersecurity advisories from the US government", "https://www.cisa.gov/news-events/cybersecurity-advisories"),
        ("CISA Home", "The US Cybersecurity and Infrastructure Security Agency", "https://www.cisa.gov/"),
        ("CISA Stop Ransomware", "Alerts and advice on ransomware", "https://www.cisa.gov/stopransomware/official-alerts-statements-cisa"),
        ("NSA Cybersecurity Guidance", "Advisories issued by the NSA", "https://www.nsa.gov/press-room/cybersecurity-advisories-guidance/"),
        ("FIRST.org", "Worldwide community of incident response teams", "https://www.first.org/"),
        ("CERT/CC Vulnerability Notes", "Notes from coordinated disclosure", "https://www.kb.cert.org/vuls/"),
        ("NIST CSRC", "Standards and publications on computer security", "https://csrc.nist.gov/"),
    ],
    "CVEs & Zero-Days": [
        ("NVD", "The US National Vulnerability Database", "https://nvd.nist.gov/"),
        ("NVD CVE Search", "Find any published CVE", "https://nvd.nist.gov/vuln/search"),
        ("MSRC", "Microsoft patches and security advisories", "https://msrc.microsoft.com/"),
        ("Huntr", "Bounties for finding bugs in AI/ML software", "https://huntr.com/"),
    ],
    "Cloud Security": [
        ("AWS Security Blog", "Security posts from Amazon Web Services", "https://aws.amazon.com/blogs/security/"),
        ("Azure Security Blog", "Security posts from Microsoft Azure", "https://azure.microsoft.com/en-us/blog/category/security/"),
        ("Google Cloud Security", "Identity and security news for Google Cloud", "https://cloud.google.com/blog/products/identity-security"),
        ("Cloudflare Security", "Edge protection and DDoS analysis", "https://blog.cloudflare.com/tag/security/"),
        ("Microsoft Security Blog", "Research published by Microsoft", "https://www.microsoft.com/en-us/security/blog/"),
        ("Google Security Blog", "Research published by Google", "https://security.googleblog.com/"),
        ("Apple Security Research", "Research on Apple platform security", "https://security.apple.com/"),
    ],
    "AI & Adversary Tradecraft": [
        ("MITRE ATT&CK", "A catalog of attacker tactics and techniques", "https://attack.mitre.org/"),
        ("MITRE ATLAS", "A matrix of threats against AI systems", "https://atlas.mitre.org/"),
        ("OWASP LLM Top 10", "The leading risks in LLM-based apps", "https://owasp.org/www-project-top-10-for-large-language-model-applications/"),
        ("LLM Security", "Studies on prompt injection and similar threats", "https://llmsecurity.net/"),
        ("NIST AI RMF", "A framework for handling AI risk", "https://airc.nist.gov/"),
        ("AI Village", "The AI security community at DEF CON", "https://aivillage.org/"),
        ("Anthropic Research", "Work on AI safety and alignment", "https://www.anthropic.com/research"),
        ("OpenAI Safety", "Work on AI safety and alignment", "https://openai.com/safety"),
        ("Google DeepMind Safety", "Research on AI safety", "https://deepmind.google/safety/"),
        ("NIST AI", "Standards for trustworthy AI", "https://www.nist.gov/artificial-intelligence"),
    ],
}

RULES = [
    "Only assess systems you own, or those for which you hold explicit written permission.",
    "Breaking into systems without permission is a crime in most countries, so study the laws where you live.",
    "When you discover a real vulnerability, tell the owner privately rather than exploiting it, selling it or sitting on it.",
    "Everything on this site exists for learning, defense, authorized testing and CTF play. Use it to protect people, not to hurt them.",
    "Aim to be the kind of professional that newcomers look up to.",
]


@app.context_processor
def inject_globals():
    return dict(site_name=SITE_NAME, owner=OWNER, tagline=TAGLINE, description=DESCRIPTION, nav=NAV)


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
