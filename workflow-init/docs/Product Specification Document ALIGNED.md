# Healthcare Worker Dispatch System (PHC)
## Prestige Health Care Agency Ltd

**Document Version:** 1.1 (ALIGNED WITH PRD)
**Date:** November 24, 2025
**Status:** Aligned with Product Requirements Document

---

## Document Control

| Version | Date       | Author        | Changes                      |
|---------|------------|---------------|------------------------------|
| 1.0     | 2025-11-24 | System Analyst| Initial draft for client review |

---

## Executive Summary

This document specifies the functional and technical requirements for the Prestige Health Dispatch System (PHC), a web-based platform designed to automate healthcare worker-to-facility matching based on merit-based scoring and real-time availability.

**Project Objectives:**

- Increase shift fill rate from 85% to 95%+ within 3 months
- Reduce coordinator time by 75% (3 hours → 45 min/day)
- Decrease no-shows from 5% to <2%
- Launch complete system in 60 days
- Process 500+ daily assignments across 500+ staff

**Key Differentiator:** Merit-based scoring algorithm ensures fair, transparent allocation based on reliability history, not manual bias.

**Target Users:**

1. **Nursing Assistants (500+)** - Receive shift assignments via WhatsApp, confirm via web portal
2. **PHC Administrators (5-10)** - Monitor operations, handle exceptions, verify attendance via admin dashboard
3. **ERP System** - Bidirectional data sync (13 API endpoints)

---

## 1. Product Overview

### 1.1 System Purpose

The PHC system automates dispatch of nursing assistants to care home shifts using:
- Scoring algorithm for merit-based allocation
- Real-time ERP integration
- WhatsApp notifications (manual template-based for MVP)
- Web-based confirmation portal
- Attendance verification (QR code OR supervisor verification)

### 1.2 System Context

**External Systems:**
- Existing ERP System (primary source of truth for staff, locations, job demands)
- WhatsApp (primary communication channel)
- Firebase Cloud Messaging (web push notifications for reminders)

**Primary Users:**
- Nursing assistants (recipients of assignments)
- PHC administrators (monitoring, overrides, attendance verification)

### 1.3 System Boundaries

**In Scope (Version 1.0):**
- Scoring and performance tracking (FR-1)
- Automated matching engine (FR-2)
- WhatsApp + Firebase hybrid notifications (FR-3)
- Admin dashboard (FR-4)
- ERP integration (13 APIs) (FR-5)
- Attendance tracking (admin-based verification) (FR-6)
- Penalty management (FR-7)
- Emergency file upload and distribution (FR-8)
- Emergency job posting (FR-9)
- Settlement reconciliation (FR-10)
- Manual assignment override (FR-11)
- System monitoring (FR-12)
- Reporting (FR-13)

**Out of Scope (Version 1.0):**
- Native mobile applications (use web portal on mobile)
- Payment processing (handled by ERP)
- Automated fair sharing (manual control for MVP)
- Distance-based matching (deferred to v2.0)
- Advanced ML predictions (deferred to v2.0)
- Billing/invoicing (ERP handles)
- WhatsApp Business API (using manual templates for MVP)

**Future Enhancements (Version 2.0+):**
- QR Code System (facility identification and attendance tracking)
- Geographic intelligence (distance-based matching)
- WhatsApp Business API automation
- Predictive analytics
- Native mobile app
- Advanced fair sharing algorithm

---

## 2. User Roles and Permissions

### 2.1 User Role Definitions

| Role | Description | Key Permissions |
|------|-------------|----------------|
| **System Administrator** | Full system access | All permissions, user management, system settings |
| **PHC Administrator** | Operations management | Create/edit/delete jobs, assign workers, view all data, manual overrides, verify attendance |
| **Nursing Assistant** | Frontline staff | Receive assignments, confirm/cancel shifts, view score/history |
| **ERP Integration** | System-to-system | API access for data sync (read staff/locations, write assignments/attendance) |

### 2.2 Permission Matrix

| Function | Admin | Worker | ERP |
|----------|-------|--------|-----|
| View Dashboard | ✓ | ✓ | ✗ |
| Create Job Post | ✓ | ✗ | ✓ |
| Edit Job Post | ✓ | ✗ | ✗ |
| Assign Worker | ✓ | ✗ | ✗ |
| Confirm/Cancel Shift | ✗ | ✓ | ✗ |
| Verify Attendance | ✓ | ✗ | ✗ |
| View Score | ✗ | ✓ | ✗ |
| Manual Override | ✓ | ✗ | ✗ |
| ERP API Access | ✓ | ✗ | ✓ |

---

## 3. Functional Requirements

### 3.1 Scoring Algorithm (FR-1)

**Description:** Merit-based scoring system for fair, transparent allocation

**Scoring Rules:**
- Attend shift: +1 point
- Cancel shift with notice: -1 point, -100 HKD penalty
- Starting score for new staff: 50 points

**Score Tiers:**
- Gold: 20+ points (first priority)
- Silver: 10-19 points (second priority)
- Bronze: 0-9 points (third priority)
- Under Review: <0 points (manual approval required)
- Score floor: -10 points (minimum)

**System Behavior:**
- Scores update automatically upon attendance verification
- ERP synced in real-time via PATCH /api/v1/staff/{id}/score
- Manual override requires reason and audit trail
- Staff can view current score and history in portal

