"""
EVE Security Tools Module
Legitimate security and penetration testing tools for authorized use only.
"""

import socket
import asyncio
import re
import os
import subprocess
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import ssl
import struct
import json
from datetime import datetime
import dns.resolver
import whois
from urllib.parse import urlparse

@dataclass
class SecurityFinding:
    """Represents a security finding"""
    severity: str  # critical, high, medium, low, info
    category: str
    title: str
    description: str
    recommendation: str
    evidence: Dict[str, Any]

class SecurityTools:
    """
    Security testing tools for authorized penetration testing only.
    WARNING: Use only on systems you have explicit permission to test.
    """
    
    def __init__(self):
        self.findings: List[SecurityFinding] = []
    
    # ============= Network Scanning =============
    
    async def scan_ports(self, target: str, ports: List[int] = None) -> Dict[str, Any]:
        """
        Perform TCP port scanning on target.
        NOTE: Use only on systems you have permission to test.
        """
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 3389, 5432, 8080, 8443]
        
        results = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'open_ports': [],
            'closed_ports': [],
            'scan_type': 'TCP Connect'
        }
        
        common_ports = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            445: 'SMB',
            993: 'IMAPS',
            995: 'POP3S',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            8080: 'HTTP-Proxy',
            8443: 'HTTPS-Alt'
        }
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((target, port))
                sock.close()
                
                if result == 0:
                    service = common_ports.get(port, 'Unknown')
                    results['open_ports'].append({
                        'port': port,
                        'service': service,
                        'state': 'open'
                    })
                else:
                    results['closed_ports'].append(port)
                    
            except Exception as e:
                results['closed_ports'].append(port)
        
        return results
    
    async def scan_network(self, cidr: str) -> Dict[str, Any]:
        """
        Scan a network range for live hosts.
        NOTE: Use only on networks you have permission to test.
        """
        results = {
            'network': cidr,
            'timestamp': datetime.now().isoformat(),
            'live_hosts': []
        }
        
        # Basic ping sweep - extract network from CIDR
        # This is a simplified version
        return results
    
    # ============= Reconnaissance =============
    
    async def dns_lookup(self, domain: str) -> Dict[str, Any]:
        """Perform DNS lookup on a domain"""
        results = {
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'records': {}
        }
        
        try:
            # A records
            try:
                answers = dns.resolver.resolve(domain, 'A')
                results['records']['A'] = [str(rdata) for rdata in answers]
            except:
                pass
            
            # AAAA records
            try:
                answers = dns.resolver.resolve(domain, 'AAAA')
                results['records']['AAAA'] = [str(rdata) for rdata in answers]
            except:
                pass
            
            # MX records
            try:
                answers = dns.resolver.resolve(domain, 'MX')
                results['records']['MX'] = [str(rdata) for rdata in answers]
            except:
                pass
            
            # NS records
            try:
                answers = dns.resolver.resolve(domain, 'NS')
                results['records']['NS'] = [str(rdata) for rdata in answers]
            except:
                pass
            
            # TXT records
            try:
                answers = dns.resolver.resolve(domain, 'TXT')
                results['records']['TXT'] = [str(rdata) for rdata in answers]
            except:
                pass
                
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def whois_lookup(self, domain: str) -> Dict[str, Any]:
        """Perform WHOIS lookup"""
        results = {
            'domain': domain,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            w = whois.whois(domain)
            results['registrar'] = w.registrar
            results['creation_date'] = str(w.creation_date)
            results['expiration_date'] = str(w.expiration_date)
            results['name_servers'] = w.name_servers
            results['status'] = w.status
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    # ============= Web Analysis =============
    
    async def analyze_headers(self, url: str) -> Dict[str, Any]:
        """Analyze HTTP security headers"""
        results = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'headers': {},
            'security_headers': {},
            'findings': []
        }
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.head(url, allow_redirects=True) as response:
                    results['headers'] = dict(response.headers)
                    
                    # Check security headers
                    security_checks = {
                        'Strict-Transport-Security': 'HSTS enabled - good',
                        'Content-Security-Policy': 'CSP configured - good',
                        'X-Content-Type-Options': 'Prevents MIME sniffing',
                        'X-Frame-Options': 'Clickjacking protection',
                        'X-XSS-Protection': 'XSS filter enabled',
                        'Referrer-Policy': 'Referrer policy set',
                        'Permissions-Policy': 'Feature permissions set'
                    }
                    
                    for header, description in security_checks.items():
                        if header in response.headers:
                            results['security_headers'][header] = {
                                'present': True,
                                'value': response.headers[header],
                                'description': description
                            }
                        else:
                            results['security_headers'][header] = {
                                'present': False,
                                'description': description,
                                'severity': 'medium'
                            }
                            results['findings'].append({
                                'severity': 'medium',
                                'title': f'Missing {header}',
                                'description': description
                            })
                            
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    async def ssl_analysis(self, hostname: str, port: int = 443) -> Dict[str, Any]:
        """Analyze SSL/TLS configuration"""
        results = {
            'hostname': hostname,
            'port': port,
            'timestamp': datetime.now().isoformat(),
            'certificate': {},
            'tls_version': None,
            'cipher_suites': [],
            'findings': []
        }
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    results['tls_version'] = ssock.version()
                    results['cipher'] = ssock.cipher()
                    
                    # Parse certificate
                    results['certificate'] = {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': cert.get('version'),
                        'notBefore': cert.get('notBefore'),
                        'notAfter': cert.get('notAfter'),
                        'serialNumber': cert.get('serialNumber')
                    }
                    
                    # Check expiration
                    not_after = datetime.strptime(cert.get('notAfter'), '%b %d %H:%M:%S %Y %Z')
                    days_remaining = (not_after - datetime.now()).days
                    
                    if days_remaining < 0:
                        results['findings'].append({
                            'severity': 'critical',
                            'title': 'SSL Certificate Expired',
                            'description': f'Certificate expired {abs(days_remaining)} days ago'
                        })
                    elif days_remaining < 30:
                        results['findings'].append({
                            'severity': 'high',
                            'title': 'SSL Certificate Expiring Soon',
                            'description': f'Certificate expires in {days_remaining} days'
                        })
                        
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    # ============= Password Security =============
    
    def analyze_password_strength(self, password: str) -> Dict[str, Any]:
        """Analyze password strength"""
        results = {
            'length': len(password),
            'score': 0,
            'strength': 'very_weak',
            'feedback': []
        }
        
        # Length check
        if len(password) >= 8:
            results['score'] += 1
        else:
            results['feedback'].append('Password should be at least 8 characters')
        
        if len(password) >= 12:
            results['score'] += 1
            
        if len(password) >= 16:
            results['score'] += 1
        
        # Character variety
        if re.search(r'[a-z]', password):
            results['score'] += 1
        else:
            results['feedback'].append('Add lowercase letters')
            
        if re.search(r'[A-Z]', password):
            results['score'] += 1
        else:
            results['feedback'].append('Add uppercase letters')
            
        if re.search(r'\d', password):
            results['score'] += 1
        else:
            results['feedback'].append('Add numbers')
            
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            results['score'] += 1
        else:
            results['feedback'].append('Add special characters')
        
        # Determine strength
        if results['score'] >= 6:
            results['strength'] = 'very_strong'
        elif results['score'] >= 4:
            results['strength'] = 'strong'
        elif results['score'] >= 3:
            results['strength'] = 'medium'
        elif results['score'] >= 2:
            results['strength'] = 'weak'
        
        return results
    
    def identify_hash(self, hash_value: str) -> Dict[str, Any]:
        """Identify hash type"""
        results = {
            'hash': hash_value,
            'type': 'unknown',
            'length': len(hash_value)
        }
        
        hash_length = len(hash_value)
        
        # MD5 (32 hex chars)
        if hash_length == 32 and re.match(r'^[a-fA-F0-9]{32}$', hash_value):
            results['type'] = 'MD5'
            results['possible_uses'] = ['File checksums', 'Legacy storage']
            
        # SHA1 (40 hex chars)
        elif hash_length == 40 and re.match(r'^[a-fA-F0-9]{40}$', hash_value):
            results['type'] = 'SHA-1'
            results['possible_uses'] = ['Git commits', 'File integrity']
            
        # SHA256 (64 hex chars)
        elif hash_length == 64 and re.match(r'^[a-fA-F0-9]{64}$', hash_value):
            results['type'] = 'SHA-256'
            results['possible_uses'] = ['File integrity', 'Blockchain']
            
        # bcrypt (60 chars)
        elif hash_length == 60 and hash_value.startswith('$2'):
            results['type'] = 'bcrypt'
            results['possible_uses'] = ['Password hashing']
            
        # NTLM (32 hex chars - like MD5)
        elif hash_length == 32 and re.match(r'^[a-fA-F0-9]{32}$', hash_value):
            results['type'] = 'NTLM'
            results['possible_uses'] = ['Windows authentication']
            
        return results
    
    # ============= Report Generation =============
    
    def generate_report(self, findings: List[Dict], target: str) -> str:
        """Generate a penetration test report"""
        report = f"""
================================================================================
                         PENETRATION TEST REPORT
================================================================================

Target: {target}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generated by: EVE AI Security Assistant

================================================================================
                              FINDINGS SUMMARY
================================================================================

"""
        # Group by severity
        severity_order = ['critical', 'high', 'medium', 'low', 'info']
        severity_counts = {s: 0 for s in severity_order}
        
        for finding in findings:
            severity = finding.get('severity', 'info')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        report += "Severity Breakdown:\n"
        for sev in severity_order:
            count = severity_counts.get(sev, 0)
            if count > 0:
                report += f"  [{sev.upper():8}] {count} finding(s)\n"
        
        report += f"\nTotal Findings: {len(findings)}\n"
        
        report += """
================================================================================
                            DETAILED FINDINGS
================================================================================

"""
        
        for i, finding in enumerate(findings, 1):
            report += f"""
-------------------------------------------------------------------------------
Finding #{i}: {finding.get('title', 'Untitled')}
-------------------------------------------------------------------------------
Severity:      {finding.get('severity', 'N/A').upper()}
Category:     {finding.get('category', 'N/A')}
Description:  {finding.get('description', 'No description')}
"""
            if 'recommendation' in finding:
                report += f"Recommendation: {finding['recommendation']}\n"
        
        report += """
================================================================================
                              END OF REPORT
================================================================================

NOTE: This report was generated for authorized security testing only.
      Use only on systems you have explicit permission to test.
================================================================================
"""
        return report

