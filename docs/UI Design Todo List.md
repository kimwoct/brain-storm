# UI Design Todo List
**Prestige Health Dispatch System (PHC)**

**Version:** 1.0
**Date:** 2025-11-27
**Based On:** User Stories v1.1

---

## OVERVIEW

This document outlines the UI screens required for the PHC system, organized by user role. Each screen includes priority, related user stories, and key UI components.

---

## USER ROLES

| Role | Description | Portal |
|------|-------------|--------|
| 🩺 **Nursing Assistant (NA)** | Healthcare workers who apply for and complete shifts | Staff Portal (Web) |
| 👔 **PHC Administrator** | System administrators who manage jobs, staff, and operations | Admin Portal (Web) |
| 💰 **Finance Administrator** | Finance team members who handle settlements and reconciliation | Admin Portal (Web) |
| 🔗 **ERP System** | Backend integration (no UI) | API Only |

---

## 🩺 NURSING ASSISTANT PORTAL

### Authentication Screens

| # | Screen | Priority | User Story | Status |
|---|--------|----------|------------|--------|
| NA-01 | Login Page | Critical | - | ⬜ Todo |
| NA-02 | Registration Page | Critical | - | ⬜ Todo |
| NA-03 | Forgot Password | Medium | - | ⬜ Todo |
| NA-04 | Profile Settings | Medium | - | ⬜ Todo |

**NA-01: Login Page**
- [ ] Phone number / Email input
- [ ] Password input
- [ ] "Remember me" checkbox
- [ ] Forgot password link
- [ ] Bilingual toggle (EN/繁中)
- [ ] Mobile responsive

**NA-02: Registration Page**
- [ ] Staff ID verification (from ERP)
- [ ] Phone number input
- [ ] Password creation
- [ ] Terms acceptance checkbox

---

### Main Navigation

| # | Screen | Priority | User Story | Status |
|---|--------|----------|------------|--------|
| NA-05 | Dashboard / Home | Critical | US-NA-01, US-NA-02 | ⬜ Todo |
| NA-06 | Available Shifts List | Critical | US-NA-01, US-NA-02 | ⬜ Todo |
| NA-07 | Shift Details | Critical | US-NA-02 | ⬜ Todo |
| NA-08 | My Shifts | Critical | US-NA-02, US-NA-03 | ⬜ Todo |
| NA-09 | My Job History | High | US-NA-05 | ⬜ Todo |
| NA-10 | Job Detail View | High | US-NA-05 | ⬜ Todo |
| NA-11 | My Penalties | High | US-NA-06 | ⬜ Todo |
| NA-12 | My Score *(Deferred)* | Medium | US-NA-04 | ⏸️ Deferred |
| NA-13 | Document Acknowledgment | High | US-NA-07 | ⬜ Todo |
| NA-14 | Notifications Inbox | Medium | US-NA-01 | ⬜ Todo |

---

### Screen Details

#### NA-05: Dashboard / Home
**Priority:** Critical | **User Story:** US-NA-01, US-NA-02

**Components:**
- [ ] Welcome banner with staff name
- [ ] Upcoming shifts summary (next 7 days)
- [ ] New available shifts badge/count
- [ ] Quick action: "View Available Shifts"
- [ ] Pending document acknowledgments alert
- [ ] Recent notifications list
- [ ] Current score display (if not deferred)

---

#### NA-06: Available Shifts List
**Priority:** Critical | **User Story:** US-NA-01, US-NA-02

**Components:**
- [ ] List of available shifts (cards)
- [ ] Each card shows: date, location, time, contact person
- [ ] Filter by: date range, region, shift type
- [ ] Sort by: date, location
- [ ] "Apply" button on each card
- [ ] Already applied indicator
- [ ] Conflict warning if overlapping shift exists
- [ ] Pull-to-refresh (mobile)
- [ ] Pagination / infinite scroll

---

#### NA-07: Shift Details
**Priority:** Critical | **User Story:** US-NA-02

