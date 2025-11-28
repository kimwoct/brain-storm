
# User Stories v1.1

**Prestige Health Care Match/Dispatch System (PHC)**

**Version:** 1.1
**Date:** 2025-11-27

**Aligned With:** Product Specification v1.5 (Human Screening Workflow)

---

## USER STORIES

### REQUIREMENTS TRACEABILITY MATRIX

| User Story | Related FRs        | Description                               |
| ---------- | ------------------ | ----------------------------------------- |
| US-NA-01   | FR-2, FR-3         | Receive job notification                  |
| US-NA-02   | FR-1, FR-2, FR-3   | Apply for available shift                 |
| US-NA-03   | FR-1, FR-3, FR-7   | Cancel shift with penalty warning         |
| US-NA-04   | FR-1               | View current score *(Deferred)*           |
| US-NA-05   | FR-1, FR-6         | View job history                          |
| US-NA-06   | FR-7               | View penalty history                      |
| US-NA-07   | FR-8               | Acknowledge required documents            |
| US-ADM-01  | FR-4, FR-5         | View real-time dashboard                  |
| US-ADM-02  | FR-2, FR-11        | Manual confirmation + notification        |
| US-ADM-03  | FR-8               | Upload acknowledgment documents/files     |
| US-ADM-04  | FR-3, FR-8         | Distribute acknowledgment documents/files |
| US-ADM-05  | FR-9               | Post emergency job                        |
| US-ADM-06  | FR-5, FR-12, FR-13 | View system logs and reports              |
| US-ADM-07  | FR-2               | View job applications overview            |
| US-ADM-08  | FR-8               | Verify document acknowledgment            |
| US-ERP-01  | FR-5               | Staff master data sync                    |
| US-ERP-02  | FR-5               | Location master data sync                 |
| US-ERP-03  | FR-5               | Job demand sync                           |
| US-ERP-04  | FR-2, FR-5         | Receive assignment submission             |
| US-ERP-05  | FR-5, FR-6         | Receive attendance records                |
| US-ERP-06  | FR-1, FR-5, FR-7   | Receive penalty records                   |
| US-FIN-01  | FR-10              | Generate settlement reconciliation report |
| US-FIN-02  | FR-10              | Investigate settlement discrepancy        |

---

### 1. Nursing Assistant (護理員) User Stories

#### US-NA-01: Receive Job Notification via Web Push Notification/WhatsApp
**As a** nursing assistant,
**I want** to receive job notifications via Web Push Notification/WhatsApp when shifts are available,
**So that** I can apply for suitable shifts quickly.

**Scenario:**
```gherkin
Given: PHC System has sent the web push notifcation when receive the new job posting from ERP system
Given: PHC coordinator has generated a WhatsApp template for available shifts
When: Coordinator sends the message to my WhatsApp (individual or broadcast)
Then: I receive notification with shift details
And: Message includes: date, location name, shift time, contact person
And: Message includes a application link to the PHC portal
And: I can click the link to view and apply for the shift
```

**Acceptance Criteria:**
✅ WhatsApp message includes: date, location name, shift time, contact person
✅ Application link opens PHC web portal with shift details
✅ Web push reminder sent if not applied within 2 hours (if logged into portal)
✅ Works on both mobile and desktop browsers
✅ Bilingual support (English + Traditional Chinese)

**Priority:** Critical

**Note:** WhatsApp is primary channel (manual template-based). Web push notification is secondary for portal alerts only.

---

#### US-NA-02: Apply for Available Shift
**As a** nursing assistant,
**I want** to apply for available shifts via the PHC web portal,
**So that** I can be considered for assignment by the PHC administrator.

**Scenario - Apply for Shift:**
```gherkin
Given: I click the application link from WhatsApp message
When: I open the PHC web portal
Then: I see the shift details (date, location, time, contact person, special notes)
And: I see the cancellation penalty warning
When: I click "Apply" button
Then: My application is recorded with status "pending_approval"
And: PHC administrator receives notification of my application
```

**Scenario - Application Approved:**
```gherkin
Given: I have applied for a shift
When: PHC administrator approves my application
Then: Assignment status changes to "confirmed"
And: I receive confirmation notification (WhatsApp or web push)
And: Assignment appears in "My Shifts" with confirmed status
And: My score will increase by +1 point upon attendance verification
```

**Acceptance Criteria:**
✅ Application recorded immediately with "pending_approval" status
✅ Cancellation penalty warning displayed before applying
✅ Admin notified of new application
✅ Score increases (+1 point) only after attendance verification (not upon confirmation)
✅ ERP updated via API after admin approval
✅ Confirmation visible in "My Shifts" section
✅ Conflict check: Cannot apply if already assigned to overlapping shift

**Priority:** Critical

**Note:** This implements the Human Screening Workflow per Product Spec v1.5 - staff apply, admin screens and approves.

---

#### US-NA-03: Cancel Shift with Penalty Warning
**As a** nursing assistant,
**I want** to cancel a confirmed shift when needed via the PHC portal,
**So that** the system can find a replacement, and I understand the consequences.

**Scenario - Early Cancellation (>48 hours before shift):**
```gherkin
Given: I have a confirmed assignment more than 48 hours before shift start
When: I navigate to "My Shifts" in the PHC portal
And: I click "Cancel Shift"
Then: I see confirmation modal: "You are cancelling with sufficient notice."
And: I see penalty details: -1 score, no financial penalty
When: I confirm cancellation
Then: Assignment status changes to "cancelled"
And: Score decreases by 1 point
And: No financial penalty applied
And: I receive cancellation confirmation
And: Re-matching triggered for the vacancy
```

**Scenario - Late Cancellation (<48 hours before shift):**
```gherkin
Given: I have a confirmed assignment less than 48 hours before shift start
When: I navigate to "My Shifts" in the PHC portal
And: I click "Cancel Shift"
Then: I see warning modal: "⚠️ Late Cancellation Warning: 300 HKD admin cost will be deducted!"
And: I see penalty details: -1 score AND -300 HKD
And: I see buttons: [Keep Shift] [Confirm Cancellation]
When: I click "Confirm Cancellation"
Then: Assignment status changes to "cancelled"
And: Score decreases by 1 point
And: 300 HKD penalty recorded for next settlement deduction
And: I receive cancellation confirmation
And: Re-matching triggered with urgent flag
```

**Acceptance Criteria:**
✅ System checks cancellation window (48-hour threshold)
✅ Warning modal displayed clearly for late cancellations
✅ Early cancellation: -1 score only, no financial penalty
✅ Late cancellation: -1 score AND 300 HKD penalty
✅ Staff can keep shift (reject cancellation) after seeing warning
✅ ERP updated via penalty API (POST /api/v1/penalties)
✅ Re-matching triggered for vacancy (urgent if <24 hours)
✅ Cancellation recorded in staff's assignment history
✅ Admin alerted if unfilled after 30 minutes

