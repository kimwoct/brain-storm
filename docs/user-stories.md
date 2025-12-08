
# User Stories v1.0

> Prestige Health Care Match/Dispatch System (PHC).

**Version:** 1.0
**Date:** 2025-12-08

---

## VIEWS

Based on the user stories, here is a list of views (UI screens/pages) that are required or mentioned to deliver the functions described. I've categorized them by user role and noted the associated user stories for context.

### ERP / Third-Party Integration Views

1. **ERP Integration Health & Logs View**
   - Shows ERP API uptime, error rates, retry queues, and recent request/response logs.
   - Mentioned in: US-ERP-01, US-ERP-02, US-ERP-03, US-ERP-04, US-ERP-05, US-ERP-06

2. **Master Data Sync Status View**
   - Displays last sync timestamps, record counts, and failure summaries for staff and locations; supports manual re-sync trigger.
   - Mentioned in: US-ERP-01, US-ERP-02

3. **Job Demand & Assignment Exchange Monitor**
   - Shows inbound job demands from ERP and outbound assignment submissions with statuses (success, conflict, retry pending).
   - Mentioned in: US-ERP-03, US-ERP-04

4. **Attendance & Penalty Submission Tracker**
   - Lists attendance and penalty payloads sent to ERP, with payment/penalty application status and reconciliation flags.
   - Mentioned in: US-ERP-05, US-ERP-06, US-FIN-01

### Nursing Assistant (Staff) Views

1. **User Dashboard**
   - Post-login container with tabs for Jobs List and Penalty History; default tab shows available jobs and filters; penalties tab shows penalty history.
   - Mentioned in: US-NA-00, US-NA-02, US-NA-03, US-NA-05, US-NA-06

2. **Jobs List View**
   - Shows available jobs by default; filters: Applied, My Jobs (confirmed), Job History.
   - Supports sorting (date/time), search, and pagination.
   - Entry points: apply/cancel, open Job Details; surfacing penalty warnings before cancel.
   - Mentioned in: US-NA-02, US-NA-03, US-NA-05

3. **Job Details View**
   - Job Details view showing full job info: facility/address, date/time, worker type, gender req, rate, special notes, penalties.
   - Staff actions: Apply (from link or list), view/cancel confirmed job, acknowledge documents.
   - Contains staff-only documents/acknowledgment section for confirmed assignments (US-NA-07).
   - Mentioned in: US-NA-01, US-NA-02, US-NA-05, US-NA-07

4. **Penalty History View**
   - Lists all penalties with details and related assignments.
   - Mentioned in: US-NA-06

### PHC Admin Views

1. **Admin Dashboard**
   - Real-time metrics (jobs, applications, jobs, API health); drill-down to details.
   - Mentioned in: US-ADM-01

2. **Job Details View**
   - Job Details view showing full job info: facility/address, date/time, worker type, gender req, rate, special notes, penalties.
   - Shows job info and applications with conflict indicators for screening/approvals.
   - All assignment actions (approve/confirm/manual assign) occur here.
   - Admin actions: approve/reject applications, manual confirm/override with reason, send notifications/templates.
   - Document controls: upload/distribute/track acknowledgment status for attached docs.
   - Mentioned in: US-ADM-03, US-ADM-04, US-ADM-07, US-ADM-08, US-ADM-02

3. **User List View**
   - Lists staff/users with search and filters (name, staff number, availability, score, region).
   - Shows conflict warnings (overlaps, blacklist, fair sharing) and quick profile context (read-only Jobs List/Penalty History views).
   - Deep-links into the target job's Job Details View to execute assignment actions; lookup/entry only (no approvals here).
   - Mentioned in: US-ADM-02

### Reports Views (Admin/Finance)

1. **Attendance Performance Dashboard**
   - Metrics like fill rate, attendance rate, and visualizations.
   - Mentioned in: US-RPT-01

2. **Penalty Summary Report**
   - Lists penalties by type with trends and filters.
   - Mentioned in: US-RPT-02

