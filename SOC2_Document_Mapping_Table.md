# SOC2 Document to Client Requirement Mapping
## Quick Reference Guide

This table provides a quick lookup for auditors and stakeholders to find which OversiteAI policy document addresses specific client requirements.

## Document Legend

| Code | Document Name |
|------|---------------|
| **ISP** | Information Security Policy |
| **RMP** | Risk Management Policy |
| **ACP** | Access Control Policy |
| **AMP** | Asset Management and Data Protection Policy |
| **CMP** | Change Management and Business Continuity Policy |
| **IRP** | Incident Response Plan |
| **HRP** | Human Resources Security and Governance Policy |
| **PDA** | Privacy and Data Protection Addendum |

## Requirement Mapping by Domain

### A. Enterprise Risk Management
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| A.1 | Risk governance plan | Yes | RMP | Sections 1-3 |
| A.1.1 | Risk policies and controls | Yes | RMP | Sections 6, 8 |
| A.2 | Fourth party access | No | RMP | Section 17 (explains no access) |
| A.2.1 | Third party risk management | Blank | RMP | Section 7.5 |
| A.2.2 | Contractual relationships | Blank | RMP | Section 17 |
| A.2.3 | Risk tracking responsibility | Blank | RMP | Section 2 |

### B. Security Policy
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| B.1 | Information security policies | Yes | ISP | All sections |
| B.1.1 | External system protection | Yes | ISP | Sections 5, 7 |
| B.1.2 | Annual policy review | Yes | ISP | Section 2.4 |

### C. Organizational Security
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| C.1 | Asset protection responsibilities | Yes | All docs | RACI matrices |
| C.2 | Information security personnel | Yes | ISP | Section 2 |
| C.3 | Security assessments for projects | Yes | CMP | Section 5 |

### D. Asset and Information Management
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| D.1 | Asset management program | Yes | AMP | Section 1 |
| D.1.1 | Asset inventory/CMDB | Yes | AMP | Section 1.3 |
| D.2 | Acceptable use policy | Yes | HRP | Section 3 |
| D.3 | Asset return process | Yes | HRP | Section 2.5 |
| D.4 | Information classification | Yes | AMP | Section 2 |
| D.4.1 | Handling procedures | Yes | AMP | Section 2.4 |
| D.4.2 | Retention/destruction | N/A | AMP | Section 2.5 (no customer data) |
| D.5 | Physical media | N/A | AMP | Policy excludes physical media |
| D.6 | Electronic data transmission | Yes | AMP | Section 3 |
| D.7 | Data protection safeguards | Yes | AMP | Section 3.2 |

### E. Human Resources Security
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| E.1 | HR security policies | Yes | HRP | All sections |
| E.2 | 24-hour access removal | Yes | HRP | Section 2.5 |

### F. Physical and Environmental
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| F.1 | Physical security program | Yes | HRP | Section 6 |
| F.2 | Environmental hazard assessment | N/A | HRP | Section 6 (remote only) |
| F.3 | Visitor management | Yes | HRP | Section 6.2 |


### G. IT Operations Management
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| G.1 | Change management policy | Yes | CMP | Sections 1-3 |
| G.2 | Security requirements for new systems | Yes | CMP | Section 3.3 |

### H. Access Control (Comprehensive)
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| H.1 | Access control program | Yes | ACP | All sections |
| H.2 | Constituent access to data | Yes | ACP | Section 3 |
| H.3 | Unique IDs required | Yes | ACP | Section 2.1 |
| H.4 | Password policy | Yes | ACP | Section 4 |
| H.5 | Password reset restrictions | Yes | ACP | Section 4.3 |
| H.6 | Regular password changes | Yes | ACP | Section 4.2 |
| H.7 | Password confidentiality | Yes | ACP | Section 4.1 |
| H.7.1 | Separate media distribution | Yes | ACP | Section 10.3 |
| H.7.2 | Compromise response | Yes | ACP | Section 4.4 |
| H.8 | Multi-factor authentication | Yes | ACP | Section 5 |
| H.9 | Session management | Yes | ACP | Section 6 |
| H.10 | Access review process | Yes | ACP | Section 7 |
| H.11 | Inactive account management | Yes | ACP | Section 6.2 |

