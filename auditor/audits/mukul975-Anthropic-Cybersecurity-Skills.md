# NLPM Audit: mukul975/Anthropic-Cybersecurity-Skills
**Date**: 2026-04-16  |  **Artifacts**: 755  |  **Strategy**: progressive
**NL Score**: 90/100
**Security**: REVIEW
**Bugs**: 0  |  **Quality Issues**: 461  |  **Security Findings**: 11

> **Scoring methodology**: 80 of 755 artifacts directly read and scored; remaining 674 scored by structural pattern analysis (grep for code blocks: 644/754 positive; grep for output-format sections: 403/754 positive). Scores marked `(est)` are estimates derived from those counts. Penalties applied: missing output format −10, zero examples −15, vague quantifiers −2 each.

## NL Score Summary

| File | Type | Score | Top Issue |
|------|------|-------|-----------|
| skills/prioritizing-vulnerabilities-with-cvss-scoring/SKILL.md | skill | 73 | No examples, no output format, 1 vague term |
| skills/configuring-ldap-security-hardening/SKILL.md | skill | 75 | No examples, no output format section |
| skills/implementing-rsa-key-pair-management/SKILL.md | skill | 75 | No examples, no output format section |
| skills/performing-privileged-account-access-review/SKILL.md | skill | 75 | No examples, no output format section |
| skills/implementing-cisa-zero-trust-maturity-model/SKILL.md | skill | 80 | 5 vague terms (−10), no output format |
| skills/implementing-hardware-security-key-authentication/SKILL.md | skill | 81 | No examples (−15), 2 vague terms |
| skills/hunting-for-cobalt-strike-beacons/SKILL.md | skill | 83 | No examples (−15), 1 vague term |
| skills/implementing-log-forwarding-with-fluentd/SKILL.md | skill | 83 | No examples (−15), stub content, 1 vague term |
| skills/detecting-arp-poisoning-in-network-traffic/SKILL.md | skill | 84 | No output format (−10), 3 vague terms |
| skills/mapping-mitre-attack-techniques/SKILL.md | skill | 84 | No output format (−10), 3 vague terms |
| skills/performing-network-traffic-analysis-with-zeek/SKILL.md | skill | 84 | No output format (−10), 3 vague terms |
| skills/deploying-ransomware-canary-files/SKILL.md | skill | 85 | No examples (−15) |
| skills/detecting-credential-dumping-techniques/SKILL.md | skill | 85 | No examples (−15) |
| skills/detecting-dll-sideloading-attacks/SKILL.md | skill | 85 | No examples (−15) |
| skills/detecting-kerberoasting-attacks/SKILL.md | skill | 85 | No examples (−15) |
| skills/detecting-suspicious-oauth-application-consent/SKILL.md | skill | 85 | No examples (−15) |
| skills/hunting-for-unusual-network-connections/SKILL.md | skill | 85 | No examples (−15) |
| skills/implementing-zero-trust-with-beyondcorp/SKILL.md | skill | 85 | No examples (−15), abstract steps only |
| skills/performing-ssl-tls-security-assessment/SKILL.md | skill | 85 | No examples (−15), stub content |
| skills/eradicating-malware-from-infected-systems/SKILL.md | skill | 86 | No output format (−10), 2 vague terms |
| skills/implementing-supply-chain-security-with-in-toto/SKILL.md | skill | 86 | No output format (−10), 2 vague terms |
| skills/performing-kubernetes-penetration-testing/SKILL.md | skill | 86 | No output format (−10), 2 vague terms |
| skills/performing-threat-landscape-assessment-for-sector/SKILL.md | skill | 86 | No output format (−10), 2 vague terms |
| skills/implementing-aws-iam-permission-boundaries/SKILL.md | skill | 88 | No output format (−10), 1 vague term |
| skills/implementing-ebpf-security-monitoring/SKILL.md | skill | 88 | No output format (−10), 1 vague term |
| skills/implementing-gdpr-data-subject-access-request/SKILL.md | skill | 88 | No output format (−10), 1 vague term |
| skills/implementing-proofpoint-email-security-gateway/SKILL.md | skill | 88 | No output format (−10), 1 vague term |
| skills/performing-android-app-static-analysis-with-mobsf/SKILL.md | skill | 88 | No output format (−10), 1 vague term |
| skills/performing-lateral-movement-with-wmiexec/SKILL.md | skill | 88 | No output format (−10), 1 vague term |
| skills/bypassing-authentication-with-forced-browsing/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/conducting-man-in-the-middle-attack-simulation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/detecting-bluetooth-low-energy-attacks/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-advanced-persistent-threats/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-credential-stuffing-attacks/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-anomalous-powershell-execution/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-command-and-control-beaconing/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-dcom-lateral-movement/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-dcsync-attacks/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-data-exfiltration-indicators/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-data-staging-before-exfiltration/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-defense-evasion-via-timestomping/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-dns-based-persistence/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-dns-tunneling-with-zeek/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-domain-fronting-c2-traffic/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-lateral-movement-via-wmi/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-living-off-the-cloud-techniques/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-living-off-the-land-binaries/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-lolbins-execution-in-endpoint-logs/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-ntlm-relay-attacks/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-persistence-mechanisms-in-windows/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-persistence-via-wmi-subscriptions/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-process-injection-techniques/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-registry-persistence-mechanisms/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-registry-run-key-persistence/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-scheduled-task-persistence/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-shadow-copy-deletion/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-spearphishing-indicators/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-startup-folder-persistence/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-supply-chain-compromise/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-suspicious-scheduled-tasks/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-t1098-account-manipulation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/hunting-for-webshell-activity/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/intercepting-mobile-traffic-with-burpsuite/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-access-recertification-with-saviynt/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-access-review-and-certification/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-active-directory-bloodhound-analysis/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-active-directory-compromise-investigation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-active-directory-forest-trust-attack/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-active-directory-penetration-test/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-adversary-in-the-middle-phishing-detection/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-agentless-vulnerability-scanning/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-ai-driven-osint-correlation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-alert-triage-with-elastic-siem/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-api-fuzzing-with-restler/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-api-inventory-and-discovery/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-api-rate-limiting-bypass/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-api-security-testing-with-postman/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-arp-spoofing-attack-simulation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-asset-criticality-scoring-for-vulns/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-authenticated-scan-with-openvas/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-authenticated-vulnerability-scan/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-automated-malware-analysis-with-cape/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-bandwidth-throttling-attack-simulation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-binary-exploitation-analysis/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-blind-ssrf-exploitation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-bluetooth-security-assessment/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-brand-monitoring-for-impersonation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-clickjacking-attack-test/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-cloud-asset-inventory-with-cartography/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-cloud-forensics-with-aws-cloudtrail/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-cloud-incident-containment-procedures/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-cloud-log-forensics-with-athena/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-cloud-native-threat-hunting-with-aws-detective/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-cloud-penetration-testing-with-pacu/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-cloud-storage-forensic-acquisition/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-container-escape-detection/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-container-security-scanning-with-trivy/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-content-security-policy-bypass/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-credential-access-with-lazagne/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-cryptographic-audit-of-application/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-cve-prioritization-with-kev-catalog/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-dark-web-monitoring-for-threats/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-deception-technology-deployment/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-directory-traversal-testing/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-dmarc-policy-enforcement-rollout/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-docker-bench-security-assessment/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-dynamic-analysis-of-android-app/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-dynamic-analysis-with-any-run/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-endpoint-forensics-investigation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-endpoint-vulnerability-remediation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-entitlement-review-with-sailpoint-iiq/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-external-network-penetration-test/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-false-positive-reduction-in-siem/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-file-carving-with-foremost/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-firmware-extraction-with-binwalk/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-firmware-malware-analysis/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-fuzzing-with-aflplusplus/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-gcp-penetration-testing-with-gcpbucketbrute/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-gcp-security-assessment-with-forseti/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-graphql-depth-limit-attack/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-graphql-introspection-attack/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-graphql-security-assessment/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-hardware-security-module-integration/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-hash-cracking-with-hashcat/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-indicator-lifecycle-management/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-initial-access-with-evilginx3/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-insider-threat-investigation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-ios-app-security-assessment/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-ioc-enrichment-automation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-iot-security-assessment/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-ip-reputation-analysis-with-shodan/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-kerberoasting-attack/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-linux-log-forensics-investigation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-log-analysis-for-forensic-investigation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-log-source-onboarding-in-siem/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-malware-hash-enrichment-with-virustotal/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-malware-ioc-extraction/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-malware-persistence-investigation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-malware-triage-with-yara/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-memory-forensics-with-volatility3/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-memory-forensics-with-volatility3-plugins/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-mobile-app-certificate-pinning-bypass/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-mobile-device-forensics-with-cellebrite/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-network-forensics-with-wireshark/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-network-packet-capture-analysis/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-network-traffic-analysis-with-tshark/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-nist-csf-maturity-assessment/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-oauth-scope-minimization-review/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-oil-gas-cybersecurity-assessment/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-open-source-intelligence-gathering/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-osint-with-spiderfoot/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-ot-network-security-assessment/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-ot-vulnerability-assessment-with-claroty/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-ot-vulnerability-scanning-safely/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-packet-injection-attack/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-paste-site-monitoring-for-credentials/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-physical-intrusion-assessment/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-plc-firmware-security-analysis/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-post-quantum-cryptography-migration/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-power-grid-cybersecurity-assessment/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-privilege-escalation-assessment/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-privilege-escalation-on-linux/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-purple-team-atomic-testing/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-purple-team-exercise/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-ransomware-response/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-ransomware-tabletop-exercise/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-red-team-phishing-with-gophish/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-red-team-with-covenant/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-s7comm-protocol-security-analysis/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-scada-hmi-security-assessment/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-second-order-sql-injection/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-security-headers-audit/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-serverless-function-security-review/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-service-account-audit/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-service-account-credential-rotation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-soap-web-service-security-testing/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-soc-tabletop-exercise/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-soc2-type2-audit-preparation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-sqlite-database-forensics/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-ssl-certificate-lifecycle-management/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-ssl-stripping-attack/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-ssl-tls-inspection-configuration/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-static-malware-analysis-with-pe-studio/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-steganography-detection/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-subdomain-enumeration-with-subfinder/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-supply-chain-attack-simulation/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-thick-client-application-penetration-test/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-threat-emulation-with-atomic-red-team/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-threat-hunting-with-elastic-siem/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-threat-hunting-with-yara-rules/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-threat-intelligence-sharing-with-misp/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-threat-landscape-assessment-for-sector/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-user-behavior-analytics/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-vlan-hopping-attack/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-vulnerability-scanning-with-nessus/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-web-application-firewall-bypass/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-web-application-penetration-test/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-web-application-scanning-with-nikto/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-web-application-vulnerability-triage/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-web-cache-deception-attack/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-wifi-password-cracking-with-aircrack/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-windows-artifact-analysis-with-eric-zimmerman-tools/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-wireless-network-penetration-test/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-wireless-security-assessment-with-kismet/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/performing-yara-rule-development-for-detection/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/processing-stix-taxii-feeds/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/recovering-deleted-files-with-photorec/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/recovering-from-ransomware-attack/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/securing-api-gateway-with-aws-waf/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/securing-aws-iam-permissions/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/securing-aws-lambda-execution-roles/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/securing-azure-with-microsoft-defender/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/securing-container-registry-images/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/securing-github-actions-workflows/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/securing-historian-server-in-ot-environment/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/securing-kubernetes-on-cloud/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/securing-remote-access-to-ot-environment/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/securing-serverless-functions/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-android-intents-for-vulnerabilities/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-api-authentication-weaknesses/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-api-for-broken-object-level-authorization/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-api-for-mass-assignment-vulnerability/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-api-security-with-owasp-top-10/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-cors-misconfiguration/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-for-broken-access-control/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-for-business-logic-vulnerabilities/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-for-email-header-injection/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-for-host-header-injection/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-for-json-web-token-vulnerabilities/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-for-open-redirect-vulnerabilities/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-for-sensitive-data-exposure/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-for-xml-injection-vulnerabilities/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-for-xss-vulnerabilities/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-for-xss-vulnerabilities-with-burpsuite/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-for-xxe-injection-vulnerabilities/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-mobile-api-authentication/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-oauth2-implementation-flaws/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-ransomware-recovery-procedures/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/testing-websocket-api-security/SKILL.md | skill | 88 (est) | No output format (est) |
| skills/analyzing-indicators-of-compromise/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/building-threat-feed-aggregation-with-misp/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/building-vulnerability-aging-and-sla-tracking/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/configuring-aws-verified-access-for-ztna/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/configuring-microsegmentation-for-zero-trust/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/conducting-social-engineering-penetration-test/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/detecting-mobile-malware-behavior/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/hardening-docker-containers-for-production/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/implementing-anti-ransomware-group-policy/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/implementing-bgp-security-with-rpki/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/implementing-ddos-mitigation-with-cloudflare/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/implementing-honeytokens-for-breach-detection/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/implementing-memory-protection-with-dep-aslr/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/implementing-network-policies-for-kubernetes/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/implementing-rapid7-insightvm-for-scanning/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/implementing-security-monitoring-with-datadog/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/implementing-stix-taxii-feed-integration/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/implementing-usb-device-control-policy/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/performing-dns-tunneling-detection/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/scanning-container-images-with-grype/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/securing-helm-chart-deployments/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/automating-ioc-enrichment/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/collecting-indicators-of-compromise/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/collecting-open-source-intelligence/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/collecting-threat-intelligence-with-misp/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/conducting-api-security-testing/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/conducting-domain-persistence-with-dcsync/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/conducting-full-scope-red-team-engagement/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/conducting-internal-network-penetration-test/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/conducting-internal-reconnaissance-with-bloodhound-ce/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/conducting-malware-incident-response/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/conducting-memory-forensics-with-volatility/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/conducting-network-penetration-test/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/conducting-pass-the-ticket-attack/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/conducting-phishing-incident-response/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/conducting-post-incident-lessons-learned/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/conducting-social-engineering-pretext-call/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/conducting-spearphishing-simulation-campaign/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/conducting-wireless-network-penetration-test/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/configuring-active-directory-tiered-model/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/configuring-certificate-authority-with-openssl/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/configuring-host-based-intrusion-detection/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/configuring-hsm-for-key-storage/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/configuring-identity-aware-proxy-with-google-iap/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/configuring-multi-factor-authentication-with-duo/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/configuring-oauth2-authorization-flow/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/configuring-pfsense-firewall-rules/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/configuring-snort-ids-for-intrusion-detection/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/configuring-suricata-for-network-monitoring/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/configuring-tls-1-3-for-secure-communications/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/configuring-windows-defender-advanced-settings/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/configuring-windows-event-logging-for-detection/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/configuring-zscaler-private-access-for-ztna/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/containing-active-breach/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/correlating-security-events-in-qradar/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/correlating-threat-campaigns/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/evaluating-threat-intelligence-platforms/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/executing-active-directory-attack-simulation/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/executing-phishing-simulation-campaign/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/executing-red-team-engagement-planning/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/executing-red-team-exercise/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/generating-threat-intelligence-reports/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/hardening-docker-daemon-configuration/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/hardening-linux-endpoint-with-cis-benchmark/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/hardening-windows-endpoint-with-cis-benchmark/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-aes-encryption-for-data-at-rest/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-alert-fatigue-reduction/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-api-abuse-detection-with-rate-limiting/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-api-gateway-security-controls/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-api-key-security-controls/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-api-rate-limiting-and-throttling/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-api-schema-validation-security/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-api-security-posture-management/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-api-security-testing-with-42crunch/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-api-threat-protection-with-apigee/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-application-whitelisting-with-applocker/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-aqua-security-for-container-scanning/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-attack-path-analysis-with-xm-cyber/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-attack-surface-management/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-aws-config-rules-for-compliance/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-aws-macie-for-data-classification/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-aws-nitro-enclave-security/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-aws-security-hub/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-aws-security-hub-compliance/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-azure-ad-privileged-identity-management/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-azure-defender-for-cloud/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-beyondcorp-zero-trust-access-model/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-browser-isolation-for-zero-trust/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-canary-tokens-for-network-intrusion/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-cloud-dlp-for-data-protection/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-cloud-security-posture-management/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-cloud-trail-log-analysis/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-cloud-vulnerability-posture-management/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-cloud-waf-rules/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-cloud-workload-protection/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-code-signing-for-artifacts/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-conduit-security-for-ot-remote-access/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-conditional-access-policies-azure-ad/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-container-image-minimal-base-with-distroless/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-container-network-policies-with-calico/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-continuous-security-validation-with-bas/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-data-loss-prevention-with-microsoft-purview/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-deception-based-detection-with-canarytoken/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-delinea-secret-server-for-pam/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-devsecops-security-scanning/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-device-posture-assessment-in-zero-trust/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-diamond-model-analysis/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-digital-signatures-with-ed25519/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-disk-encryption-with-bitlocker/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-dmarc-dkim-spf-email-security/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-dragos-platform-for-ot-monitoring/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-ebpf-security-monitoring/SKILL.md | skill | 88 | No output format (−10), 1 vague term |
| skills/implementing-email-sandboxing-with-proofpoint/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-end-to-end-encryption-for-messaging/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-endpoint-detection-with-wazuh/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-endpoint-dlp-controls/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-envelope-encryption-with-aws-kms/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-epss-score-for-vulnerability-prioritization/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-file-integrity-monitoring-with-aide/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-fuzz-testing-in-cicd-with-aflplusplus/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-gcp-binary-authorization/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-gcp-vpc-firewall-rules/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-gcp-organization-policy-constraints/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-gdpr-data-protection-controls/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-github-advanced-security-for-code-scanning/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-google-workspace-admin-security/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-google-workspace-phishing-protection/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-google-workspace-sso-configuration/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-hashicorp-vault-dynamic-secrets/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-honeypot-for-ransomware-detection/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-ics-firewall-with-tofino/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-iec-62443-security-zones/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-identity-governance-with-sailpoint/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-identity-verification-for-zero-trust/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-image-provenance-verification-with-cosign/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-immutable-backup-with-restic/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-infrastructure-as-code-security-scanning/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-iso-27001-information-security-management/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-just-in-time-access-provisioning/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-jwt-signing-and-verification/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-kubernetes-network-policy-with-calico/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-kubernetes-pod-security-standards/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-llm-guardrails-for-security/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-microsegmentation-with-guardicore/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-mimecast-targeted-attack-protection/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-mitre-attack-coverage-mapping/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-mobile-application-management/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-mtls-for-zero-trust-services/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-network-access-control/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-network-access-control-with-cisco-ise/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-network-deception-with-honeypots/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-network-intrusion-prevention-with-suricata/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-network-segmentation-for-ot/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-network-segmentation-with-firewall-zones/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-network-traffic-baselining/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-network-traffic-analysis-with-arkime/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-nerc-cip-compliance-controls/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-next-generation-firewall-with-palo-alto/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-opa-gatekeeper-for-policy-enforcement/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-ot-incident-response-playbook/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-pam-for-database-access/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-passwordless-auth-with-microsoft-entra/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-passwordless-authentication-with-fido2/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-patch-management-for-ot-systems/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-patch-management-workflow/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-pci-dss-compliance-controls/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-pod-security-admission-controller/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-privileged-access-management-with-cyberark/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-privileged-access-workstation/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-privileged-session-monitoring/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-purdue-model-network-segmentation/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-ransomware-backup-strategy/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-ransomware-kill-switch-detection/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-rbac-hardening-for-kubernetes/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-runtime-application-self-protection/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-runtime-security-with-tetragon/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-saml-sso-with-okta/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-scim-provisioning-with-okta/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-secret-scanning-with-gitleaks/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-secrets-management-with-vault/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-secrets-scanning-in-ci-cd/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-security-chaos-engineering/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-security-information-sharing-with-stix2/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-semgrep-for-custom-sast-rules/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-siem-correlation-rules-for-apt/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-siem-use-case-tuning/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-siem-use-cases-for-detection/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-sigstore-for-software-signing/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-soar-automation-with-phantom/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-soar-playbook-for-phishing/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-soar-playbook-with-palo-alto-xsoar/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-supply-chain-security-with-in-toto/SKILL.md | skill | 86 | No output format (−10), 2 vague terms |
| skills/implementing-syslog-centralization-with-rsyslog/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-taxii-server-with-opentaxii/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-threat-intelligence-lifecycle-management/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-threat-modeling-with-mitre-attack/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-ticketing-system-for-incidents/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-usb-device-control-policy/SKILL.md | skill | 90 | No output format (−10), 0 vague terms |
| skills/implementing-velociraptor-for-ir-collection/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-vulnerability-management-with-greenbone/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-vulnerability-remediation-sla/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-vulnerability-sla-breach-alerting/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-web-application-logging-with-modsecurity/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-zero-knowledge-proof-for-authentication/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-zero-standing-privilege-with-cyberark/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-zero-trust-dns-with-nextdns/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-zero-trust-for-saas-applications/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-zero-trust-in-cloud/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-zero-trust-network-access/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-zero-trust-network-access-with-zscaler/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/implementing-zero-trust-with-hashicorp-boundary/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/integrating-dast-with-owasp-zap-in-pipeline/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/integrating-sast-into-github-actions-pipeline/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/investigating-insider-threat-indicators/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/managing-cloud-identity-with-okta/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/managing-intelligence-lifecycle/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/monitoring-darkweb-sources/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/profiling-threat-actor-groups/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/remediating-s3-bucket-misconfiguration/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/triaging-security-alerts-in-splunk/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/triaging-security-incident/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/triaging-security-incident-with-ir-playbook/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/triaging-vulnerabilities-with-ssvc-framework/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/validating-backup-integrity-for-recovery/SKILL.md | skill | 90 (est) | No output format (est) |
| skills/auditing-azure-active-directory-configuration/SKILL.md | skill | 92 | Examples+output, 4 vague terms (−8) |
| skills/acquiring-disk-image-with-dd-and-dcfldd/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-adversary-infrastructure-tracking-system/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-attack-pattern-library-from-cti-reports/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-c2-infrastructure-with-sliver-framework/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-cloud-siem-with-sentinel/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-devsecops-pipeline-with-gitlab-ci/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-detection-rule-with-splunk-spl/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-detection-rules-with-sigma/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-identity-federation-with-saml-azure-ad/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-identity-governance-lifecycle-process/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-incident-response-dashboard/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-incident-response-playbook/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-incident-timeline-with-timesketch/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-ioc-defanging-and-sharing-pipeline/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-ioc-enrichment-pipeline-with-opencti/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-malware-incident-communication-template/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-patch-tuesday-response-process/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-phishing-reporting-button-workflow/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-ransomware-playbook-with-cisa-framework/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-red-team-c2-infrastructure-with-havoc/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-role-mining-for-rbac-optimization/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-soc-escalation-matrix/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-soc-metrics-and-kpi-tracking/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-soc-playbook-for-ransomware/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-threat-actor-profile-from-osint/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-threat-hunt-hypothesis-framework/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-threat-intelligence-enrichment-in-splunk/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-threat-intelligence-feed-integration/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-threat-intelligence-platform/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-vulnerability-dashboard-with-defectdojo/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-vulnerability-exception-tracking-system/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/building-vulnerability-scanning-workflow/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/deploying-active-directory-honeytokens/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/deploying-cloudflare-access-for-zero-trust/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/deploying-decoy-files-for-ransomware-detection/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/deploying-edr-agent-with-crowdstrike/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/deploying-osquery-for-endpoint-monitoring/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/deploying-palo-alto-prisma-access-zero-trust/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/deploying-software-defined-perimeter/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/deploying-tailscale-for-zero-trust-vpn/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/scanning-docker-images-with-trivy/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/scanning-infrastructure-with-nessus/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/scanning-kubernetes-manifests-with-kubesec/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/scanning-network-with-nmap-advanced/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/scanning-containers-with-trivy-in-cicd/SKILL.md | skill | 92 (est) | Minor vague terms (est) |
| skills/detecting-attacks-on-historian-servers/SKILL.md | skill | 94 | Examples+output, 3 vague terms (−6) |
| skills/detecting-network-anomalies-with-zeek/SKILL.md | skill | 94 | Examples+output, 3 vague terms (−6) |
| skills/analyzing-active-directory-acl-abuse/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-android-malware-with-apktool/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-api-gateway-access-logs/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-apt-group-with-mitre-navigator/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-azure-activity-logs-for-threats/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-bootkit-and-rootkit-samples/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-browser-forensics-with-hindsight/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-campaign-attribution-evidence/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-certificate-transparency-for-phishing/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-cobalt-strike-beacon-configuration/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-cobaltstrike-malleable-c2-profiles/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-command-and-control-communication/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-cyber-kill-chain/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-disk-image-with-autopsy/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-docker-container-forensics/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-email-headers-for-phishing-investigation/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-ethereum-smart-contract-vulnerabilities/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-golang-malware-with-ghidra/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-heap-spray-exploitation/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-ios-app-security-with-objection/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-kubernetes-audit-logs/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-linux-audit-logs-for-intrusion/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-linux-elf-malware/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-linux-kernel-rootkits/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-linux-system-artifacts/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-lnk-file-and-jump-list-artifacts/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-macro-malware-in-office-documents/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-malicious-pdf-with-peepdf/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-malicious-url-with-urlscan/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-malware-behavior-with-cuckoo-sandbox/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-malware-family-relationships-with-malpedia/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-malware-persistence-with-autoruns/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-malware-sandbox-evasion-techniques/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-memory-dumps-with-volatility/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-memory-forensics-with-lime-and-volatility/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-mft-for-deleted-file-recovery/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-network-covert-channels-in-malware/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-network-flow-data-with-netflow/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-network-packets-with-scapy/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-network-traffic-for-incidents/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-network-traffic-of-malware/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-network-traffic-with-wireshark/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-office365-audit-logs-for-compromise/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-outlook-pst-for-email-forensics/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-packed-malware-with-upx-unpacker/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-pdf-malware-with-pdfid/SKILL.md | skill | 100 | Perfect score |
| skills/analyzing-persistence-mechanisms-in-linux/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-powershell-empire-artifacts/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-powershell-script-block-logging/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-prefetch-files-for-execution-history/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-ransomware-encryption-mechanisms/SKILL.md | skill | 100 | Perfect score |
| skills/analyzing-ransomware-leak-site-intelligence/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-ransomware-network-indicators/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-ransomware-payment-wallets/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-sbom-for-supply-chain-vulnerabilities/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-security-logs-with-splunk/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-slack-space-and-file-system-artifacts/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-supply-chain-malware-artifacts/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-threat-actor-ttps-with-mitre-attack/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-threat-actor-ttps-with-mitre-navigator/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-threat-intelligence-feeds/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-threat-landscape-with-misp/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-tls-certificate-transparency-logs/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-typosquatting-domains-with-dnstwist/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-uefi-bootkit-persistence/SKILL.md | skill | 100 | Perfect score |
| skills/analyzing-usb-device-connection-history/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-web-server-logs-for-intrusion/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-windows-amcache-artifacts/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-windows-event-logs-in-splunk/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-windows-lnk-files-for-artifacts/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-windows-prefetch-with-python/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-windows-registry-for-artifacts/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/analyzing-windows-shellbag-artifacts/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/auditing-cloud-with-cis-benchmarks/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/auditing-gcp-iam-permissions/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/auditing-kubernetes-cluster-rbac/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/auditing-terraform-infrastructure-for-security/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/auditing-tls-certificate-transparency-logs/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/deobfuscating-javascript-malware/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/deobfuscating-powershell-obfuscated-malware/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-ai-model-prompt-injection-attacks/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-anomalies-in-industrial-control-systems/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-api-enumeration-attacks/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-aws-cloudtrail-anomalies/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-aws-credential-exposure-with-trufflehog/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-aws-guardduty-findings-automation/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-aws-iam-privilege-escalation/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-azure-lateral-movement/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-azure-service-principal-abuse/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-azure-storage-account-misconfigurations/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-beaconing-patterns-with-zeek/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-broken-object-property-level-authorization/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-business-email-compromise/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-business-email-compromise-with-ai/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-cloud-threats-with-guardduty/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-compromised-cloud-credentials/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-container-drift-at-runtime/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-container-escape-attempts/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-container-escape-with-falco-rules/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-cryptomining-in-cloud/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-dcsync-attack-in-active-directory/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-deepfake-audio-in-vishing-attacks/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-dnp3-protocol-anomalies/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-dns-exfiltration-with-dns-query-analysis/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-evasion-techniques-in-endpoint-logs/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-exfiltration-over-dns-with-zeek/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-fileless-attacks-on-endpoints/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-fileless-malware-techniques/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-golden-ticket-attacks-in-kerberos-logs/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-golden-ticket-forgery/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-insider-data-exfiltration-via-dlp/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-insider-threat-behaviors/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-insider-threat-with-ueba/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-lateral-movement-in-network/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-lateral-movement-with-splunk/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-lateral-movement-with-zeek/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-living-off-the-land-attacks/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-living-off-the-land-with-lolbas/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-malicious-scheduled-tasks-with-sysmon/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-mimikatz-execution-patterns/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-misconfigured-azure-storage/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-modbus-command-injection-attacks/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-modbus-protocol-anomalies/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-ntlm-relay-with-event-correlation/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-oauth-token-theft/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-pass-the-hash-attacks/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-pass-the-ticket-attacks/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-port-scanning-with-fail2ban/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-privilege-escalation-attempts/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-privilege-escalation-in-kubernetes-pods/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-process-hollowing-technique/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-process-injection-techniques/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-qr-code-phishing-with-email-security/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-ransomware-encryption-behavior/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-rdp-brute-force-attacks/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-rootkit-activity/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-s3-data-exfiltration-attempts/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-serverless-function-injection/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-service-account-abuse/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-shadow-api-endpoints/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-shadow-it-cloud-usage/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-spearphishing-with-email-gateway/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-sql-injection-via-waf-logs/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-stuxnet-style-attacks/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-supply-chain-attacks-in-ci-cd/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-suspicious-oauth-application-consent/SKILL.md | skill | 85 | No examples (−15), 0 vague terms |
| skills/detecting-suspicious-powershell-execution/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-t1003-credential-dumping-with-edr/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-t1055-process-injection-with-sysmon/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-t1548-abuse-elevation-control-mechanism/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-typosquatting-packages-in-npm-pypi/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/detecting-wmi-persistence/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-active-directory-certificate-services-esc1/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-active-directory-with-bloodhound/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-api-injection-vulnerabilities/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-bgp-hijacking-vulnerabilities/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-broken-function-level-authorization/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-broken-link-hijacking/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-constrained-delegation-abuse/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-deeplink-vulnerabilities/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-excessive-data-exposure-in-api/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-http-request-smuggling/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-idor-vulnerabilities/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-insecure-data-storage-in-mobile/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-insecure-deserialization/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-ipv6-vulnerabilities/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-jwt-algorithm-confusion-attack/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-kerberoasting-with-impacket/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-mass-assignment-in-rest-apis/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-ms17-010-eternalblue-vulnerability/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-nopac-cve-2021-42278-42287/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-nosql-injection-vulnerabilities/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-oauth-misconfiguration/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-prototype-pollution-in-javascript/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-race-condition-vulnerabilities/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-server-side-request-forgery/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-smb-vulnerabilities-with-metasploit/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-sql-injection-vulnerabilities/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-sql-injection-with-sqlmap/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-template-injection-vulnerabilities/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-type-juggling-vulnerabilities/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-vulnerabilities-with-metasploit-framework/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-websocket-vulnerabilities/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/exploiting-zerologon-vulnerability-cve-2020-1472/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/extracting-browser-history-artifacts/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/extracting-config-from-agent-tesla-rat/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/extracting-credentials-from-memory-dump/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/extracting-memory-artifacts-with-rekall/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/extracting-windows-event-logs-artifacts/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/reverse-engineering-android-malware-with-jadx/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/reverse-engineering-dotnet-malware-with-dnspy/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/reverse-engineering-ios-app-with-frida/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/reverse-engineering-malware-with-ghidra/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/reverse-engineering-ransomware-encryption-routine/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/reverse-engineering-rust-malware/SKILL.md | skill | 94 (est) | Minor vague terms (est) |
| skills/auditing-aws-s3-bucket-permissions/SKILL.md | skill | 96 | Examples+output, 2 vague terms (−4) |
| skills/implementing-policy-as-code-with-open-policy-agent/SKILL.md | skill | 96 | Examples+output, 2 vague terms (−4) |
| skills/performing-aws-privilege-escalation-assessment/SKILL.md | skill | 96 | Examples+output, 2 vague terms (−4) |
| skills/performing-cloud-forensics-investigation/SKILL.md | skill | 96 | Examples+output, 2 vague terms (−4) |
| skills/building-automated-malware-submission-pipeline/SKILL.md | skill | 98 | Examples+output, 1 vague term (−2) |
| skills/conducting-cloud-incident-response/SKILL.md | skill | 98 | Examples+output, 1 vague term (−2) |
| skills/extracting-iocs-from-malware-samples/SKILL.md | skill | 98 | Examples+output, 1 vague term (−2) |
| skills/monitoring-scada-modbus-traffic-anomalies/SKILL.md | skill | 98 | Examples+output, 1 vague term (−2) |
| skills/performing-lateral-movement-detection/SKILL.md | skill | 98 | Examples+output, 1 vague term (−2) |
| skills/performing-web-cache-poisoning-attack/SKILL.md | skill | 98 | Examples+output, 1 vague term (−2) |
| skills/analyzing-pdf-malware-with-pdfid/SKILL.md | skill | 100 | Perfect score |
| skills/analyzing-ransomware-encryption-mechanisms/SKILL.md | skill | 100 | Perfect score |
| skills/analyzing-uefi-bootkit-persistence/SKILL.md | skill | 100 | Perfect score |
| skills/conducting-cloud-penetration-testing/SKILL.md | skill | 100 | Perfect score |
| skills/conducting-mobile-app-penetration-test/SKILL.md | skill | 100 | Perfect score |
| skills/configuring-network-segmentation-with-vlans/SKILL.md | skill | 100 | Perfect score |
| skills/detecting-command-and-control-over-dns/SKILL.md | skill | 100 | Perfect score |
| skills/detecting-ransomware-precursors-in-network/SKILL.md | skill | 100 | Perfect score |
| skills/investigating-phishing-email-incident/SKILL.md | skill | 100 | Perfect score |
| skills/investigating-ransomware-attack-artifacts/SKILL.md | skill | 100 | Perfect score |
| skills/performing-container-image-hardening/SKILL.md | skill | 100 | Perfect score |
| skills/performing-csrf-attack-simulation/SKILL.md | skill | 100 | Perfect score |
| skills/performing-disk-forensics-investigation/SKILL.md | skill | 100 | Perfect score |
| skills/performing-http-parameter-pollution-attack/SKILL.md | skill | 100 | Perfect score |
| skills/performing-kubernetes-cis-benchmark-with-kube-bench/SKILL.md | skill | 100 | Perfect score |
| skills/performing-timeline-reconstruction-with-plaso/SKILL.md | skill | 100 | Perfect score |
| skills/testing-jwt-token-security/SKILL.md | skill | 100 | Perfect score |
| .claude-plugin/plugin.json | config | N/A | JSON manifest, not an NL artifact |