**Acceptance Criteria:**
✅ Score updates automatically upon attendance confirmation
✅ ERP sync confirmed within 1 minute
✅ Manual override requires reason field
✅ Score floor enforced at -10
✅ Tier displayed correctly in staff portal

---

### 3.2 Matching Engine (FR-2)

**Description:** Automated selection of best staff for each shift based on multiple criteria

**Matching Criteria (Priority Order):**

1. **Underlist** (previous work history at facility)
   - Staff who worked at facility before get priority
   - Ordered by positive history and frequency

2. **Score Tier** (Gold → Silver → Bronze)
   - Rank by score tier first
   - Within tier: by actual score value

3. **Availability** (from ERP sync)
   - Must be marked as available
   - Check for conflicting shifts

4. **Document Validity**
   - Required certificates/permits valid
   - Expiration dates checked

5. **Blacklist Exclusion**
   - Facility-specific blacklist respected
   - Cannot assign blacklisted staff

6. **Fair Sharing Limit** (from ERP)
   - Maximum shifts per staff per period
   - Prevents over-allocation

7. **Manual Override** (admin)
   - Admin can manually assign specific staff
   - Reason required, audit logged

**Matching Process:**
```
Input: Job demand (facility, date, shift, count)

Step 1: Filter eligible staff
- Remove unavailable staff
- Remove blacklisted staff
- Remove expired documents
- Remove exceeding fair share limit

Step 2: Prioritize by underlist
- If staff on facility underlist → highest priority
- Order by underlist priority score

Step 3: Rank by score tier
- Gold tier first, then Silver, then Bronze
- Within tier: sort by actual score (descending)

Step 4: Apply additional factors
- Prefer staff with recent positive history
- Consider proximity (future enhancement)
- Balance with other concurrent assignments

Step 5: Select best matches
- Pick top-ranked staff for needed count
- Generate assignment records

Step 6: Notify and confirm
- Send WhatsApp notification
- Wait for confirmation (2-hour window)
- If declined, move to next candidate
```

**Matching SLA:**
- Match completed: < 5 minutes from job posting
- Re-matching triggered automatically if staff decline
- All filters applied correctly

**Acceptance Criteria:**
✅ Match completes within 5 minutes
✅ All filters applied correctly (availability, blacklist, documents)
✅ Underlist respected first
✅ Re-matching triggered automatically on declines
✅ ERP assignment API called with correct data
✅ Unfilled jobs flagged for manual intervention

---

### 3.3 WhatsApp + Firebase Hybrid Notifications (FR-3)

**Description:** WhatsApp for primary notifications (manual template-based) + Firebase web push for portal alerts and reminders

**WhatsApp Notifications (Primary Channel):**
- System generates WhatsApp message templates with shift details
- Coordinator copies template and sends via WhatsApp
- Templates include: date, location, shift time, contact person, confirmation link
- Support for urgent shift notifications
- Bilingual templates (English + Traditional Chinese)

**Template Format:**
```
🩺 Prestige Health Assignment
📅 Date: {date}
🏥 Location: {location_name}
⏰ Shift: {start_time} - {end_time}
👤 Contact: {supervisor_name} ({phone})

Please confirm: {confirmation_link}

⚠️ Confirm within 2 hours to secure this shift
✅ Your score will increase by +1 when you attend
```

**Coordinator Workflow:**
1. View assignment in PHC portal
2. Click "Copy Template" button
3. Paste into WhatsApp (individual chat or broadcast list)
4. Send to staff
5. Mark as "sent_via_whatsapp" in system
6. Track confirmation status

**Firebase Web Push (Secondary - Portal Alerts):**

**Triggers:**
1. **New Assignment Alert**
   - When: Immediately after coordinator marks sent
   - Audience: Assigned staff
   - Purpose: Alert in web portal (if logged in)

2. **Pending Confirmation Reminder**
   - When: 2 hours after assignment (if not confirmed)
   - Audience: Staff with pending confirmations
   - Content: "Reminder: Shift confirmation pending - 2 hours left"

3. **Day-Before Shift Reminder**
   - When: 24 hours before shift start
   - Audience: All confirmed staff for next day
   - Content: "Reminder: Your shift tomorrow at {location}"

4. **Admin Confirmation Notification**
   - When: Staff confirms shift
   - Audience: Coordinators/supervisors
   - Content: "{staff_name} confirmed shift at {location}"

**Firebase Implementation:**
- Service Worker registration for web push
- FCM token storage per user device
- Permission request on first login
- Graceful degradation if denied (rely on WhatsApp primary)
- Token refresh handling

**Delivery SLA:**
- WhatsApp template generation: < 5 seconds
- Coordinator send time: < 1 minute per assignment
- Firebase notification delivery: < 30 seconds

**Acceptance Criteria:**
✅ Template generated with correct details
✅ Confirmation link works with deep linking to assignment
✅ Firebase notifications delivered within 30 seconds
✅ Staff can confirm/cancel via web portal after clicking link
✅ Automatic reminders sent at 2h and 24h
✅ Works on mobile and desktop browsers
✅ Coordinator dashboard shows pending confirmations

---

### 3.4 Admin Dashboard (FR-4)

**Description:** Real-time view of all operations

**Dashboard Widgets:**
- Today's jobs (total, filled, unfilled)
- Confirmed staff vs pending confirmations
- Completed shifts vs no-shows
- Cancellations and penalties today
- API health status
- Last ERP sync time
- Failed API calls
- Average confirmation time
- Score distribution (Gold/Silver/Bronze counts)