**Priority:** High

**Note:** Per Product Spec FR-7, only late cancellations (<48h) incur financial penalty.

---

#### US-NA-04: View My Score *(Deferred to Phase 2)*
**As a** nursing assistant,
**I want** to view my current score and score history,
**So that** I understand my reliability standing and can improve it.

**Acceptance Criteria:**
✅ Current score displayed as number (starting at 50, floor at -10)
✅ Score history available (last 10 changes)
✅ Each change shows: date, reason (attended/cancelled), impact (+1/-1)
✅ Assignment reference for each score change

**Priority:** Medium *(Deferred)*

**Note:** Per Product Spec v1.3, tier system (Gold/Silver/Bronze) was removed. System uses raw score values only for ranking. Negative scores require manual admin approval for assignments.

---

#### US-NA-05: View Job History
**As a** nursing assistant,
**I want** to view my job history and attendance records,
**So that** I can track completed shifts, review penalties, and verify my work history.

**Scenario - View Job History List:**
```gherkin
Given: I am logged into the PHC platform
When: I navigate to "My Job History" section
Then: I see a list of my past assignments sorted by date (newest first)
And: each record shows date, location name, shift time, and status
And: I can filter by date range and status
```

**Scenario - View Job Details:**
```gherkin
Given: I am viewing my job history list
When: I click on a specific job record
Then: I see detailed information including assignment date, shift times, location, clock-in/out times, attendance status, score impact, and any penalties applied
```

**Acceptance Criteria:**
✅ Job history displays past assignments (last 12 months)
✅ Each record shows: date, location, shift time, status
✅ Status clearly indicated: Completed, Cancelled, No-Show
✅ Score impact shown: +1 (attended), -1 (cancelled)
✅ Penalties displayed with amount (300 HKD for late cancellation) and reason
✅ Filter by date range available
✅ Filter by status available
✅ Pagination supported (20 records per page)
✅ Clock-in/out times displayed for completed shifts
✅ Export to PDF available

**Priority:** High

---

#### US-NA-06: View Penalty History
**As a** nursing assistant,
**I want** to view my penalty history,
**So that** I can understand past deductions and improve my reliability.

**Scenario:**
```gherkin
Given: I am logged into the PHC platform
When: I navigate to "My Penalties" section
Then: I see a list of all penalties applied to my account
And: Each record shows: date, type (late cancellation), amount (300 HKD), score impact (-1)
And: I can see the related assignment details
```

**Acceptance Criteria:**
✅ Penalty history displays all past penalties
✅ Each record shows: date, penalty type, amount, score impact
✅ Related assignment details accessible
✅ Filter by date range available
✅ Penalties synced with ERP records
✅ Clear explanation of penalty reason shown

**Priority:** High

---

### 2. PHC Admin User Stories (Continued)

#### US-ADM-07: View Job Applications Overview
**As a** PHC administrator,
**I want** to view all staff applications for each job posting,
**So that** I can screen candidates and approve assignments.

**Scenario:**
```gherkin
Given: A job posting has received staff applications
When: I navigate to the job posting details
Then: I see a list of all staff who have applied
And: Each applicant shows: name, score, availability status, relevant history
And: I can approve or reject each application
When: I approve an application
Then: The assignment is confirmed and staff is notified
```

**Acceptance Criteria:**
✅ All applications visible for each job posting
✅ Applicant details include score and work history
✅ Approve/reject actions available
✅ Bulk approval supported for multiple applicants
✅ Rejected applicants notified with reason (optional)
✅ Approved assignments synced to ERP

**Priority:** High

**Note:** This replaces the removed Care Home Supervisor role. PHC Admin now handles application screening.

---

#### US-ADM-08: Verify Staff Document Acknowledgment
**As a** PHC administrator,
**I want** to verify that staff have read and acknowledged required documents (remarks, supplements, protocols) before starting their duty,
**So that** I can ensure compliance and staff preparedness.

**Scenario - View Document Acknowledgment Status:**
```gherkin
Given: A job posting has required documents attached (remarks, supplements, protocols)
When: I navigate to the job posting details
Then: I see a list of assigned staff with their document acknowledgment status
And: Each staff shows: name, documents required, documents viewed, documents acknowledged
And: Staff who have not acknowledged are highlighted in red
```

**Scenario - Send Reminder for Unacknowledged Documents:**
```gherkin
Given: Staff have not acknowledged required documents before shift start
When: I click "Send Reminder" for specific staff
Then: A push notification is sent reminding them to review documents
And: Reminder is logged in the system
```

**Acceptance Criteria:**
✅ Document acknowledgment status visible per staff per job
✅ Shows: document name, view timestamp, acknowledgment timestamp
✅ Unacknowledged documents clearly highlighted (red indicator)
✅ Filter by acknowledgment status (All/Acknowledged/Pending)
✅ Bulk reminder option for all staff with pending acknowledgments
✅ Individual reminder option per staff
✅ Report exportable showing acknowledgment compliance rate
✅ Staff cannot be marked as "ready for duty" until all required documents acknowledged
✅ Acknowledgment tracking synced with acknowledgment document distribution (FR-8)

**Priority:** High

---

#### US-NA-07: Acknowledge Required Documents
**As a** nursing assistant,
**I want** to view and acknowledge required documents before my shift,
**So that** I am prepared and compliant with duty requirements.

**Scenario:**
```gherkin
Given: I have a confirmed assignment with required documents
When: I navigate to my assignment details
Then: I see a list of required documents to review
And: Each document shows: title, priority (Normal/High/Critical), status (Unread/Read/Acknowledged)
When: I open and read a document
Then: The document is marked as "Read" with timestamp
When: I click "I Acknowledge" checkbox
Then: The document is marked as "Acknowledged" with click action
And: Admin can see my acknowledgment status
```

**Acceptance Criteria:**
✅ Required documents displayed prominently on assignment details
✅ Documents accessible via link (opens in new tab or viewer)
✅ Read status tracked when document is opened
✅ Acknowledgment requires explicit action (checkbox or button)
✅ Acknowledgment timestamp recorded
✅ Push notification reminder if documents not acknowledged 24h before shift
✅ Critical priority documents highlighted
✅ Acknowledgment status visible in "My Job History"

**Priority:** High

---

### 3. PHC Admin User Stories

#### US-ADM-01: View Real-Time Dashboard
**As a** PHC administrator,
**I want** to see real-time operational metrics on the dashboard,
**So that** I can monitor system health, track job fill rates, and identify issues.

**Dashboard Widgets:**
- Today's jobs (total/filled/unfilled)
- Confirmed staff vs pending applications
- Completed shifts
- Cancellations and penalties today
- API health status
- Last ERP sync time
- Failed API calls
- Average confirmation time
- Score distribution histogram