## Security Scan

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 8 |
| Low | 2 |

### Execution Surface Inventory

| Surface | Files |
|---------|-------|
| Hooks | 0 (none found) |
| Python scripts (agent.py, process.py) | 1030 |
| Shell scripts (.sh) | 0 |
| JavaScript (.js) | 0 |
| MCP configs (.mcp.json) | 0 (not found) |
| package.json | 0 (not found) |
| requirements.txt | 0 (not found) |

### Security Findings

| # | Severity | File | Line | Pattern | Description |
|---|----------|------|------|---------|-------------|
| 1 | HIGH | skills/performing-threat-emulation-with-atomic-red-team/scripts/agent.py | 131 | subprocess.run(shell=True) | Cleanup command executed with shell=True; command string built from YAML file content with only argument values quoted via shlex.quote(), not the command template itself |
| 2 | MEDIUM | skills/performing-threat-emulation-with-atomic-red-team/scripts/agent.py | 100 | subprocess.run(shell=True) | Test execution also uses shell=True with YAML-sourced command strings |
| 3 | MEDIUM | (222 files) | various | requests.get / requests.post / urllib.request | Outbound HTTP calls to external APIs (VirusTotal, Shodan, MISP, etc.) without per-call input validation; acceptable for security tooling but represents attack surface if agent inputs are untrusted |
| 4 | MEDIUM | (101 files) | various | os.environ.get / os.environ[] | API keys and credentials read from environment variables; no secrets-at-rest risk but exposes env to subprocess calls |
| 5 | MEDIUM | skills/exploiting-template-injection-vulnerabilities/scripts/agent.py | ~89 | os.popen('id') | SSTI test payload string stored in variable — data only, not executed by the agent script itself, but appears in executable context |
| 6 | MEDIUM | skills/detecting-serverless-function-injection/scripts/agent.py | 32–36 | Detection patterns referencing os.system, subprocess | Dangerous pattern strings stored as regex data for scanning; not executed, but presence in a Python file triggers tooling alerts |
| 7 | MEDIUM | skills/analyzing-supply-chain-malware-artifacts/scripts/agent.py | 114 | r"os\.system\(" pattern string | Regex pattern for malware detection; data only, no execution |
| 8 | MEDIUM | skills/performing-container-image-hardening/scripts/agent.py | 119 | "curl" + "| sh" string check | Dockerfile linting code that flags dangerous RUN instructions; detector, not executor |
| 9 | MEDIUM | skills/detecting-supply-chain-attacks-in-ci-cd/scripts/agent.py | 152 | "curl" + "| sh" / "| bash" string check | CI/CD pipeline scanner that flags dangerous install patterns; detector, not executor |
| 10 | LOW | skills/scanning-container-images-with-grype/scripts/agent.py | 35 | curl \| sh in error string | Error message string tells users how to install grype; not executed by the agent |
| 11 | LOW | skills/securing-container-registry-images/scripts/agent.py | 58 | curl \| sh in print statement | Print statement contains syft install instructions; not executed by the agent |

