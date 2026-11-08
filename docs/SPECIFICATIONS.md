# 🚀 SpaceX Application Functional Specifications

> Comprehensive functional overview and product requirements specification for the SpaceX Database & Mission Management application.

---

## 📑 Page Architecture & User Flows

### 1. Landing Page (`/`)
- **Dynamic Hero Carousel**: Positioned below the top navigation, highlighting the corporate logo, inspiring aerospace slogans, and high-impact historical spaceflight milestones.
- **Upcoming Missions Overview**: Displays real-time database queries of active missions, scheduled launch windows, and designated mission commanders.
- **Footer**: Centralized corporate links, social channels, trademark notices, and privacy policy documentation.

### 2. Space Missions Directory (`/mission`)
- Complete index of planned, ongoing, and completed space missions.
- Chronological sorting by target launch date, mission name, and assigned operational team.

### 3. Flight Crew Roster (`/spaceman`)
- Directory of astronauts and mission commanders.
- Multi-column sort options based on seniority, spaceflight experience, salary tiers, and initial mission start dates.

### 4. Scientific Division (`/scientist`)
- Staff directory for research personnel and payload specialists.
- Filterable by research achievements and operational milestones.

### 5. Recruitment & Career Portal (`/workwithus`)
- Interactive applicant submission pipeline allowing candidates to submit CV details.
- Form submissions are automatically persisted into the `JobApplication` database staging table for administrative review.

### 6. Administrative Management Portal (`/management`)
- **Strict Access Control**: Protected by role-based session authentication.
- **Mission Lifecycle Management**: Create, reschedule, and archive orbital and interplanetary missions.
- **Automated Candidate Hiring**: Promotes candidate records from `JobApplication` to active `Employee` status via atomic T-SQL stored procedures (`sp_MoveJobApplicationToEmployee`).
- **Personnel Administration**: Update compensation tiers, assign roles, and adjust team compositions without requiring manual SQL queries.

### 7. Authentication Flow (`/login`)
- Clean, focused credential entry (Username & Password).
- Internal account provisioning: Accounts are provisioned exclusively by system administrators to maintain security.

---

## 🎨 Design System

- **Color Palette**: Dark-mode monochromatic base (`#0f0f1a` / `#000000`) accented with atmospheric space-blue (`#0B1B3D`) and silver highlights.
- **Typography & Accessibility**: Clean sans-serif interface designed for legibility across administrative tables and public dashboards.
