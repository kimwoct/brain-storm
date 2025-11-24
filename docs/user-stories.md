# User Stories & Test Cases
**Prestige Health Dispatch System (PHC)**

**Version:** 1.0
**Date:** 2025-11-24

---

## USER STORIES

### REQUIREMENTS TRACEABILITY MATRIX

| User Story | Related FRs | Description |
|------------|-------------|-------------|
| US-NA-01 | FR-2, FR-3 | Receive assignment notification |
| US-NA-02 | FR-1, FR-2, FR-3 | Confirm shift assignment |
| US-NA-03 | FR-1, FR-3, FR-7 | Cancel shift with warning |
| US-NA-04 | FR-1 | View score and tier |
| US-NA-05 | FR-1, FR-3, FR-6, FR-7 | No-show penalty notification |
| US-CS-01 | FR-2 | View today's assigned staff |
| US-CS-02 | FR-6 | Verify staff clock-in |
| US-CS-03 | FR-6, FR-7 | Mark staff as no-show |
| US-ADM-01 | FR-4, FR-5 | View real-time dashboard |
| US-ADM-02 | FR-2, FR-11 | Manual assignment override |
| US-ADM-03 | FR-8 | Upload emergency protocol |
| US-ADM-04 | FR-3, FR-8 | Distribute emergency files |
| US-ADM-05 | FR-9 | Post emergency job |
| US-ADM-06 | FR-5, FR-12, FR-13 | View system logs and reports |
| US-ERP-01 | FR-5 | Staff master data sync |
| US-ERP-02 | FR-5 | Location master data sync |
| US-ERP-03 | FR-5 | Job demand sync |
| US-ERP-04 | FR-2, FR-5 | Receive assignment submission |
| US-ERP-05 | FR-5, FR-6 | Receive attendance records |
| US-ERP-06 | FR-1, FR-5, FR-7 | Receive penalty records |

---

### 1. Nursing Assistant (護理員) User Stories

#### US-NA-01: Receive Shift Assignment Notification
**As a** nursing assistant,
**I want** to receive platform notifications (via Firebase) when assigned to a shift,
**So that** I can respond quickly and confirm my availability.

**Acceptance Criteria:**
✅ Notification includes: date, location name, shift time, contact person
✅ Firebase push notification delivered within 5 minutes of assignment
✅ Contains confirmation button
✅ Contains cancellation button
✅ Reminder sent if not confirmed within 2 hours
✅ Works on both desktop and mobile browsers

**Priority:** Critical

---

#### US-NA-02: Confirm Shift Assignment
**As a** nursing assistant,
**I want** to confirm my shift assignment via the PHC platform,
**So that** the care home knows I'm coming and my score increases.

**Scenario:**
```gherkin
Given: I receive a platform notification about a new assignment
When: I open the PHC platform (web or mobile)
And: I click "Confirm" button
Then: My response is recorded
And: Assignment status changes to "confirmed"
And: My score increases by 1 point
And: I receive confirmation push notification
```

**Acceptance Criteria:**
✅ Confirmation recorded immediately
✅ Score increases (+1 point)
✅ ERP updated via API
✅ Confirmation Firebase push notification delivered
✅ Confirmation visible in platform

**Priority:** Critical

---

#### US-NA-03: Cancel Shift with Warning
**As a** nursing assistant,
**I want** to cancel a shift when needed via the PHC platform,
**So that** the system can find a replacement, but I understand the penalty.

**Scenario:**
```gherkin
Given: I have a pending assignment
When: I open the PHC platform
And: I view my assignment
And: I click "Cancel Shift"
Then: I see warning modal: "100HKD will be deducted when you apply AL within 48 hours before coming job!"
And: I see penalty details (-1 score, -100 HKD)
When: I confirm cancellation
Then: Assignment cancelled
And: Score decreases by 1 point
And: 100 HKD deducted from payment
And: I receive cancellation confirmation via push notification
```

**Acceptance Criteria:**
✅ Warning modal displayed clearly in platform
✅ Penalty applied immediately (score + financial)
✅ Staff can keep shift (reject cancellation)
✅ ERP updated via API
✅ Re-matching triggered
✅ Cancellation recorded in staff's assignment history

**Priority:** High

---

#### US-NA-04: View My Score and Tier
**As a** nursing assistant,
**I want** to view my current score and tier,
**So that** I understand my priority level and can improve it.

