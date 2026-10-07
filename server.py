import os
from datetime import datetime
from flask import Flask, render_template, jsonify, Response

app = Flask(__name__)

SITE_NAME = "Learn With Iss"
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "contact@example.com")  # Render > Environment এ নিজের ইমেইল দিন
OWNER = "Muhib Ibrahim"
TAGLINE = f"A Cybersecurity Learning Hub by {OWNER}"
DESCRIPTION = (
    f"{SITE_NAME} is a cybersecurity learning hub curated by {OWNER}: ten core security domains, structured study roadmaps, "
    "essential tools, legal practice labs and trusted threat-intelligence sources."
)

NAV = [
    ("welcome", "Welcome"), ("knowledge", "Knowledge"), ("paths", "Roadmaps"),
    ("arsenal", "Tools"), ("practice", "Labs"), ("glossary", "Terms"),
    ("intel", "News Feeds"), ("rules", "Rules"), ("legal", "Legal"),
]

ETHOS = [
    ("🧠", "Stay curious", "Great security work starts with one question: how does this really work? Explore, experiment and take systems apart in environments built for it."),
    ("🤝", "Share what you learn", "The security community grows through open write-ups, tools and mentoring. Whatever you gain, give something back."),
    ("🛡️", "Act responsibly", "Skill without integrity causes harm. Test only what you own or are authorized to assess, and report findings the right way."),
    ("♾️", "Keep improving", "Threats evolve every day. Lasting expertise comes from building the habit of continuous learning, not from memorizing answers."),
]

