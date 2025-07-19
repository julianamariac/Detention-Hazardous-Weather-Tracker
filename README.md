# Detention-Facility-Extreme-Weather-Tracker

**An open-source, humanitarian project to monitor extreme weather conditions near detention and holding facilities, with the goal of increasing transparency, supporting advocacy, and protecting lives.**

## Mission Statement

This project exists to address a life-threatening gap in public awareness: people are being detained in facilities across the U.S. without access to air conditioning, proper sanitation, or safety planning during extreme weather events. Many of these individuals have no have no ability to communicate the safety concerns outside of the facilities.

By publicly tracking dangerous weather events near these locations and making that data open, verifiable, and transparent, we hope to:
- Increase public awareness of detention conditions during climate emergencies
- Inform advocacy efforts and emergency response planning
- Support community-led monitoring and reporting
- Offer a replicable, ethical model for future projects

---

## Ethical Guidelines

We are committed to safety, data integrity, and respect for vulnerable populations. The following values guide every aspect of this project:

- **Privacy First:** We do not collect or publish any personally identifiable information (PII). All data refers to weather near known detention facilities—not inside them.
- **Transparency:** All code, data structures, and collection methods are open source and documented.
- **Verification:** Community contributions are encouraged, but data must be verified before being published.
- **Nonpartisan and Nonviolent:** This project does not engage in political speculation or call for illegal action. Our goal is data transparency in service of humanitarian care.

---

## Project Modules

This project is modular and built to grow. Here are the key components we’re developing:

### 1. **Weather Data Collection**
- Real-time weather data pulled from public APIs (e.g., OpenWeatherMap)
- Focus on heat index, humidity, wind speeds, precipitation, storm alerts
- Targets specific geographic coordinates of known facilities

### 2. **Public Dashboards**
- Real-time visualizations showing conditions near detention centers
- Color-coded risk indicators (e.g., Heat Index >105°F = Critical)
- Open-source dashboard built using Python and Streamlit or Leaflet.js

###  3. **Facility Metadata**
- List of publicly documented detention sites in Florida
- Google Sheets or Airtable backend for community contribution
- Includes fields like region, county, operational status, last verified date

### 4. **Community Reporting Tool**
- A privacy-safe way for the public to report known detentions or releases
- Anti-spam protections and clear contributor ethics
- Reports will not be published without secondary verification

### 5. **Resource Finder (Separate Sheet)**
- Regional directory of mental health, legal, and nonprofit support
- Focus on free, public-facing services for immigrants and refugees
- Includes verification status and ethical contact guidance

---

## How to Contribute

We welcome volunteers, especially those with experience in:
- Data science, Python, or Streamlit
- GIS or map visualization
- Policy, human rights, or climate advocacy
- Spanish, Haitian Creole, or other translation support

 **Start by reviewing our [`CONTRIBUTING.md`](./CONTRIBUTING.md) and `DATA_POLICY.md` for ethical and technical guidelines.**

---

## Roadmap

- [ ] Build weather data collection script
- [ ] Set up public dashboard with mock data
- [ ] Create spreadsheet for verified detention facilities
- [ ] Publish resource tracker for local aid groups
- [ ] Deploy first public dashboard (target: Florida)
- [ ] Connect with ACLU of Florida and other partners
- [ ] Develop modular documentation for replication in other states

---

## Repo Structure

```plaintext
/scripts              # Python scripts for data collection
/data                 # Sample or real weather data
/docs                 # Policy documents, guidelines
/dashboards           # Dashboard code (e.g., Streamlit app)
CONTRIBUTING.md       # How to contribute
DATA_POLICY.md        # Data ethics and privacy policy
README.md             # This file