3. **Staff Score Report**
   - Shows score distributions and changes.
   - Mentioned in: US-RPT-03

4. **System Logs and Reports View**
   - Displays API calls, logs, and reports with filters.
   - Mentioned in: US-RPT-04

5. **Settlement Reconciliation Report**
   - Monthly report comparing PHC and ERP data; generates action lists.
   - Mentioned in: US-FIN-01

6. **Settlement Discrepancy Investigation View**
   - Details on discrepancies with API logs; allows marking as resolved.
   - Mentioned in: US-FIN-02

### Notes

- The PHC web portal is the overarching platform containing most of these views.
- ERP and finance stories (US-ERP-01..US-ERP-06, US-FIN-01..US-FIN-02) primarily involve external systems; ERP integration views above surface monitoring and operational controls.
- Some views overlap (e.g., job details appear in multiple contexts).
- View counting approach (excluding ERP/3rd-party integration monitors): ~11 distinct screens, represented as ~15 role-specific variants (e.g., shared User Dashboard tabs for Jobs/Penalties plus shared Job List/Details with staff-only or admin-only sections such as acknowledgments). NA-01 notifications are delivered via WhatsApp/web push and surface in the shared Job Details view when opened via the link.

---

## USER STORIES

### REQUIREMENTS TRACEABILITY MATRIX

| User Story | Description                               |
| ---------- | ----------------------------------------- |
| US-ERP-01  | Staff master data sync                    |
| US-ERP-02  | Location master data sync                 |
| US-ERP-03  | Job demand sync                           |
| US-ERP-04  | Receive assignment submission             |
| US-ERP-05  | Receive attendance records                |
| US-ERP-06  | Receive penalty records                   |
| US-NA-00   | Staff Login (ERP Credentials)             |
| US-NA-01   | Receive job notification                  |
| US-NA-02   | Apply for available job                   |
| US-NA-03   | Cancel job with penalty warning           |
| US-NA-05   | View job history                          |
| US-NA-06   | View penalty history                      |
| US-NA-07   | Acknowledge required documents            |
| US-ADM-01  | View real-time dashboard                  |
| US-ADM-02  | Manual confirmation + notification        |
| US-ADM-03  | Upload acknowledgment documents/files     |
| US-ADM-04  | Distribute acknowledgment documents/files |
| US-ADM-05  | Post emergency job                        |
| US-ADM-07  | View job applications overview            |
| US-ADM-08  | Verify document acknowledgment            |
| US-RPT-01  | View attendance performance dashboard     |
| US-RPT-02  | Generate penalty summary report           |
| US-RPT-03  | Generate staff score report               |
| US-RPT-04  | View system logs                          |
| US-FIN-01  | Generate settlement reconciliation report |
| US-FIN-02  | Investigate settlement discrepancy        |

---

### 0. ERP Team User Stories (External System)

#### US-ERP-01: Staff Master Data Sync
**As an** ERP system,
**I want** to provide staff data to PHC daily,
**So that** PHC has up-to-date nursing assistant information.

**Sync Frequency:** Daily 02:00 AM
**Data Provided:**
- Staff ID, names, contact info, HKID
- Worker type (e.g., Nursing Assistant, Care Worker)
- Skillsets (e.g., elderly_care, dementia_care, medication_admin)
- Gender
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
- Location ID, facility name, full address, contact
- Region, district
- Worker types accepted (e.g., Nursing Assistant, Care Worker)
- Skillset requirements (e.g., elderly_care, dementia_care)
- Gender preferences (if any)
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
- Demand ID
- Facility name and full address/location
- Date, job start time, job end time
- Worker type / skillset required
- Gender requirement (M/F/Any)
- Required staff count
- Assigned count
- Status (open/filled/cancelled)
- Priority, special requirements
- Contact person and phone number

**Acceptance Criteria:**
✅ API responds in <3 seconds
✅ Unfilled demands (status: open) returned
✅ Full demand details provided (facility, address, times, worker type, gender)
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
- Date, job times, assigned timestamp
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
**Trigger:** Post-job verification by PHC admin (within 1 hour of job completion)
**Data Received:**
- Assignment ID, staff ID, location ID
- Job date
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
✅ Submitted within 1 hour of job completion