**Features:**
- Auto-refresh every 30 seconds
- Click any metric to drill down to details
- Color-coded status (green/yellow/red)
- Export to PDF/Excel for management reports
- Filter by date range, facility, shift type

**Acceptance Criteria:**
✅ All metrics accurate and real-time
✅ Auto-refresh works without manual intervention
✅ Load time < 3 seconds
✅ Drill-down navigation functional
✅ Color coding matches status accurately

---

### 3.5 ERP Integration (FR-5)

**Description:** Bi-directional data sync with existing ERP (13 API endpoints)

**ERP → PHC (7 pull endpoints):**

1. **GET /api/v1/staff/active** - Daily at 02:00 AM
   - All active staff data
   - Fields: staff_id, names, contact, HKID, certificates, bank account, status
   - Validates HKID format, phone numbers (8 digits)
   - Sync completed in < 5 minutes

2. **GET /api/v1/staff/availability** - Daily at 02:30 AM
   - Staff availability schedules
   - Fields: staff_id, available dates/times, preferred locations

3. **GET /api/v1/staff/{id}/documents** - Weekly
   - Download required documents: qualifications, certs, permits
   - Validate expiration dates

4. **GET /api/v1/locations/active** - Daily at 03:00 AM
   - All active care home locations
   - Fields: location_id, name, address, contact, region, district
   - Includes underlist (priority staff) and blacklist

5. **GET /api/v1/locations/{id}/preferences** - Daily at 03:30 AM
   - Location-specific requirements
   - Fields: special requirements, certifications needed

6. **GET /api/v1/jobs/demands** - Every 15 minutes (09:00-22:00)
   - Unfilled job demands
   - Fields: demand_id, location_id, date, shift_start/end, required_count, status
   - Webhook support if available

7. **GET /api/v1/settlements/{id}** - Monthly (1st of month)
   - Settlement data for reconciliation
   - Fields: staff_id, payment_amount, deductions, period

**PHC → ERP (6 push endpoints):**

8. **POST /api/v1/jobs/assignments** - Real-time
   - Submit confirmed assignments
   - Fields: phc_assignment_id, demand_id, staff_id, location_id, date, shift_times
   - Return: erp_assignment_id, confirmation
   - Handles 409 conflict if staff unavailable

9. **PATCH /api/v1/jobs/assignments/{id}** - Real-time
   - Update assignment status changes
   - Fields: status, timestamps

10. **POST /api/v1/attendance** - Post-shift (within 1 hour)
    - Submit attendance records
    - Fields: assignment_id, staff_id, location_id, clock_in/out, actual_hours, status
    - Status: completed, partial, no_show

11. **POST /api/v1/penalties** - Real-time
    - Submit penalty records
    - Fields: assignment_id, staff_id, penalty_type (cancellation/no_show), amount (100 HKD), score_impact (-1 or -2)
    - ERP deducts from next settlement

12. **PATCH /api/v1/staff/{id}/score** - Real-time
    - Update score after attendance/penalty
    - Fields: score_change, new_score, reason, assignment_id

13. **POST /api/v1/finance/deduction** - TBD
    - Actual financial deduction (awaiting ERP API specification)

**Integration Details:**

**Polling Frequency:**
- Staff/Locations: Daily at 02:00-03:30 AM (low traffic period)
- Job Demands: Every 15 minutes (09:00-22:00 business hours)
- Assignments/Attendance/Penalties/Scores: Real-time (immediate trigger)

**Error Handling:**
- Connection failures: Retry 3 times with exponential backoff (5min, 15min, 45min)
- Data validation errors: Log error, alert admin staff, skip record, continue processing
- Duplicate records: Compare timestamps, keep latest, log warning
- API timeouts: Alert after 3 failures, queue for manual retry

**Data Validation:**
- Staff: HKID format validation, phone numbers (8 digits), active status check
- Locations: Unique codes, active status, regional mapping
- Assignments: Staff availability conflict check, blacklist check, fair sharing limits

**Acceptance Criteria:**
✅ All 13 APIs tested and working (mock + real ERP endpoints)
✅ Zero data loss during sync
✅ Retry logic executes 3 attempts as specified
✅ Error logging captures all failures
✅ Alerts sent to admin for critical failures (>3 consecutive)
✅ Performance SLA met: < 3 seconds per API call
✅ Daily sync completed by 05:00 AM
✅ Real-time updates sent within 1 minute

---

### 3.6 Attendance Tracking (FR-6)

**Description:** Admin-based attendance verification via centralized portal

**Admin Portal Verification:**

**How it works:**
1. PHC Administrator opens admin portal
2. Views "Attendance Dashboard" with all facilities
3. Filters by facility and date
4. Sees list of confirmed staff with photos
5. Marks attendance status for each staff:
   - ✅ Present (clock-in time recorded)
   - ❌ No-show (penalty applied automatically)
   - ⏰ Late (with notes)
   - 🏠 Early departure (with notes)
6. System records all timestamps
7. Calculates actual hours worked
8. Syncs to ERP within 1 hour

**Admin Workflow:**
- Centralized view of all facilities
- Batch processing capability
- Can delegate to facility contacts via phone confirmation
- Total time: ~5 minutes for 20 facilities
- Add notes for deviations (late arrival, early departure)