DOMAINS = [
    ("🕸️", "Web Application Security", "Websites and APIs are the most exposed layer of modern systems. Learn how the browser, server and backend can each be misused.",
     ["Injection flaws: SQL, OS command, template and LDAP", "Cross-site scripting (stored, reflected, DOM) and CSP weaknesses", "SSRF, IDOR, authentication and access-control failures", "Request smuggling, insecure deserialization, unsafe file uploads"],
     [("OWASP Top 10", "https://owasp.org/www-project-top-ten/"), ("PortSwigger Web Security Academy", "https://portswigger.net/web-security"), ("OWASP Cheat Sheets", "https://cheatsheetseries.owasp.org/")]),
    ("🌐", "Network & Infrastructure", "Understanding how traffic flows reveals where networks are weak. Protocols often expose far more than administrators expect.",
     ["Host discovery, port scanning and service fingerprinting", "Tunneling, pivoting and lateral movement", "Man-in-the-middle, ARP and DNS spoofing, protocol abuse", "Basics of firewall and IDS/IPS evasion"],
     [("Nmap Reference", "https://nmap.org/book/man.html"), ("HackTricks — Pentesting", "https://book.hacktricks.xyz/"), ("Wireshark Docs", "https://www.wireshark.org/docs/")]),
    ("🧬", "Binary Exploitation & Reverse Engineering", "Study how software behaves at the machine level, how memory is managed, and how mistakes in it become vulnerabilities.",
     ["Stack overflows, ROP chains and format-string bugs", "Heap corruption and use-after-free flaws", "Static analysis, dynamic analysis and debugging", "Disassembly and decompilation workflows"],
     [("Nightmare (heap/pwn course)", "https://guyinatuxedo.github.io/"), ("Ghidra", "https://ghidra-sre.org/"), ("pwn.college", "https://pwn.college/")]),
    ("🔐", "Cryptography", "Never invent your own cipher. Instead, learn how well-known schemes fail when they are implemented or used incorrectly.",
     ["Symmetric and asymmetric algorithms and their modes", "Padding oracles, length extension and nonce reuse", "Hash functions, password cracking and rainbow tables", "TLS, PKI and the points where trust breaks down"],
     [("Cryptopals Challenges", "https://cryptopals.com/"), ("Crypto 101", "https://www.crypto101.io/"), ("NIST CSRC", "https://csrc.nist.gov/")]),
    ("🔎", "OSINT & Reconnaissance", "Information gathering is a quiet but decisive phase. A surprising amount of data about any target is already public.",
     ["Domain, DNS, certificate transparency and subdomain discovery", "Organization and people footprinting, document metadata", "Leaked credentials and breach exposure", "Finding exposed cloud assets and storage buckets"],
     [("OSINT Framework", "https://osintframework.com/"), ("crt.sh — cert transparency", "https://crt.sh/"), ("Shodan", "https://www.shodan.io/")]),
    ("⬆️", "Privilege Escalation & Post-Exploitation", "Initial access is only the beginning. The real skill lies in understanding how far an intruder can go and what they could reach.",
     ["Privilege escalation on Linux and Windows", "Credential theft and token abuse", "Persistence and defense evasion (lab environments only)", "Attack paths in Active Directory"],
     [("GTFOBins", "https://gtfobins.github.io/"), ("LOLBAS", "https://lolbas-project.github.io/"), ("PayloadsAllTheThings", "https://github.com/swisskyrepo/PayloadsAllTheThings")]),
    ("📡", "Wireless & Hardware Security", "Radio signals, firmware and physical ports form an attack surface that you can literally hold in your hands.",
     ["Wi-Fi security (WPA2/WPA3) and handshake analysis", "Bluetooth, RFID/NFC and software-defined radio basics", "Firmware extraction and analysis", "UART/JTAG interfaces and embedded debugging"],
     [("Hak5", "https://hak5.org/"), ("OpenWrt", "https://openwrt.org/"), ("Firmware Analysis (OWASP)", "https://owasp.org/www-project-firmware-security-testing-methodology/")]),
    ("☁️", "Cloud & Container Security", "In the cloud, identity and access management is the new perimeter, and misconfiguration is the most common weakness.",
     ["IAM misconfigurations and privilege-escalation paths", "Exposed storage and metadata-service SSRF", "Container breakout and Kubernetes attack surface", "CI/CD pipeline and software supply-chain risk"],
     [("HackTricks Cloud", "https://cloud.hacktricks.xyz/"), ("CIS Benchmarks", "https://www.cisecurity.org/cis-benchmarks"), ("Kubernetes Security", "https://kubernetes.io/docs/concepts/security/")]),
    ("🤖", "AI & LLM Security", "AI models are software too, and they bring their own class of vulnerabilities that security teams are only starting to map.",
     ["Direct and indirect prompt injection", "Jailbreaks, data leakage and tool misuse", "Training-data poisoning and AI supply-chain risk", "Model theft and adversarial inputs"],
     [("OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/"), ("MITRE ATLAS", "https://atlas.mitre.org/"), ("LLM Security", "https://llmsecurity.net/")]),
    ("🎭", "Social Engineering", "People are part of every system. Study these techniques only with consent, a defined scope and a defensive goal.",
     ["Pretexting and phishing: recognition and defense", "OSINT-based target profiling (authorized engagements only)", "Physical security concepts such as tailgating", "Security-awareness training and organizational resilience"],
     [("SANS Security Awareness", "https://www.sans.org/security-awareness-training/"), ("NIST Phishing Guidance", "https://csrc.nist.gov/"), ("Social-Engineer.org", "https://www.social-engineer.org/")]),
]