**Acceptance Criteria:**
✅ All metrics auto-refresh every 60 seconds
✅ Click any metric to drill down to details
✅ Color-coded status indicators (green/yellow/red)
✅ Load time < 30 seconds
✅ Filter by date range, facility, shift type
✅ Export to PDF/Excel for management reports

**Priority:** High

**Note:** Per Product Spec v1.2, no-show tracking was removed. Dashboard shows completed vs cancelled shifts only.

---

#### US-ADM-02: Manual confirmation + notification
**As a** PHC administrator,
**I want** to manually confirm specific staff to jobs and send confirmation notification,
**So that** I can handle special facility requests, unique qualifications, and emergency situations.

**Scenario:**
```gherkin
Given: A job demand is unfilled or requires specific staff
When: I click "Manual Confirmation" on the job details
And: I search for staff by name, staff number, or availability
Then: I see search results with staff profiles (from ERP)
And: Each result shows: name, score, availability, recent history
When: I select a staff member
Then: System displays conflict warnings if any:
  - Staff already assigned to overlapping shift
  - Staff on facility blacklist
  - Staff unavailable that day
  - Staff will exceed fair sharing limits
When: I enter override reason (max 100 words)
And: I confirm assignment
Then: Assignment created with assigned_by = "manual_admin" or "admin_id"
And: Confimration notification send to staff or copy WhatsApp template generated for coordinator to send
And: Override logged with: admin ID, timestamp, reason, original match (if any)
```

**Acceptance Criteria:**
✅ Search by name, staff number, score, location preference, availability status
✅ Staff profiles fetched from ERP with current data
✅ Conflict warnings displayed clearly (from ERP data)
✅ Override reason required (minimum 20 characters)
✅ Audit trail complete and immutable
✅ ERP updated with manual assignment flag
✅ WhatsApp template ready for coordinator
✅ Original algorithm selection recorded for analysis

**Priority:** Medium

**Note:** Per Product Spec FR-11, audit trail cannot be deleted or modified after creation.

---

#### US-ADM-03: Upload Acknowledgment Documents/Files
**As a** PHC admin,
**I want** to upload acknowledgment documents/files,
**So that** I can quickly distribute critical information to staff.

**Acceptance Criteria:**
✅ Upload/Share PDF, DOC, DOCX, JPG, PNG (max 10MB)
✅ Enter title (required), description, priority, regions
✅ Files stored securely (secure file server)
✅ Unique file ID generated
✅ Upload logged with my admin ID

**Priority:** Medium

---

#### US-ADM-04: Distribute Acknowledgment Documents/Files
**As a** PHC administrator,
**I want** to distribute acknowledgment documents/files to relevant staff via WhatsApp and web push,
**So that** they receive critical information quickly.

**Scenario:**
```gherkin
Given: I uploaded an acknowledgment document with priority = Critical
And: I specified target regions (e.g., HKI, KLN)
When: File upload completes successfully
Then: System identifies affected staff based on regions
And: Generates WhatsApp message template with file link
And: Coordinator sends WhatsApp to affected staff
And: For Critical priority: Web push notification sent as in-app alert
And: Notification appears in staff's device
And: System tracks who viewed the file
And: System tracks who confirmed receipt
```

**Acceptance Criteria:**
✅ WhatsApp template generated with file link within 5 minutes
✅ Only affected staff notified (filtered by region if specified)
✅ Web push notification for Critical priority
✅ View tracking works (accurate counts per staff)
✅ Confirmation tracking works (explicit acknowledgment)
✅ Admin dashboard shows: sent count, viewed count, confirmed count
✅ Staff who haven't viewed highlighted in red
✅ Report exportable for compliance documentation

**Priority:** Medium

**Note:** WhatsApp is primary channel per Product Spec FR-3. Web push notification is supplementary for in-portal alerts.

---

#### US-ADM-05: Post Emergency Job
**As a** PHC administrator,
**I want** to post emergency jobs manually,
**So that** urgent staffing needs are filled immediately without waiting for the standard polling cycle.

**Scenario:**
```gherkin
Given: There is an urgent staffing need (e.g., 2 staff needed today 18:00-22:00)
When: I click "Emergency Job Posting" in the admin portal
And: I fill the form: facility, date/time, staff count, urgency reason
And: I click "Post Emergency Job"
Then: Job posted immediately (bypasses 15-minute polling delay)
And: Matching engine runs instantly
And: Urgent WhatsApp template generated for shortlisted staff
And: Coordinator sends WhatsApp with urgent flag
And: In-app alert sent via web push notification (Critical priority)
And: Dashboard shows real-time filling progress
And: If unfilled after 30 minutes: admin receives push/email alert
```

**Acceptance Criteria:**
✅ No delay in posting (bypasses standard 15-minute polling)
✅ Matching triggered instantly
✅ Urgent WhatsApp template with "URGENT" badge
✅ Web push notification in-app alert for Critical priority
✅ Dashboard updates with real-time filling progress
✅ Admin alert sent if unfilled after 30 minutes
✅ Staff can accept immediately via portal
✅ ERP updated within 1 minute of confirmation

**Priority:** High

**Note:** Per Product Spec FR-9, emergency jobs receive highest priority in the matching engine.

---

#### US-ADM-06: View System Logs
**As a** PHC admin,
**I want** to view system logs and API calls,
**So that** I can troubleshoot issues and monitor activity.

**Logs Available:**
- All ERP API calls (request/response)
- Staff sync logs (success/failure)
- Assignment status changes
- Score changes
- Admin actions (logins, overrides)
- Error logs

**Acceptance Criteria:**
✅ Filter by date range, staff, endpoint, status
✅ Search by text
✅ View request/response details
✅ Logs retained for 90 days
✅ Export logs to CSV

**Priority:** Medium

---

### 4. ERP Team User Stories

#### US-ERP-01: Staff Master Data Sync
**As an** ERP system,
**I want** to provide staff data to PHC daily,
**So that** PHC has up-to-date nursing assistant information.

**Sync Frequency:** Daily 02:00 AM
**Data Provided:**
- Staff ID, names, contact info, HKID
- Bank account details
- Certificate expiry dates
- Status (active/inactive)

**Acceptance Criteria:**
✅ API responds in <3 seconds
✅ Pagination support (100 items per page)
✅ All active staff returned
✅ No duplicate staff IDs

**Priority:** Critical

---

#### US-ERP-02: Location Master Data Sync
**As an** ERP system,
**I want** to provide location data to PHC daily,
**So that** PHC knows all available care homes and their requirements.

**Sync Frequency:** Daily 03:00 AM
**Data Provided:**
- Location ID, name, address, contact
- Region, district
- Underlist (priority staff list)
- Blacklist
- Special requirements

**Acceptance Criteria:**
✅ API responds in <3 seconds
✅ Only active locations returned
✅ Underlist ordered by priority
✅ Blacklist accurate

**Priority:** Critical

---

#### US-ERP-03: Job Demand Sync
**As an** ERP system,
**I want** to provide job demands to PHC every 15 minutes,
**So that** PHC can match staff to fill care home needs.