**Facility Contact Phone Confirmation:**
- Admin calls facility contact person
- Verbally confirms staff attendance
- Admin records in system
- Maintains single source of truth in PHC system

**Clock-in/Clock-out Recording:**
- Admin records clock-in time (via facility contact confirmation)
- Admin records clock-out time at shift end
- Actual hours calculated automatically
- Deviation alerts: >1 hour difference from scheduled hours
- Admin reviews and approves/adjusts as needed

**No-Show Detection:**
- Automatic: If shift end + 15 minutes passes with no attendance record
- Admin can manually mark earlier if confirmed by facility
- System applies penalty automatically (FR-7)
- Triggers re-matching for urgent replacement

**ERP Sync:**
- Attendance submitted to ERP within 1 hour of shift completion
- Fields: assignment_id, staff_id, location_id, clock_in/out, actual_hours, status
- Status: completed, partial, no_show
- Calculated payment by ERP based on hours (rate TBD)

**Benefits:**
- No additional user role needed
- No tablet/device requirements at facilities
- Centralized control and oversight
- Maintains audit trail
- Simpler permission model

**Trade-offs:**
- Slightly more admin workload (5 min vs 2 min distributed)
- Requires phone communication with facilities
- Less real-time (but acceptable for post-shift verification)

**Acceptance Criteria:**
✅ Attendance recorded accurately (timestamp precision)
✅ Deviation > 1 hour flagged for admin review
✅ No-show detected automatically if no clock-in by shift end + 15min
✅ ERP submitted within 1 hour
✅ Admin can process entire day's attendance in < 10 minutes
✅ Works offline with sync when connection restored
✅ Audit trail complete for all attendance records

---

### 3.7 Penalty Management (FR-7)

**Description:** Automatic penalty application for violations

**Penalty Rules:**

1. **Cancellation** (with notice, >48 hours before shift)
   - Score: -1 point
   - Financial: --- HKD (admin cost)
   - Warning: None (acceptable notice period)

2. **Late Cancellation** (<48 hours before shift)
   - Score: -1 point
   - Financial: -300 HKD (admin cost)
   - Warning: Modal displays "300 HKD admin cost will be deducted" before allowing cancel
   - Staff can keep shift and reject cancellation

**Warning Workflow:**
```
Staff clicks "Cancel Shift" → System checks cancellation window
IF < 48 hours before shift:
  → Show warning modal: "100 HKD will be deducted when you apply AL within 48 hours before coming job!"
  → Show penalty details (-1 score, -100 HKD)
  → Buttons: [Keep Shift] [Confirm Cancellation]
ELSE:
  → Allow cancellation without penalty
  → Apply only -1 score (no financial penalty)
```

**Penalty Application Process:**
1. Cancellation or no-show recorded in PHC
2. Penalty record created: type, amount (300 HKD), score_impact, assignment_ref
3. Score updated immediately (FR-1)
4. Staff receives notification via WhatsApp
5. Notification appears in portal inbox
6. ERP API called for penalty record (POST /api/v1/penalties)
7. Penalty visible in staff's penalty history
8. Deduction applied to next settlement

**Financial Deduction:**
- API to ERP: POST /api/v1/finance/deduction (TBD - awaiting ERP specification)
- Staff ID, amount (300 HKD), reason, assignment reference
- ERP deducts from payment in next payroll cycle
- Confirmation receipt sent to PHC
- Penalty record marked as "processed"

**Re-matching on Cancellation/No-Show:**
- When shift cancelled or no-show detected
- System immediately starts re-matching process (FR-2)
- Looks for replacement staff from available pool
- Urgent flag set if < 24 hours before shift
- Admin alerted if unfilled after 30 minutes (emergency protocol)

**Acceptance Criteria:**
✅ Warning modal displayed clearly before late cancellation
✅ Penalty applied immediately (score + financial)
✅ Staff can keep shift (reject cancellation) after seeing warning
✅ ERP updated via API successfully
✅ Re-matching triggered for vacancy
✅ Cancellation recorded in staff assignment history
✅ Penalty history visible to staff in portal
✅ Successful submission to ERP confirmed

---

### 3.8 Emergency File Upload (FR-8)

**Description:** Upload and distribute emergency protocols to staff

**File Upload:**
- Supported formats: PDF, DOC, DOCX, JPG, PNG, MP4
- Maximum file size: 10MB per file
- Required metadata:
  - Title (required)
  - Description
  - Priority: Normal/High/Critical
  - Regions (Optional): HKI/KLN/NT (select multiple)

**Storage:**
- Secure cloud storage (AWS S3 or Azure Blob)
- Encrypted in transit (TLS 1.3) and at rest (AES-256)
- File metadata stored in PHC database
- Unique file ID generated
- Upload logged with admin ID and timestamp

**Distribution:**
- System identifies affected staff based on regions (if specified)
- Sends WhatsApp message with file link to relevant staff
- For Critical priority: also sends in-app alert
- Track views and confirmations in portal
- Generate report: delivery rate, confirmation rate

**Notification Message Template:**
```
🚨 URGENT - Emergency Protocol
📋 Title: {file_title}
📅 Posted: {timestamp}
⚠️ Priority: {priority}

View details: {file_link}

Please read and confirm receipt via portal
```

**Tracking Dashboard:**
- Admin can see: sent count, viewed count, confirmed count
- Filter by file, region, date
- Export report for compliance documentation
- Staff who haven't viewed highlighted in red