# ============= Tool Registry =============

SECURITY_TOOLS = {
    'port_scan': {
        'name': 'Port Scanner',
        'description': 'Scan target for open ports',
        'category': 'network',
        'params': ['target', 'ports']
    },
    'dns_lookup': {
        'name': 'DNS Lookup',
        'description': 'Perform DNS enumeration',
        'category': 'recon',
        'params': ['domain']
    },
    'whois_lookup': {
        'name': 'WHOIS Lookup',
        'description': 'Domain registration information',
        'category': 'recon',
        'params': ['domain']
    },
    'header_analysis': {
        'name': 'Security Headers',
        'description': 'Analyze HTTP security headers',
        'category': 'web',
        'params': ['url']
    },
    'ssl_analysis': {
        'name': 'SSL/TLS Analysis',
        'description': 'Certificate and TLS configuration',
        'category': 'web',
        'params': ['hostname', 'port']
    },
    'password_strength': {
        'name': 'Password Analyzer',
        'description': 'Password strength analysis',
        'category': 'security',
        'params': ['password']
    },
    'hash_identify': {
        'name': 'Hash Identifier',
        'description': 'Identify hash type',
        'category': 'security',
        'params': ['hash']
    }
}

# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        tools = SecurityTools()
        
        # Example: Analyze security headers
        print("=== Security Header Analysis ===")
        result = await tools.analyze_headers("https://example.com")
        print(json.dumps(result, indent=2))
        
        print("\n=== Password Strength ===")
        result = tools.analyze_password_strength("MySecureP@ss123!")
        print(json.dumps(result, indent=2))
        
        print("\n=== Hash Identification ===")
        result = tools.identify_hash("5d41402abc4b2a76b9719d911017c592")
        print(json.dumps(result, indent=2))
    
    asyncio.run(main())