PATHS = [
    ("Foundations", "A starting point for complete beginners.", [
        "Get comfortable with Linux: shell, file permissions and processes", "Understand networking: TCP/IP, DNS, HTTP and ports",
        "Choose a language: Python for tooling, then basic C", "Build a home lab with a VM, Kali or Parrot, and a practice target",
        "Complete OverTheWire Bandit and TryHackMe Pre-Security"]),
    ("Core Offense", "Develop practical attacker skills within ethical limits.", [
        "Finish the PortSwigger Web Security Academy from start to end", "Practice reconnaissance with nmap, enumeration and OSINT",
        "Solve machines on Hack The Box and TryHackMe", "Study the OWASP Top 10 and reproduce each category in your lab",
        "Keep notes and publish write-ups; it speeds up learning dramatically"]),
    ("Specialize", "Follow your interests and build depth.", [
        "Select a focus area: web, binary, cloud, AI or Active Directory", "Join CTF competitions (check CTFtime for schedules)",
        "Use MITRE ATT&CK to understand how real adversaries operate", "Contribute through bug bounties, open-source tools and write-ups",
        "Learn defensive security as well; it makes you a stronger attacker"]),
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
    ("PortSwigger Web Security Academy", "Free, high-quality web security labs", "https://portswigger.net/web-security"),
    ("Hack The Box", "Live machines and advanced pro labs", "https://www.hackthebox.com/"),
    ("TryHackMe", "Guided rooms suited to beginners", "https://tryhackme.com/"),
    ("picoCTF", "Entry-level CTF from Carnegie Mellon University", "https://picoctf.org/"),
    ("OverTheWire", "Classic command-line wargames", "https://overthewire.org/wargames/"),
    ("VulnHub", "Downloadable intentionally vulnerable VMs", "https://www.vulnhub.com/"),
    ("pwn.college", "Systems security and binary exploitation", "https://pwn.college/"),
    ("Cryptopals", "Practical cryptographic attack exercises", "https://cryptopals.com/"),
    ("Root-Me", "Large library of security challenges", "https://www.root-me.org/"),
    ("CTFtime", "Calendar of upcoming CTF events", "https://ctftime.org/"),
]

GLOSSARY = [
    ("0-day", "A flaw that is unknown to the vendor and has no patch, leaving defenders no time to prepare."),
    ("CVE", "Common Vulnerabilities and Exposures: a standard identifier for a publicly disclosed vulnerability."),
    ("Payload", "The component of an exploit that carries out the attacker's intended action."),
    ("Pivot", "Using one compromised system as a stepping stone to reach otherwise unreachable networks."),
    ("Recon", "Reconnaissance: collecting information about a target before any engagement begins."),
    ("RCE", "Remote Code Execution: the ability to run arbitrary code on a system over a network."),
    ("PrivEsc", "Privilege escalation: moving from limited access to administrator or root rights."),
    ("C2", "Command and Control: the infrastructure an operator uses to manage compromised systems."),
    ("Bug Bounty", "A program that rewards researchers for responsibly reporting security flaws."),
    ("Responsible Disclosure", "Privately informing the owner of a flaw and allowing reasonable time to fix it."),
    ("Red Team", "The offensive side: emulating real attackers to test an organization's defenses."),
    ("Blue Team", "The defensive side: monitoring, incident response and system hardening."),
]