**Sync Frequency:** Every 15 minutes (or webhook push)
**Data Provided:**
- Demand ID, location, date, time
- Required staff count
- Assigned count
- Status (open/filled/cancelled)
- Priority, special requirements

**Acceptance Criteria:**
✅ API responds in <3 seconds
✅ Unfilled demands (status: open) returned
✅ Full demand details provided
✅ Webhook supported (optional)

**Priority:** Critical

---

#### US-ERP-04: Receive Assignment Submission
**As an** ERP system,
**I want** to receive approved staff assignments from PHC,
**So that** I can track confirmed placements and process payroll.

**API:** POST /api/v1/jobs/assignments
**Trigger:** When PHC admin approves a staff application
**Data Received:**
- PHC assignment ID, demand ID, staff ID, location ID
- Date, shift times, assigned timestamp
- assigned_by: "system_auto" or "manual_admin"

**Acceptance Criteria:**
✅ Accepts valid assignment data
✅ Returns ERP assignment ID
✅ Validates staff availability (no conflicts)
✅ Returns 409 if staff unavailable or already assigned
✅ Response time < 3 seconds

**Priority:** Critical

**Note:** Per Product Spec v1.5, assignments submitted after admin screening approval.

---

#### US-ERP-05: Receive Attendance Records
**As an** ERP system,
**I want** to receive attendance records from PHC,
**So that** I can calculate accurate payroll.

**API:** POST /api/v1/attendance
**Trigger:** Post-shift verification by PHC admin (within 1 hour of shift completion)
**Data Received:**
- Assignment ID, staff ID, location ID
- Shift date
- Actual hours worked (calculated decimal)
- Status: completed, partial
- Verification method: admin_portal, phone_confirmation
- Verified by: admin user_id
- Notes (for late arrival, early departure)

**Acceptance Criteria:**
✅ Accepts valid attendance data
✅ Calculates payment based on actual hours
✅ Returns calculated payment amount
✅ Links to assignment and staff records
✅ Submitted within 1 hour of shift completion

**Priority:** High

**Note:** Per Product Spec v1.2, no-show status was removed. Admin verifies attendance via phone confirmation with facility contacts.

---

#### US-ERP-06: Receive Penalty Records
**As an** ERP system,
**I want** to receive penalty records from PHC,
**So that** I can deduct amounts from staff settlements.

**API:** POST /api/v1/penalties
**Trigger:** When staff cancels a confirmed shift
**Data Received:**
- Assignment ID, staff ID
- Penalty type: "cancellation" (>48h) or "late_cancellation" (<48h)
- Amount: 0 HKD (cancellation) or 300 HKD (late_cancellation)
- Score impact: -1
- Reason text

**Acceptance Criteria:**
✅ Accepts valid penalty data
✅ Deducts 300 HKD from next settlement (for late_cancellation only)
✅ Returns deduction confirmation with penalty_id
✅ Links to original assignment record

**Priority:** High

**Note:** Per Product Spec FR-7:
- Cancellation (>48h): -1 score only, NO financial penalty
- Late cancellation (<48h): -1 score AND 300 HKD penalty
- No-show penalties removed in v1.2



---

### 8. Finance Team User Stories

#### US-FIN-01: Generate Settlement Reconciliat ion Report

**As a** finance administrator,
**I want** to generate a monthly settlement reconciliation report,
**So that** I can verify PHC records match ERP settlements, identify discrepancies, and generate action lists for manual ERP updates.

**Scenario - Generate Monthly Report:**
```gherkin
Given: It is December 3, 2025
And: PHC has processed 150 staff assignments for November 2025
And: ERP has processed settlements for the same period
When: I select Reports → Settlement Reconciliation
And: I choose Period: November 2025
And: I click "Generate Report"
Then: System fetches settlement data from ERP via GET /api/v1/settlements/{period}
And: Compares each PHC assignment with ERP settlement record
And: Matches on: staff_id, assignment_id, hours worked, penalties
And: Calculates match rate (target: >99%)
And: Lists all discrepancies with categorization
And: Generates Excel export with Matched/Unmatched tabs
```

**Scenario - Generate Penalty Action List:**
```gherkin
Given: PHC has 15 late cancellation penalties for November 2025
And: 13 penalties have been applied in ERP
And: 2 penalties are missing in ERP
When: I generate the Settlement Reconciliation Report
Then: Report includes "Penalty Action List" section
And: Lists 2 missing penalties with: staff_id, assignment details, amount (300 HKD), date
And: Provides ERP reference numbers for manual update
And: I can export Action List as separate worksheet
```

**Discrepancy Categories:**
- Missing attendance record (PHC has, ERP missing)
- Penalty not applied (PHC penalty, ERP not deducted)
- Hours mismatch (actual hours differ)
- Rate discrepancy (payment amount differs)
- Missing assignment (ERP has, PHC missing)

**Acceptance Criteria:**
✅ Settlement data fetched from ERP by 1st of month
✅ Report generated by 3rd of each month
✅ Match rate calculated and displayed (target: >99%)
✅ All discrepancies categorized and listed with details
✅ Penalty Action List generated for manual ERP updates
✅ Export to Excel format (tabs: Summary, Matched, Unmatched, Action List)
✅ Historical reports accessible for audit trail

**Priority:** High

**Note:** Per Meeting Minutes (Section 6.1 - "Safe Mode"), PHC does NOT directly modify ERP financial data. The Settlement Reconciliation generates Action Lists for finance team to manually update ERP.

---

#### US-FIN-02: Investigate Settlement Discrepancy

**As a** finance administrator,
**I want** to investigate a flagged discrepancy,
**So that** I can resolve it by updating ERP manually and mark it as completed in PHC.

**Scenario - Investigate Missing Penalty:**
```gherkin
Given: Settlement Report shows 2 missing penalties in ERP
When: I click on a discrepancy row in the Action List
Then: I see full discrepancy details:
  - Staff ID, name, contact
  - Assignment date, location, shift time
  - Penalty type: late_cancellation
  - Amount: 300 HKD
  - PHC penalty record timestamp
  - ERP sync status: "Not Found"
And: I see related API call logs (POST /api/v1/penalties)
And: I can see if API call failed or was never triggered
```

**Scenario - Resolve Discrepancy:**
```gherkin
Given: I have investigated the discrepancy
And: I have manually updated ERP with the penalty
When: I click "Mark as Resolved"
And: I enter resolution notes: "Manually applied in ERP. Ref: ERP-PEN-12345"
Then: Discrepancy status changes to "Resolved"
And: Resolution logged with: my admin ID, timestamp, notes
And: Match rate recalculates for the period
```