**Acceptance Criteria:**
✅ Current score displayed (number)
✅ Tier displayed (Gold/Silver/Bronze/UnderReview)
✅ Score history available (last 10 changes)
✅ Reason for each change shown
✅ Tips provided for improving score

**Priority:** Medium

---

#### US-NA-05: Receive No-Show Penalty Notification
**As a** nursing assistant,
**If** I don't show up for a confirmed shift,
**Then** I receive penalty notification via platform and understand consequences.

**Scenario:**
```gherkin
Given: I confirmed a shift but didn't attend
When: Shift end time passes
Then: Supervisor marks me as absent in platform
And: I receive push notification: "You were marked absent. 100 HKD penalty applied. Score: -2 points"
And: I see the penalty in my platform notification center
```

**Acceptance Criteria:**
✅ Penalty notification delivered via Firebase push
✅ Notification appears in platform inbox
✅ Score decreases by 2 points
✅ 100 HKD deducted
✅ ERP penalty record created
✅ Penalty visible in staff's penalty history

**Priority:** High

---

### 2. Care Home Supervisor User Stories

#### US-CS-01: View Today's Assigned Staff
**As a** care home supervisor,
**I want** to see who is assigned to work today,
**So that** I can prepare and verify attendance.

**Acceptance Criteria:**
✅ List shows all confirmed assignments for today
✅ Shows staff name, contact number, shift time
✅ Shows photo (if available)
✅ Shows expected arrival time

**Priority:** High

---

#### US-CS-02: Verify Staff Clock-In
**As a** care home supervisor,
**I want** to verify staff clock-in/out,
**So that** attendance is accurately recorded.

**Scenario (Option A - QR Code):**
```gherkin
Given: Staff scans QR code at location
When: QR contains valid assignment data
Then: Clock-in time recorded
And: Supervisor notified
```

**Scenario (Option B - Manual Verification):**
```gherkin
Given: Staff arrives at location
When: Supervisor confirms presence in portal
Then: Clock-in time recorded
And: Attendance marked as "present"
```

**Acceptance Criteria:**
✅ Clock-in time within 1 hour of shift start accepted
✅ Clock-out time recorded at shift end
✅ Deviations > 1 hour flagged for approval
✅ QR code or manual verification works

**Priority:** High

---

#### US-CS-03: Mark Staff as No-Show
**As a** care home supervisor,
**I want** to mark staff as absent when they don't arrive,
**So that** penalty is applied and replacement can be found.

**Acceptance Criteria:**
✅ No-show button shown after shift end + 15 minutes
✅ Requires supervisor confirmation (Are you sure?)
✅ Penalties automatically applied
✅ Re-matching triggered immediately
✅ Admin notified of no-show

**Priority:** High

---

### 3. PHC Admin User Stories

#### US-ADM-01: View Real-Time Dashboard
**As a** PHC admin,
**I want** to see real-time metrics on dashboard,
**So that** I can monitor system health and performance.

**Dashboard Widgets:**
- Today's jobs (total/filled/unfilled)
- Confirmed staff vs pending confirmations
- Completed shifts vs no-shows
- Cancellations and penalties today
- API health status
- Last sync time
- Failed API calls

**Acceptance Criteria:**
✅ All metrics update every 30 seconds
✅ Click to drill down to details
✅ Color-coded status (green/yellow/red)

**Priority:** High

---

#### US-ADM-02: Manual Assignment Override
**As a** PHC admin,
**I want** to manually assign staff to jobs,
**So that** I can handle special cases and emergencies.

**Scenario:**
```gherkin
Given: A job demand is unfilled
When: I search for available staff
And: Select specific staff member
And: Provide override reason
Then: Assignment created (assigned_by: manual_admin)
And: WhatsApp notification sent
And: Override logged with my admin ID
```

**Acceptance Criteria:**
✅ Search by name, location, score, availability
✅ Conflict warnings displayed
✅ Reason required for all overrides
✅ Audit log complete
✅ ERP updated via API

**Priority:** Medium

---

#### US-ADM-03: Upload Emergency Protocol
**As a** PHC admin,
**I want** to upload emergency documents/files,
**So that** I can quickly distribute critical information to staff.

**Acceptance Criteria:**
✅ Upload PDF, DOC, DOCX, JPG, PNG (max 10MB)
✅ Enter title (required), description, priority, regions
✅ Files stored securely (S3/Azure Blob)
✅ Unique file ID generated
✅ Upload logged with my admin ID

**Priority:** Medium

---