**Acceptance Criteria:**
✅ File uploaded successfully (validates size, type)
✅ Notifications sent within 5 minutes to affected staff
✅ Only staff in specified regions notified (if regions selected)
✅ In-app alert displayed for Critical priority
✅ View tracking works (accurate counts)
✅ Confirmation tracking works
✅ Report dashboard functional
✅ File stored securely with encryption

---

### 3.9 Emergency Job Posting (FR-9)

**Description:** Manual override for urgent staffing needs

**Priority Levels:**
- **Normal:** Standard 15-minute polling cycle
- **Urgent:** Bypass standard polling, immediate matching
- **Emergency:** Highest priority, immediate notification

**Emergency Workflow:**
1. Admin clicks "Emergency Job Posting" in portal
2. Fill form with urgent details:
   - Facility (dropdown)
   - Date and time (pre-filled with current/next shift)
   - Number of staff needed
   - Urgency reason (text)
3. Click "Post Emergency Job"
4. System bypasses 15-minute polling delay
5. Matching runs immediately (FR-2)
6. Urgent WhatsApp notification sent to shortlisted staff
7. In-app alert sent via Firebase (Critical priority)
8. Staff can "Accept Immediately" from portal
9. Real-time dashboard shows filling progress
10. Admin alerted if not filled within 30 minutes

**Staff Experience:**
- Receive urgent WhatsApp with link to expedited confirmation
- Portal shows "URGENT" badge on assignment
- One-tap "Accept Immediately" button
- Confirmation recorded instantly
- Score increased immediately (+1 point)

**Admin Alerts:**
- 📱 Push notification if position unfilled after 30 minutes
- 📧 Email to coordinator distribution list
- 🔴 Dashboard shows red "URGENT UNFILLED" banner

**Acceptance Criteria:**
✅ No delay in posting (bypasses 15-min polling)
✅ Matching triggered instantly
✅ Urgent notification sent via WhatsApp with in-app alert
✅ Dashboard updates showing filling progress (real-time)
✅ Admin alert sent correctly if unfilled after 30 minutes
✅ Staff can accept immediately via portal
✅ Confirmation recorded and ERP updated in < 1 minute

---

### 3.10 Settlement Reconciliation (FR-10)

**Description:** Monthly settlement verification with ERP

**Reconciliation Process:**
1. **Data Retrieval** (1st of month)
   - PHC calls ERP API: GET /api/v1/settlements/{period}
   - Fetch all settlement records for previous month
   - Include: staff_id, amount, deductions, bonuses

2. **Comparison** (by 3rd of month)
   - Compare PHC records with ERP data
   - Match on: staff_id, assignment_id, hours worked, penalties
   - Flag discrepancies where amounts differ
   - Identify missing records (in PHC but not ERP, or vice versa)

3. **Discrepancy Investigation**
   - Log all mismatches with details
   - Categorize by type:
     - Missing attendance record
     - Penalty not applied
     - Hours mismatch
     - Rate discrepancy

4. **Report Generation**
   - Create reconciliation report for finance team
   - Include: summary (total matched/unmatched), detail list of discrepancies
   - Format: Excel spreadsheet with tabs for Matched/Unmatched
   - Deliver by 3rd of month to finance

5. **Resolution**
   - Finance team reviews discrepancies
   - Updates ERP or PHC as needed
   - Confirms final settlement amounts
   - System marks discrepancies as resolved

**Metrics:**
- **Match Rate Target:** > 99% (discrepancies < 1% of total records)
- **Processing Time:** Completed by 3rd of every month
- **Accuracy:** Zero financial discrepancies after reconciliation

**Acceptance Criteria:**
✅ Settlement data fetched from ERP by 1st of month
✅ Reconciliation completed by 3rd of month
✅ All discrepancies flagged and documented
✅ Reports generated automatically
✅ Match rate > 99%
✅ Report format suitable for finance review

---

### 3.11 Manual Assignment Override (FR-11)

**Description:** Admin can manually assign staff to jobs

**Use Cases:**
- Special requests from facility
- Staff with unique qualifications needed
- Emergency situations
- Exception to scoring algorithm

**Workflow:**
1. Admin views job demand (unfilled or to override)
2. Clicks "Manual Assignment" button
3. Search for staff by:
   - Name (partial match)
   - Staff number
   - Location preference
   - Current score tier
   - Availability status
4. System shows search results with profiles
5. Select staff member
6. System shows conflict warnings if:
   - Staff already assigned to overlapping shift
   - Staff on facility blacklist
   - Staff unavailable that day
   - Staff will exceed fair sharing limits
7. Admin enters override reason (required field, minimum 20 characters)
8. Confirm assignment
9. System creates assignment (assigned_by: manual_admin)
10. WhatsApp notification sent to staff
11. Override logged in audit trail with:
    - Admin ID
    - Timestamp
    - Original matched staff (if applicable)
    - Override reason
    - Staff assigned

**Audit Trail:**
- All manual assignments recorded
- Reportable for compliance review
- Shows pattern of manual intervention (identify system issues)
- Cannot be deleted or modified after creation

**Acceptance Criteria:**
✅ Search works correctly (returns relevant, available staff)
✅ Conflict warnings displayed clearly
✅ Override logged with admin ID and full reason
✅ Audit trail complete and immutable
✅ ERP updated with manual assignment flag
✅ Staff receives standard confirmation WhatsApp
✅ Original matching algorithm's selection recorded for analysis

