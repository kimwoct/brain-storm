# Software Requirements Specification (SRS)
**Prestige Health Dispatch System (PHC)**

**Document Version:** 2.0 (Consolidated)
**Date:** 2025-11-24
**Project:** PHC - Prestige Health Care Dispatch Automation
**Timeline:** 1.5 Months / 60 Man-Days (Condensed from 12 weeks)

---

## 📋 TABLE OF CONTENTS

1. [Introduction](#1-introduction)
2. [Overall System Description](#2-overall-system-description)
3. [Functional Requirements](#3-functional-requirements)
4. [ERP Integration Requirements](#4-erp-integration-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [User Interface Requirements](#6-user-interface-requirements)
7. [Implementation Timeline (Condensed)](#7-implementation-timeline-condensed)
8. [Acceptance Criteria](#8-acceptance-criteria)
9. [Appendices](#9-appendices)

---

## 1. INTRODUCTION

### 1.1 Purpose

This Software Requirements Specification (SRS) defines the complete functional and non-functional requirements for the Prestige Health Dispatch System (PHC), an intelligent healthcare staffing automation platform that replaces manual WhatsApp-based coordination with automated matching of care homes and nursing assistants.

### 1.2 Scope

**In Scope:**
- Automated matching of nursing assistants to care home shifts
- Four-stage workflow automation (Registration, Job Posting, Matching, Completion)
- Real-time ERP integration (bi-directional sync)
- Staff Web Portal for login, dashboard, and shift management
- Scoring algorithm with attendance-based points system
- Financial penalty system (−100 HKD, score deductions)
- Manual emergency protocol management
- Admin file upload for supplements

**Out of Scope:**
- Geographic intelligence (distance-based matching)
- Automated fair sharing (manually controlled in ERP)
- Native Mobile app development (Web Portal + WhatsApp only)
- Billing/invoicing beyond penalty deductions

### 1.3 System Overview

**Problem Statement:** Current manual WhatsApp coordination between care homes and nursing assistants is inefficient, error-prone, and lacks transparency in allocation decisions.

**Solution:** PHC automates the entire workflow from demand posting to settlement, integrating with existing ERP for master data and financial processing.

---

## 2. OVERALL SYSTEM DESCRIPTION

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Prestige Health Dispatch System (PHC)    │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Web Portal  │  │  Matching    │  │  WhatsApp    │     │
│  │  (Admin)     │◄─┤  Engine      │◄─┤  API         │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│          ▲                  ▲                  ▲            │
│          │                  │                  │            │
│  ┌───────┴───────┐  ┌──────┴──────┐  ┌──────┴──────┐      │
│  │ Scoring       │  │ Attendance  │  │ Penalties   │      │
│  │ Algorithm     │  │ Tracking    │  │ Management  │      │
│  └───────────────┘  └─────────────┘  └─────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                                ▲
                                │ Bi-directional Sync
                                │
┌─────────────────────────────────────────────────────────────┐
│                    Existing ERP System                      │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Staff Master │  │ Locations    │  │ Financial    │     │
│  │  Data        │  │ Master       │◄─┤  Processing  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 User Classes

| User Class | Description | Key Functions |
|------------|-------------|---------------|
| **Nursing Assistant** | Care workers receiving shift assignments | Login to portal, view dashboard, apply for shifts, confirm/cancel assignments |
| **Care Home Supervisor** | On-site staff verifying attendance | Verify clock-in/out, mark absent, view assigned staff |
| **PHC Admin** | System administrators managing operations | Manual overrides, emergency protocols, file uploads, system monitoring |
| **ERP Admin** | Existing ERP system users | Manage master data (staff, locations), configure fair sharing rules |

### 2.3 Operating Environment

- **Platform:** Web-based system (responsive design)
- **Server:** Cloud-hosted (AWS/Azure recommended)
- **Database:** PostgreSQL/MySQL
- **ERP Integration:** RESTful APIs (JSON)
- **Notifications:** WhatsApp Business API
- **Authentication:** OAuth 2.0 or API keys

---

## 3. FUNCTIONAL REQUIREMENTS

### 3.0 Flow 0: Authentication

#### 3.0.1 FR-AUTH-01: Staff Login
**Priority:** Critical
**Description:** Staff must be able to log in using credentials synced from ERP.

**System Actions:**
1. User enters Mobile Number
2. User enters Password
3. System validates credentials against PHC database (synced from ERP)
4. If valid:
   - Generate JWT token
   - Create session
   - Redirect to Staff Dashboard
5. If invalid:
   - Increment failure count
   - Show error message
6. If failure count >= 5:
   - Lock account for 30 minutes
   - Send alert email/SMS

**Acceptance Criteria:**
- Login works with Mobile Number only
- Account locking works
- Session timeout after 30 mins

#### 3.0.2 FR-AUTH-02: Forgot Password
**Priority:** High
**Description:** Staff can reset password via OTP.

**System Actions:**
1. User clicks "Forgot Password"
2. Enters Mobile Number or Email
3. System generates 6-digit OTP
4. Sends OTP via SMS/Email
5. User enters OTP
6. System validates OTP
7. User sets new password

**Acceptance Criteria:**
- OTP delivered < 1 min
- Password reset successful

---

### 3.1 Flow 1: Registration (开卡) - Daily ERP Sync

#### 3.1.1 FR-REG-01: Automated Staff Synchronization
**Priority:** Critical
**Description:** System must pull registered nursing assistant data from ERP daily at 02:00 AM.

**System Actions:**
1. Trigger at 02:00 AM daily (configurable)
2. Call ERP API: `GET /api/v1/staff/active`
3. Retrieve all active staff with complete profile:
   - ERP staff_id (unique identifier)
   - Name (Chinese & English)
   - HKID
   - Contact number & WhatsApp number
   - Email (optional)
   - Registration date
   - Status (active/inactive)
   - Preferred regions (HKI/KLN/NT)
4. Validate HKID format (regex: `[A-Z]{1,2}[0-9]{6}[0-9A]`)
5. Validate contact number (8 digits)
6. Check for duplicates by erp_staff_id
7. For new staff: Create PHC account
8. For existing staff: Update changed fields
9. Log all changes with timestamp
10. Alert admin for validation failures

**Acceptance Criteria:**
- Sync success rate > 99%
- New staff created within 24 hours of ERP registration
- Validation errors logged and alerted
- Duplicate staff not created

**Estimated Effort:** 5 man-days (including testing)

---

#### 3.1.2 FR-REG-02: Certificate Synchronization
**Priority:** High
**Description:** System must sync and validate staff certificates from ERP.

**System Actions:**
1. After staff sync, call ERP API: `GET /api/v1/staff/{staff_id}/documents`
2. Retrieve certificate details:
   - Certificate type (health_worker_certificate, health_check, etc.)
   - Issue date (YYYY-MM-DD)
   - Expiry date (YYYY-MM-DD)
   - Document URL
3. Validate expiry dates
4. Alert admin if expiry < 30 days
5. Mark staff as "document invalid" if critical cert expired
6. Prevent assignment to shifts if documents invalid

**Acceptance Criteria:**
- Certificate expiry alerts sent 30 days before
- Staff with invalid documents blocked from assignment
- Weekly sync of certificates

**Estimated Effort:** 3 man-days

---

#### 3.1.3 FR-REG-03: Availability Synchronization
**Priority:** High
**Description:** System must sync staff availability for next 7 days from ERP.

**System Actions:**
1. Call ERP API: `GET /api/v1/staff/availability`
2. Retrieve availability for date range: Today to Today+7
3. Map availability data to PHC calendar
4. Mark unavailable dates (e.g., AL - Annual Leave)
5. Validate no conflicts with existing assignments
6. Update availability matrix daily

**Acceptance Criteria:**
- Availability reflects ERP data within 24 hours
- No double-booking allowed
- Alert for availability conflicts

**Estimated Effort:** 4 man-days

---

### 3.2 Flow 2: Job Posting (出Post) - Demand Integration

#### 3.2.1 FR-JOB-01: Location Master Data Sync
**Priority:** Critical
**Description:** System must sync care home location data from ERP daily.

**System Actions:**
1. Trigger at 03:00 AM daily (configurable)
2. Call ERP API: `GET /api/v1/locations/active`
3. Retrieve all active locations:
   - ERP location_id (unique)
   - Location code (e.g., CH_HKI_001)
   - Name (Chinese & English)
   - Address
   - Region (HKI/KLN/NT)
   - District
   - Contact person & number
   - Service type
   - Special requirements (dementia_experience, cantonese_speaking)
4. For new locations: Create in PHC
5. For existing locations: Update changed fields
6. Call API 2.3: `GET /api/v1/locations/{id}/preferences`
7. Sync:
   - Underlist staff (priority list with rankings)
   - Blacklisted staff (cannot assign)
   - Required certificates
8. Validate location data completeness
9. Alert admin for missing critical data

**Acceptance Criteria:**
- All active locations synced daily
- Underlist/blacklist accurately reflected
- Missing required fields flagged

**Estimated Effort:** 5 man-days

---

#### 3.2.2 FR-JOB-02: Job Demand Polling
**Priority:** Critical
**Description:** System must poll ERP for new job demands every 15 minutes.

**System Actions:**
1. Call ERP API: `GET /api/v1/jobs/demands`
2. Filter: status = "open" (unfilled demands)
3. Retrieve demand details:
   - ERP demand_id (unique)
   - Location reference (location_id)
   - Required date (YYYY-MM-DD)
   - Shift times (start: HH:MM, end: HH:MM)
   - Required staff count (integer)
   - Assigned staff count
   - Status
   - Priority (normal/urgent)
   - Special requirements
   - Contact person on duty
4. Validate: Required date >= Today
5. Validate: Start time < End time
6. For new demands: Create job posting in PHC
7. For updated demands: Update existing posting
8. For cancelled demands: Close posting
9. Trigger matching algorithm for new demands
10. Log all demand changes

**Acceptance Criteria:**
- New demands appear in PHC within 15 minutes
- Demand updates reflected in real-time
- Cancelled demands immediately closed

**Estimated Effort:** 4 man-days

---

#### 3.2.3 FR-JOB-03: Webhook Integration (Optional)
**Priority:** Medium
**Description:** System should receive real-time webhooks from ERP when demands are posted.

**System Actions:**
1. Expose endpoint: `POST /webhook/erp/job-demand`
2. Receive webhook payload from ERP
3. Validate webhook authenticity (signature validation)
4. Parse demand data
5. Immediately create job posting (skip 15-min delay)
6. Trigger matching algorithm instantly
7. Return HTTP 200 to ERP
8. Log webhook receipt and processing
9. If webhook fails: Fall back to polling

**Acceptance Criteria:**
- Webhook processing latency < 1 minute
- Failed webhooks logged
- Fallback to polling works seamlessly

**Estimated Effort:** 3 man-days

---

### 3.3 Flow 3: Matching & Confirmation

#### 3.3.1 FR-MAT-01: Scoring Algorithm Engine
**Priority:** Critical
**Description:** System must calculate nursing assistant scores for priority-based allocation.

**Scoring Rules:**
```
Initial Score (for new staff): 5 points (configurable)

Attendance Impact:
├─ Attended (present): +1 point
├─ Cancelled (with notice): -1 point
└─ Absent (no-show): -2 points

Score Tiers:
├─ Gold: 20+ points → First priority
├─ Silver: 10-19 points → Second priority
├─ Bronze: 0-9 points → Third priority
└─ Under Review: < 0 points → Manual review required

Manual Override:
- Admin can manually adjust scores
- Require reason for manual adjustment
- Log all manual changes with admin ID, timestamp, reason
```

**System Actions:**
1. Calculate current score for each staff
2. Apply score changes immediately when:
   - Shift completed (attended) → +1
   - Shift cancelled → -1 (plus penalty)
   - No-show → -2 (plus penalty)
3. Enforce score_floor = -10 (minimum)
4. Assign tier based on current score
5. Display score in staff profile
6. Display score in matching interface

**Acceptance Criteria:**
- Score calculation accurate
- Tier assignment correct
- Manual overrides logged
- Score history tracked

**Estimated Effort:** 5 man-days

---

#### 3.3.2 FR-MAT-02: Matching Algorithm
**Priority:** Critical
**Description:** System must automatically match nursing assistants to job demands based on multiple criteria.

**Matching Criteria (Priority Order):**
1. **Availability:** Must be available on date/time
2. **Document Validity:** Certifications must be valid
3. **Underlist Priority:**
   - Underlist staff get priority matching to their preferred locations
   - Rank by preference position (priority: 1, 2, 3...)
4. **Score Tier:**
   - Gold first, then Silver, then Bronze
   - Within same tier: Sort by actual score (descending)
5. **Blacklisted Filter:** Blacklisted staff automatically excluded
6. **Certificate Requirements:** Staff must have required certs
7. **Location Preferences:** Respect staff region preferences
8. **Tie-Breakers (in order):**
   - Previous work history at that location
   - Geographic proximity (for future enhancement)
   - Seniority (registration date)
   - First-come-first-served (application order)

**Fair Sharing (Manual Control):**
- Fair sharing controlled manually in ERP system
- ERP admin manages maximum assignments per staff per month
- PHC validates: Staff monthly count ≤ ERP limit
- If exceeds: Skip to next candidate
- Alert ERP admin when approaching limit

**System Actions:**
1. When new demand arrives:
   a. Filter candidates by availability
   b. Filter by document validity
   c. Filter by blacklist
   d. Filter by certificate requirements
   e. Apply fair sharing limits (from ERP)
   f. Rank by underlist priority
   g. Rank by score tier and actual score
   h. Apply tie-breakers
2. Select top candidates (N = required staff count)
3. Create tentative assignments
4. Submit assignments to ERP (API 3.1)
5. If ERP returns "staff unavailable":
   a. Remove that staff from candidates
   b. Move to next candidate
   c. Re-submit
6. Log matching decisions

**Acceptance Criteria:**
- Matching completes within 5 minutes per demand
- All criteria filters applied correctly
- Underlist respected
- Under-review staff (< 0 score) excluded from auto-matching

**Estimated Effort:** 8 man-days (complex algorithm)

---

#### 3.3.3 FR-MAT-03: Assignment Submission to ERP
**Priority:** Critical
**Description:** When matches are selected, system must submit assignments to ERP.

**System Actions:**
1. Call ERP API 3.1: `POST /api/v1/jobs/assignments`
2. Submit payload:
```json
{
  "assignment_id": "PHC_GENERATED_ID",
  "demand_id": "ERP_DEMAND_ID",
  "location_id": "ERP_LOCATION_ID",
  "staff_id": "ERP_STAFF_ID",
  "assignment_date": "2025-11-25",
  "shift_start": "08:00",
  "shift_end": "20:00",
  "assigned_by": "system_auto",
  "assigned_timestamp": "2025-11-20T15:30:00Z",
  "status": "pending_confirmation"
}
```
3. Handle response:
   - **Success (200):** Store ERP assignment_id, proceed to notification
   - **Conflict (409):** Staff unavailable → Remove, re-match
   - **Error (500):** Retry up to 3 times, then alert admin
4. Store assignment in PHC database
5. Set status: "pending_confirmation"
6. Log submission attempt

**Acceptance Criteria:**
- Assignment submitted within 1 minute of matching
- ERP rejection handled gracefully
- Re-matching triggered automatically
- Retry logic works correctly

**Estimated Effort:** 4 man-days

---

#### 3.3.4 FR-MAT-04: WhatsApp Notification
**Priority:** High
**Description:** System must notify nursing assistants of assignments via WhatsApp.

**System Actions:**
1. When assignment submitted and ERP confirms:
2. Trigger WhatsApp Business API
3. Send message:
```
【Prestige Health Dispatch】
Date: 2025-11-25 (Mon)
Location: Hong Kong Care Home
Shift: 08:00 - 20:00 (12 hours)
Contact: Ms. Wong (21234567)

Please confirm within 2 hours:
Confirm: [link]
Cancel: [link]

Reply 1 to Confirm
Reply 2 to Cancel
```
4. Include confirmation link (with token)
5. Track message delivery status
6. If no confirmation in 2 hours: Send reminder
7. If no confirmation in 4 hours: Alert admin

**Acceptance Criteria:**
- WhatsApp delivered within 5 minutes
- Click tracking works
- Reminders sent automatically
- Response captured correctly

**Estimated Effort:** 4 man-days (including WhatsApp API integration)

---

#### 3.3.5 FR-MAT-05: Staff Confirmation/Cancellation
**Priority:** Critical
**Description:** Staff must be able to confirm or cancel assignments via WhatsApp links.

**Confirmation Flow:**
1. Staff clicks "Confirm" link in WhatsApp
2. Browser opens confirmation page
3. System validates assignment token
4. Update assignment status: "confirmed"
5. Call ERP API 3.2: `PATCH /api/v1/jobs/assignments/{id}`
6. Submit:
```json
{
  "status": "confirmed",
  "confirmed_timestamp": "2025-11-20T16:00:00Z",
  "confirmation_method": "whatsapp_link"
}
```
7. Send confirmation WhatsApp:
```
Confirmed! See you on 2025-11-25 at Hong Kong Care Home (08:00-20:00)
```
8. Update staff score: +1 point
9. Call ERP API 4.4: Update staff score
10. Log confirmation

**Cancellation Flow:**
1. Staff clicks "Cancel" link in WhatsApp
2. System shows warning modal:
```
⚠️ Cancellation Warning
━━━━━━━━━━━━━━━━━━━━
Cancelling this shift will result in:
• Score penalty: -1 point
• Financial penalty: 100 HKD deduction

"100HKD will be deducted when you apply AL within 48 hours before coming job!"

Do you want to proceed?
[Confirm Cancellation] [Keep Shift]
```
3. **If staff clicks "Keep Shift":**
   - Close modal
   - Assignment remains "pending_confirmation"
   - Log cancellation attempt but rejection
4. **If staff clicks "Confirm Cancellation":**
   - Update assignment status: "cancelled"
   - Apply penalties:
     * Score: -1 point
     * Financial: -100 HKD
   - Call ERP API 3.2: Status update
   - Call ERP API 4.2: Submit penalty
   - Call ERP API 4.4: Update score
   - Trigger TBD API for financial deduction
   - Send cancellation confirmation WhatsApp:
   ```
   Shift cancelled. 100 HKD penalty will be deducted from your next payment.
   ```
   - Log cancellation
   - Re-trigger matching algorithm for vacant position

**Acceptance Criteria:**
- Warning displayed clearly
- Staff can reject and keep shift
- Penalties applied immediately if cancelled
- ERP updated in real-time
- Re-matching triggered automatically

**Estimated Effort:** 5 man-days (complex flow)

---

#### 3.3.6 FR-MAT-06: Manual Override by Admin
**Priority:** Medium
**Description:** Admin must be able to manually override automatic assignments.

**System Actions:**
1. Admin views pending assignments
2. Admin can:
   - Reassign to different staff
   - Force-assign (bypass matching algorithm)
   - Cancel assignment
   - Extend confirmation deadline
3. For manual changes:
   - Require reason field (mandatory)
   - Log admin ID, timestamp, reason
   - Apply changes immediately
   - Update ERP via API 3.1 or 3.2
4. Track all overrides in audit log

**Acceptance Criteria:**
- All manual changes logged
- ERP reflects manual changes
- Audit trail complete
- Reason required for all overrides

**Estimated Effort:** 3 man-days

---

### 3.4 Flow 4: Completion & Settlement

#### 3.4.1 FR-SET-01: Clock-In/Clock-Out Interface
**Priority:** High
**Description:** System must provide interface for staff to clock in and out at location.

**Options (to be decided):**

**Option A: QR Code System**
1. Location displays QR code (digital or printed)
2. Staff scans QR code with phone
3. QR contains:
   - Location ID
   - Shift date
   - Current timestamp
4. System validates:
   - Staff has confirmed assignment for that shift
   - Current time within 1 hour of shift start (for clock-in)
5. Record clock-in time
6. For clock-out: Staff scans again at end of shift
7. Record clock-out time

**Option B: Supervisor Verification**
1. Supervisor logs into PHC portal
2. Views list of assigned staff for shift
3. Checks staff physically present
4. Marks as "present" (clocks in)
5. At end of shift: Confirms completion (clocks out)

**System Actions (Regardless of Option):**
1. Capture clock-in timestamp
2. Capture clock-out timestamp
3. Calculate actual hours worked
4. Validate actual hours vs scheduled hours
5. If deviation > 1 hour: Flag for supervisor approval
6. Update status: "completed" (if verified)
7. Store in PHC database
8. Submit to ERP via API 4.1 (real-time or batch)

**Acceptance Criteria:**
- Clock times recorded accurately
- Deviation alerts work
- Only verified staff can clock in/out
- ERP receives attendance data

**Estimated Effort:** 6 man-days (includes both options, pick one)

---

#### 3.4.2 FR-SET-02: Attendance Submission to ERP
**Priority:** Critical
**Description:** System must submit attendance records to ERP for payment processing.

**System Actions:**
1. When shift completes and verified:
2. Call ERP API 4.1: `POST /api/v1/attendance`
3. Submit payload:
```json
{
  "attendance_id": "PHC_GENERATED_ID",
  "assignment_id": "ERP_ASSIGNMENT_ID",
  "staff_id": "ERP_STAFF_ID",
  "location_id": "ERP_LOCATION_ID",
  "shift_date": "2025-11-25",
  "clock_in_time": "2025-11-25T07:55:00Z",
  "clock_out_time": "2025-11-25T20:05:00Z",
  "actual_hours": 12.17,
  "status": "completed",
  "verified_by": "supervisor_name",
  "verification_method": "qr_code_scan"
}
```
4. Handle response:
   - Success: ERP calculates payment, returns amount
   - Store payment calculation in PHC
5. Update staff score: +1 point (attended)
6. Call ERP API 4.4: Update staff score in ERP
7. Log attendance submission

**Alternative for Partial Completion:**
If staff leaves early or arrives late:
- Set status: "partial"
- Calculate actual hours
- Supervisor must approve partial attendance
- Payment based on actual hours (ERP calculates)

**Acceptance Criteria:**
- Attendance submitted within 1 hour of completion
- ERP payment calculation received
- Score updated correctly
- Partial attendance requires approval

**Estimated Effort:** 4 man-days

---

#### 3.4.3 FR-SET-03: No-Show Handling
**Priority:** High
**Description:** System must handle staff who don't show up without cancelling.

**System Actions:**
1. When shift end time passes:
2. Check if staff clocked in
3. If not clocked in:
   a. Mark assignment as "no_show" in PHC
   b. Alert supervisor (WhatsApp notification)
   c. Supervisor confirms no-show in system
   d. Apply penalties:
      - Score: -2 points
      - Financial: -100 HKD
   e. Call ERP API 4.2: `POST /api/v1/penalties`
   ```json
   {
     "penalty_id": "PHC_GENERATED_ID",
     "staff_id": "ERP_STAFF_ID",
     "assignment_id": "ERP_ASSIGNMENT_ID",
     "penalty_type": "no_show",
     "penalty_amount": 100.00,
     "currency": "HKD",
     "reason": "Absent without notice",
     "applied_timestamp": "2025-11-25T20:00:00Z",
     "deduct_from_payment": true,
     "score_impact": -2
   }
   ```
   f. Call ERP API 4.4: Update staff score (-2)
   g. Trigger TBD financial deduction API
   h. Send WhatsApp to staff:
   ```
   You were marked absent for shift on 2025-11-25.
   100 HKD penalty applied.
   Score: -2 points
   ```
   i. Re-trigger matching for vacancy
4. Supervisor can override (if staff had emergency):
   - Require reason
   - Log override with supervisor ID
   - Waive penalty if justified

**Acceptance Criteria:**
- No-show detected automatically after shift end
- Supervisor notified and must confirm
- Penalties applied correctly
- Staff notified via WhatsApp
- Re-matching triggered

**Estimated Effort:** 5 man-days

---

#### 3.4.4 FR-SET-04: Financial Deduction Integration
**Priority:** Critical
**Description:** When penalties are applied, system must deduct 100 HKD from staff payment.

**System Actions:**
1. When cancellation or no-show penalty applied:
2. Initiate financial deduction process
3. **NOTE: ERP team to specify API endpoint**
4. Until ERP API specified:
   - Log deduction in PHC:
     * Staff ID
     * Assignment ID
     * Amount: 100 HKD
     * Reason: cancellation / no_show
     * Date applied
   - Flag as "pending_ERP_processing"
5. When ERP API available:
   - Call: `POST /api/v1/finance/deduction` (TBD)
   - Submit:
   ```json
   {
     "staff_id": "ERP_STAFF_ID",
     "assignment_id": "ERP_ASSIGNMENT_ID",
     "deduction_amount": 100.00,
     "currency": "HKD",
     "reason_code": "CANCELLATION_PENALTY",
     "reason_description": "Cancelled within 48 hours",
     "deduct_from_settlement": true,
     "settlement_period": "2025-12"
   }
   ```
6. ERP processes deduction and returns confirmation
7. Mark deduction as "processed" in PHC
8. Track deduction ID from ERP
9. Include deduction in settlement report

**Acceptance Criteria:**
- 100 HKD recorded for each penalty
- Pending list maintained until ERP integration
- ERP integration can be added later without re-work

**Estimated Effort:** 3 man-days (including future API integration)

---

#### 3.4.5 FR-SET-05: Settlement Reconciliation
**Priority:** Medium
**Description:** System must reconcile completed shifts with ERP for monthly payment processing.

**System Actions:**
1. On 1st of each month:
2. For each staff member:
   a. Call ERP API 4.3: `GET /api/v1/settlements/{staff_id}`
   b. Submit parameters:
      - period: "YYYY-MM" (e.g., "2025-11")
   c. Retrieve settlement data:
      - Total shifts
      - Total hours
      - Gross payment
      - Penalties total
      - Net payment
   d. Compare with PHC records
   e. Flag discrepancies:
      - Mismatched shift count
      - Different hours
      - Calculation errors
   f. Generate discrepancy report
3. Generate settlement summary report (all staff)
4. Send to finance team via email
5. Export CSV for bank payment processing
6. Store settlement records in PHC archive

**Acceptance Criteria:**
- Reconciliation completed by 3rd of month
- Discrepancies flagged
- Reports generated automatically
- PHC records match ERP > 99%

**Estimated Effort:** 4 man-days

---

### 3.5 Emergency Protocols (Manual - Admin File Upload)

#### 3.5.1 FR-EMG-01: Emergency File Upload
**Priority:** High
**Description:** Admin must be able to upload emergency supplement files/PDFs to dispatch system.

**System Actions:**
1. Admin logs into PHC portal
2. Navigates to "Emergency Protocols" section
3. Clicks "Upload Emergency File"
4. Selects file from local system (PDF, DOC, DOCX, JPG, PNG)
5. Enters metadata:
   - Title (required)
   - Description (optional)
   - Effective date (required)
   - Priority (Normal/High/Critical)
   - Applicable regions (optional)
6. System validates:
   - File type supported
   - File size < 10 MB
   - Title not empty
7. Upload to secure storage (S3, Azure Blob)
8. Generate unique file_id
9. Store metadata in database
10. Display success message
11. Log upload with admin ID, timestamp

**Acceptance Criteria:**
- Files up to 10 MB can be uploaded
- Supported formats: PDF, DOC, DOCX, JPG, PNG
- Metadata stored correctly
- Files accessible via download link
- Audit trail maintained

**Estimated Effort:** 3 man-days

---

#### 3.5.2 FR-EMG-02: Emergency File Management
**Priority:** Medium
**Description:** Admin must manage (view, download, update, delete) emergency files.

**System Actions:**
1. Display list of uploaded emergency files
2. Show metadata for each:
   - Title
   - Description
   - Upload date
   - Uploaded by (admin name)
   - Priority
   - Applicable regions
3. Provide actions:
   - Download file
   - View file (PDF preview)
   - Edit metadata
   - Delete file (with confirmation)
   - Archive (hide from active list)
4. For PDFs: Show preview inline
5. For images: Show thumbnail
6. Filter by:
   - Priority
   - Upload date range
   - Region
   - Title search
7. Sort by:
   - Upload date (newest first)
   - Title (alphabetical)
   - Priority

**Acceptance Criteria:**
- All files listed with complete metadata
- Download works correctly
- PDF preview functional
- Edit/Delete/Archive work
- Filters return correct results

**Estimated Effort:** 3 man-days

---

#### 3.5.3 FR-EMG-03: Emergency Protocol Distribution
**Priority:** Medium
**Description:** System should notify relevant staff of new emergency protocols.

**System Actions:**
1. When new emergency file uploaded with Critical/High priority:
2. Identify affected staff:
   - If no regions specified: All active staff
   - If regions specified: Staff in those regions
3. Send WhatsApp notification:
```
【Prestige Health - Emergency Protocol】
Title: Emergency Staffing Procedures - Typhoon
Priority: Critical
Effective: 2025-11-25

View: [link]

Please read immediately. Reply "READ" to confirm.
```
4. Track who has viewed the file
5. Track who has confirmed via WhatsApp
6. Generate report:
   - Total staff notified
   - Staff who viewed
   - Staff who confirmed
   - Staff not yet confirmed
7. Follow up with non-confirmed staff after 24 hours
8. Admin can view confirmation status dashboard

**Acceptance Criteria:**
- Critical/High priority files trigger notifications
- Only affected staff notified
- Confirmation tracking works
- Reports generated accurately

**Estimated Effort:** 4 man-days

---

#### 3.5.4 FR-EMG-04: Emergency Job Posting Override
**Priority:** High
**Description:** Admin must be able to manually post emergency jobs bypassing standard workflow.

**System Actions:**
1. Admin clicks "Emergency Job Posting"
2. Fill form:
   - Location (dropdown from synced locations)
   - Required date and time
   - Number of staff needed
   - Special requirements
   - Urgency level
   - Contact person on duty
3. Optionally: Upload emergency file (link from FR-EMG-01)
4. System validates:
   - Date/time in future
   - Required count > 0
5. Immediately post to job board (bypass 15-min poll)
6. Immediately trigger matching algorithm
7. Send urgent WhatsApp to best-matched staff:
```
【URGENT - Immediate Staff Needed】
Location: Hong Kong Care Home
Date: Today 2025-11-25
Time: 18:00 - 22:00 (4 hours)
Urgency: Critical

Are you available?
Reply YES immediately
```
8. Staff replies YES → Immediate confirmation (no 2-hour wait)
9. Show real-time status in emergency dashboard:
   - Staff needed vs. Staff confirmed
   - Pending confirmations
   - Time remaining
10. Alert admin if staff shortage after 30 minutes

**Acceptance Criteria:**
- Emergency job posted immediately
- Matching triggered in real-time
- Urgent notifications sent
- Real-time dashboard functional
- Admin alerted for shortages

**Estimated Effort:** 5 man-days

---

### 3.6 Admin Portal Features

#### 3.6.1 FR-ADM-01: Admin Dashboard
**Priority:** High
**Description:** Admin dashboard showing key metrics and system status.

**Dashboard Widgets:**
1. **Today's Overview:**
   - Total jobs posted
   - Jobs filled / unfilled
   - Confirmed staff
   - Pending confirmations
2. **Matching Status:**
   - Successful matches (last 24h)
   - Failed assignments
   - Re-matching required
3. **Attendance:**
   - Completed shifts
   - No-shows
   - Pending verification
4. **Penalties:**
   - Cancellations today
   - No-shows today
   - Total deductions (100 HKD × count)
5. **System Health:**
   - Last ERP sync time
   - API status (ERP, WhatsApp)
   - Failed API calls
   - Pending retries
6. **Emergency Alerts:**
   - Active emergency protocols
   - Staff shortages
   - Unfilled jobs
7. **Quick Actions:**
   - Manual assignment
   - Emergency job posting
   - Upload emergency file

**Acceptance Criteria:**
- All widgets display accurate real-time data
- Auto-refresh every 30 seconds
- Click to drill down to details

**Estimated Effort:** 4 man-days

---

#### 3.6.2 FR-ADM-02: Manual Assignment Interface
**Priority:** Medium
**Description:** Admin can manually assign staff to jobs (override automatic matching).

**System Actions:**
1. Admin views unfilled job demands
2. Searches for staff:
   - By name
   - By location preference
   - By availability
   - By score/tier
3. Select staff manually
4. System shows warning:
   - Document validity
   - Blacklist status
   - Availability conflicts
5. Admin confirms assignment
6. Call ERP API 3.1 (emergency assignment)
7. Set assigned_by: "manual_admin"
8. Store admin ID and timestamp
9. Send WhatsApp notification to staff
10. Log manual assignment with reason

**Acceptance Criteria:**
- Search filters work correctly
- Conflict warnings displayed
- ERP updated correctly
- Audit log complete

**Estimated Effort:** 3 man-days

---

#### 3.6.3 FR-ADM-03: System Monitoring
**Priority:** Medium
**Description:** Admin can monitor all system activities and logs.

**Monitoring Features:**
1. **API Call Logs:**
   - View all ERP API calls
   - Filter by:
     * API endpoint
     * Timestamp range
     * Status (success/error)
     * Staff/Location ID
   - Show request/response details
   - Show retry attempts
2. **Sync Status:**
   - Last sync time for each data type
   - Next scheduled sync
   - Items synced (count)
   - Errors encountered
3. **User Activity:**
   - Admin actions (login, overrides, uploads)
   - Staff confirmations/cancellations
   - Login timestamps
4. **Error Dashboard:**
   - Failed API calls
   - Sync errors
   - Validation failures
   - Duplicate detection
   - Alert for critical errors

**Acceptance Criteria:**
- All logs searchable and filterable
- Critical errors trigger alerts
- Logs retained for 90 days

**Estimated Effort:** 4 man-days

---

## 4. ERP INTEGRATION REQUIREMENTS

### 4.1 Integration Architecture

**Bi-Directional Sync:**
- **Pull (ERP → PHC):** Master data, demands
- **Push (PHC → ERP):** Assignments, attendance, penalties, scores
- **Modes:** Real-time (assignments), Batch (attendance), Scheduled (master data)

**API Standards:**
- Protocol: HTTPS
- Data Format: JSON
- Authentication: OAuth 2.0 or API Keys (TBD)
- Rate Limiting: To be specified by ERP team
- Timeout: 30 seconds per request

---

### 4.2 Required ERP APIs (To Be Specified by ERP Team)

#### 4.2.1 GET /api/v1/staff/active
**Purpose:** Get list of active nursing assistants
**Frequency:** Daily at 02:00 AM
**Response:** See Section 3.1.1

#### 4.2.2 GET /api/v1/staff/availability
**Purpose:** Get staff availability for next 7 days
**Frequency:** Daily at 02:00 AM
**Response:** See Section 3.1.3

#### 4.2.3 GET /api/v1/staff/{id}/documents
**Purpose:** Get staff certificates and documents
**Frequency:** Weekly
**Response:** See Section 3.1.2

#### 4.2.4 GET /api/v1/locations/active
**Purpose:** Get active care home locations
**Frequency:** Daily at 03:00 AM
**Response:** See Section 3.2.1

#### 4.2.5 GET /api/v1/locations/{id}/preferences
**Purpose:** Get location preferences (underlist, blacklist, requirements)
**Frequency:** Daily at 03:00 AM
**Response:** See Section 3.2.1

#### 4.2.6 GET /api/v1/jobs/demands
**Purpose:** Get job demands (open/unfilled)
**Frequency:** Every 15 minutes
**Response:** See Section 3.2.2

#### 4.2.7 POST /api/v1/jobs/assignments
**Purpose:** Submit staff assignment
**Frequency:** Real-time (on match)
**Request:** See Section 3.3.3

#### 4.2.8 PATCH /api/v1/jobs/assignments/{id}
**Purpose:** Update assignment status (confirm/cancel)
**Frequency:** Real-time
**Request:** See Section 3.3.5

#### 4.2.9 POST /api/v1/attendance
**Purpose:** Submit attendance record
**Frequency:** Real-time or batch (end of shift)
**Request:** See Section 3.4.2

#### 4.2.10 POST /api/v1/penalties
**Purpose:** Submit penalty record (cancellation/no-show)
**Frequency:** Real-time
**Request:** See Section 3.4.3

#### 4.2.11 PATCH /api/v1/staff/{id}/score
**Purpose:** Update staff score
**Frequency:** Real-time
**Request:** See Section 3.4.3

#### 4.2.12 GET /api/v1/settlements/{id}
**Purpose:** Get settlement/payment status
**Frequency:** Monthly (1st of month)
**Response:** See Section 3.4.5

#### 4.2.13 POST /api/v1/finance/deduction (TBD)
**Purpose:** Process 100 HKD penalty deduction
**Frequency:** Real-time (when penalty applied)
**Status:** API specification to be provided by ERP team before development

---

### 4.3 Webhook Integration (Optional - To Be Confirmed)

**ERP to PHC Webhook:**
- Endpoint: `POST /webhook/erp/job-demand`
- Trigger: When new demand posted in ERP
- Payload: Full demand details (see Section 3.2.2)
- Authentication: Signature validation
- Processing: Real-time posting and matching

**PHC to ERP Webhook:**
- To be defined if needed

---

### 4.4 Data Mapping

See detailed data mapping tables in Appendix A.

---

### 4.5 Data Retention

| Data Type | Retention Period | Archive Location |
|-----------|------------------|------------------|
| API Logs | 90 days | Database |
| Assignment Records | 7 years | Database + Archive |
| Attendance Records | 7 years | Database + Archive |
| Settlement Records | 7 years | Database + Archive |
| Emergency Files | Until superseded + 1 year | S3/Azure Blob |
| System Logs | 30 days | Log aggregator |

---

## 5. NON-FUNCTIONAL REQUIREMENTS

### 5.1 Performance Requirements

| Metric | Target | Measurement |
|--------|--------|-------------|
| API Response Time (ERP) | < 3 seconds average | 95th percentile |
| API Response Time (WhatsApp) | < 5 seconds | Average |
| Matching Algorithm | < 5 minutes per demand | End-to-end |
| Demand Sync Latency | < 15 minutes | Polling mode |
| Webhook Processing | < 1 minute | End-to-end |
| Page Load Time (Admin Portal) | < 3 seconds | Average |
| Concurrent Users | 50+ admins | Load test |
| Database Query Time | < 500ms | 95th percentile |

---

### 5.2 Scalability Requirements

- Support 500+ nursing assistants
- Support 100+ care home locations
- Handle 500+ job demands per month
- Handle 200+ daily assignments
- Database growth: ~50GB/year
- API calls: ~10,000/day (estimated)

---

### 5.3 Availability Requirements

- **System Uptime:** 99.5% (excluding maintenance windows)
- **Maintenance Window:** Sunday 02:00-04:00 AM (2 hours)
- **Scheduled Sync Jobs:** Must complete within window
- **Emergency Access:** 24/7 for critical functions

---

### 5.4 Reliability Requirements

- **API Success Rate:** > 99% (excluding client errors)
- **Data Integrity:** Zero data loss
- **Sync Success Rate:** > 99% for all scheduled jobs
- **Retry Logic:** 3 attempts with exponential backoff
- **Queue Persistence:** Jobs survive system restart
- **Backup:** Daily database backup (retain 30 days)

---

### 5.5 Security Requirements

#### 5.5.1 Authentication & Authorization
- **User Authentication:** OAuth 2.0 or SAML
- **API Authentication:** OAuth 2.0 or API keys
- **Password Policy:**
  - Minimum 8 characters
  - Uppercase, lowercase, number, special char
  - Expire every 90 days
- **Session Timeout:** 30 minutes inactivity
- **Multi-Factor Auth:** Required for admin accounts
- **Role-Based Access Control:**
  - Admin: Full access
  - Supervisor: View only (own location)
  - Staff: View own assignments only

#### 5.5.2 Data Protection
- **Encryption at Rest:** AES-256 for sensitive data (HKID, bank accounts)
- **Encryption in Transit:** TLS 1.2+
- **Sensitive Data Masking:**
  - HKID: A123***(*)
  - Bank account: ****1234
  - Phone: 9123****
- **API Key Management:** Rotate every 90 days
- **Audit Logging:** Log all access and changes (retain 90 days)

#### 5.5.3 Compliance
- **Data Privacy:** Comply with Hong Kong PDPO
- **Audit Trail:** Complete audit for all financial transactions
- **Access Logs:** Record IP address, timestamp, user ID for all access
- **Data Retention:** Follow retention policy (Section 4.5)
- **Right to Erasure:** Support data deletion requests (within legal limits)

---

### 5.6 Usability Requirements

#### 5.6.1 Admin Portal
- **Responsive Design:** Works on desktop, tablet, mobile
- **Browser Support:** Chrome, Firefox, Safari, Edge (latest 2 versions)
- **Page Load:** < 3 seconds average
- **Error Messages:** User-friendly, actionable
- **Help Tooltips:** Where needed
- **Keyboard Navigation:** Support tab order
- **Color Contrast:** WCAG AA compliance
- **Language:** English + Traditional Chinese

#### 5.6.2 WhatsApp Notifications
- **Message Length:** < 1000 characters
- **Clear Call-to-Action:** Buttons or numbered options
- **Language:** Traditional Chinese (primary), English (optional)
- **Character Set:** Support Chinese characters, emojis
- **Rich Media:** Support images, documents (for emergency files)

---

### 5.7 Maintainability Requirements

- **Code Documentation:** Inline comments for complex logic
- **API Documentation:** Swagger/OpenAPI for all APIs
- **Runbook:** Operations and troubleshooting guide
- **Deployment:** Automated CI/CD pipeline
- **Monitoring:** Health checks, metrics, logging
- **Version Control:** Git with feature branch workflow
- **Testing:** Unit tests (coverage > 80%), integration tests

---

## 6. USER INTERFACE REQUIREMENTS

### 6.1 Admin Portal Pages

#### 6.1.1 Login Page
- Username/email field
- Password field
- "Forgot password" link
- Login button
- Error messages (invalid credentials)

#### 6.1.2 Dashboard (Home)
- Real-time metrics widgets (see FR-ADM-01)
- Quick action buttons
- Recent activity feed
- Alerts/notifications

#### 6.1.3 Staff Management
- Staff list with search/filter
- Staff details view
- Document/certificate view
- Score history
- Manual score adjustment
- Manual assignment override

#### 6.1.4 Location Management
- Location list with search/filter
- Location details view
- Underlist management
- Blacklist management
- Special requirements

#### 6.1.5 Job Postings
- Active job postings list
- Create/edit/delete postings
- Manual emergency posting
### 6.2 Staff Portal Interface

#### 6.2.1 Login Page
- Fields: Mobile Number, Password
- "Forgot Password" link
- "Remember Me" checkbox
- Language toggle (EN/ZH)

#### 6.2.2 Staff Dashboard
- **My Score:** Current score and tier
- **Upcoming Shifts:** List of confirmed assignments
- **Available Shifts:** List of open jobs matching criteria
- **Notifications:** Recent alerts

#### 6.2.3 My Shifts
- List of all assignments (Pending, Confirmed, Completed, Cancelled)
- Details view for each assignment
- Action buttons: Confirm, Cancel

#### 6.2.4 Profile
- Personal details (read-only, synced from ERP)
- Certificate status
- Availability calendar management

### 6.3 Supervisor Portal (Mobile-Friendly)
#### 6.1.8 Penalties
- Penalty list (today/historical)
- Penalty details
- Manual waiver
- Penalty statistics

#### 6.1.9 Emergency Protocols
- Upload emergency files
- Emergency file list
- Emergency job posting
- Confirmation tracking
- Distribution reports

#### 6.1.10 Monitoring
- API logs view
- Sync status
- Error dashboard
- Performance metrics
- Data quality reports

#### 6.1.11 Reports
- Settlement reports
- Attendance reports
- Penalty reports
- Score reports
- Custom date range
- Export to Excel/PDF

### 6.2 Staff WhatsApp Interface

#### 6.2.1 Assignment Notification
See FR-MAT-04

#### 6.2.2 Confirmation Response
- Staff replies "1" to confirm
- Staff replies "2" to cancel
- Or clicks link in message

#### 6.2.3 Cancellation Warning
See FR-MAT-05

#### 6.2.4 Confirmation Message
Success message sent after confirmation

### 6.3 Supervisor Portal (Mobile-Friendly)

#### 6.3.1 Today's Schedule
- List of assigned staff for shift
- Staff photos (if available)
- Contact numbers
- Expected arrival time

#### 6.3.2 Clock-In/Out Verification
See FR-SET-01

#### 6.3.3 No-Show Marking
- Button to mark staff as absent
- Confirm no-show (with reason)
- View no-show history

---

## 7. IMPLEMENTATION TIMELINE (CONDENSED)

**Target:** 1.5 Months / 60 Man-Days (from 12 weeks)

### Phase 1: Core Foundation (Week 1-2, 20 man-days)

#### Week 1 (10 man-days)
- **Day 1-2:** API authentication setup, ERP connection
- **Day 3-5:** Staff sync implementation (API 1.1, 1.2)
- **Day 6-7:** Location sync (API 2.1, 2.3)
- **Day 8-10:** Database schema for staff, locations, scoring

**Deliverable:** Master data syncing operational

#### Week 2 (10 man-days)
- **Day 1-3:** Job demand polling (API 2.2)
- **Day 4-7:** Admin dashboard basic version
- **Day 8-10:** Emergency file upload (FR-EMG-01)

**Deliverable:** Job postings syncing, admin can upload files

---

### Phase 2: Matching & Scoring (Week 3-4, 18 man-days)

#### Week 3 (10 man-days)
- **Day 1-5:** Scoring algorithm engine (FR-MAT-01, FR-MAT-02)
- **Day 6-8:** Matching algorithm implementation
- **Day 9-10:** Assignment submission to ERP (API 3.1)

**Deliverable:** Matching engine operational

#### Week 4 (8 man-days)
- **Day 1-3:** WhatsApp notification integration
- **Day 4-6:** Staff confirmation flow (FR-MAT-05)
- **Day 7-8:** Manual override interface (FR-MAT-06)

**Deliverable:** End-to-end matching flow working

---

### Phase 3: Attendance & Settlement (Week 5-6, 14 man-days)

#### Week 5 (8 man-days)
- **Day 1-3:** Clock-in/out interface (QR code)
- **Day 4-6:** Attendance submission to ERP (API 4.1)
- **Day 7-8:** No-show handling (FR-SET-03)

**Deliverable:** Attendance tracking working

#### Week 6 (6 man-days)
- **Day 1-4:** Penalty management (calculation, warnings, ERP sync - API 4.2, 4.4)
- **Day 5-6:** Score updates and tier calculation

**Deliverable:** Penalty system operational

---

### Phase 4: Enhanced Features & Testing (Week 7-8, 8 man-days)

#### Week 7 (4 man-days)
- **Day 1-2:** Settlement reconciliation (API 4.3)
- **Day 3-4:** Emergency job posting (FR-EMG-04)

**Deliverable:** Emergency protocols complete

#### Week 8 (4 man-days)
- **Day 1-2:** Complete admin dashboard
- **Day 3-4:** End-to-end testing, bug fixes, documentation

**Deliverable:** System ready for UAT

---

### Final Checks & Go-Live (2 man-days buffer)
- **1 day:** User acceptance testing support
- **1 day:** Bug fixes and final deployment

---

## 8. ACCEPTANCE CRITERIA

### 8.1 Overall System

✅ All 4 main flows operational (Registration, Job Posting, Matching, Settlement)
✅ ERP bi-directional sync working (all 13 APIs)
✅ Scoring algorithm accurate (100% accuracy)
✅ Financial penalties applied correctly (100% accuracy)
✅ WhatsApp notifications delivered (< 5 min)
✅ Attendance tracking functional (QR or supervisor verification)
✅ Emergency file upload and distribution working
✅ Admin dashboard shows real-time metrics
✅ Zero critical data loss in testing
✅ System uptime > 99% during testing period

### 8.2 Performance Targets

✅ Matching completes in < 5 minutes
✅ Demand sync latency < 15 minutes (polling)
✅ API response time < 3 seconds average
✅ Page load time < 3 seconds
✅ WhatsApp delivery < 5 minutes

### 8.3 Integration Requirements

✅ All ERP API calls tested with sample data
✅ Webhook implemented (if ERP supports)
✅ Retry logic working (3 attempts)
✅ Error handling functional
✅ Data mapping validated

### 8.4 Documentation

✅ User manual for admin
✅ Runbook for operations
✅ API documentation
✅ Troubleshooting guide
✅ Training materials

---

## 9. APPENDICES

### Appendix A: Data Mapping Tables

See complete data mapping in `erp-api-integration-specification.md`

### Appendix B: API Specification

See complete API specs in `erp-api-integration-specification.md`

### Appendix C: Scoring Algorithm Details

See complete scoring spec in `scoring-algorithm-specification.md`

### Appendix D: Integration To-Do List

See complete checklist in `integration-todo-list.md`

---

## 📌 NOTES

1. **Fair Sharing:** Manually controlled in existing ERP system. PHC respects limits but doesn't implement algorithm.

2. **Geographic Intelligence:** Excluded from v1.0. Can be added later:
   - Distance-based matching
   - Transportation time
   - Regional pooling

3. **Emergency Protocols:** Fully manual through file upload. No automated emergency triggers.

4. **Financial Deduction API:** TBD by ERP team. PHC will log penalties until API specified.

5. **Webhook:** Optional. Sync works with polling only.

6. **Clock-In/Out:** Two options provided. Team can choose based on complexity preference:
   - Option A (QR): More complex, requires mobile interface
   - Option B (Supervisor): Simpler, portal-based

7. **Timeline:** Aggressive 1.5-month timeline requires dedicated team and assumes:
   - No major blockers
   - Rapid ERP team response
   - Parallel development possible
   - Overtime acceptable

---

**Document Owner:** BMAD Analyst (Mary)
**Approved By:** [To be signed off]
**Date:** 2025-11-24
**Version:** 2.0

**Next Review:** After Phase 1 completion (Week 2)