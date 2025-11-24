# ERP API Integration Specification

**Document Version:** 1.0
**Date:** 2025-11-24
**Project:** Prestige Health Dispatch System (PHC)
**Integration Type:** Bi-directional ERP Synchronization

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Four Main Flows Integration](#four-main-flows-integration)
3. [Master Data Synchronization](#master-data-synchronization)
4. [API Integration Points](#api-integration-points)
5. [Trigger Points & Automation](#trigger-points--automation)
6. [Data Mapping Requirements](#data-mapping-requirements)
7. [Integration To-Do List](#integration-to-do-list)
8. [Implementation Timeline](#implementation-timeline)

---

## 🔍 Overview

### Integration Architecture
```
Prestige Health Dispatch System (PHC)
        ↕︎ Bi-directional Sync
        Existing ERP System
```

**Integration Modes:**
- **Pull (Sync from ERP):** Master data (staff, locations, etc.)
- **Push (Sync to ERP):** Transactional data (attendance, penalties, settlements)
- **Real-time:** Critical operations (penalties, availability)
- **Batch:** Non-time-sensitive data (reports, analytics)

---

## 🔄 Four Main Flows Integration

### Flow 1: Registration (開卡) - Daily ERP Sync

#### Purpose
Synchronize nursing assistant registration data, certificates, and availability from ERP system.

#### ERP API Requirements

**API 1.1: Get Registered Staff List**
```
Endpoint: GET /api/v1/staff/active
Method: GET
Trigger: Daily at 02:00 AM (or configurable)
Frequency: Daily

Request Parameters:
- date: YYYY-MM-DD (optional, defaults to today)
- status: "active" (default)
- location: "all" or specific region code

Expected Response:
{
  "status": "success",
  "data": [
    {
      "staff_id": "ERP_UNIQUE_ID",
      "name_chinese": "陳小明",
      "name_english": "Chan Siu Ming",
      "hkid": "A123456(7)",
      "contact_number": "91234567",
      "whatsapp_number": "91234567",
      "email": "chan@email.com",
      "registration_date": "2024-01-15",
      "status": "active",
      "preferred_regions": ["HKI", "KLN", "NT"],
      "certificates": [
        {
          "type": "health_worker_certificate",
          "issue_date": "2024-01-15",
          "expiry_date": "2025-01-14",
          "document_url": "https://erp.docs/..."
        },
        {
          "type": "health_check",
          "issue_date": "2024-03-01",
          "expiry_date": "2025-02-28",
          "document_url": "https://erp.docs/..."
        }
      ],
      "bank_account": {
        "bank_code": "004",
        "account_number": "1234567890",
        "account_name": "CHAN SIU MING"
      }
    }
  ],
  "pagination": {
    "total": 150,
    "page": 1,
    "per_page": 100,
    "total_pages": 2
  }
}
```

**API 1.2: Get Staff Availability**
```
Endpoint: GET /api/v1/staff/availability
Method: GET
Trigger: Daily at 02:00 AM (after staff sync)
Frequency: Daily

Request Parameters:
- start_date: YYYY-MM-DD (next 7 days)
- end_date: YYYY-MM-DD

Expected Response:
{
  "status": "success",
  "data": [
    {
      "staff_id": "ERP_UNIQUE_ID",
      "availability": [
        {
          "date": "2025-11-25",
          "available": true,
          "preferred_shift": "morning"
        },
        {
          "date": "2025-11-26",
          "available": false,
          "reason": "AL"
        }
      ]
    }
  ]
}
```

**API 1.3: Sync Staff Certificates/Documents**
```
Endpoint: GET /api/v1/staff/{staff_id}/documents
Method: GET
Trigger: On-demand or weekly sync
Frequency: Weekly or when document expiry warning triggered

Expected Response:
{
  "status": "success",
  "staff_id": "ERP_UNIQUE_ID",
  "documents": [
    {
      "document_id": "DOC001",
      "document_type": "health_worker_certificate",
      "issue_date": "2024-01-15",
      "expiry_date": "2025-01-14",
      "status": "valid",
      "file_url": "https://erp.docs/...",
      "last_updated": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Data Flow: ERP → PHC System
```
Daily Sync Job (02:00 AM)
    ↓
Call API 1.1 → Get all active staff
    ↓
For each staff → Store in PHC database
    ↓
Call API 1.2 → Get availability for next 7 days
    ↓
Update availability matrix
    ↓
Validate certificates against expiry rules
    ↓
Mark staff as "document valid/invalid"
```

#### Error Handling
- **API Unavailable:** Retry 3 times with exponential backoff, then alert admin
- **Partial Data Failure:** Log failed records, continue with others
- **Data Validation Errors:** Flag invalid records for manual review
- **Duplicate Staff:** Match by ERP staff_id, update existing records

---

### Flow 2: Job Posting (出Post) - Location & Demand Sync

#### Purpose
Get job locations, care home requirements, and post job demands from ERP system.

#### ERP API Requirements

**API 2.1: Get Job Locations (Care Homes)**
```
Endpoint: GET /api/v1/locations/active
Method: GET
Trigger: Weekly sync or on-demand
Frequency: Daily at 03:00 AM

Request Parameters:
- status: "active" (default)
- region: "all" or specific region code

Expected Response:
{
  "status": "success",
  "data": [
    {
      "location_id": "LOC001",
      "location_code": "CH_HKI_001",
      "name_chinese": "香港護老院",
      "name_english": "Hong Kong Care Home",
      "address": "123 King's Road, Hong Kong",
      "region": "HKI",
      "district": "Eastern",
      "contact_person": "Ms. Wong",
      "contact_number": "21234567",
      "email": "info@hkcarehome.com",
      "service_type": "elderly_care",
      "status": "active",
      "special_requirements": ["dementia_experience", "cantonese_speaking"],
      "preferred_staff": ["ERP_STAFF_ID_1", "ERP_STAFF_ID_2"],
      "blacklisted_staff": ["ERP_STAFF_ID_3"]
    }
  ]
}
```

**API 2.2: Get Posted Job Demands**
```
Endpoint: GET /api/v1/jobs/demands
Method: GET
Trigger: Real-time (every 15 minutes) or webhook from ERP
Frequency: Every 15 minutes (configurable)

Request Parameters:
- status: "open" (only get unfilled demands)
- date_from: YYYY-MM-DD
- date_to: YYYY-MM-DD
- urgency: "normal" or "urgent"

Expected Response:
{
  "status": "success",
  "data": [
    {
      "demand_id": "DEM001",
      "location_id": "LOC001",
      "location_name": "Hong Kong Care Home",
      "required_date": "2025-11-25",
      "required_time": {
        "start": "08:00",
        "end": "20:00"
      },
      "shift_type": "morning",
      "required_staff_count": 3,
      "assigned_staff_count": 1,
      "status": "open",
      "priority": "normal",
      "special_requirements": ["dementia_experience"],
      "posting_date": "2025-11-20",
      "contact_person_on_duty": "Ms. Wong",
      "contact_number_duty": "21234567"
    }
  ]
}
```

**API 2.3: Get Location Preferences**
```
Endpoint: GET /api/v1/locations/{location_id}/preferences
Method: GET
Trigger: On new location sync or weekly update
Frequency: Weekly

Expected Response:
{
  "status": "success",
  "location_id": "LOC001",
  "preferences": {
    "underlist_staff": [
      {"staff_id": "ERP001", "priority": 1},
      {"staff_id": "ERP002", "priority": 2}
    ],
    "blacklisted_staff": ["ERP003", "ERP004"],
    "required_certificates": ["health_worker_certificate", "dementia_care"],
    "preferred_shift_times": ["morning", "afternoon"],
    "auto_accept": false,
    "notification_method": "whatsapp"
  }
}
```

#### Data Flow: ERP → PHC System
```
Location Sync (03:00 AM daily)
    ↓
Call API 2.1 → Get all active locations
    ↓
Store/update location master data
    ↓
For each location → Call API 2.3 → Get preferences
    ↓
Update underlist/blacklist in PHC
    ↓

Job Demand Sync (Every 15 minutes)
    ↓
Call API 2.2 → Get open job demands
    ↓
Filter demands by status (open/unfilled)
    ↓
Create job postings in PHC system
    ↓
Trigger matching algorithm
```

#### Webhook Alternative (Recommended)
```
ERP System (when new demand posted)
    ↓
Webhook POST to PHC: /webhook/erp/job-demand
    ↓
PHC validates and processes immediately
    ↓
Real-time matching triggered
```

#### Error Handling
- **Webhook Failure:** Fall back to polling every 15 minutes
- **Location Not Found:** Create placeholder, flag for review
- **Invalid Requirements:** Log and skip, alert admin
- **Duplicate Demands:** Match by demand_id, update if changed

---

### Flow 3: Matching & Confirmation - Real-time API Integration

#### Purpose
Update ERP system with matched staff assignments and handle confirmations.

#### ERP API Requirements

**API 3.1: Submit Staff Assignment**
```
Endpoint: POST /api/v1/jobs/assignments
Method: POST
Trigger: When matching algorithm selects staff
Frequency: Real-time (as matches occur)

Request Body:
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

Expected Response (Success):
{
  "status": "success",
  "message": "Assignment submitted successfully",
  "assignment_id": "ERP_ASSIGNMENT_ID"
}

Expected Response (Error - Staff Unavailable):
{
  "status": "error",
  "error_code": "STAFF_UNAVAILABLE",
  "message": "Staff has been assigned to another job"
}
```

**API 3.2: Update Assignment Status**
```
Endpoint: PATCH /api/v1/jobs/assignments/{assignment_id}
Method: PATCH
Trigger: When staff confirms/cancels assignment
Frequency: Real-time

Request Body (Staff Confirmed):
{
  "status": "confirmed",
  "confirmed_timestamp": "2025-11-20T16:00:00Z",
  "confirmation_method": "whatsapp"
}

Request Body (Staff Cancelled):
{
  "status": "cancelled",
  "cancelled_timestamp": "2025-11-20T16:00:00Z",
  "reason": "AL",
  "penalty_applied": true,
  "penalty_amount": 100
}

Expected Response:
{
  "status": "success",
  "message": "Assignment status updated"
}
```

**API 3.3: Get Assignment Status (for sync verification)**
```
Endpoint: GET /api/v1/jobs/assignments/{assignment_id}
Method: GET
Trigger: Periodic verification or reconciliation
Frequency: Every 1 hour

Expected Response:
{
  "status": "success",
  "data": {
    "assignment_id": "ERP_ASSIGNMENT_ID",
    "demand_id": "ERP_DEMAND_ID",
    "staff_id": "ERP_STAFF_ID",
    "status": "confirmed",
    "confirmed_timestamp": "2025-11-20T16:00:00Z"
  }
}
```

#### Data Flow: PHC → ERP System

```
Matching Algorithm Selects Staff
    ↓
PHC creates internal assignment record
    ↓
Call API 3.1 → Submit assignment to ERP
    ↓
ERP validates staff availability
    ↓
If success:
    └─→ Store ERP assignment_id in PHC
    └─→ Send WhatsApp notification to staff
    └─→ Update PHC status to "pending_confirmation"
    ↓
If error (staff unavailable):
    └─→ Remove from PHC
    └─→ Trigger re-matching with next candidate
    ↓
Staff confirms via WhatsApp
    ↓
PHC updates internal status
    ↓
Call API 3.2 → Update ERP status to "confirmed"
    ↓
Sync complete
```

#### Cancellation Flow (with Penalty)

```
Staff requests cancellation
    ↓
PHC shows warning: "100HKD will be deducted when you apply AL within 48 hours before coming job!"
    ↓
Staff accepts cancellation
    ↓
PHC applies: -1 score, -100 HKD
    ↓
Call API 3.2 → Update ERP status to "cancelled"
    ↓
Trigger API to ERP for financial deduction (TBD endpoint)
    ↓
Update PHC assignment status
    ↓
Trigger re-matching for vacant position
```

#### Error Handling
- **Assignment Conflict:** If ERP returns "staff unavailable", immediately re-match
- **API Timeout:** Retry with exponential backoff (3 attempts)
- **Status Sync Failure:** Queue for retry, alert admin if persists > 1 hour
- **Duplicate Assignments:** ERP should reject, PHC should validate before sending

---

### Flow 4: Completion & Settlement - Attendance & Financial Integration

#### Purpose
Sync attendance records, calculate payments, apply penalties, and process settlements.

#### ERP API Requirements

**API 4.1: Submit Attendance Record**
```
Endpoint: POST /api/v1/attendance
Method: POST
Trigger: When staff clocks in/out OR shift completed
Frequency: Real-time or end-of-shift batch

Request Body:
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
  "verified_by": "location_supervisor",
  "verification_method": "qr_code_scan"
}

Expected Response:
{
  "status": "success",
  "attendance_id": "ERP_ATTENDANCE_ID",
  "payment_calculated": 1800.00,
  "penalty_applied": 0
}
```

**API 4.2: Submit Penalty Record (Scoring & Financial)**
```
Endpoint: POST /api/v1/penalties
Method: POST
Trigger: When cancellation/no-show penalty applied
Frequency: Real-time

Request Body (Cancellation):
{
  "penalty_id": "PHC_GENERATED_ID",
  "staff_id": "ERP_STAFF_ID",
  "assignment_id": "ERP_ASSIGNMENT_ID",
  "penalty_type": "cancellation",
  "penalty_amount": 100.00,
  "currency": "HKD",
  "reason": "Cancelled within 48 hours",
  "applied_timestamp": "2025-11-20T16:00:00Z",
  "deduct_from_payment": true,
  "score_impact": -1
}

Request Body (No-show):
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

Expected Response:
{
  "status": "success",
  "penalty_id": "ERP_PENALTY_ID",
  "payment_adjusted": true,
  "adjusted_amount": 100.00
}
```

**API 4.3: Get Settlement/Payment Status**
```
Endpoint: GET /api/v1/settlements/{staff_id}
Method: GET
Trigger: When staff queries payment OR monthly reconciliation
Frequency: On-demand or monthly batch

Request Parameters:
- staff_id: ERP_STAFF_ID
- period: "2025-11" (YYYY-MM format)

Expected Response:
{
  "status": "success",
  "staff_id": "ERP_STAFF_ID",
  "period": "2025-11",
  "settlements": [
    {
      "settlement_id": "STL001",
      "total_shifts": 15,
      "total_hours": 180.5,
      "gross_payment": 27075.00,
      "penalties_total": 200.00,
      "net_payment": 26875.00,
      "payment_status": "pending",
      "payment_date": "2025-12-05",
      "bank_account": {
        "bank_code": "004",
        "account_number": "1234567890"
      }
    }
  ]
}
```

**API 4.4: Update Staff Score in ERP**
```
Endpoint: PATCH /api/v1/staff/{staff_id}/score
Method: PATCH
Trigger: When score changes
Frequency: Real-time or daily batch

Request Body:
{
  "score_change": -1,
  "reason": "shift_cancellation",
  "assignment_id": "ERP_ASSIGNMENT_ID",
  "current_score": 15
}

Expected Response:
{
  "status": "success",
  "staff_id": "ERP_STAFF_ID",
  "new_score": 15,
  "message": "Score updated successfully"
}
```

#### Data Flow: PHC ↔ ERP System

**4A: Successful Completion Flow**
```
Staff completes shift
    ↓
Supervisor verifies attendance (QR code)
    ↓
PHC creates attendance record
    ↓
Call API 4.1 → Submit attendance to ERP
    ↓
ERP calculates payment (hourly rate × actual hours)
    ↓
Store ERP payment calculation in PHC
    ↓
Update staff score: +1 point (attended)
    ↓
Call API 4.4 → Update ERP staff score
    ↓
Attendance sync complete
```

**4B: Cancellation Flow with Penalties (as specified)**
```
Staff cancels shift (with notice)
    ↓
PHC shows warning: "100HKD will be deducted when you apply AL within 48 hours before coming job!"
    ↓
Staff accepts
    ↓
Apply penalty in PHC: -1 score, -100 HKD
    ↓
Call API 4.2 → Submit penalty record to ERP
    ↓
Call API 4.4 → Update staff score in ERP
    ↓
Trigger ERP payment deduction (API to be determined)
    ↓
Update assignment status
    ↓
Penalty processing complete
```

**4C: No-Show Flow**
```
Shift end time passes
    ↓
Staff didn't attend and didn't cancel
    ↓
Supervisor marks as "absent" in PHC
    ↓
Apply penalty: -2 score, -100 HKD
    ↓
Call API 4.2 → Submit no-show penalty to ERP
    ↓
Call API 4.4 → Update staff score in ERP
    ↓
Trigger automatic ERP deduction
    ↓
Notify staff: "You were marked absent. 100 HKD penalty applied."
```

**4D: Monthly Settlement Flow**
```
End of month (e.g., last day of November)
    ↓
PHC aggregates all completed shifts
    ↓
For each staff → Call API 4.3 → Get settlement status from ERP
    ↓
Verify PHC records match ERP calculations
    ↓
Generate settlement report
    ↓
Send to finance for payment processing
    ↓
Settlement complete
```

#### Financial Reconciliation

```
ERP calculates: Gross payment - Penalties = Net payment
    ↓
PHC verifies calculation accuracy
    ↓
If mismatch detected:
    └─→ Flag for manual review
    └─→ Alert finance team
    └─→ Sync correction
    ↓
Generate payment instruction
    ↓
Send to bank for transfer
```

#### Error Handling
- **Attendance Record Conflict:** ERP duplicate detection, use assignment_id as unique key
- **Penalty Calculation Error:** Log dispute, finance team reviews manually
- **Payment Status Sync Failure:** Retry every hour for 24 hours, then alert
- **Score Update Failure:** Queue for retry, alert admin if persists

---

## 🏗️ Master Data Synchronization

### Master Data Objects from ERP

#### 1. Staff Master Data
**Synchronization:** Daily at 02:00 AM
**Source:** API 1.1, 1.2, 1.3
**Fields:**
- ERP staff_id (unique identifier)
- Personal details (name, contact, HKID)
- Certificates with expiry dates
- Bank account details
- Status (active/inactive)
- Preferred regions

**Validation Rules:**
- HKID format validation
- Contact number format
- Certificate expiry check (alert if < 30 days)
- Duplicate detection by staff_id

#### 2. Location Master Data
**Synchronization:** Daily at 03:00 AM
**Source:** API 2.1, 2.3
**Fields:**
- ERP location_id (unique)
- Name, address, contact details
- Region and district
- Service type
- Special requirements
- Underlist staff (priority list)
- Blacklisted staff

**Validation Rules:**
- Unique location_id
- Required contact information
- Region code validation
- Duplicate name check

#### 3. Demand/Job Posting Data
**Synchronization:** Every 15 minutes (or webhook)
**Source:** API 2.2
**Fields:**
- ERP demand_id (unique)
- Location reference
- Date and shift times
- Required staff count
- Assigned count
- Status (open/filled/cancelled)
- Special requirements
- Priority level

**Validation Rules:**
- Date must be in future
- Required count > 0
- Valid location_id
- Shift time logic (start < end)

#### 4. Payment Rates & Rules
**Synchronization:** Monthly or when changed
**Source:** API to be defined
**Fields:**
- Staff tier/rate level
- Hourly rate by shift type
- Overtime rates
- Holiday rates
- Peak period bonuses

---

## 🔌 API Integration Points Summary

### Pull APIs (ERP → PHC)

| API ID | Endpoint | Purpose | Frequency | Priority |
|--------|----------|---------|-----------|----------|
| 1.1 | GET /api/v1/staff/active | Get registered staff | Daily 02:00 | Critical |
| 1.2 | GET /api/v1/staff/availability | Get staff availability | Daily 02:00 | High |
| 1.3 | GET /api/v1/staff/{id}/documents | Get staff certificates | Weekly | High |
| 2.1 | GET /api/v1/locations/active | Get job locations | Daily 03:00 | Critical |
| 2.2 | GET /api/v1/jobs/demands | Get job postings | Every 15 min | Critical |
| 2.3 | GET /api/v1/locations/{id}/preferences | Get location prefs | Daily 03:00 | High |
| 4.3 | GET /api/v1/settlements/{id} | Get payment status | Monthly | Medium |

### Push APIs (PHC → ERP)

| API ID | Endpoint | Purpose | Trigger | Priority |
|--------|----------|---------|---------|----------|
| 3.1 | POST /api/v1/jobs/assignments | Submit assignment | When matched | Critical |
| 3.2 | PATCH /api/v1/jobs/assignments/{id} | Update status | Confirmation/cancellation | Critical |
| 4.1 | POST /api/v1/attendance | Submit attendance | Shift complete | High |
| 4.2 | POST /api/v1/penalties | Submit penalty | Cancellation/no-show | High |
| 4.4 | PATCH /api/v1/staff/{id}/score | Update score | Score change | Medium |
| **TBD** | POST /api/v1/finance/deduction | Process deduction | Penalty applied | Critical |

### Webhook Alternative (Optional but Recommended)

**ERP → PHC Webhooks:**
```
Endpoint: POST /webhook/erp/job-demand
Trigger: When new demand posted in ERP
Priority: Critical

Payload:
{
  "event": "job_demand_created",
  "timestamp": "2025-11-20T10:00:00Z",
  "data": {
    "demand_id": "DEM001",
    "location_id": "LOC001",
    "required_date": "2025-11-25",
    // ... full job demand details
  }
}
```

---

## ⏱️ Trigger Points & Automation

### Automated Jobs Schedule

```
02:00 AM - Staff Sync Job
    ├─→ API 1.1 (Get staff list)
    ├─→ API 1.2 (Get availability)
    └─→ Validate certificates

03:00 AM - Location Sync Job
    ├─→ API 2.1 (Get locations)
    └─→ API 2.3 (Get preferences)

Every 15 minutes - Demand Sync Job
    └─→ API 2.2 (Get job demands)
    └─→ Process new demands

Hourly - Assignment Status Verification
    └─→ API 3.3 (Verify assignment status)
    └─→ Reconcile any discrepancies

End of Shift - Attendance Submission
    └─→ API 4.1 (Submit attendance)
    └─→ API 4.4 (Update score)

Real-time - When Penalty Applied
    └─→ API 4.2 (Submit penalty)
    └─→ API 4.4 (Update score)
    └─→ TBD (Financial deduction)

Monthly (1st of month) - Settlement Reconciliation
    └─→ API 4.3 (Get settlement status)
    └─→ Generate reports
```

### Real-Time Triggers

1. **Matching Algorithm Selects Staff**
   - Immediately call API 3.1
   - No delay, blocking call

2. **Staff Confirms Assignment**
   - Immediately call API 3.2 (status: confirmed)
   - Trigger WhatsApp notification

3. **Staff Cancels Assignment**
   - Show warning → User accepts
   - Immediately call API 3.2 (status: cancelled)
   - Call API 4.2 (penalty) and API 4.4 (score)

4. **Staff No-Show**
   - Supervisor marks absent
   - Immediately call API 4.2 (no-show penalty)
   - Call API 4.4 (score update)
   - Re-trigger matching

5. **Staff Clocks In/Out**
   - Real-time or batch (end of shift)
   - Submit via API 4.1

---

## 🗺️ Data Mapping Requirements

### Staff Data Mapping (ERP → PHC)

| ERP Field | PHC Field | Type | Validation | Required |
|-----------|-----------|------|------------|----------|
| staff_id | erp_staff_id | String | Unique | Yes |
| name_chinese | name_zh | String | Max 100 chars | Yes |
| name_english | name_en | String | Max 100 chars | Yes |
| hkid | hkid | String | Regex pattern | Yes |
| contact_number | phone | String | 8 digits | Yes |
| whatsapp_number | whatsapp | String | 8 digits | Yes |
| email | email | String | Email format | No |
| registration_date | joined_date | Date | YYYY-MM-DD | Yes |
| status | status | Enum | active/inactive | Yes |
| certificates | documents | Array | Validate expiry | Yes |
| bank_account.bank_code | bank_code | String | 3 digits | Yes |
| bank_account.account_number | bank_account | String | Max 20 chars | Yes |

### Location Data Mapping (ERP → PHC)

| ERP Field | PHC Field | Type | Validation | Required |
|-----------|-----------|------|------------|----------|
| location_id | erp_location_id | String | Unique | Yes |
| location_code | location_code | String | Max 20 chars | Yes |
| name_chinese | name_zh | String | Max 200 chars | Yes |
| name_english | name_en | String | Max 200 chars | Yes |
| address | address | String | Max 500 chars | Yes |
| region | region | Enum | HKI/KLN/NT | Yes |
| district | district | String | Max 50 chars | Yes |
| contact_person | contact_name | String | Max 100 chars | Yes |
| contact_number | contact_phone | String | 8 digits | Yes |
| service_type | service_type | Enum | elderly_care/etc | Yes |
| special_requirements | requirements | Array | Certificate codes | No |
| preferred_staff | underlist | Array | Staff IDs | No |
| blacklisted_staff | blacklist | Array | Staff IDs | No |

### Assignment Data Mapping (PHC → ERP)

| PHC Field | ERP Field | Type | Notes |
|-----------|-----------|------|-------|
| phc_assignment_id | external_reference | String | For tracking |
| erp_demand_id | demand_id | String | Link to job demand |
| erp_staff_id | staff_id | String | Who is assigned |
| erp_location_id | location_id | String | Where |
| date | assignment_date | Date | Shift date |
| shift_start | shift_start | Time | HH:MM format |
| shift_end | shift_end | Time | HH:MM format |
| status | status | Enum | pending/confirmed/cancelled |
| assigned_timestamp | assigned_timestamp | DateTime | ISO 8601 |

### Attendance Data Mapping (PHC → ERP)

| PHC Field | ERP Field | Type | Notes |
|-----------|-----------|------|-------|
| phc_attendance_id | external_reference | String | For tracking |
| erp_assignment_id | assignment_id | String | Link to assignment |
| erp_staff_id | staff_id | String | Who attended |
| clock_in_actual | clock_in_time | DateTime | ISO 8601 |
| clock_out_actual | clock_out_time | DateTime | ISO 8601 |
| actual_hours | actual_hours | Decimal | Calculated |
| status | status | Enum | completed/partial/no_show |
| verified_by | verified_by | String | Supervisor name |

---

## ✅ Integration To-Do List

### Phase 1: Core Integration (Critical Path)

#### API Specification & Design
- [ ] **Document ERP API endpoints** - Get complete API documentation from ERP team
- [ ] **Define authentication method** - OAuth 2.0, API keys, or basic auth
- [ ] **Specify rate limits** - Max requests per minute/hour
- [ ] **Define error codes** - Standardize error handling across all APIs
- [ ] **Create API test environment** - Sandbox for development testing

#### Master Data Sync Implementation
- [ ] **Implement Staff Sync Job (API 1.1)** - Daily 02:00 pull
- [ ] **Implement Availability Sync (API 1.2)** - Daily staff availability
- [ ] **Implement Certificate Sync (API 1.3)** - Weekly document sync
- [ ] **Implement Location Sync (API 2.1)** - Daily 03:00 location pull
- [ ] **Implement Preference Sync (API 2.3)** - Daily location preferences
- [ ] **Build data validation layer** - Validate all incoming data
- [ ] **Create duplicate detection logic** - Match existing records
- [ ] **Implement error logging & alerts** - Notify admins of sync failures

#### Job Demand Integration
- [ ] **Implement Demand Polling (API 2.2)** - Every 15 minutes
- [ ] **Set up webhook endpoint** - POST /webhook/erp/job-demand
- [ ] **Configure webhook in ERP** - Register PHC endpoint
- [ ] **Implement webhook validation** - Verify webhook authenticity
- [ ] **Create fallback mechanism** - If webhook fails, use polling

#### Assignment Management
- [ ] **Implement Assignment Submit (API 3.1)** - Real-time matching
- [ ] **Implement Status Update (API 3.2)** - Confirm/cancel updates
- [ ] **Build reconciliation job** - Hourly verification (API 3.3)
- [ ] **Handle assignment conflicts** - Re-matching when ERP rejects

### Phase 2: Attendance & Settlement (High Priority)

#### Attendance Tracking
- [ ] **Implement Attendance Submit (API 4.1)** - Shift completion
- [ ] **Build clock-in/out interface** - QR code or manual entry
- [ ] **Implement attendance verification** - Supervisor confirmation
- [ ] **Create attendance discrepancy handling** - When PHC vs ERP differ

#### Penalty Management
- [ ] **Implement Penalty Submit (API 4.2)** - Cancellation/no-show
- [ ] **Build penalty calculation engine** - -100 HKD, -1 or -2 score
- [ ] **Create warning message UI** - "100HKD will be deducted..."
- [ ] **Implement penalty dispute process** - Staff can appeal
- [ ] **Create manual override** - Admin can waive penalties

#### Score Management
- [ ] **Implement Score Update (API 4.4)** - Real-time score sync
- [ ] **Build score history tracking** - Log all score changes
- [ ] **Create score recovery mechanism** - Time decay rules
- [ ] **Implement tier calculation** - Gold/Silver/Bronze status

#### Financial Integration
- [ ] **Define Financial Deduction API** - ERP API for -100 HKD (TBD)
- [ ] **Implement deduction trigger** - When penalty applied
- [ ] **Build payment reconciliation** - Monthly settlement (API 4.3)
- [ ] **Create settlement reports** - For finance team

### Phase 3: Automation & Monitoring

#### Automated Jobs
- [ ] **Set up cron jobs** - For all scheduled sync tasks
- [ ] **Implement retry logic** - Exponential backoff (3 attempts)
- [ ] **Create job monitoring dashboard** - View all sync statuses
- [ ] **Build failure notification system** - Email/Slack alerts

#### Data Quality & Governance
- [ ] **Implement data validation rules** - For all incoming/outgoing data
- [ ] **Create data quality reports** - Weekly master data health check
- [ ] **Build data correction workflows** - For admin to fix sync errors
- [ ] **Implement audit logging** - Track all API calls and changes

#### Testing & Validation
- [ ] **Create API test suite** - Automated tests for each endpoint
- [ ] **Perform integration testing** - End-to-end flow testing
- [ ] **Conduct load testing** - Simulate high volume (1000+ staff)
- [ ] **Implement health check endpoints** - Monitor API availability

### Phase 4: Enhancement & Optimization

#### Performance Optimization
- [ ] **Implement API caching** - Cache master data (1-hour TTL)
- [ ] **Optimize sync queries** - Only fetch changed records
- [ ] **Implement bulk operations** - Batch multiple records
- [ ] **Set up CDN for documents** - Certificate files

#### Analytics & Reporting
- [ ] **Build sync performance metrics** - Track API response times
- [ ] **Create integration dashboard** - Real-time sync status
- [ ] **Implement error trend analysis** - Identify common failures
- [ ] **Build capacity planning reports** - Predict future load

#### Advanced Features
- [ ] **Implement real-time sync** - WebSockets for instant updates
- [ ] **Build conflict resolution** - When data diverges
- [ ] **Create data archiving** - Archive old sync logs
- [ ] **Implement encryption** - Secure sensitive data (HKID, bank accounts)

---

## 📅 Implementation Timeline

**Phase 1: Core Integration (Weeks 1-4)**
- Week 1: API documentation & authentication setup
- Week 2: Master data sync (staff & locations)
- Week 3: Job demand integration (polling + webhook)
- Week 4: Assignment management & testing

**Phase 2: Attendance & Settlement (Weeks 5-8)**
- Week 5: Attendance submission & verification
- Week 6: Penalty management (cancellation/no-show)
- Week 7: Score tracking & financial integration
- Week 8: Settlement reconciliation

**Phase 3: Automation & Monitoring (Weeks 9-10)**
- Week 9: Automated jobs & retry logic
- Week 10: Monitoring dashboard & alerting

**Phase 4: Optimization (Weeks 11-12)**
- Week 11: Performance optimization & caching
- Week 12: Analytics, reporting & documentation

**Total Estimated Timeline: 12 weeks (3 months)**

---

## 🔐 Security Requirements

1. **Authentication:** All APIs must use secure authentication (OAuth 2.0 recommended)
2. **Encryption:** Sensitive data (HKID, bank accounts) encrypted at rest and in transit
3. **API Keys:** Rotate API keys every 90 days
4. **IP Whitelisting:** Restrict API access to known IP ranges
5. **Audit Logs:** Log all API access for compliance
6. **Rate Limiting:** Prevent API abuse with request throttling
7. **Data Masking:** Mask sensitive data in logs and reports

---

## 📞 ERP Team Coordination Checklist

Before development starts:

- [ ] **Schedule kickoff meeting** with ERP team
- [ ] **Get API documentation** (Swagger/OpenAPI preferred)
- [ ] **Access to test/sandbox environment**
- [ ] **Test API credentials** (API keys, OAuth tokens)
- [ ] **Confirm rate limits** (requests per minute/hour)
- [ ] **Define SLA** (API response time targets)
- [ ] **Escalation contacts** (technical & business)
- [ ] **Establish communication channel** (Slack/Teams)
- [ ] **Schedule weekly sync meetings** during implementation

---

## 📝 Assumptions & Dependencies

**Assumptions:**
1. ERP system has RESTful API capability
2. API response time < 3 seconds (average)
3. ERP system uptime > 99%
4. Webhook capability available
5. API versioning in place (e.g., /api/v1/)

**Dependencies:**
1. ERP team provides API documentation
2. Test environment available before development
3. API credentials provisioned
4. Network connectivity between systems
5. VPN or secure connection (if required)

---

## 🤔 Open Questions for ERP Team

1. **API Authentication:** What authentication method is supported?
2. **Rate Limits:** What are the API call limits?
3. **Webhook:** Can ERP send webhooks to PHC?
4. **API Versioning:** How is API versioning handled?
5. **Error Codes:** Standard error code documentation?
6. **Testing:** Load testing environment available?
7. **Support:** Technical support during implementation?

---

**Next Steps:**
1. Review this specification with ERP team
2. Get API documentation and test credentials
3. Prioritize Phase 1 implementation
4. Schedule weekly sync meetings
5. Start with master data sync (API 1.1, 2.1)

**Document Owner:** BMAD Analyst (Mary)
**Review Date:** To be scheduled with stakeholders