**Acceptance Criteria:**
✅ Can view full discrepancy details with all related data
✅ Access to API call logs for debugging
✅ Add investigation notes (minimum 10 characters)
✅ Update status: Pending → In Progress → Resolved / Escalated
✅ Resolution requires notes (ERP reference number recommended)
✅ Audit trail: who resolved, when, what notes
✅ Cannot delete discrepancy records (immutable for audit)
✅ Escalated items notify finance manager via email

**Priority:** High

**Note:** PHC tracks resolution status but the actual financial correction is done manually in ERP. This maintains the "Safe Mode" principle from Meeting Minutes.

---

### 9. Reports User Stories

#### US-RPT-01: View Attendance Performance Dashboard

**As a** PHC administrator,
**I want** to view attendance performance metrics,
**So that** I can monitor system effectiveness.

**Metrics:**
- Fill rate (target: 95%+)
- No-show rate (target: <2%)
- Confirmation speed
- Score distribution

**Acceptance Criteria:**
✅ Dashboard shows real-time metrics
✅ Visualizations render correctly
✅ Filters work properly

**Priority:** High

---

#### US-RPT-02: Generate Penalty Summary Report

**As a** PHC administrator,
**I want** to generate a penalty summary report,
**So that** I can track cancellations and late cancellation penalties.

**Acceptance Criteria:**
✅ Lists all penalties by type (cancellation, late_cancellation)
✅ Shows amounts (300 HKD for late cancellation only)
✅ Shows score impacts (-1 for each)
✅ Trend analysis (improving/declining by period)
✅ Filter by date range, staff, facility
✅ Export to Excel/PDF

**Priority:** High

**Note:** Per Product Spec v1.2, no-show penalties were removed.

---

#### US-RPT-03: Generate Staff Score Report

**As a** PHC administrator,
**I want** to generate a staff score performance report,
**So that** I can identify top performers and staff needing attention.

**Acceptance Criteria:**
✅ Shows score distribution histogram (by score ranges)
✅ Lists staff with significant score changes
✅ Identifies staff with negative scores (requiring manual approval)
✅ Shows correlation between score and assignment success
✅ Filter by date range, score range, facility
✅ Export to Excel/PDF

**Priority:** Medium

**Note:** Per Product Spec v1.3, tier system (Gold/Silver/Bronze) was removed. Report uses raw score values only.

---

## TEST CASES

### TEST TRACEABILITY

| Test Case | Related FRs | Objective |
|-----------|-------------|-----------|
| TC-001 | FR-5 | Verify staff sync from ERP |
| TC-002 | FR-1, FR-2 | Matching algorithm with underlist and score ranking |
| TC-003 | FR-1, FR-5, FR-6 | Score update on attendance verification |
| TC-004 | FR-1, FR-3, FR-7 | Penalty on early cancellation (>48h) |
| TC-005 | FR-1, FR-3, FR-7 | Penalty on late cancellation (<48h) |
| TC-007 | FR-3, FR-8 | Acknowledgment document upload |
| TC-008 | FR-3, FR-9 | Emergency job posting |
| TC-ADM-01 | FR-4 | Admin dashboard functionality |
| TC-ERP-01 | FR-5 | ERP staff API response |
| TC-ERP-02 | FR-2, FR-5 | Assignment submission to ERP |
| TC-ERP-03 | FR-2 | Assignment conflict handling |
| TC-ERP-04 | FR-5, FR-6 | Attendance submission |
| TC-ERP-05 | FR-5, FR-7 | Penalty submission |
| TC-ERP-06 | FR-1, FR-5 | Score update to ERP |
| TC-ERP-07 | FR-5 | Error handling - API timeout |
| TC-ERP-08 | FR-5 | Webhook integration |
| TC-PERF-01 | FR-2 | Matching performance |
| TC-PERF-02 | FR-2, FR-5 | API response times |
| TC-SEC-01 | NFR | Authentication required |
| TC-SEC-02 | NFR | Data encryption |
| TC-RPT-01 | FR-10 | Settlement reconciliation |
| TC-RPT-02 | FR-13 | Attendance metrics |
| TC-FIN-01 | FR-10 | Settlement discrepancy investigation |

---

## USER STORY COVERAGE SUMMARY

**Updated Coverage Tracker:**

| FR    | Feature                          | Stories                                                          | Test Cases                                              | Coverage   |
| ----- | -------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------- | ---------- |
| FR-1  | Scoring Algorithm                | US-NA-02, US-NA-03, US-NA-05, US-ERP-06                          | TC-003, TC-004, TC-005                                  | ✓ Complete |
| FR-2  | Matching Engine                  | US-NA-01, US-ERP-04, US-ADM-02                                   | TC-002, TC-ERP-02, TC-ERP-03, TC-PERF-01                | ✓ Complete |
| FR-3  | WhatsApp + Web Push Notification | US-NA-01, US-NA-02, US-NA-05, US-ADM-04, US-ADM-05               | TC-007, TC-008                                          | ✓ Complete |
| FR-4  | Admin Dashboard                  | US-ADM-01                                                        | TC-ADM-01                                               | ✓ Complete |
| FR-5  | ERP Integration                  | US-ERP-01, US-ERP-02, US-ERP-03, US-ERP-05, US-ERP-06, US-ADM-06 | TC-001, TC-003, TC-ERP-01 through TC-ERP-08, TC-PERF-02 | ✓ Complete |
| FR-6  | Attendance Tracking              | US-NA-05                                                         | TC-ERP-04, TC-RPT-02                                    | ✓ Complete |
| FR-7  | Penalty Management               | US-NA-03, US-NA-05                                               | TC-004, TC-005, TC-ERP-05                               | ✓ Complete |
| FR-8  | Acknowledgment Document Upload            | US-ADM-03, US-ADM-04                                             | TC-007                                                  | ✓ Complete |
| FR-9  | Emergency Job Posting            | US-ADM-05                                                        | TC-008                                                  | ✓ Complete |
| FR-10 | Settlement Reconciliation        | US-FIN-01, US-FIN-02                                             | TC-RPT-01                                               | ✓ Complete |
| FR-11 | Manual Override                  | US-ADM-02                                                        | TC-ERP-02                                               | ✓ Complete |
| FR-12 | System Monitoring                | US-ADM-06                                                        | TC-ERP-07                                               | ✓ Complete |
| FR-13 | Reporting                        | US-RPT-01, US-RPT-02, US-RPT-03                                  | TC-RPT-02                                               | ✓ Complete |

**FR-10 Coverage:** Complete with 2 user stories (US-FIN-01, US-FIN-02) and 1 test case (TC-RPT-01)
**FR-13 Coverage:** Complete with 3 user stories (admin reports) and 1 test case (TC-RPT-02)

---

### STORY SUMMARY

**Total Stories: 24**
- Nursing Assistant stories (US-NA-01 to US-NA-07): 7
- Admin stories (US-ADM-01 to US-ADM-08): 8
- ERP System stories (US-ERP-01 to US-ERP-06): 6
- **Finance Team stories:** US-FIN-01 to US-FIN-02: **2**
- **Reports stories:** US-RPT-01 to US-RPT-03: **3**