#### US-ADM-04: Distribute Emergency Files
**As a** PHC admin,
**I want** to notify staff of new emergency protocols via platform push notifications,
**So that** they receive critical information quickly without leaving the platform.

**Scenario:**
```gherkin
Given: I uploaded emergency file with Critical priority
When: File uploaded successfully
Then: System identifies affected staff
And: Sends Firebase push notification to all relevant staff within 5 minutes
And: Staff receive in-app alert for Critical priority
And: Notifications appear in platform inbox
And: Tracks who viewed the file in platform
And: Tracks who confirmed in platform
```

**Acceptance Criteria:**
✅ Firebase push notifications sent within 5 minutes
✅ Only affected staff notified (by region if specified)
✅ View tracking works in platform
✅ Confirmation tracking works in platform
✅ Reports show delivery/confirmation rates
✅ In-app alert for Critical priority
✅ Notifications appear in platform inbox

**Priority:** Medium

---

#### US-ADM-05: Post Emergency Job
**As a** PHC admin,
**I want** to post emergency jobs manually,
**So that** urgent staffing needs are filled immediately.

**Acceptance Criteria:**
✅ Emergency job posted immediately (bypasses standard workflow)
✅ Bypasses 15-minute polling delay
✅ Real-time matching triggered
✅ Urgent Firebase push notification sent with in-app alert
✅ Real-time dashboard shows filling progress
✅ Admin alerted if shortage after 30 minutes

**Priority:** High

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
**I want** to receive staff assignments from PHC,
**So that** I can track confirmed placements and process payroll.

**API:** POST /api/v1/jobs/assignments
**Data Received:**
- Assignment ID, demand ID, staff ID, location ID
- Date, shift times, assigned timestamp

**Acceptance Criteria:**
✅ Accepts valid assignment data
✅ Returns assignment ID
✅ Validates staff availability (no conflicts)
✅ Returns 409 if staff unavailable

**Priority:** Critical

---

#### US-ERP-05: Receive Attendance Records
**As an** ERP system,
**I want** to receive attendance records from PHC,
**So that** I can calculate accurate payroll.

**API:** POST /api/v1/attendance
**Data Received:**
- Assignment ID, staff ID, location ID
- Clock-in/out times
- Actual hours worked
- Status (completed/partial/no_show)

**Acceptance Criteria:**
✅ Accepts valid attendance data
✅ Calculates payment based on hours
✅ Returns calculated amount
✅ Links to assignment and staff records

**Priority:** High

---

#### US-ERP-06: Receive Penalty Records
**As an** ERP system,
**I want** to receive penalty records from PHC,
**So that** I can deduct 100 HKD from staff payments.

**API:** POST /api/v1/penalties
**Data Received:**
- Penalty type (cancellation/no_show)
- Amount (100 HKD)
- Score impact (-1 or -2)
- Assignment reference

**Acceptance Criteria:**
✅ Accepts valid penalty data
✅ Deducts from next settlement
✅ Returns deduction confirmation

**Priority:** High

**Note:** Actual deduction API TBD before development

---

## TEST CASES

### TEST TRACEABILITY

| Test Case | Related FRs | Objective |
|-----------|-------------|-----------|
| TC-001 | FR-5 | Verify staff sync from ERP |
| TC-002 | FR-1, FR-2 | Test matching algorithm |
| TC-003 | FR-1, FR-5, FR-6 | Score update on attendance |
| TC-004 | FR-1, FR-3, FR-7 | Penalty on cancellation |
| TC-005 | FR-1, FR-3, FR-7 | Penalty on no-show |
| TC-006 | FR-6 | QR code clock-in |
| TC-007 | FR-3, FR-8 | Emergency file upload |
| TC-008 | FR-3, FR-9 | Emergency job posting |
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
**Objective:** Verify matching selects appropriate staff

**Preconditions:**
- Job demand: 2025-11-25, 08:00-20:00, 1 staff needed
- Location: Hong Kong Care Home (CH_HKI_001)
- Underlist: Staff A (priority 1), Staff B (priority 2)
- Staff scores: A=15 (Silver), B=25 (Gold), C=8 (Bronze)
- All staff: available, valid docs, not blacklisted

**Test Steps:**
1. Create job demand
2. Run matching algorithm

**Expected Results:**
✅ Underlist applied first: Staff A selected
✅ If Staff A unavailable: Staff B selected
✅ If both unavailable: Staff C selected (highest score)
✅ Blacklisted staff not considered
✅ Unavailable staff not considered

