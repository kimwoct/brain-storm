# User Stories Comparison Summary

**Comparison Date:** 2025-12-08  
**Files Compared:**
- `user-stories.md` (v1.0) - Simplified version with UI Views focus
- `User Stories & Test Cases.md` (v1.4) - Comprehensive version with test cases

---

## Executive Summary

| Aspect | user-stories.md (v1.0) | User Stories & Test Cases.md (v1.4) |
|--------|------------------------|--------------------------------------|
| **Version** | 1.0 | 1.4 |
| **Total Stories** | 26 | 28 |
| **Test Cases** | None | 28 |
| **UI Views Section** | ✅ Yes (detailed) | ❌ No |
| **Requirements Traceability** | Basic (story + description) | Enhanced (story + FRs + description) |
| **Aligned With** | Not specified | Product Specification v1.5 |

---

## Key Structural Differences

### 1. UI Views Documentation

**user-stories.md (v1.0)** includes a comprehensive **VIEWS** section listing all required UI screens:

- **ERP / Third-Party Integration Views** (4 views)
  - ERP Integration Health & Logs View
  - Master Data Sync Status View
  - Job Demand & Assignment Exchange Monitor
  - Attendance & Penalty Submission Tracker

- **Nursing Assistant Views** (4 views)
  - User Dashboard
  - Jobs List View
  - Job Details View
  - Penalty History View

- **PHC Admin Views** (3 views)
  - Admin Dashboard
  - Job Details View
  - User List View

- **Reports Views** (6 views)
  - Attendance Performance Dashboard
  - Penalty Summary Report
  - Staff Score Report
  - System Logs and Reports View
  - Settlement Reconciliation Report
  - Settlement Discrepancy Investigation View

**User Stories & Test Cases.md (v1.4)** does NOT include this views section.

---

### 2. Requirements Traceability Matrix

**user-stories.md (v1.0):**
- Simple 2-column format (Story | Description)
- 26 stories listed

**User Stories & Test Cases.md (v1.4):**
- Enhanced 3-column format (Story | Related FRs | Description)
- 28 stories with functional requirement mappings
- Includes NEW markers for recently added stories

---

## Story-Level Differences

### Stories Present in v1.4 but Missing in v1.0

| Story ID | Description | Status |
|----------|-------------|--------|
| **US-NA-07** | Update Personal Information (mobile number change) | NEW in v1.4 |
| **US-ADM-06** | View System Logs and Reports | NEW in v1.4 |
| **US-ADM-09** | Update Job Posting Details | NEW in v1.4 |
| **US-ERP-07** | Post Job Detail Updates to PHC | NEW in v1.4 |
| **US-ERP-08** | Receive OT Job Demand Sync | NEW in v1.4 |
| **US-ERP-09** | Facility Blacklist Sync | NEW in v1.4 |

### Stories Present in v1.0 but Missing in v1.4

| Story ID | Description | Status |
|----------|-------------|--------|
| **US-RPT-01** | View Attendance Performance Dashboard | In v1.0 only |
| **US-RPT-02** | Generate Penalty Summary Report | In v1.0 only |
| **US-RPT-03** | Generate Staff Score Report | In v1.0 only |
| **US-RPT-04** | View System Logs | In v1.0 only |

> **Note:** Report stories (US-RPT-xx) exist in v1.0 but appear consolidated under US-ADM-06 in v1.4.

---

## Acceptance Criteria Differences

### US-NA-00: Staff Login

| Criteria | v1.0 | v1.4 |
|----------|------|------|
| Failed login lockout | 5 attempts | **10 attempts** |
| Password reset flow | SMS/Email OTP | **Email/Admin WhatsApp Reset Link** |
| Post-login destination | Jobs tab | Personal dashboard |

### US-NA-01: Receive Job Notification

| Criteria | v1.0 | v1.4 |
|----------|------|------|
| Inbox UI design | Not mentioned | **NEW: Highlights unread with visual indicators** |

### US-NA-02: Apply for Available Shift

| Criteria | v1.0 | v1.4 |
|----------|------|------|
| Apply button disabled logic | Not mentioned | **NEW: Disabled if quota (including waiting list) is full** |
| Empty job handling | Not mentioned | **NEW: ERP/Admin notification then re-matching** |

### US-NA-03: Cancel Shift with Penalty Warning