**Priority:** High

**Note:** Per Product Spec v1.2, no-show status was removed. Admin verifies attendance via phone confirmation with facility contacts.

---

#### US-ERP-06: Receive Penalty Records
**As an** ERP system,
**I want** to receive penalty records from PHC,
**So that** I can deduct amounts from staff settlements.

**API:** POST /api/v1/penalties
**Trigger:** When staff cancels a confirmed job
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

**Note:** Per Product Spec:
- Cancellation (>48h): -1 score only, NO financial penalty
- Late cancellation (<48h): -1 score AND 300 HKD penalty
- No-show penalties removed in v1.2



---

### 1. Nursing Assistant (護理員) User Stories

#### US-NA-00: Staff Login
**As a** nursing assistant,
**I want** to log in to the PHC platform using my registered credentials (mobile number, username, or email),
**So that** I can access my dashboard and apply for jobs.

**Scenario - Login:**
```gherkin
Given: My staff account has been synced from ERP
When: I enter my mobile number
And: I enter my password
Then: I am successfully logged in
And: I land on the User Dashboard defaulting to the Jobs tab (available jobs) with any reminders/alerts visible
```

**Acceptance Criteria:**
✅ Login supported via Mobile Number (only)
✅ Credentials validated against synced ERP data
✅ Account locked after 5 failed attempts
✅ "Forgot Password" flow via SMS/Email OTP
✅ Session timeout after 30 minutes of inactivity

**Priority:** Critical

**Note:** Staff accounts are created automatically via ERP sync.

---

#### US-NA-01: Receive Job Notification via Web Push Notification/WhatsApp
**As a** nursing assistant,
**I want** to receive job notifications via Web Push Notification/WhatsApp when jobs are available,
**So that** I can apply for suitable jobs quickly.

**Scenario:**
```gherkin
Given: PHC System has sent the web push notifcation when receive the new job posting from ERP system
Given: PHC coordinator has generated a WhatsApp template for available jobs
When: Coordinator sends the message to my WhatsApp (individual or broadcast)
Then: I receive notification with job details
And: Message includes complete job information:
  - Facility name and address/location
  - Date and job times (start time, end time)
  - Worker type / skillset required
  - Gender requirement (if any)
  - Contact person
And: Message includes an application link to the PHC portal
And: I can click the link to view and apply for the job
```

**Acceptance Criteria:**
✅ WhatsApp message includes: facility name, address, date, job start/end times, worker type, gender requirement, contact person
✅ Application link opens Job Details View in the PHC web portal with job details and Apply button
✅ Web push reminder sent if not applied within 2 hours (if logged into portal)
✅ Works on both mobile and desktop browsers
✅ Bilingual support (English + Traditional Chinese)

**Priority:** Critical

**Note:** WhatsApp is primary channel (manual template-based). Web push notification is secondary for portal alerts only.

---

#### US-NA-02: Apply for Available Job
**As a** nursing assistant,
**I want** to apply for available jobs via the PHC web portal,
**So that** I can be considered for assignment by the PHC administrator.

**Scenario - Apply for Job:**
```gherkin
Given: I click the application link from WhatsApp message
When: I open the Job Details View in the PHC web portal
Then: I see the complete job details:
  - Facility name and full address/location
  - Date and job times (start time, end time, duration)
  - Worker type / skillset required
  - Gender requirement (if applicable)
  - Hourly rate and estimated total pay
  - Contact person and phone number
  - Special notes/requirements
And: I see the cancellation penalty warning
When: I click "Apply" button
Then: My application is recorded with status "pending_approval"
And: PHC administrator receives notification of my application
```

**Scenario - Application Approved:**
```gherkin
Given: I have applied for a job
When: PHC administrator approves my application
Then: Assignment status changes to "confirmed"
And: I receive confirmation notification (WhatsApp or web push)
And: Assignment appears in Jobs List (filtered to "My Jobs") with confirmed status
And: My score will increase by +1 point upon attendance verification
```