**Components:**
- [ ] Full shift details: date, time, location address, contact person
- [ ] Location map (optional)
- [ ] Special notes/requirements
- [ ] Required documents list
- [ ] **Cancellation penalty warning banner** ⚠️
- [ ] "Apply" button (prominent)
- [ ] Confirmation modal after apply
- [ ] Status indicator after application

---

#### NA-08: My Shifts
**Priority:** Critical | **User Story:** US-NA-02, US-NA-03

**Components:**
- [ ] Tabs: Upcoming | Pending Approval | Completed
- [ ] Shift cards with status badges
- [ ] Status colors: Pending (yellow), Confirmed (green), Cancelled (red)
- [ ] "Cancel Shift" button for confirmed shifts
- [ ] **Cancel Shift Modal - Early (>48h)**
  - [ ] Confirmation message: "You are cancelling with sufficient notice."
  - [ ] Penalty info: "-1 score, no financial penalty"
  - [ ] [Keep Shift] [Confirm Cancellation] buttons
- [ ] **Cancel Shift Modal - Late (<48h)** ⚠️
  - [ ] Warning: "⚠️ Late Cancellation Warning"
  - [ ] Penalty info: "-1 score AND 300 HKD deduction"
  - [ ] [Keep Shift] [Confirm Cancellation] buttons
- [ ] View required documents button
- [ ] Contact facility button

---

#### NA-09: My Job History
**Priority:** High | **User Story:** US-NA-05

**Components:**
- [ ] List of past assignments (last 12 months)
- [ ] Each record shows: date, location, shift time, status
- [ ] Status badges: Completed ✓, Cancelled ✗
- [ ] Score impact: +1 (green), -1 (red)
- [ ] Penalty indicator if applicable
- [ ] Filter by: date range, status
- [ ] Pagination (20 per page)
- [ ] Click to view details
- [ ] Export to PDF button

---

#### NA-10: Job Detail View
**Priority:** High | **User Story:** US-NA-05

**Components:**
- [ ] Assignment date and shift times
- [ ] Location details
- [ ] Clock-in/out times (if completed)
- [ ] Attendance status
- [ ] Score impact
- [ ] Penalty details (if any)
- [ ] Document acknowledgment status

---

#### NA-11: My Penalties
**Priority:** High | **User Story:** US-NA-06

**Components:**
- [ ] List of all penalties
- [ ] Each record: date, type, amount, score impact
- [ ] Type: "Late Cancellation" badge
- [ ] Amount: "300 HKD" (red)
- [ ] Score impact: "-1"
- [ ] Related assignment link
- [ ] Filter by date range
- [ ] Total penalties summary

---

#### NA-13: Document Acknowledgment
**Priority:** High | **User Story:** US-NA-07

**Components:**
- [ ] List of required documents for upcoming shift
- [ ] Each document shows: title, priority badge, status
- [ ] Priority badges: Normal (gray), High (orange), Critical (red)
- [ ] Status: Unread, Read, Acknowledged
- [ ] Click to open document (new tab/viewer)
- [ ] "I Acknowledge" checkbox/button per document
- [ ] Acknowledgment timestamp display
- [ ] Progress indicator (X of Y acknowledged)

---

## 👔 PHC ADMINISTRATOR PORTAL

### Authentication Screens

| # | Screen | Priority | User Story | Status |
|---|--------|----------|------------|--------|
| ADM-01 | Admin Login | Critical | - | ⬜ Todo |
| ADM-02 | Admin Profile | Medium | - | ⬜ Todo |

---

### Main Navigation