### I. Application Security
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| I.1 | Applications for scoped data | Yes | CMP | Section 5 |
| I.1.2 | Environment separation | Yes | CMP | Section 5.4 |
| I.1.3 | Test data usage | Yes | CMP | Section 5.5 |
| I.2 | Application development | Yes | CMP | Section 5 |
| I.2.1 | Secure SDLC policy | Yes | CMP | Sections 5.1-5.8 |
| I.2.2 | Security evaluation | Yes | CMP | Section 5.3 |
| I.2.3 | Vulnerability remediation | Yes | CMP | Section 5.7 |
| I.3 | Web application support | Yes | CMP | Section 5 |
| I.3.1 | Web server standards | Yes | ACP | Section 9 |
| I.3.2 | API availability | Yes | CMP | Section 5.3 |
| I.3.2.1 | API security program | Yes | CMP | Section 5.3 |

### J. Cybersecurity Incident Management
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| J.1 | Incident management program | Yes | IRP | All sections |
| J.2 | Formal response plan | Yes | IRP | Section 3 |
| J.3 | Event review methodology | Yes | IRP | Section 2 |
| J.3.1 | Malware monitoring | Yes | IRP | Section 2.2 |
| J.4 | 24/7 incident reporting | Yes | IRP | Section 5 |


### K. Operational Resilience
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| K.1 | Business resilience program | Yes | CMP | Section 6 |
| K.1.1 | Services in scope | Yes | CMP | Section 6.1 |
| K.2 | DR testing program | Yes | CMP | Section 7.4 |
| K.3 | Third party dependencies | No | CMP | Section 6 (no dependencies) |
| K.3.1 | Third party notifications | Blank | N/A | No dependencies |
| K.4 | Pandemic plan | No | CMP | Inherently remote |
| K.4.1 | Preventive program | Blank | N/A | Remote work model |
| K.5 | Backup policy | Yes | CMP | Section 7.2 |
| K.6 | Risk identification process | Yes | RMP + CMP | Integrated |
| K.7 | BC procedures | Yes | CMP | Section 6.3 |
| K.8 | Management responsibility | Yes | CMP | Section 2 |
| K.9 | Offsite backup | Yes | CMP | Section 7.2 |
| K.10 | Data retention policy | Yes | AMP | Section 2.5 |
| K.11 | Ransomware recovery | Yes | IRP | Section 4.2 |

### L. Compliance and Operations Risk
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| L.1 | Compliance policies | Yes | HRP | Section 7 |
| L.2 | Internal audit function | Yes | HRP | Section 7.3 |
| L.3 | ESG program | Yes | HRP | Section 7.4 |
| L.7 | Anti-trust compliance | Yes | HRP | Section 7.1 |
| L.8 | Ethics program | Yes | HRP | Section 7.1 |
| L.10 | Cybersecurity compliance | Yes | All docs | Compliance sections |
| L.11 | Fraud prevention | Yes | HRP | Section 7.1 |
| L.12 | Records retention | Yes | AMP | Section 2.5 |

### M. Endpoint Device Security
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| M.1 | End user devices | Yes | AMP | Section 1 |
| M.1.1 | Device security standards | Yes | AMP | Section 4.2 |
| M.1.2 | Anti-virus procedures | Yes | AMP | Section 4.2 |
| M.1.3 | Mobile device usage | Yes | HRP | Section 3.3 |
| M.1.3.1 | MDM program | Yes | AMP | Section 1.4 |
| M.1.4.1 | BYOD allowed | No | HRP | Section 3.3 (prohibited) |
| M.2 | Collaborative computing | No | ACP | Not for scoped data |