**Deferred Stories:** US-NA-04 (Score tiers removed, raw scores only)

**Priorities:**
- Critical: 6 stories
- High: 9 stories
- Medium: 8 stories
- Low: 0 stories

---



---

### 1. Functional Test Cases

#### TC-001: Staff Sync from ERP
**Objective:** Verify staff data syncs correctly from ERP

**Preconditions:**
- ERP has 150 active staff
- Last sync was yesterday
- 5 new staff added to ERP today
- 3 staff changed contact info

**Test Steps:**
1. Trigger staff sync job at 02:00 AM
2. Check database after sync

**Expected Results:**
✅ All 150 staff exist in PHC database
✅ 5 new staff created with all fields populated
✅ 3 updated staff reflect new contact info
✅ No duplicate staff records
✅ Sync completed in <5 minutes
✅ Success rate: 100%

**Priority:** Critical

---

#### TC-002: Matching Algorithm - Basic Match
**Objective:** Verify matching selects appropriate staff based on underlist priority and score ranking

**Preconditions:**
- Job demand: 2025-11-25, 08:00-20:00, 1 staff needed
- Location: Hong Kong Care Home (CH_HKI_001)
- Underlist: Staff A (priority 1), Staff B (priority 2)
- Staff scores: A=15, B=25, C=8
- All staff: available, valid docs, not blacklisted

**Test Steps:**
1. Create job demand
2. Run matching algorithm

**Expected Results:**
✅ Underlist applied first: Staff A selected (highest underlist priority)
✅ If Staff A unavailable: Staff B selected (next on underlist)
✅ If both unavailable: Staff B selected (highest raw score = 25)
✅ Blacklisted staff not considered
✅ Unavailable staff not considered
✅ Matching completed within 5 minutes

**Priority:** Critical

**Note:** Per Product Spec v1.3, tier system removed. Ranking by raw score only.

---

#### TC-003: Score Update on Attendance Verification
**Objective:** Verify score increases when admin verifies staff attendance

**Preconditions:**
- Staff has score = 10
- Shift assignment confirmed and completed

**Test Steps:**
1. Verify staff score = 10 before shift
2. Admin opens Attendance Dashboard
3. Admin verifies attendance as "Present" via phone confirmation with facility
4. System submits attendance to PHC

**Expected Results:**
✅ Staff score = 11 (+1 point)
✅ Score history record created with reason "attended_shift"
✅ ERP API PATCH /api/v1/staff/{id}/score called
✅ Attendance submitted to ERP via POST /api/v1/attendance
✅ Score update visible in staff portal

**Priority:** Critical

**Note:** Per Product Spec v1.5, score updates upon admin attendance verification, not upon confirmation.

---

#### TC-004: Penalty on Early Cancellation (>48h)
**Objective:** Verify early cancellation applies score penalty only, no financial penalty

**Preconditions:**
- Staff has confirmed assignment (shift in 3 days)
- Staff score = 12
- Cancellation >48 hours before shift

**Test Steps:**
1. Staff opens PHC portal
2. Staff navigates to "My Shifts"
3. Staff clicks "Cancel Shift"
4. Reviews confirmation modal (no financial penalty warning)
5. Confirms cancellation
6. Check staff record

**Expected Results:**
✅ Confirmation modal displayed (no financial penalty mentioned)
✅ Cancellation confirmation notification sent
✅ Assignment status = cancelled
✅ Staff score = 11 (-1 point)
✅ NO financial penalty applied (amount = 0)
✅ Penalty record created (type: "cancellation", amount: 0, score_impact: -1)
✅ Re-matching triggered for vacancy
✅ ERP API POST /api/v1/penalties NOT called (or called with 0 amount)

**Priority:** Critical

**Note:** Per Product Spec FR-7, cancellation >48h has NO financial penalty, only score impact.

---

#### TC-005: Penalty on Late Cancellation (<48h)
**Objective:** Verify late cancellation penalties applied correctly

**Preconditions:**
- Staff has confirmed assignment
- Cancellation requested < 48 hours before shift
- Staff score = 15

**Test Steps:**
1. Staff clicks "Cancel Shift" in portal
2. Warning modal displayed with penalty details
3. Staff confirms cancellation

**Expected Results:**
✅ Warning modal displayed: "300 HKD admin cost will be deducted"
✅ Staff score = 14 (-1)
✅ Penalty record created (300 HKD, -1 score)
✅ Staff receives web push notification
✅ ERP API called (penalty submission)
✅ Re-matching triggered for vacancy

**Priority:** High

---

#### TC-007: Acknowledgment Document Upload
**Objective:** Verify admin can upload and distribute acknowledgment documents/files

**Preconditions:**
- Admin logged in
- File: "Typhoon Emergency Procedures.pdf" (5MB)

**Test Steps:**
1. Navigate to Acknowledgment Documents
2. Click "Upload File"
3. Select PDF file
4. Enter title, description, priority=Critical, region=HKI
5. Submit

**Expected Results:**
✅ File uploaded to S3/Azure Blob
✅ File metadata saved to database
✅ File appears in acknowledgment document list
✅ WhatsApp notification sent to all HKI staff within 5 minutes
✅ Staff can view file via link
✅ Track view and confirmation

**Priority:** Medium

---

#### TC-008: Emergency Job Posting
**Objective:** Verify emergency job bypasses standard workflow

**Preconditions:**
- Urgent need: 2 staff today 18:00-22:00
- Location: New Territories Care Home

**Test Steps:**
1. Admin clicks "Emergency Job Posting"
2. Fill form with urgent details
3. Submit

**Expected Results:**
✅ Job posted immediately (no 15-min delay)
✅ Matching runs instantly
✅ Urgent web push notification sent with in-app alert
✅ Real-time dashboard shows progress
✅ Admin alerted if not filled in 30 minutes

**Priority:** High

---

#### TC-ADM-01: Admin Dashboard Functionality
**Objective:** Verify admin dashboard displays real-time metrics correctly

**Preconditions:**
- Admin user logged in
- System has active data (jobs, assignments, staff)
- ERP sync completed within last 24 hours

**Test Data:**
- Today's jobs: 20 total, 18 filled, 2 unfilled
- Pending applications: 5
- Completed shifts today: 15
- Cancellations today: 2
- Last ERP sync: 02:00 AM today

**Test Steps:**
1. Admin navigates to Dashboard
2. Verify all widgets load
3. Check Today's Jobs widget
4. Check Pending Applications widget
5. Check Completed Shifts widget
6. Check Cancellations widget
7. Check ERP Sync Status widget
8. Wait 60 seconds for auto-refresh
9. Click on a metric to drill down
10. Apply date filter
11. Export report