| # | Screen | Priority | User Story | Status |
|---|--------|----------|------------|--------|
| ADM-03 | Dashboard | High | US-ADM-01 | ⬜ Todo |
| ADM-04 | Job Management | Critical | US-ADM-05, US-ADM-07 | ⬜ Todo |
| ADM-05 | Job Details / Applications | Critical | US-ADM-07 | ⬜ Todo |
| ADM-06 | Staff Management | High | - | ⬜ Todo |
| ADM-07 | Manual Assignment | Medium | US-ADM-02 | ⬜ Todo |
| ADM-08 | Emergency Job Posting | High | US-ADM-05 | ⬜ Todo |
| ADM-09 | Emergency Files | Medium | US-ADM-03, US-ADM-04 | ⬜ Todo |
| ADM-10 | Document Acknowledgment Tracker | High | US-ADM-08 | ⬜ Todo |
| ADM-11 | Attendance Verification | High | US-ERP-05 | ⬜ Todo |
| ADM-12 | System Logs | Medium | US-ADM-06 | ⬜ Todo |
| ADM-13 | Reports Dashboard | High | US-RPT-01, US-RPT-02, US-RPT-03 | ⬜ Todo |
| ADM-14 | Penalty Report | High | US-RPT-02 | ⬜ Todo |
| ADM-15 | Staff Score Report | Medium | US-RPT-03 | ⬜ Todo |

---

### Screen Details

#### ADM-03: Dashboard
**Priority:** High | **User Story:** US-ADM-01

**Components:**
- [ ] **Today's Jobs Widget**
  - Total / Filled / Unfilled counts
  - Fill rate percentage
  - Color indicator (green >95%, yellow 80-95%, red <80%)
- [ ] **Pending Applications Widget**
  - Count of applications awaiting review
  - Click to navigate to applications
- [ ] **Completed Shifts Widget**
  - Today's completed count
- [ ] **Cancellations Widget**
  - Today's cancellation count
  - Penalty breakdown
- [ ] **ERP Sync Status Widget**
  - Last sync timestamp
  - Status indicator (green/red)
  - Failed API calls count
- [ ] **Average Confirmation Time**
- [ ] **Score Distribution Histogram** (optional)
- [ ] Auto-refresh every 60 seconds
- [ ] Date range filter
- [ ] Export to PDF/Excel button

---

#### ADM-04: Job Management
**Priority:** Critical | **User Story:** US-ADM-05, US-ADM-07

**Components:**
- [ ] Tabs: Today | This Week | All Jobs
- [ ] Job list table
  - Columns: Date, Location, Time, Required, Filled, Status, Actions
- [ ] Status badges: Open (yellow), Filled (green), Cancelled (gray)
- [ ] Filter by: date, location, status
- [ ] Search by demand ID
- [ ] "Post Emergency Job" button (prominent)
- [ ] Click row to view job details

---

#### ADM-05: Job Details / Applications
**Priority:** Critical | **User Story:** US-ADM-07

**Components:**
- [ ] Job summary header (date, location, time, required count)
- [ ] **Applications Tab**
  - List of staff who applied
  - Each row: name, score, availability, work history summary
  - Sort by: score (desc), application time
  - "Approve" button (green)
  - "Reject" button (red) with optional reason
  - Bulk selection checkboxes
  - Bulk approve button
- [ ] **Assigned Staff Tab**
  - List of confirmed staff
  - Document acknowledgment status per staff
  - "Send Reminder" button
- [ ] **Unfilled Positions Alert**
  - Show if positions still unfilled
  - "Manual Assignment" button

---

#### ADM-07: Manual Assignment
**Priority:** Medium | **User Story:** US-ADM-02

**Components:**
- [ ] Search staff: name, staff number, availability
- [ ] Search results list
  - Each result: name, score, availability status, recent history
- [ ] Select staff button
- [ ] **Conflict Warning Panel** ⚠️
  - Overlapping shift warning
  - Blacklist warning
  - Unavailable warning
  - Fair sharing limit warning
- [ ] Override reason text area (min 20 chars, required)
- [ ] Character counter
- [ ] Confirm assignment button
- [ ] Cancel button

---

#### ADM-08: Emergency Job Posting
**Priority:** High | **User Story:** US-ADM-05

**Components:**
- [ ] Form: Facility selector
- [ ] Date picker
- [ ] Time range picker (start/end)
- [ ] Required staff count
- [ ] Urgency reason text area
- [ ] "Post Emergency Job" button (red/urgent styling)
- [ ] Confirmation modal
- [ ] Real-time filling progress (after posting)
- [ ] WhatsApp template preview