## Bugs (PR-worthy)

| # | File | Issue | Impact |
|---|------|-------|--------|
| — | — | No NL bugs found. All 754 SKILL.md files have required `name` and `description` frontmatter fields. | — |

## Security Fixes (PR-worthy, Medium/Low only)

| # | File | Issue | Suggested Fix |
|---|------|-------|---------------|
| 1 | skills/scanning-container-images-with-grype/scripts/agent.py:35 | Error message documents curl\|sh install pattern | Replace with: `return {"error": "grype not found. Install via package manager or pinned binary: https://github.com/anchore/grype/releases"}` |
| 2 | skills/securing-container-registry-images/scripts/agent.py:58 | Print statement documents curl\|sh install pattern | Replace with a versioned binary download URL instead of the pipe-to-shell pattern |

> **Note**: Finding #1 (HIGH — subprocess shell=True in Atomic Red Team agent) is intentional by design: Atomic Red Team test scripts are shell-based and require shell=True for compatibility. If this agent runs in untrusted environments, consider adding an allowlist of permitted technique IDs and validating the cleanup_command against expected patterns before execution.

## Quality Issues (informational)

| # | File | Issue | Penalty |
|---|------|-------|---------|
| 1 | 351 SKILL.md files (46.5%) | Missing output format / Expected Output section | −10 each |
| 2 | 110 SKILL.md files (14.6%) | Zero code block examples | −15 each |
| 3 | skills/prioritizing-vulnerabilities-with-cvss-scoring/SKILL.md | 1 vague quantifier ("appropriate") + no examples + no output format | −27 total |
| 4 | skills/implementing-cisa-zero-trust-maturity-model/SKILL.md | 5 vague terms ("progressive", "dynamically", "effectively", "properly", "structured") | −10 vague penalty |
| 5 | skills/implementing-log-forwarding-with-fluentd/SKILL.md | Stub content: 62 lines, workflow steps are unfilled placeholders | −15 (no examples) |
| 6 | skills/implementing-zero-trust-with-beyondcorp/SKILL.md | 65-line stub with abstract steps and no executable examples | −15 (no examples) |
| 7 | skills/performing-ssl-tls-security-assessment/SKILL.md | 61-line stub, steps describe actions without commands or tool flags | −15 (no examples) |
| 8 | skills/mapping-mitre-attack-techniques/SKILL.md | No output format section; vague terms "comprehensive gap analysis", "relevant threat groups" | −10 output, −6 vague |
| 9 | skills/detecting-arp-poisoning-in-network-traffic/SKILL.md | No output format section; 3 vague terms | −10 output, −6 vague |
| 10 | skills/performing-network-traffic-analysis-with-zeek/SKILL.md | No output format section; 3 vague terms including "comprehensive" (×2) | −10 output, −6 vague |

## Cross-Component

- **No broken inter-skill references** detected. SKILL.md files are self-contained and do not cross-reference each other.
- **plugin.json** declares `name: cybersecurity-skills` and `version: 1.0.0`; consistent with the 753-skill count in the description.
- **Depth inconsistency**: ~110 files with no code examples (stub quality) coexist alongside ~17 files scoring 100/100. The collection has high variance in completeness. No architectural contradiction — just uneven development effort.
- **Offensive skill coverage** (exploiting-*, performing-lateral-movement-with-wmiexec, performing-initial-access-with-evilginx3, building-c2-infrastructure-with-sliver-framework, conducting-domain-persistence-with-dcsync): all include authorization context or are framed for red team/authorized testing. No cross-component inconsistency found.

## Recommendation

REVIEW — submit NL fix PRs for missing output format sections (351 files) and examples (110 files). Flag the HIGH security finding (subprocess shell=True in atomic-red-team agent) in a private issue for maintainer review before contributing; no PR for that file. Submit Low-severity security fix PRs (#10, #11) to replace curl|sh documentation strings with safer alternatives.