### N. Network Security
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| N.1 | Network security policy | Yes | ACP | Section 9 |
| N.2 | Security standards | Yes | ACP | Section 9.2 |
| N.2.1 | Default password changes | Yes | ACP | Section 9.1 |
| N.3 | Patch testing | Yes | AMP | Section 4.4 |
| N.4 | Firewall termination | Yes | ACP | Section 9.3 |
| N.5 | Network segregation | Yes | ACP | Section 9.4 |
| N.5.1 | Quarterly ACL review | Yes | ACP | Section 9.5 |
| N.6 | Remote access policy | Yes | ACP | Section 10 |
| N.7 | Encrypted communications | Yes | ACP | Section 10.2 |
| N.8 | Collaborative computing | Yes | ACP | Section 13 |
| N.9 | Network IDS | Yes | ACP | Section 9.6 |
| N.10 | DMZ environment | Yes | ACP | Section 9.4 |
| N.11 | Wireless policy | Yes | ACP | Section 11 |


### P. Privacy (Comprehensive No-Data Approach)
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| P.1 | Personal data collection | No | PDA | Section 3 (architecture) |
| P.1.1 | Privacy program | Blank | PDA | All sections |
| P.1.2 | GLBA data | Blank | PDA | Section 5 (no access) |
| P.1.3 | FACTA data | Blank | PDA | Section 5 (no access) |
| P.1.4 | HIPAA PHI | Blank | PDA | Section 5 (no access) |
| P.1.4.1 | PHI breach detection | Blank | PDA | N/A |
| P.1.5 | State privacy laws | Blank | PDA | Section 5 (no access) |
| P.1.6 | EU personal data | Blank | PDA | Section 5 (no access) |
| P.1.7 | Canadian privacy | Blank | PDA | Section 5 (no access) |
| P.1.8 | Other international | Blank | PDA | Section 5 (no access) |
| P.1.9 | Data flow documentation | Blank | PDA | Section 3 |
| P.1.10 | Privacy training | Blank | HRP | Section 4 |
| P.1.11 | Breach detection | Blank | IRP | Privacy incidents |
| P.2 | Internet-facing collection | No | PDA | Section 3 |
| P.3 | Direct collection | No | PDA | Section 3 |
| P.4 | Client-provided data | No | PDA | Section 3 |
| P.4.1 | Data minimization | Blank | PDA | By design |
| P.5 | Data compliance procedures | N/A | PDA | No data processing |
| P.6 | Third party privacy | N/A | PDA | No data sharing |
| P.6.1 | Fourth party access | Blank | PDA | No fourth parties |
| P.7 | Third party risk management | N/A | PDA | No data to protect |
| P.8 | Data accuracy maintenance | N/A | PDA | No data maintained |
| P.9 | Privacy enforcement | N/A | PDA | No PII |

### T. Threat Management
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| T.1 | Vulnerability management | Yes | AMP | Section 4 |
| T.2 | Supply chain risk | Yes | RMP | Section 17 |

### U. Server Security
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| U.1 | Servers for scoped data | Yes | AMP | Section 1 |
| U.1.1 | Annual standard review | Yes | AMP | Section 4.4 |
| U.1.2 | Unnecessary services | Yes | ACP | Section 9.2 |
| U.1.3 | Default passwords | Yes | ACP | Section 4.1 |
| U.1.4 | Regular patching | Yes | AMP | Section 4.4 |
| U.1.4.1 | EOL operating systems | No | AMP | Current versions only |
| U.1.5 | Windows servers | Yes | AMP | Azure VMs |
| U.1.5.1 | Anti-malware policy | Yes | AMP | Section 4.2 |
| U.1.6 | Unix/Linux usage | Yes | AMP | Containers |
| U.1.7 | AS/400 usage | No | N/A | Not used |
| U.1.8 | Mainframe usage | No | N/A | Not used |
| U.1.9 | Hypervisor usage | Yes | AMP | Azure managed |
| U.2 | IoT device management | Yes | AMP | Section 1.5 |

### V. Cloud Hosting Services
| Req # | Requirement | Response | Document | Section |
|-------|-------------|----------|----------|---------|
| V.2 | Backup snapshot authorization | N/A | CMP | Different model |
| V.3 | Cloud provider SOC reports | Yes | AMP | Azure compliance |

---

## Summary Statistics

- **Total Requirements**: 140
- **Requirements with "Yes"**: 100 (71%)
- **Requirements with "No"**: 12 (9%)
- **Requirements with "N/A"**: 9 (6%)
- **Requirements with "Blank"**: 19 (14%)

**All requirements are fully addressed in our documentation.**