---

#### ADM-09: Emergency Files
**Priority:** Medium | **User Story:** US-ADM-03, US-ADM-04

**Components:**
- [ ] File upload area (drag & drop)
- [ ] Supported formats: PDF, DOC, DOCX, JPG, PNG (max 10MB)
- [ ] Title input (required)
- [ ] Description text area
- [ ] Priority selector: Normal, High, Critical
- [ ] Region multi-select: HKI, KLN, NT
- [ ] Upload button
- [ ] **File Distribution Status**
  - Sent count
  - Viewed count
  - Acknowledged count
  - Staff who haven't viewed (red highlight)
- [ ] Export compliance report button

---

#### ADM-10: Document Acknowledgment Tracker
**Priority:** High | **User Story:** US-ADM-08

**Components:**
- [ ] Job selector / filter
- [ ] Staff list with acknowledgment status
  - Columns: Staff Name, Documents Required, Viewed, Acknowledged
  - Status indicators: ✓ (green), ✗ (red)
  - Unacknowledged rows highlighted red
- [ ] Filter: All / Acknowledged / Pending
- [ ] "Send Reminder" button per staff
- [ ] "Send Bulk Reminder" button
- [ ] Export report button

---

#### ADM-11: Attendance Verification
**Priority:** High | **User Story:** US-ERP-05

**Components:**
- [ ] List of shifts to verify (completed within last 24h)
- [ ] Each row: Staff, Location, Shift Time, Status
- [ ] "Verify" button per row
- [ ] **Verification Modal**
  - Staff details
  - Shift details
  - Actual hours input
  - Verification method: Phone confirmation
  - Notes field (for late arrival, early departure)
  - Confirm button
- [ ] Batch verification option

---

#### ADM-12: System Logs
**Priority:** Medium | **User Story:** US-ADM-06

**Components:**
- [ ] Log type tabs: API Calls | Staff Sync | Assignments | Scores | Admin Actions | Errors
- [ ] Filter by: date range, staff, endpoint, status
- [ ] Search by text
- [ ] Log entries table
  - Timestamp, Type, Details, Status
- [ ] Click to expand request/response details
- [ ] Export to CSV button

---

#### ADM-13: Reports Dashboard
**Priority:** High | **User Story:** US-RPT-01

**Components:**
- [ ] **Attendance Performance Section**
  - Fill rate metric (target: 95%+)
  - Attendance rate metric
  - Cancellation rate
  - Trend chart (line graph)
- [ ] **Top/Bottom Facilities Table**
- [ ] Date range filter
- [ ] Export button

---

#### ADM-14: Penalty Report
**Priority:** High | **User Story:** US-RPT-02

**Components:**
- [ ] Summary cards: Total Penalties, Total Amount, Avg per Staff
- [ ] Penalty list table
  - Columns: Date, Staff, Type, Amount, Score Impact
- [ ] Filter by: date range, staff, facility
- [ ] Trend analysis chart
- [ ] Export to Excel/PDF

---

#### ADM-15: Staff Score Report
**Priority:** Medium | **User Story:** US-RPT-03

**Components:**
- [ ] Score distribution histogram
- [ ] Staff with significant changes list
- [ ] Negative score staff list (requiring manual approval)
- [ ] Filter by: date range, score range, facility
- [ ] Export to Excel/PDF

---

## 💰 FINANCE ADMINISTRATOR PORTAL

### Screens

| # | Screen | Priority | User Story | Status |
|---|--------|----------|------------|--------|
| FIN-01 | Settlement Reconciliation | High | US-FIN-01 | ⬜ Todo |
| FIN-02 | Discrepancy Investigation | High | US-FIN-02 | ⬜ Todo |

---

### Screen Details

#### FIN-01: Settlement Reconciliation
**Priority:** High | **User Story:** US-FIN-01