**Priority:** Critical

---

#### TC-003: Score Update on Attendance
**Objective:** Verify score increases when staff attends shift

**Preconditions:**
- Staff has score = 10
- Shift assignment confirmed

**Test Steps:**
1. Verify staff score = 10
2. Supervisor verifies attendance (present)
3. Submit attendance to PHC

**Expected Results:**
✅ Staff score = 11 (+1)
✅ Score history record created
✅ Tier updated (if applicable)
✅ ERP API 4.4 called with score update
✅ Attendance submitted to ERP

**Priority:** Critical

---

#### TC-004: Penalty on Cancellation
**Objective:** Verify penalties applied correctly

**Preconditions:**
- Staff has pending assignment
- Staff score = 12
- No previous penalties

**Test Steps:**
1. Staff opens PHC platform
2. Staff navigates to assignment
3. Staff clicks "Cancel Shift"
4. Reviews warning modal in platform
5. Confirms cancellation
6. Check staff record

**Expected Results:**
✅ Warning modal displayed: "100HKD will be deducted..."
✅ Cancellation confirmation received via Firebase push
✅ Assignment status = cancelled
✅ Staff score = 11 (-1)
✅ Penalty record created (100 HKD, -1 score)
✅ ERP API 4.2 called (penalty submission)
✅ ERP API 4.4 called (score update)
✅ Re-matching triggered for vacancy

**Priority:** Critical

---

#### TC-005: Penalty on No-Show
**Objective:** Verify no-show penalties (heavier than cancellation)

**Preconditions:**
- Staff confirmed assignment
- Staff does not arrive
- Shift end time passed
- Supervisor notified
- Staff score = 15

**Test Steps:**
1. Supervisor marks staff as absent in portal
2. Supervisor confirms no-show

**Expected Results:**
✅ Staff score = 13 (-2)
✅ Penalty record created (100 HKD, -2 score)
✅ Staff receives Firebase push notification
✅ Notification appears in platform inbox
✅ ERP API 4.2 called (penalty submission)
✅ ERP API 4.4 called (score update)

**Priority:** High

---

#### TC-006: QR Code Clock-In
**Objective:** Verify QR code attendance tracking

**Preconditions:**
- Staff has confirmed assignment
- QR code displayed at location
- QR contains: location_id, assignment_id, shift_date

**Test Steps:**
1. Staff scans QR with phone (15 minutes before shift - valid)
2. System validates QR data
3. Clock-in recorded

**Expected Results:**
✅ Clock-in time recorded accurately
✅ Attendance status = checked_in
✅ Supervisor notified
✅ QR rejected if scanned >1 hour before shift
✅ QR rejected if assignment not confirmed

**Priority:** High

---

#### TC-007: Emergency File Upload
**Objective:** Verify admin can upload and distribute emergency protocols

**Preconditions:**
- Admin logged in
- File: "Typhoon Emergency Procedures.pdf" (5MB)

**Test Steps:**
1. Navigate to Emergency Protocols
2. Click "Upload File"
3. Select PDF file
4. Enter title, description, priority=Critical, region=HKI
5. Submit

**Expected Results:**
✅ File uploaded to S3/Azure Blob
✅ File metadata saved to database
✅ File appears in emergency file list
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
✅ Urgent Firebase push notification sent with in-app alert
✅ Real-time dashboard shows progress
✅ Admin alerted if not filled in 30 minutes

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

**Request (Cancellation):**
```json
{
  "assignment_id": "ERP-ASSIGN-001",
  "staff_id": "STF123",
  "penalty_type": "cancellation",
  "amount": 100.00,
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
  "adjusted_amount": 100.00
}
```

**Validation:**
✅ Penalty ID returned
✅ Payment adjusted = true
✅ Correct amount (100 HKD)

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
| API | Target | Acceptable |
|-----|--------|------------|
| POST /assignments | <2s | <3s |
| PATCH /status | <1s | <2s |
| POST /attendance | <2s | <3s |
| GET /dashboard | <3s | <5s |
| ERP API calls | <3s | <5s |

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

## TEST EXECUTION SUMMARY

### Test Coverage Targets

| Category | Test Cases | Status |
|----------|-----------|--------|
| Functional | 8 | Pending |
| ERP Integration | 8 | Pending |
| Performance | 2 | Pending |
| Security | 2 | Pending |
| **Total** | **20** | **Pending** |

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

**Last Updated:** 2025-11-24
**Next Review:** Before testing begins