---

### 3.12 System Monitoring (FR-12)

**Description:** View API logs and system health

**Monitoring Dashboard:**
- **API Logs:** All ERP API calls logged with request/response
- **Sync Status Dashboard:** Show last sync time, success/failure counts
- **Error Tracking:** Failed API calls, errors by type, trends
- **Filter/Search:** Filter by date range, staff, endpoint, status
- **Request/Response Details:** View full payload for debugging

**Log Retention:**
- API logs retained for 90 days
- Critical errors trigger immediate alerts
n- Export logs to CSV for analysis

**Alerting:**
- Critical errors: Immediate email + push notification to admin
- High error rate (>10%): Alert after 1 hour
- Sync failures: Alert after 2 consecutive failures

**Metrics:**
- API response times (average, 95th percentile)
- Daily sync success rate (target: 100%)
- Assignment success rate
- Error rate trend (should be < 2%)

**Acceptance Criteria:**
✅ Logs viewable with filters and search
✅ Critical errors trigger alerts immediately
✅ 90-day retention enforced
✅ Export to CSV works correctly
✅ Dashboard shows real-time API health
✅ Sync status accurate and up-to-date

---

### 3.13 Reporting (FR-13)

**Description:** Generate management reports

**Report Types:**

1. **Settlement Reports**
   - Monthly reconciliation summary
   - Matched vs unmatched records
   - Financial discrepancies

2. **Attendance Reports**
   - Staff attendance by period
   - Fill rate by facility
   - No-show rates
   - Compare scheduled vs actual hours

3. **Penalty Reports**
   - Cancellation and no-show counts
   - Penalty amounts by staff
   - Trend analysis (improving/declining)

4. **Score Reports**
   - Staff score distribution (Gold/Silver/Bronze counts)
   - Score changes over time
   - Impact on assignment rates

**Filters:**
- Date range (customizable)
- Facility (single or multi-select)
- Staff (individual or group)
- Region/District

**Export Options:**
- Excel (.xlsx) for analysis
- PDF for management presentation
- CSV for import into other systems

**Scheduling:**
- Automated monthly reports (delivered by email to stakeholders)
- On-demand generation (instant)

**Acceptance Criteria:**
✅ All report types generate accurately
✅ Export functions work (Excel and PDF formats)
✅ Format suitable for management review and presentation
✅ Filters applied correctly to data
✅ Scheduled reports delivered on time
✅ Performance: < 5 seconds for on-demand generation

---

## 4. Data Model

### Core Data Entities

**Entity: Users (Staff, Supervisors, Admins)**
- user_id: Primary key
- phone_number: UNIQUE, login credential (8-digit HK format)
- email: UNIQUE (for staff, NULL for workers)
- password_hash: bcrypt hashed (cost factor 12)
- full_name: English or Traditional Chinese
- role: ENUM (admin, supervisor, worker)
- status: ENUM (active, inactive)
- created_at: Registration timestamp
- last_login: Last session timestamp

**Entity: Nursing Assistants (Workers)**
- worker_id: References user_id
- staff_number: UNIQUE (agency-assigned ID)
- current_score: Integer (starting at 5)
- score_tier: ENUM (gold, silver, bronze, under_review)
- preferred_facilities: JSON array of facility_ids
- availability_status: ENUM (available, on_job, unavailable)
- certificates: JSON array (type, expiry_date)

**Entity: Care Home Locations**
- location_id: Primary key
- location_code: UNIQUE (3-digit code)
- location_name: English and Traditional Chinese
- district: HK district
- address: Full address
- contact_person: Name
- contact_phone: Phone number
- qr_token: For QR code generation
- underlist: JSON array (staff_id, priority_order)
- blacklist: JSON array (staff_id, reason, date)
- shift_config: JSON object (shift_codes, start/end times)

**Entity: Job Demands / Assignments**
- demand_id: Primary key
- erp_demand_id: ERP reference
- location_id: Foreign key to locations
- assignment_date: Date of service
- shift_type: ENUM (PC8, A, B, C, D, N)
- start_time: Shift start
- end_time: Shift end
- working_hours: Calculated decimal
- positions_needed: Integer (default 1)
- positions_filled: Integer
- status: ENUM (open, assigned, confirmed, completed, cancelled, no_show)
- assigned_staff: JSON array(staff_id assignments)
- confirmation_deadline: Timestamp (2 hours from notification)

**Entity: Attendance Records**
- record_id: Primary key
- assignment_id: References job demand
- staff_id: References worker
- clock_in: Timestamp
- clock_out: Timestamp
- actual_hours: Calculated decimal
- status: ENUM (completed, partial, no_show)
- verification_method: ENUM (qr_code, supervisor, manual)

**Entity: Penalties**
- penalty_id: Primary key
- staff_id: References worker
- assignment_id: References job demand
- penalty_type: ENUM (cancellation, no_show)
- amount: Decimal (100.00 HKD)
- score_impact: Integer (-1 or -2)
- applied_at: Timestamp
- erp_sync_status: ENUM (pending, synced, failed)
- settlement_id: ERP reference (when processed)

---

## 5. Technical Architecture

### 5.1 Technology Stack (ALIGNED WITH PRD)

**Frontend:**
- React.js 18+
- TailwindCSS
- Redux Toolkit
- Recharts (metrics visualization)

**Backend:**
- Java Spring Boot 2.7+
- Spring Security (authentication/authorization)
- Spring Batch OR Quartz (job scheduling)