| Criteria | v1.0 | v1.4 |
|----------|------|------|
| Re-matching workflow | Basic "Re-matching triggered" | **Enhanced: Closes current job post, raises new demand to ERP for updated candidate list** |
| Admin notification | Not specified | **NEW: Admin notified of vacancy and re-matching initiation** |
| Early cancellation bonus | Not mentioned | **No attendance bonus** |

### US-ADM-02: Manual Confirmation

| Criteria | v1.0 | v1.4 |
|----------|------|------|
| Override reason limit | max 100 words | max 100 words (same) |
| View workflow | Detailed (User List → Job Details) | Simplified |
| Assignment execution location | Job Details View only | Not specified |

### US-ADM-03: Upload Acknowledgment Documents

| Criteria | v1.0 | v1.4 |
|----------|------|------|
| Job Details View integration | ✅ Document appears in Job Details View | Not mentioned |

### US-ADM-05: Post Emergency Job

| Criteria | v1.0 | v1.4 |
|----------|------|------|
| Emergency flag approach | Flag/toggle on job posting form | Dedicated "Emergency Job Posting" button |

---

## Test Cases (v1.4 Only)

**User Stories & Test Cases.md (v1.4)** includes 28 test cases:

| Category | Count | Test Case IDs |
|----------|-------|---------------|
| Functional | 8 | TC-001 to TC-008, TC-ADM-01 |
| ERP Integration | 11 | TC-ERP-01 to TC-ERP-11 |
| Performance | 2 | TC-PERF-01, TC-PERF-02 |
| Security | 4 | TC-SEC-01 to TC-SEC-04 |
| Finance & Reports | 3 | TC-FIN-01, TC-RPT-01, TC-RPT-02 |

### New Test Cases in v1.4

- **TC-ERP-09:** Job Demand Update Reception
- **TC-ERP-10:** OT Job Demand Sync
- **TC-ERP-11:** Facility Blacklist Sync
- **TC-SEC-04:** Update Personal Information

---

## Project Timeline (v1.4 Only)

**User Stories & Test Cases.md (v1.4)** includes a detailed project timeline:

| Milestone | Date | Actioned by |
|-----------|------|-------------|
| Requirements Confirmation | 2025-Dec-12 | Ms Sze |
| API Preparation | 2025-Dec-9 to 2025-Dec-12 | Octopus |
| Project Start | 2025-Dec-15 | Octopus |
| API Integration | 2025-Dec-15 to 2025-Dec-19 | Octopus |
| UI Design Layout | 2025-Dec-17 | Octopus |
| UI Design Confirmation | 2025-Dec-19 | Ms Sze |
| Phase 1: Unit Testing | 2025-Dec-15 to 2025-Dec-29 | Octopus |
| Phase 2: Integration Testing | 2025-Dec-30 to 2026-Jan-13 | Octopus |
| Phase 3: System Testing | 2026-Jan-14 to 2026-Jan-23 | Octopus |
| Phase 4: UAT | 2026-Jan-24 to 2026-Feb-02 | Ms Sze |
| Go-Live Target | 2026-Feb-03 | Octopus |

---

## Terminology Differences

| Concept | v1.0 | v1.4 |
|---------|------|------|
| Work assignment | "Job" | "Shift" (primary) |
| Scenario format | Gherkin (```gherkin) | Plain code block (```) |
| Story numbering | US-NA-04 missing | US-NA-04 = View job history |

---

## Recommendations

### 1. Consolidation Strategy
- **Merge UI Views** from v1.0 into v1.4 to create a comprehensive reference
- Views documentation is valuable for UI/UX design and development

### 2. Story Alignment
- Clarify relationship between US-RPT-xx stories (v1.0) and US-ADM-06 (v1.4)
- Ensure all report functionalities are captured

### 3. Version Control
- Consider v1.0 as "UI Design Reference" document
- Maintain v1.4 as "Master User Stories & Test Cases" document

### 4. Missing Elements to Add to v1.4
- [ ] UI Views section from v1.0
- [ ] Detailed workflow diagrams for Admin views
- [ ] View-to-story mapping for development reference

---

## Change Log Summary

| Version | File | Key Changes |
|---------|------|-------------|
| v1.0 | user-stories.md | Initial draft with UI Views, 26 stories |
| v1.4 | User Stories & Test Cases.md | Added 28 test cases, 6 new stories, project timeline, FR traceability |

---

**Generated:** 2025-12-08  
**Purpose:** Document analysis and alignment for PHC Dispatch System