**Expected Results:**
✅ Dashboard loads within 30 seconds
✅ Today's Jobs shows: 20 total, 18 filled (90%), 2 unfilled
✅ Pending Applications shows: 5 awaiting review
✅ Completed Shifts shows: 15
✅ Cancellations shows: 2 with penalty breakdown
✅ ERP Sync Status shows: "Last sync: 02:00 AM" with green indicator
✅ All widgets auto-refresh after 60 seconds
✅ Click drill-down opens detailed view
✅ Date filter updates all widgets correctly
✅ Export generates PDF/Excel with current data
✅ Color indicators correct: green (good), yellow (warning), red (critical)

**Priority:** High

---

### 2. ERP Integration Test Cases

#### TC-ERP-01: Staff Sync API Response
**Objective:** Verify ERP returns staff data in correct format

**API Call:** GET /api/v1/staff/active

**Expected Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "staff_id": "ERP001",
      "name_chinese": "陳小明",
      "name_english": "Chan Siu Ming",
      "hkid": "A123456(7)",
      "contact_number": "91234567",
      "whatsapp_number": "91234567",
      "email": "chan@email.com",
      "status": "active",
      "certificates": [ ... ],
      "bank_account": { ... }
    }
  ],
  "pagination": { "total": 150, "page": 1, "per_page": 100 }
}
```

**Validation:**
✅ Response time < 3 seconds
✅ All required fields present
✅ HKID format valid
✅ Phone numbers 8 digits
✅ Staff status = active

**Priority:** Critical

---

#### TC-ERP-02: Assignment Submission to ERP
**Objective:** Verify PHC successfully submits assignments to ERP

**API Call:** POST /api/v1/jobs/assignments

**Request:**
```json
{
  "phc_assignment_id": "PHC-001",
  "demand_id": "DEM456",
  "location_id": "LOC789",
  "staff_id": "STF123",
  "assignment_date": "2025-11-25",
  "shift_start": "08:00",
  "shift_end": "20:00",
  "assigned_by": "system_auto"
}
```

**Expected Response (201):**
```json
{
  "status": "success",
  "assignment_id": "ERP-ASSIGN-001",
  "message": "Assignment submitted successfully"
}
```

**Validation:**
✅ ERP returns assignment_id
✅ Status = success
✅ Response time < 3 seconds

**Priority:** Critical

---

#### TC-ERP-03: Assignment Conflict Handling
**Objective:** Verify re-matching when ERP rejects assignment

**Preconditions:**
- Staff already assigned to another job in ERP
- ERP will return conflict

**API Call:** POST /api/v1/jobs/assignments

**Expected Response (409):**
```json
{
  "status": "error",
  "error_code": "STAFF_UNAVAILABLE",
  "message": "Staff has been assigned to another job"
}
```

**System Behavior:**
✅ PHC receives 409
✅ Staff removed from candidate pool
✅ Next best candidate selected
✅ New assignment submitted to ERP
✅ No manual intervention needed

**Priority:** High

---

#### TC-ERP-04: Attendance Submission
**Objective:** Verify attendance data submitted to ERP for payroll

**API Call:** POST /api/v1/attendance

**Request:**
```json
{
  "assignment_id": "ERP-ASSIGN-001",
  "staff_id": "STF123",
  "location_id": "LOC789",
  "shift_date": "2025-11-25",
  "clock_in": "2025-11-25T07:55:00Z",
  "clock_out": "2025-11-25T20:05:00Z",
  "actual_hours": 12.17,
  "status": "completed"
}
```

**Expected Response (200):**
```json
{
  "status": "success",
  "attendance_id": "ATT-001",
  "payment_calculated": 1800.00,
  "penalty_applied": 0
}
```

**Validation:**
✅ Payment calculated by ERP
✅ Hours match actual clock time
✅ No penalties (if attended)

**Priority:** High

---

#### TC-ERP-05: Penalty Submission
**Objective:** Verify penalty records submitted to ERP for deduction

**API Call:** POST /api/v1/penalties

**Request (Late Cancellation):**
```json
{
  "assignment_id": "ERP-ASSIGN-001",
  "staff_id": "STF123",
  "penalty_type": "late_cancellation",
  "amount": 300.00,
  "score_impact": -1,
  "reason": "Cancelled within 48 hours"
}
```

**Expected Response (200):**
```json
{
  "status": "success",
  "penalty_id": "PEN-001",
  "payment_adjusted": true,
  "adjusted_amount": 300.00
}
```

**Validation:**
✅ Penalty ID returned
✅ Payment adjusted = true
✅ Correct amount (300 HKD)

**Priority:** High

**Note:** Actual financial deduction API to be tested when available

---

#### TC-ERP-06: Score Update to ERP
**Objective:** Verify score changes synced to ERP

**API Call:** PATCH /api/v1/staff/{id}/score

**Request:**
```json
{
  "score_change": 1,
  "new_score": 16,
  "reason": "attended_shift",
  "assignment_id": "ERP-ASSIGN-001"
}
```

**Expected Response (200):**
```json
{
  "status": "success",
  "staff_id": "STF123",
  "new_score": 16
}
```

**Validation:**
✅ New score returned
✅ Score change recorded in ERP

**Priority:** Medium

---

#### TC-ERP-07: Error Handling - API Timeout
**Objective:** Verify retry logic when ERP API times out

**Test Scenario:**
1. Mock ERP API to timeout after 30 seconds
2. PHC calls assignment submission
3. First attempt times out
4. PHC retries with exponential backoff

**Expected Behavior:**
✅ First attempt fails after 30s
✅ 5-minute wait before 2nd attempt
✅ 15-minute wait before 3rd attempt
✅ After 3 failures, alert admin
✅ Job queued for manual retry

**Priority:** High

---

#### TC-ERP-08: Webhook Integration (if enabled)
**Objective:** Verify real-time job demand processing via webhook

**Webhook Payload:**
```json
{
  "event": "job_demand_created",
  "timestamp": "2025-11-20T10:00:00Z",
  "data": {
    "demand_id": "DEM789",
    "location_id": "LOC456",
    "required_date": "2025-11-25",
    "shift_start": "14:00",
    "shift_end": "22:00",
    "required_count": 2,
    "priority": "urgent"
  }
}
```

**Expected Behavior:**
✅ PHC receives webhook within 1 minute
✅ Demand created in PHC
✅ Matching triggered within 2 minutes
✅ No 15-minute polling delay

**Priority:** Medium

---

### 3. Performance Test Cases

#### TC-PERF-01: Matching with Large Dataset
**Objective:** Verify matching completes within 5 minutes with 500+ staff

**Test Setup:**
- 500 active staff in database
- Various underlists, blacklists, scores
- 10 job demands to process

**Expected Result:**
✅ All 10 demands matched within 5 minutes
✅ Algorithm applied all filters correctly
✅ No partial matches

**Priority:** High

---

#### TC-PERF-02: API Response Time
**Objective:** Verify API meets performance SLA

**Test:** Measure response time for key APIs

**Expected Results:**

| API                | Target | Acceptable |
| ------------------ | ------ | ---------- |
| POST /assignments  | <2s    | <3s        |
| PATCH /status      | <1s    | <2s        |
| POST /attendance   | <2s    | <3s        |
| GET /dashboard     | <3s    | <5s        |
| ERP API calls      | <3s    | <5s        |

**Priority:** Medium

---

### 4. Security Test Cases

#### TC-SEC-01: Authentication Required
**Objective:** Verify all endpoints require authentication

**Test:** Call endpoints without JWT token

**Expected Results:**
✅ All endpoints return 401 Unauthorized
✅ Admin endpoints require admin role
✅ Supervisor endpoints require supervisor role

**Priority:** Critical

---

#### TC-SEC-02: Data Encryption
**Objective:** Verify sensitive data encrypted

**Test:** Check database for HKID, bank accounts

**Expected Results:**
✅ HKID encrypted at rest
✅ Bank accounts encrypted at rest
✅ No plain text sensitive data

**Priority:** Critical

---

### 5. Finance Test Cases

#### TC-FIN-01: Settlement Discrepancy Investigation
**Objective:** Verify finance admin can investigate and resolve discrepancies

**Preconditions:**
- Settlement Report generated for previous month
- Discrepancy exists (e.g., missing penalty in ERP)
- Finance admin logged in

**Test Steps:**
1. Navigate to Reports → Settlement Reconciliation
2. Generate report for relevant period
3. Click on a discrepancy in the Action List
4. Review discrepancy details and API logs
5. Manually update ERP (simulated)
6. Click "Mark as Resolved" and enter notes

**Expected Results:**
✅ Discrepancy details viewable with all context
✅ API logs accessible
✅ Status changes to "Resolved" after confirmation
✅ Resolution notes saved in audit trail
✅ Match rate updated for the period

**Priority:** High

---

### 6. Report Test Cases

#### TC-RPT-01: Settlement Reconciliation Accuracy
**Objective:** Verify settlement reconciliation report correctly identifies discrepancies

**Test Data:**
- Period: November 2025
- PHC assignments: 150 staff worked
- PHC penalties: 15 late cancellations (300 HKD each = 4,500 HKD total)
- ERP penalties: 13 applied (3,900 HKD)
- Expected discrepancy: 2 penalties missing in ERP (600 HKD)

**Preconditions:**
- November 2025 assignments completed
- ERP settlement data available via API
- Finance administrator logged in

**Test Steps:**
1. Navigate to Reports → Settlement Reconciliation
2. Select Period: November 2025
3. Click "Generate Report"
4. Review Summary tab
5. Review Unmatched tab
6. Review Action List tab

**Expected Results:**
✅ Report generated within 30 seconds
✅ Match rate displayed: 13/15 = 86.7% (penalties)
✅ Summary shows: 150 assignments, 15 PHC penalties, 13 ERP penalties
✅ Unmatched tab lists 2 missing penalties with details:
   - Staff ID, assignment date, location, amount (300 HKD)
   - Discrepancy type: "Penalty not applied"
✅ Action List provides ERP reference format for manual update
✅ Export to Excel includes all tabs (Summary, Matched, Unmatched, Action List)
✅ Discrepancies can be marked for investigation

**Priority:** High

---

#### TC-RPT-02: Attendance Performance Metrics
**Objective:** Verify attendance dashboard shows correct metrics

**Test Data:**
- Period: Nov 1-30, 2025
- 500 assignments created
- 475 assignments filled (confirmed)
- 25 assignments unfilled
- 450 attended (from confirmed)
- 25 cancelled (from confirmed)

**Test Steps:**
1. View Attendance Performance Dashboard for November 2025
2. Check fill rate metric
3. Check attendance rate metric
4. Verify visualization data

**Expected Results:**
✅ Fill rate: 475/500 = 95.0%
✅ Attendance rate: 450/475 = 94.7%
✅ Cancellation rate: 25/475 = 5.3%
✅ Chart shows trend correctly (improving/declining)
✅ Table shows top/bottom performing facilities

**Priority:** High

**Note:** Per Product Spec v1.2, no-show tracking was removed. Metrics show completed vs cancelled only.

---

## TEST EXECUTION SUMMARY

### Test Coverage Targets

| Category | Test Cases | Status |
|----------|-----------|--------|
| Functional | 8 | Pending |
| ERP Integration | 8 | Pending |
| Performance | 2 | Pending |
| Security | 2 | Pending |
| Finance & Reports | 3 | Pending |
| **Total** | **23** | **Pending** |

---

### Testing Schedule

**Phase 1: Unit Testing (Days 1-15)**
- Individual component testing
- Mock external APIs

**Phase 2: Integration Testing (Days 16-30)**
- End-to-end flow testing
- Test with ERP sandbox

**Phase 3: System Testing (Days 31-40)**
- Full system testing
- Performance testing
- Security testing

**Phase 4: UAT (Days 41-50)**
- User acceptance testing
- Real-world scenarios

**Total Testing Window: 50 days** (within 60-day timeline)

---

## CHANGE LOG

| Version | Date       | Author          | Changes                                                      |
| ------- | ---------- | --------------- | ------------------------------------------------------------ |
| 1.0     | 2025-11-24 | System Analyst  | Initial draft                                                |
| 1.1     | 2025-11-27 | System Analyst  | Aligned with Product Spec v1.5 (Human Screening Workflow)    |

**v1.1 Changes (2025-11-27):**

**Terminology Alignment:**
- US-NA-01: Renamed to "Receive Job Notification via WhatsApp" (WhatsApp primary, web push notification secondary)
- US-NA-02: Renamed to "Apply for Available Shift" with Human Screening Workflow (staff apply, admin screens)
- US-NA-03: Clarified early vs late cancellation penalties per FR-7

**Removed:**
- Supervisor role stories (US-CS-01, US-CS-03): Removed per Product Spec v1.2
- Score tier system references: Removed per Product Spec v1.3 (raw scores only)
- No-show penalty references: Removed per Product Spec v1.2

**Updated:**
- US-NA-04: Deferred to Phase 2 (tier system removed)
- US-ADM-01: Dashboard auto-refresh changed to 60 seconds (was 30)
- US-ADM-02: Enhanced with full conflict warning and audit trail details
- US-ERP-04/05/06: Updated to reflect Human Screening Workflow and attendance verification
- TC-002/003/004/005: Updated test case names and scenarios
- TC-006: Marked as Deferred to v2.0 (QR Code System)

**Clarifications:**
- Score increases upon attendance verification, not confirmation
- Early cancellation (>48h): -1 score only, NO financial penalty
- Late cancellation (<48h): -1 score AND 300 HKD penalty

---

**Last Updated:** 2025-11-27
**Next Review:** Before testing begins
**Aligned With:** Product Specification v1.5, PHC Meeting Minutes, PHC Requirements