**Database:**
- MySQL 8+ (primary relational database)
- Redis 6+ (caching, sessions, job queues)

**Notifications:**
- WhatsApp (manual template-based, no API for MVP)
- Firebase Cloud Messaging (web push for reminders)

**Storage:**
- AWS S3 OR Azure Blob (emergency files, documents)
- Encrypted at rest (AES-256)

**Authentication:**
- JWT tokens with Spring Security
- Refresh token rotation
- bcrypt password hashing (cost factor 12)

**Hosting:**
- AWS OR Azure cloud infrastructure
- Docker containerization
- Load balancing for scalability

**Rationale:** Selected for proven reliability, team expertise, scalability to 1000+ staff, and 60-day timeline feasibility.

---

## 6. User Interface

### 6.1 Design Principles

- **Mobile-First:** Optimized for smartphone (staff) and tablet (supervisors)
- **Speed:** All page loads < 3 seconds, all actions < 1 second
- **Clarity:** Clear call-to-action buttons, minimal cognitive load
- **Transparency:** Staff can view score history and reason for each change
- **Bilingual:** English + Traditional Chinese throughout

### 6.2 Primary User Journeys

**Journey 1: Nursing Assistant Gets Assigned**
1. Coordinator sends WhatsApp message (from PHC-generated template)
2. Staff receives WhatsApp with shift details and confirmation link
3. Staff clicks link (opens PHC web portal)
4. Reviews shift details and location
5. Clicks "Confirm" button
6. Gets confirmation message and score update (+1 point)
7. Receives day-before reminder via Firebase (24h before shift)

**Journey 2: Admin Posts Emergency Job**
1. Login to PHC admin portal
2. Click "Emergency Job Posting"
3. Fill form with urgent details (1 minute)
4. Submit → job posted immediately
5. Matching runs instantly (FR-2)
6. Staff notified via WhatsApp (urgent template)
7. Dashboard shows real-time filling progress

**Journey 3: Admin Verifies Attendance (via facility contact)**
1. Login to PHC admin portal
2. Navigate to "Attendance Dashboard"
3. Filter by facility and today's date
4. Call facility contact person to confirm attendance
5. Mark each staff as Present/No-show/Late based on confirmation
6. Add notes for any deviations
7. System auto-calculates hours and syncs to ERP
8. Done (~5 minutes for 20 facilities)

---

## 7. Implementation Guidance

### 7.1 MVP Prioritization

**Phase 1: Core Automation (Must complete for 60-day launch)**

1. **Scoring Algorithm (FR-1)**
   - Implement point system and tier logic
   - Real-time ERP score sync
   - Staff portal score display

2. **Matching Engine (FR-2)**
   - Filtering logic (availability, blacklist, documents)
   - Ranking by underlist and score tier
   - < 5 minute matching SLA

3. **WhatsApp + Firebase Notifications (FR-3)**
   - Template generation system
   - Coordinator dashboard for sending
   - Firebase FCM setup for reminders

4. **Admin Dashboard (FR-4)**
   - Real-time metrics widgets
   - Auto-refresh implementation
   - Drill-down navigation

5. **ERP Integration (FR-5)**
   - 13 API endpoints (7 pull, 6 push)
   - Daily sync for staff/locations
   - Real-time sync for assignments/penalties/scores
   - Every 15-min sync for job demands

6. **Attendance Tracking (FR-6)**
   - QR code generation and validation OR
   - Supervisor verification workflow
   - Clock-in/out recording
   - Deviation detection

7. **Penalty Management (FR-7)**
   - Penalty calculation logic
   - Warning modal for late cancellations
   - ERP penalty API integration
   - Re-matching trigger

**Phase 1 Success Criteria:**
- All 7 P0 features functional
- 50 pilot staff operational
- 95% fill rate achieved
- System stable for 2 weeks
- Coordinator time reduced by 50%+

---

## 8. Traceability Matrix

### FR to User Story Coverage

| FR | Feature | Covered In | Status |
|----|---------|------------|--------|
| FR-1 | Scoring Algorithm | US-NA-02, US-NA-03, US-NA-05, US-ERP-06 | ✓ |
| FR-2 | Matching Engine | US-ERP-04, US-ADM-02 | ✓ |
| FR-3 | WhatsApp + Firebase | US-NA-01, US-NA-02, US-ADM-04, US-ADM-05 | ✓ |
| FR-4 | Admin Dashboard | US-ADM-01 | ✓ |
| FR-5 | ERP Integration | US-ERP-01 through US-ERP-06 | ✓ |
| FR-6 | Attendance Tracking | US-CS-02, US-CS-03, US-NA-05 | ✓ |
| FR-7 | Penalty Management | US-NA-03, US-NA-05, US-ERP-06 | ✓ |
| FR-8 | Emergency File Upload | US-ADM-03, US-ADM-04 | ✓ |
| FR-9 | Emergency Job Posting | US-ADM-05 | ✓ |
| FR-10 | Settlement Reconciliation | Test Cases TC-ERP-01, TC-ERP-07 | ⚠️ |
| FR-11 | Manual Override | US-ADM-02 | ✓ |
| FR-12 | System Monitoring | US-ADM-06 | ✓ |
| FR-13 | Reporting | US-ADM-06 | ⚠️ |

**Note:** FR-10 and FR-13 have minimal story coverage - recommend adding dedicated stories.

