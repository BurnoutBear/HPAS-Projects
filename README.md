# Human and Physical Aspects of Security - Projects

This is the repository for the projects of the master course *Human and Physical Aspects of Security* (Academic Year 2025/2026) at Politecnico di Milano.

**Teacher** : Longari Stefano

**Final Score**: to be determined

## Project List

### Threat Modeling

The goal of this project is to develop a threat model for a **Virtual Power Plant (VPP)** scenario using the **STRIDE methodology**.

The analyzed system consists of a cloud-based aggregator managing distributed energy resources, residential edge devices, and power hardware components such as smart inverters and battery management systems.

The project includes:
- System scenario description
- Data Flow Diagram (DFD) with assets, actors, processes, data stores, external entities, communications, and trust boundaries
- Threat identification using STRIDE
- Risk assessment and mitigation strategies for the most critical threats

**Scenario**: Virtual Power Plant (VPP)  
**Approach**: STRIDE Threat Modeling  
**Tool**: OWASP Threat Dragon

### Social Engineering

The goal of this project is to develop a **spear-phishing scenario** targeting the **Agenzia delle Entrate** website, using **Carta d'Identità Elettronica (CIE)** authentication.

The chosen target is the new **“Registra il tuo domicilio digitale”** feature, which allows citizens and professionals to register a PEC address as their digital domicile.

The project includes:
- Goal definition and target selection
- Ethical information gathering and analysis
- Phishing email design
- Implementation of a malicious replica of the chosen portal
- Static asset linking and reproducible deployment

**Scenario**: Agenzia delle Entrate - “Registra il tuo domicilio digitale”  
**Authentication**: Carta d'Identità Elettronica (CIE)  
**Approach**: Spear-phishing simulation

### Intrusion Detection System

The goal of this project is to implement an **Intrusion Detection System (IDS)** for the **Controller Area Network (CAN)** bus capable of detecting malicious traffic.

The IDS is trained using normal CAN traffic and evaluated against multiple attack datasets without relying on attack labels or predefined signatures.

The project includes:
- Analysis of CAN traffic
- Design and implementation of the IDS
- Detection of anomalous network behavior
- Performance evaluation using the F1-score

**Target**: Controller Area Network (CAN)  
**Approach**: Anomaly-based Intrusion Detection  
**Language**: Python (Jupyter Notebook)

## The Team

- [Marco Galli](https://github.com/Me-P-eM)
- [Simone Frazzei](https://github.com/BurnoutBear)
- [Francesco Ambesi](https://github.com/Ambesss)

## Technologies

- **OWASP Threat Dragon**: threat modeling
- **Visual Studio Code**: main IDE
- **Python**: programming language for SE and IDS projects
- **Jupyter Notebook**: for the IDS project
- **Git**: version control system