**Acceptance Criteria:**
✅ Application recorded immediately with "pending_approval" status
✅ Cancellation penalty warning displayed before applying
✅ Admin notified of new application
✅ Score increases (+1 point) only after attendance verification (not upon confirmation)
✅ ERP updated via API after admin approval
✅ Confirmation visible in Jobs List (filtered to "My Jobs") section
✅ Conflict check: Cannot apply if already assigned to overlapping job

**Priority:** Critical

**Note:** This implements the Human Screening Workflow per Product Spec v1.5 - staff apply, admin screens and approves.

---

#### US-NA-03: Cancel Job with Penalty Warning
**As a** nursing assistant,
**I want** to cancel a confirmed job when needed via the PHC portal,
**So that** the system can find a replacement, and I understand the consequences.

**Scenario - Early Cancellation (>48 hours before job start):**
```gherkin
Given: I have a confirmed assignment more than 48 hours before job start
When: I navigate to the Jobs List and filter to "My Jobs"
And: I click "Cancel Job"
Then: I see confirmation modal: "You are cancelling with sufficient notice."
And: I see penalty details: -1 score, no financial penalty
When: I confirm cancellation
Then: Assignment status changes to "cancelled"
And: Score decreases by 1 point
And: No financial penalty applied
And: I receive cancellation confirmation
And: Re-matching triggered for the vacancy
```

**Scenario - Late Cancellation (<48 hours before job start):**
```gherkin
Given: I have a confirmed assignment less than 48 hours before job start
When: I navigate to the Jobs List and filter to "My Jobs"
And: I click "Cancel Job"
Then: I see warning modal: "⚠️ Late Cancellation Warning: 300 HKD admin cost will be deducted!"
And: I see penalty details: -1 score AND -300 HKD
And: I see buttons: [Keep Job] [Confirm Cancellation]
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
✅ Staff can keep job (reject cancellation) after seeing warning
✅ ERP updated via penalty API (POST /api/v1/penalties)
✅ Re-matching triggered for vacancy (urgent if <24 hours)
✅ Cancellation recorded in staff's assignment history
✅ Admin alerted if unfilled after 30 minutes

**Priority:** High

**Note:** Per Product Spec, only late cancellations (<48h) incur financial penalty.

---

#### US-NA-05: View Job History
**As a** nursing assistant,
**I want** to view my job history and attendance records,
**So that** I can track completed jobs, review penalties, and verify my work history.

**Scenario - View Job History List:**
```gherkin
Given: I am logged into the PHC platform
When: I navigate to the Jobs List and filter to "Job History"
Then: I see a list of my past assignments sorted by date (newest first)
And: each record shows:
  - Facility name and location
  - Date and job times (start, end)
  - Worker type / skillset
  - Status (Completed, Cancelled, etc.)
And: I can filter by date range and status
```

**Scenario - View Job Details:**
```gherkin
Given: I am viewing the Jobs List filtered to "Job History"
When: I click on a specific job record
Then: I see detailed information including:
  - Facility name and full address
  - Assignment date
  - Job start time and end time
  - Worker type / skillset required
  - Gender requirement (if applicable)
  - Clock-in/out times
  - Attendance status
  - Score impact
  - Any penalties applied
```

**Acceptance Criteria:**
✅ Job history displays past assignments (last 12 months)
✅ Each record shows: facility name, address, date, job start/end times, worker type, status
✅ Status clearly indicated: Completed, Cancelled, No-Show
✅ Score impact shown: +1 (attended), -1 (cancelled)
✅ Penalties displayed with amount (300 HKD for late cancellation) and reason
✅ Filter by date range available
✅ Filter by status available
✅ Pagination supported (20 records per page)
✅ Clock-in/out times displayed for completed jobs
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
When: I navigate to the Job Details View
Then: I see the complete job information:
  - Facility name and full address/location
  - Date, job start time, job end time
  - Worker type / skillset required
  - Gender requirement (if applicable)
  - Contact person
And: I see a list of all staff who have applied
And: Each applicant shows: name, score, availability status, relevant history, matching skillset
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
When: I navigate to the Job Details View
Then: I see a list of assigned staff with their document acknowledgment status
And: Each staff shows: name, documents required, documents viewed, documents acknowledged
And: Staff who have not acknowledged are highlighted in red
```