---

## 9. Non-Functional Requirements

### 9.1 Performance
- Page load time: < 3 seconds
- API response time: < 500ms (95th percentile)
- Matching completion: < 5 minutes
- Database query time: < 100ms
- Concurrent users: 200+ simultaneous

### 9.2 Scalability
- Support 500 workers in v1.0
- Scalable to 2,000 workers within 12 months
- Handle 500+ job postings per day
- 99.5% uptime target

### 9.3 Security
- TLS 1.3 for all connections
- JWT tokens with 4-hour expiration
- Password hashing with bcrypt (cost 12)
- Role-based access control (RBAC)
- Audit logging of all authentication and data modifications
- HK Personal Data (Privacy) Ordinance compliance

### 9.4 Reliability
- Daily backups (full) + hourly incremental
- RPO < 1 hour, RTO < 4 hours
- Auto-retry on ERP failures (3 attempts)
- Graceful degradation if Firebase unavailable
- WhatsApp primary ensures communication always works

---

## 10. Deployment

**Infrastructure:**
- Cloud: AWS or Azure
- Containers: Docker
- Orchestration: Kubernetes (if needed for scale)
- CDN: CloudFront or Azure CDN for static assets

**Environments:**
- Development: Feature branch testing
- Staging: Pre-production validation
- Production: Live system

**CI/CD:**
- Automated testing pipeline (unit, integration, security)
- Automated deployment to staging
- Manual approval for production deployment (first 3 months)

---

## 11. Monitoring and Support

**Monitoring:**
- Dashboard health metrics (real-time)
- API performance monitoring
- Error tracking and alerting
- Log aggregation (structured JSON)
- User activity audit trails

**Support:**
- Level 1: Phone/WhatsApp support (business hours)
- Level 2: Email support (24-hour response)
- Level 3: Critical issues (2-hour response for system down)

---

## 12. Future Enhancements (Post-MVP)

### Version 2.0 (Months 4-6)

**QR Code System:**
- **Facility Identification:** Workers scan QR code to auto-fill facility info in job applications
- **Attendance Tracking:** Workers scan QR code when arriving at shift for automated clock-in
- **Implementation:**
  - System administrator generates QR codes for all facilities
  - QR codes provided as printable PDFs (A4 size)
  - Facility displays QR code at reception area
  - Mobile app or web portal supports QR scanning
  - Validation logic ensures QR code is current and matches assignment
- **Benefits:**
  - Reduces manual data entry
  - Automated attendance verification
  - Improved accuracy of location tracking
  - Eliminates phone confirmation requirement
- **Requirements:**
  - QR code printing and display at facilities
  - Camera/scanning capability on worker devices
  - Real-time validation infrastructure
- **Estimated Timeline:** Version 2.0 (Months 4-6 post-launch)
- **Priority:** OPTIONAL - Deferred to future release

**WhatsApp Business API Integration:**
- Automated message sending (no manual copy-paste)
- Message templates pre-approved by Meta
- Delivery receipts and read receipts
- Green checkmark verification
- Estimated cost: HKD 8,000-15,000/month
- ROI: Saves 1 FTE coordinator (HKD 40K/month) → Net savings HKD 25-32K/month

**Geographic Intelligence:**
- Distance-based matching
- Staff location tracking (opt-in)
- Travel time calculations
- Optimize for minimal commute

**Predictive Analytics:**
- ML model for demand forecasting
- Predict no-show risk
- Suggest optimal staffing levels
- Pattern recognition for absenteeism

### Version 3.0 (Months 7-12)

**Native Mobile App:**
- React Native (cross-platform)
- Better UX than web portal
- Offline capability
- GPS attendance tracking
- Photo verification

**Facility Self-Service Portal:**
- Limited Phase 2 - facility portal
- Post and manage own job demands
- View assignment status
- Rate staff performance

---

## 13. Change Log

**Version 1.0 → 1.1 (2025-11-24)**
- Aligned technology stack with PRD (Spring Boot 2.7+, MySQL 8+)
- Updated notification architecture to WhatsApp + Firebase (manual templates)
- Added scoring algorithm (FR-1) with full details
- Added matching engine (FR-2) with implementation logic
- Added penalty management (FR-7) with warning workflow
- Added FR traceability matrix
- Removed all time estimates (architect compliance)
- Added rationale for all technology decisions
- Aligned terminology with PRD (nursing assistant vs worker)

**Version 1.1 → 1.2 (2025-11-25)**
- **REMOVED:** Care Home Supervisor role entirely
- **UPDATED:** FR-6 Attendance Tracking - Changed from QR/Supervisor options to Admin-based verification
- **UPDATED:** User Roles - Reduced from 5 to 4 roles (removed supervisor)
- **UPDATED:** Permission Matrix - Removed supervisor column
- **UPDATED:** User Journey 3 - Changed from supervisor verification to admin verification
- **MOVED:** QR Code System to Future Enhancements (Version 2.0+)
- **UPDATED:** Executive Summary - Removed supervisor from target users
- **UPDATED:** System Context - Removed supervisor from primary users
- **RATIONALE:** Simplifies MVP scope, reduces infrastructure requirements, centralizes control

---

**Document Status:** ✓ ALIGNED WITH PRD (v1.2 - Supervisor Removed, QR Optional)
**Architecture Approval:** ⏳ Ready for review
**Last Updated:** November 25, 2025