**Components:**
- [ ] Period selector (month/year)
- [ ] "Generate Report" button
- [ ] **Summary Tab**
  - Total assignments (PHC vs ERP)
  - Total penalties (PHC vs ERP)
  - Match rate percentage
  - Match rate indicator (green >99%, red <99%)
- [ ] **Matched Tab**
  - List of matched records
- [ ] **Unmatched Tab**
  - List of discrepancies
  - Discrepancy type column
  - Click to investigate
- [ ] **Action List Tab**
  - Penalties not applied in ERP
  - ERP reference format
  - "Mark for Investigation" button
- [ ] Export to Excel button (all tabs)

---

#### FIN-02: Discrepancy Investigation
**Priority:** High | **User Story:** US-FIN-02

**Components:**
- [ ] Discrepancy details panel
  - Staff ID, name, contact
  - Assignment date, location, shift time
  - Penalty type and amount
  - PHC record timestamp
  - ERP sync status
- [ ] Related API call logs
  - Request/response details
  - Error messages if any
- [ ] Investigation notes text area
- [ ] Status selector: Pending → In Progress → Resolved / Escalated
- [ ] Resolution notes (required for Resolved)
- [ ] "Mark as Resolved" button
- [ ] "Escalate" button
- [ ] Audit trail: who updated, when

---

## 📱 RESPONSIVE DESIGN REQUIREMENTS

### Mobile Priority (Nursing Assistant Portal)
All NA screens must be **mobile-first**:
- [ ] Touch-friendly buttons (min 44px)
- [ ] Single column layouts
- [ ] Bottom navigation bar
- [ ] Pull-to-refresh
- [ ] Swipe gestures for cards

### Desktop Priority (Admin/Finance Portal)
Admin screens optimized for **desktop**:
- [ ] Side navigation
- [ ] Data tables with sorting
- [ ] Multi-column layouts
- [ ] Keyboard shortcuts

---

## 🌐 BILINGUAL SUPPORT

All screens must support:
- [ ] English (EN)
- [ ] Traditional Chinese (繁體中文)
- [ ] Language toggle in header/settings
- [ ] RTL-safe layouts

---

## 🎨 UI COMPONENT LIBRARY

### Common Components Needed

| Component | Priority | Notes |
|-----------|----------|-------|
| Button (Primary, Secondary, Danger) | Critical | |
| Card | Critical | For shift/job listings |
| Modal | Critical | Confirmations, warnings |
| Table | Critical | Admin data tables |
| Badge/Tag | High | Status indicators |
| Form inputs | Critical | Text, select, date picker |
| Alert/Banner | High | Warnings, notifications |
| Tabs | High | Navigation within pages |
| Pagination | High | Lists |
| Toast notifications | High | Success/error feedback |
| Loading spinner | High | Async operations |
| Empty state | Medium | No data illustrations |
| Skeleton loader | Medium | Loading placeholders |

---

## 📊 DESIGN PRIORITY SUMMARY

### Phase 1 - Critical (MVP)
1. NA Login/Registration
2. NA Available Shifts + Apply
3. NA My Shifts + Cancel
4. ADM Login
5. ADM Dashboard
6. ADM Job Management + Applications

### Phase 2 - High Priority
1. NA Job History
2. NA Penalties
3. NA Document Acknowledgment
4. ADM Attendance Verification
5. ADM Document Tracker
6. ADM Emergency Job Posting
7. FIN Settlement Reconciliation

### Phase 3 - Medium Priority
1. NA Profile Settings
2. ADM Manual Assignment
3. ADM Emergency Files
4. ADM System Logs
5. ADM Reports
6. FIN Discrepancy Investigation

### Deferred
1. NA My Score (US-NA-04)

---

## CHANGE LOG

| Version | Date       | Author | Changes |
|---------|------------|--------|---------|
| 1.0     | 2025-11-27 | -      | Initial UI design todo list |

---

**Last Updated:** 2025-11-27
**Based On:** User Stories & Test Cases v1.1