**Scenario - Send Reminder for Unacknowledged Documents:**
```gherkin
Given: Staff have not acknowledged required documents before job start
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
✅ Acknowledgment tracking synced with acknowledgment document distribution

**Priority:** High

---

#### US-NA-07: Acknowledge Required Documents
**As a** nursing assistant,
**I want** to view and acknowledge required documents before my job,
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
✅ Push notification reminder if documents not acknowledged 24h before job
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
- Completed jobs
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
✅ Filter by date range, facility, job type
✅ Export to PDF/Excel for management reports

**Priority:** High

**Note:** Per Product Spec v1.2, no-show tracking was removed. Dashboard shows completed vs cancelled jobs only.

---

#### US-ADM-02: Manual confirmation + notification
**As a** PHC administrator,
**I want** to manually confirm specific staff to jobs and send confirmation notification,
**So that** I can handle special facility requests, unique qualifications, and emergency situations.

**Scenario:**
```gherkin
Given: A job demand is unfilled or requires specific staff
When: I navigate to the User List View
And: I search for staff by name, staff number, or availability
Then: I see search results with staff profiles (from ERP)
And: Each result shows: name, score, availability, recent history
When: I select a staff member
Then: System displays conflict warnings if any:
  - Staff already assigned to overlapping job
  - Staff on facility blacklist
  - Staff unavailable that day
  - Staff will exceed fair sharing limits
And: I can open the staff profile (read-only Jobs List/Penalty History views) for context
When: I deep-link to the target job's Job Details View from the staff row or the job listing
And: I enter override reason (max 100 words) in the Job Details View
And: I confirm assignment in the Job Details View
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
✅ All assignment approvals/confirmations executed inside the Job Details View; User List/View and staff profile views are lookup/entry points only

**Priority:** Medium

**Note:** Per Product Spec, audit trail cannot be deleted or modified after creation.

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
✅ Document appears in Job Details View for the relevant job

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
And: Document status visible in Job Details View
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
✅ All tracking and status visible in Job Details View

**Priority:** Medium

**Note:** WhatsApp is primary channel per Product Spec. Web push notification is supplementary for in-portal alerts.

---

#### US-ADM-05: Post Emergency Job
**As a** PHC administrator,
**I want** to post emergency jobs manually,
**So that** urgent staffing needs are filled immediately without waiting for the standard polling cycle.

**Scenario:**
```gherkin
Given: There is an urgent staffing need (e.g., 2 staff needed today 18:00-22:00)
When: I mark a posting as "Emergency" (flag/toggle) in the job posting form
And: I fill the form with complete job details:
  - Facility name and full address/location
  - Date, job start time, job end time
  - Worker type / skillset required
  - Gender requirement (if any)
  - Number of staff needed
  - Urgency reason
  - Contact person and phone number
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
✅ Emergency flag is a property of the job posting (no separate view)
✅ No delay in posting (bypasses standard 15-minute polling)
✅ Matching triggered instantly
✅ Urgent WhatsApp template with "URGENT" badge
✅ Web push notification in-app alert for Critical priority
✅ Dashboard updates with real-time filling progress
✅ Admin alert sent if unfilled after 30 minutes
✅ Staff can accept immediately via portal
✅ ERP updated within 1 minute of confirmation

**Priority:** High

**Note:** Per Product Spec, emergency jobs receive highest priority in the matching engine.

---

### 8. Finance Team User Stories

#### US-FIN-01: Generate Settlement Reconciliation Report

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
  - Assignment date, location, job time
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

#### US-RPT-04: View System Logs
**As a** PHC administrator,
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