FEEDS = {
    "Threat Intel": [
        ("The Hacker News", "Latest security news and incident coverage", "https://thehackernews.com/"),
        ("BleepingComputer", "Reports on vulnerabilities, malware and ransomware", "https://www.bleepingcomputer.com/news/security/"),
        ("GBHackers", "Daily cyber news and pentesting topics", "https://gbhackers.com/"),
        ("Dark Reading", "In-depth enterprise security reporting", "https://www.darkreading.com/"),
        ("Krebs on Security", "Investigative cybercrime journalism", "https://krebsonsecurity.com/"),
        ("The Record", "News desk from Recorded Future", "https://therecord.media/"),
        ("SecurityWeek", "Daily cybersecurity news", "https://www.securityweek.com/"),
        ("Infosecurity Magazine", "Industry news and analysis", "https://www.infosecurity-magazine.com/"),
        ("Schneier on Security", "Expert commentary by Bruce Schneier", "https://www.schneier.com/"),
        ("WIRED Security", "Security and technology policy coverage", "https://www.wired.com/category/security/"),
        ("Hacker News", "Community-driven technology discussion", "https://news.ycombinator.com/"),
        ("Cisco Talos", "Threat research publications", "https://talosintelligence.com/"),
        ("Palo Alto Unit 42", "Threat intelligence and incident response", "https://unit42.paloaltonetworks.com/"),
    ],
    "Government & Official Advisories": [
        ("CISA Advisories", "Official US cybersecurity advisories", "https://www.cisa.gov/news-events/cybersecurity-advisories"),
        ("CISA Home", "US Cybersecurity and Infrastructure Security Agency", "https://www.cisa.gov/"),
        ("CISA Stop Ransomware", "Ransomware alerts and guidance", "https://www.cisa.gov/stopransomware/official-alerts-statements-cisa"),
        ("NSA Cybersecurity Guidance", "Advisories published by the NSA", "https://www.nsa.gov/press-room/cybersecurity-advisories-guidance/"),
        ("FIRST.org", "Global forum of incident response teams", "https://www.first.org/"),
        ("CERT/CC Vulnerability Notes", "Coordinated vulnerability disclosure notes", "https://www.kb.cert.org/vuls/"),
        ("NIST CSRC", "Computer security standards and publications", "https://csrc.nist.gov/"),
    ],
    "CVEs & Zero-Days": [
        ("NVD", "US National Vulnerability Database", "https://nvd.nist.gov/"),
        ("NVD CVE Search", "Look up any published CVE", "https://nvd.nist.gov/vuln/search"),
        ("MSRC", "Microsoft security updates and advisories", "https://msrc.microsoft.com/"),
        ("Huntr", "Bug bounty platform for AI/ML projects", "https://huntr.com/"),
    ],
    "Cloud Security": [
        ("AWS Security Blog", "Security updates from Amazon Web Services", "https://aws.amazon.com/blogs/security/"),
        ("Azure Security Blog", "Security updates from Microsoft Azure", "https://azure.microsoft.com/en-us/blog/category/security/"),
        ("Google Cloud Security", "Identity and security on Google Cloud", "https://cloud.google.com/blog/products/identity-security"),
        ("Cloudflare Security", "Edge security and DDoS insights", "https://blog.cloudflare.com/tag/security/"),
        ("Microsoft Security Blog", "Security research from Microsoft", "https://www.microsoft.com/en-us/security/blog/"),
        ("Google Security Blog", "Security research from Google", "https://security.googleblog.com/"),
        ("Apple Security Research", "Apple platform security research", "https://security.apple.com/"),
    ],
    "AI & Adversary Tradecraft": [
        ("MITRE ATT&CK", "Knowledge base of adversary tactics and techniques", "https://attack.mitre.org/"),
        ("MITRE ATLAS", "Threat matrix for AI systems", "https://atlas.mitre.org/"),
        ("OWASP LLM Top 10", "Top risks for LLM applications", "https://owasp.org/www-project-top-10-for-large-language-model-applications/"),
        ("LLM Security", "Research on prompt injection and related risks", "https://llmsecurity.net/"),
        ("NIST AI RMF", "Framework for managing AI risk", "https://airc.nist.gov/"),
        ("AI Village", "AI security community at DEF CON", "https://aivillage.org/"),
        ("Anthropic Research", "AI safety and alignment research", "https://www.anthropic.com/research"),
        ("OpenAI Safety", "AI safety and alignment research", "https://openai.com/safety"),
        ("Google DeepMind Safety", "AI safety research", "https://deepmind.google/safety/"),
        ("NIST AI", "AI standards and trustworthiness", "https://www.nist.gov/artificial-intelligence"),
    ],
}

RULES = [
    "Test only systems that you own or have clear, written authorization to assess.",
    "Unauthorized access is illegal in most countries. Learn the computer-crime laws that apply where you live.",
    "If you find a genuine vulnerability, report it privately to the owner. Do not exploit it, sell it or ignore it.",
    "All material on this site is for education, defense, authorized testing and CTF practice. Use it to protect, never to harm.",
    "Set the standard that the next generation of security professionals will want to follow.",
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
