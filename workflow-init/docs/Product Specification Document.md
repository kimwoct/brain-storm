## Healthcare Worker Matching System (配對系統)
### Prestige Health Care Agency Ltd

**Document Version:** 1.0  
**Date:** November 24, 2025  
**Project Manager:** [Name]  
**System Analyst:** [Name]  
**Status:** Draft for Client Approval

---

## Document Control

| Version | Date       | Author        | Changes                      |
|---------|------------|---------------|------------------------------|
| 1.0     | 2025-11-24 | System Analyst| Initial draft for client review |

---

## Executive Summary

This document specifies the functional and technical requirements for the Healthcare Worker Matching System (配對系統), a web-based platform designed to streamline job posting, worker assignment, and facility coordination for Prestige Health Care Agency Ltd.

**Project Objectives:**

- Reduce manual data entry time by 60-70% through automation
- Enable staff to handle 2-3x current order volume without additional headcount
- Improve job posting speed from 5-10 minutes to under 2 minutes per post
- Create scalable foundation for future facility self-service portal
- Integrate seamlessly with existing ERP system

**Target Users:**

1. Agency Staff (Primary Phase 1 users) - Job posting and worker management
2. Healthcare Workers (Phase 1) - Job browsing and application
3. Facility Administrators (Phase 2) - Self-service job posting

---

## Table of Contents

1. System Overview
2. User Roles and Permissions
3. Functional Requirements
4. Technical Architecture
5. Data Model and Integration
6. User Interface Specifications
7. Wireframes and Screen Flows
8. Non-Functional Requirements
9. Implementation Plan
10. Testing Strategy
11. Training and Support
12. Assumptions and Constraints
13. Approval and Sign-Off

---

## 1. System Overview

### 1.1 System Purpose

The Healthcare Worker Matching System is a web-based platform that automates the process of matching healthcare workers with care facility job openings. The system replaces manual WhatsApp-based coordination with a structured digital workflow.

### 1.2 System Context

**System Context Diagram**

- **External Systems:** Existing ERP System (Primary data source)
- **Primary Users:** Agency Staff, Healthcare Workers
- **Future Integration:** Facility Portal (Phase 2)

### 1.3 System Boundaries

**In Scope:**

- Staff interface for job posting and worker assignment
- Worker mobile interface for job browsing and applications
- ERP integration for job data synchronization
- User authentication and authorization
- Job matching logic based on preferences and availability
- Notification system (SMS/Email/Push)
- Basic reporting and analytics

**Out of Scope (Phase 1):**

- Facility self-service portal
- Payment processing and commission calculation
- Worker rating and performance management
- Advanced analytics and business intelligence
- Mobile native applications (iOS/Android)

---

## 2. User Roles and Permissions

### 2.1 User Role Definitions

| Role | Description | Key Permissions |
|------|-------------|-----------------|
| System Administrator | Full system access, configuration management | All permissions, user management, system settings |
| Agency Staff | Daily operations, job posting, worker assignment | Create/edit/delete jobs, assign workers, view all data |
| Healthcare Worker | Browse jobs, submit applications, view assignments | View available jobs, apply for jobs, view own profile |
| Facility Admin (Phase 2) | Self-service job posting | Create job posts, view own facility data |

### 2.2 Permission Matrix

| Function | Admin | Staff | Worker | Facility |
|----------|-------|-------|--------|----------|
| View Dashboard | ✓ | ✓ | ✓ | ✓ |
| Create Job Post | ✓ | ✓ | ✗ | ✓ (Phase 2) |
| Edit Job Post | ✓ | ✓ | ✗ | ✓ (own only) |
| Delete Job Post | ✓ | ✓ | ✗ | ✗ |
| Assign Worker | ✓ | ✓ | ✗ | ✗ |
| Apply for Job | ✗ | ✗ | ✓ | ✗ |
| View All Workers | ✓ | ✓ | ✗ | ✗ |
| Edit Worker Profile | ✓ | ✓ | ✓ (own only) | ✗ |
| Generate Reports | ✓ | ✓ | ✗ | ✓ (own data) |
| System Configuration | ✓ | ✗ | ✗ | ✗ |

---

## 3. Functional Requirements

### 3.1 User Authentication (FR-AUTH)

**FR-AUTH-001: Worker Login**

- **Description:** Healthcare workers log in using phone number and password
- **Rationale:** Most accessible credential for workers who may not have email
- **Acceptance Criteria:**
  1. System accepts 8-digit Hong Kong phone numbers (no country code required)
  2. Password must be minimum 6 characters
  3. System remembers device for 30 days (optional)
  4. "Forgot Password" sends SMS verification code
  5. Maximum 5 failed login attempts before 15-minute lockout
- **Priority:** MUST HAVE

**FR-AUTH-002: Staff Login**

- **Description:** Agency staff log in using email and password
- **Acceptance Criteria:**
  1. Email validation follows RFC 5322 standard
  2. Password complexity: 8+ characters, 1 uppercase, 1 number
  3. Session timeout after 4 hours of inactivity
  4. Audit log records all login attempts
- **Priority:** MUST HAVE

**FR-AUTH-003: Phone Number Updates**

- **Description:** Workers can update phone numbers through staff assistance
- **Process:** Worker contacts agency → Staff verifies identity → Updates phone number → System sends confirmation SMS to new number
- **Priority:** MUST HAVE

### 3.2 Job Posting Management (FR-JOB)

**FR-JOB-001: Quick Job Creation**

- **Description:** Staff can create job posts in under 2 minutes
- **Required Fields:**
  1. Facility (dropdown selection)
  2. Service Date (date picker)
  3. Shift Type (dropdown with codes: PC8, A, B, C, D, N, etc.)
  4. Start Time (auto-populated from shift type, editable)
  5. End Time (auto-calculated, editable)
  6. Number of Workers Needed (numeric input, default 1)
  7. Special Requirements (optional text area)
- **Auto-population Logic:**
  - Selecting facility pre-fills location and contact info
  - Selecting shift type (e.g., PC8) auto-sets:
    - Start time: 09:00
    - End time: 17:00
    - Working hours: 8 hours
  - Manual time edits recalculate working hours automatically
- **Priority:** MUST HAVE

**FR-JOB-002: Batch Job Creation**

- **Description:** Create multiple jobs for same facility and date with different shifts
- **Workflow:**
  1. Select facility and date once
  2. Add multiple shift types (PC8, A, B)
  3. Specify worker count per shift
  4. System creates separate job posts for each shift
- **Priority:** SHOULD HAVE

**FR-JOB-003: Job Post Editing**

- **Description:** Staff can edit job posts before worker assignment
- **Restrictions:**
  - Can edit unassigned jobs freely
  - Editing assigned jobs requires confirmation and worker notification
  - Cannot delete jobs with confirmed workers (must cancel instead)
- **Priority:** MUST HAVE

**FR-JOB-004: Job Status Workflow**

| Status | Description | Allowed Actions |
|--------|-------------|-----------------|
| Draft | Created but not published | Edit, Delete, Publish |
| Open | Published, accepting applications | Edit (limited), Cancel, Assign |
| Assigned | Worker assigned | View, Cancel (with reason) |
| Confirmed | Worker confirmed attendance | View, Mark Complete |
| Completed | Job finished | View, Archive |
| Cancelled | Job cancelled | View only (archived) |

- **Priority:** MUST HAVE

### 3.3 ERP Integration (FR-ERP)

**FR-ERP-001: Job Data Import**

- **Description:** Import job data from ERP system to create matching system posts
- **Import Method:** RESTful API endpoint or scheduled batch import
- **Data Mapping:**

**Data Mapping:**

| ERP Field | Matching System Field | Transformation |
|-----------|-----------------------|----------------|
| FacilityCode | facility_id | Lookup facility by code |
| ServiceDate | job_date | ISO 8601 format |
| ShiftCode | shift_type | Direct mapping |
| StartTime | start_time | HH:MM format |
| EndTime | end_time | HH:MM format |
| WorkerCount | positions_needed | Integer |

- **Frequency:** Every 15 minutes during business hours (09:00-22:00)
- **Error Handling:** Log failed imports, alert staff, continue processing remaining records
- **Priority:** MUST HAVE

**FR-ERP-002: Worker Assignment Export**

- **Description:** Export confirmed job assignments back to ERP system
- **Trigger:** When worker confirms job acceptance
- **Data Sent:** Job ID, Worker ID, Confirmation timestamp, Actual start/end times (if modified)
- **Priority:** MUST HAVE

**FR-ERP-003: Data Conflict Resolution**

- **Scenario:** Same job modified in both ERP and matching system
- **Resolution Strategy:** ERP is source of truth, matching system changes flagged for staff review
- **Priority:** SHOULD HAVE

### 3.4 Worker Search and Selection (FR-SEARCH)

**FR-SEARCH-001: Multi-Criteria Worker Search**

- **Description:** Staff can search workers using multiple criteria
- **Search Fields:**
  1. Staff Number (primary)
  2. Phone Number
  3. Name (partial match supported)
  4. Current Location
  5. Availability Status
- **Search Behavior:**
  - Auto-suggest as user types (minimum 2 characters)
  - Display format: [Name] - [Staff No.] - [Location]
  - Results sorted by: Availability → Last Active → Staff No.
- **Priority:** MUST HAVE

**FR-SEARCH-002: Worker Profile Quick View**

- **Description:** Click worker name to see profile sidebar
- **Information Displayed:**
  - Profile photo
  - Staff number and phone
  - Current status (Available / On Job / Unavailable)
  - Preferred facilities (top 3)
  - Recent job history (last 5 assignments)
  - Current location
- **Priority:** SHOULD HAVE

### 3.5 Worker Job Browsing (FR-BROWSE)

**FR-BROWSE-001: Job Listing Display**

- **Description:** Workers view available jobs matching their profile
- **Default View:** Card-based layout, 6 jobs per screen
- **Job Card Information:**
  - Facility name (bold, 18px)
  - District (secondary text)
  - Date and shift time
  - Working hours
  - Pay rate (if configured)
  - "Apply" button (primary action)
- **Priority:** MUST HAVE

**FR-BROWSE-002: Preference-Based Filtering**

- **Description:** Show preferred facility jobs first
- **Logic:**
  1. Worker sets up to 5 preferred facilities in profile
  2. System prioritizes showing jobs from preferred facilities
  3. After 24 hours, if job unfilled, show to all workers
- **Visual Indicator:** Star icon for preferred facility jobs
- **Priority:** SHOULD HAVE

**FR-BROWSE-003: Job Detail View**

- **Description:** Click job card to view full details
- **Information Displayed:**
  - Facility name and full address (after application only)
  - Contact person and phone
  - Detailed shift time and break schedule
  - Special requirements and dress code
  - Facility-specific terms and conditions (images/PDFs)
  - Map showing facility location
- **Priority:** MUST HAVE

### 3.6 Job Application Process (FR-APPLY)

**FR-APPLY-001: Application Submission**

- **Description:** Worker applies for job with terms acknowledgment
- **Workflow:**
  1. Worker clicks "Apply" on job card
  2. System displays full job details + facility terms (scrollable)
  3. Worker reviews all information
  4. Worker checks "I acknowledge and accept the terms" checkbox
  5. "Confirm Application" button becomes enabled
  6. Worker clicks to submit application
  7. System shows confirmation message
  8. Staff receives notification
- **Audit Trail:** System logs application timestamp, IP address, device type
- **Priority:** MUST HAVE

**FR-APPLY-002: Application Limits**

- **Description:** Prevent workers from over-applying
- **Rules:**
  - Maximum 5 pending applications at any time
  - Cannot apply for overlapping shift times
  - Cannot apply for same facility on same date (different shifts allowed)
- **Priority:** SHOULD HAVE

**FR-APPLY-003: Application Withdrawal**

- **Description:** Worker can cancel pending application before staff assignment
- **Process:** Navigate to "My Applications" → Click "Withdraw" → Confirm → Application removed
- **Restriction:** Cannot withdraw after staff assigns job
- **Priority:** MUST HAVE

### 3.7 Notification System (FR-NOTIF)

**FR-NOTIF-001: Worker Notifications**

| Event | Notification Type | Message Example |
|-------|-------------------|-----------------|
| New job posted (preferred facility) | Push + SMS | "New job at [Facility] on [Date] - Apply now!" |
| Application accepted | Push + SMS | "Job confirmed: [Facility] on [Date] at [Time]" |
| Job cancelled | Push + SMS | "Job cancelled: [Facility] on [Date]. Reason: [X]" |
| Job reminder (2 hours before) | Push + SMS | "Reminder: Report to [Facility] at [Time]" |

- **Priority:** MUST HAVE

**FR-NOTIF-002: Staff Notifications**

- **Triggers:** New worker application, Worker confirms job, Worker withdraws application, Job unfilled 24 hours before shift
- **Delivery:** In-app notification + Email
- **Priority:** MUST HAVE

### 3.9 Facility Configuration (FR-FACILITY)

**FR-FACILITY-001: Facility Master Data**

- **Required Fields:**
  - Facility Name (English + Traditional Chinese)
  - Facility Code (3-digit alphanumeric, unique)
  - District/Region
  - Full Address
  - Contact Person and Phone
  - Operating Hours
- **Optional Fields:**
  - Google Maps coordinates
  - Facility photos
  - Parking instructions
  - Special requirements document (PDF)
- **Priority:** MUST HAVE

**FR-FACILITY-002: Shift Code Configuration**

- **Description:** Define facility-specific shift codes and time ranges
- **Configuration Table:**

| Shift Code | Start Time | End Time | Hours |
|------------|------------|----------|-------|
| PC8 | 09:00 | 17:00 | 8 |
| A | 07:00 | 15:00 | 8 |
| B | 15:00 | 23:00 | 8 |
| C | 23:00 | 07:00 | 8 |
| N | 20:00 | 08:00 | 12 |

- **Editing:** Admin can add/edit/delete shift codes per facility
- **Priority:** MUST HAVE

---

## 4. Technical Architecture
### 4.1 System Architecture Overview

**Architecture Pattern:** Three-tier web application

**System Architecture Layers**

- **Presentation Layer:** Responsive web interface (React.js or Vue.js)
- **Application Layer:** RESTful API backend (Spring Boot or Node.js)
- **Data Layer:** Relational database (MySQL or PostgreSQL)

### 4.2 Technology Stack Recommendations

| Component | Recommended Technology | Rationale |
|-----------|-------------------------|-----------|
| Frontend Framework | React.js 18+ or Vue.js 3+ | Component-based, mobile-responsive |
| Backend Framework | Spring Boot 3.x (Java 17+) | Your expertise, enterprise-grade |
| API Protocol | RESTful JSON over HTTPS | Standard, well-supported |
| Database | MySQL 8.0+ or PostgreSQL 15+ | Proven reliability, JSON support |
| Authentication | JWT with refresh tokens | Stateless, scalable |
| File Storage | AWS S3 or local filesystem | Store facility documents, photos |
| SMS Gateway | Twilio or local HK provider | Worker notifications |
| Hosting | AWS EC2/RDS or local server | Based on budget and requirements |

### 4.3 API Design Principles

**REST Endpoints Structure:**

- **Jobs:** /api/v1/jobs (GET, POST, PUT, DELETE)
- **Workers:** /api/v1/workers (GET, POST, PUT)
- **Applications:** /api/v1/applications (GET, POST, DELETE)
- **Facilities:** /api/v1/facilities (GET, POST, PUT)
- **Authentication:** /api/v1/auth/login, /api/v1/auth/refresh
- **ERP Integration:** /api/v1/erp/jobs/import, /api/v1/erp/assignments/export

**API Standards:**

1. All responses use standard HTTP status codes (200, 201, 400, 401, 404, 500)
2. JSON format for request/response bodies
3. Pagination for list endpoints (page, size, total)
4. Consistent error response structure
5. API versioning in URL path

### 4.4 Security Architecture

**Security Layers:**

- **Transport Security:** TLS 1.3 for all connections
- **Authentication:** JWT tokens with 4-hour expiration, 30-day refresh tokens
- **Authorization:** Role-based access control (RBAC) on all endpoints
- **Input Validation:** Server-side validation for all inputs, SQL injection prevention
- **Data Encryption:** Passwords hashed with bcrypt (cost factor 12), sensitive data encrypted at rest
- **Audit Logging:** All authentication attempts, data modifications logged

---

## 5. Data Model and Integration
### 5.1 Core Data Entities

**Entity: Users**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| user_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| phone_number | VARCHAR(20) | UNIQUE, NOT NULL | Login credential |
| email | VARCHAR(255) | UNIQUE, NULL | For staff only |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt hashed |
| full_name | VARCHAR(255) | NOT NULL | English or Chinese |
| role | ENUM | NOT NULL | admin, staff, worker, facility |
| status | ENUM | NOT NULL | active, inactive, suspended |
| created_at | TIMESTAMP | NOT NULL | Registration timestamp |
| last_login | TIMESTAMP | NULL | Last successful login |

**Entity: Workers**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| worker_id | INT | PRIMARY KEY | References user_id |
| staff_number | VARCHAR(20) | UNIQUE, NOT NULL | Agency staff number |
| preferred_facilities | JSON | NULL | Array of facility IDs |
| availability_status | ENUM | NOT NULL | available, on_job, unavailable |
| current_location | VARCHAR(255) | NULL | Last known location |

**Entity: Facilities**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| facility_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| facility_code | VARCHAR(10) | UNIQUE, NOT NULL | 3-digit code |
| facility_name | VARCHAR(255) | NOT NULL | English name |
| facility_name_zh | VARCHAR(255) | NULL | Traditional Chinese |
| district | VARCHAR(100) | NOT NULL | HK district |
| address | TEXT | NOT NULL | Full address |
| contact_person | VARCHAR(255) | NULL | Primary contact |
| contact_phone | VARCHAR(20) | NULL | Contact number |
| qr_code_token | VARCHAR(255) | UNIQUE, NULL | For QR code validation |
| shift_config | JSON | NULL | Shift codes and times |

**Entity: Jobs**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| job_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| facility_id | INT | FOREIGN KEY, NOT NULL | References facilities |
| erp_job_id | VARCHAR(50) | UNIQUE, NULL | ERP system reference |
| job_date | DATE | NOT NULL | Service date |
| shift_type | VARCHAR(10) | NOT NULL | PC8, A, B, etc. |
| start_time | TIME | NOT NULL | Shift start |
| end_time | TIME | NOT NULL | Shift end |
| working_hours | DECIMAL(4,2) | NOT NULL | Calculated hours |
| positions_needed | INT | NOT NULL, DEFAULT 1 | Worker count |
| positions_filled | INT | NOT NULL, DEFAULT 0 | Assigned count |
| status | ENUM | NOT NULL | draft, open, assigned, confirmed, completed, cancelled |
| special_requirements | TEXT | NULL | Additional notes |
| created_by | INT | FOREIGN KEY, NOT NULL | Staff user ID |
| created_at | TIMESTAMP | NOT NULL | Creation timestamp |

**Entity: Applications**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| application_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| job_id | INT | FOREIGN KEY, NOT NULL | References jobs |
| worker_id | INT | FOREIGN KEY, NOT NULL | References workers |
| status | ENUM | NOT NULL | pending, assigned, confirmed, withdrawn, rejected |
| applied_at | TIMESTAMP | NOT NULL | Application timestamp |
| acknowledged_terms | BOOLEAN | NOT NULL | Terms acceptance |
| acknowledgment_ip | VARCHAR(45) | NULL | IP address |

### 5.2 ERP Integration Data Flow

**Import Job Posts from ERP:**

1. ERP system exposes API endpoint: /api/export/jobs
2. Matching system polls endpoint every 15 minutes
3. Retrieves jobs created/modified since last sync
4. Validates required fields present
5. Creates job posts with status "open"
6. Logs import results (success/failure count)

**Export Assignments to ERP:**

1. Worker confirms job application
2. Matching system updates job status to "confirmed"
3. System calls ERP API: POST /api/import/assignments
4. Sends: job\_id, erp\_job\_id, worker\_id, staff\_number, confirmed\_at
5. ERP acknowledges receipt
6. System logs export success

**Error Handling:**

- Connection failures: Retry 3 times with exponential backoff
- Data validation errors: Log error, alert staff, skip record
- Duplicate records: Compare timestamps, keep latest

---

## 6. User Interface Specifications### 6.1 Design Principles

**Core Principles:**

1. **Speed over Beauty:** Prioritize fast data entry and task completion
2. **Mobile-First:** Optimize for iPad (staff) and mobile phones (workers)
3. **Minimal Typing:** Use dropdowns, autocomplete, and pre-filled fields
4. **Clear Hierarchy:** Important actions prominent, secondary actions accessible
5. **Consistent Patterns:** Reuse UI components and interaction patterns

### 6.2 Visual Design Guidelines

**Color Palette:**

- **Primary:** Teal/Blue (\#32808D) - Primary actions, links
- **Success:** Green (\#22C55E) - Confirmations, completed status
- **Warning:** Orange (\#F97316) - Pending actions, attention needed
- **Error:** Red (\#EF4444) - Errors, cancellations
- **Neutral:** Gray scale - Text, backgrounds, borders

**Typography:**

- **Headings:** 24px bold for page titles, 18px bold for section headers
- **Body Text:** 16px regular for content, 14px for secondary info
- **Labels:** 14px medium for form labels
- **Font Family:** System fonts (-apple-system, Roboto, sans-serif)

**Spacing and Layout:**

- Base spacing unit: 8px
- Form field spacing: 16px vertical
- Section spacing: 32px vertical
- Container max-width: 1200px (desktop), 100\% (mobile)
- Touch target minimum: 44x44px

### 6.3 Responsive Breakpoints

| Device | Breakpoint | Layout Changes |
|--------|------------|----------------|
| Mobile Phone | < 640px | Single column, full-width cards |
| Tablet (iPad) | 640px - 1024px | Two-column layout, side navigation |
| Desktop | > 1024px | Multi-column, expanded sidebar |

---

## 7. Wireframes and Screen Flows

### 7.1 Staff Interface - Job Posting Flow

**Wireframe 1: Dashboard (Staff View)**

```
┌─────────────────────────────────────────────────────────────┐
│ [☰ Menu]  Matching System            [🔔 3]  [👤 Staff Name] │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📊 Quick Stats                                               │
│  ┌──────────────┬──────────────┬──────────────┬────────────┐│
│  │ Jobs Today   │ Open Jobs    │ Pending Apps │ Unfilled   ││
│  │    15        │      8       │      12      │     3      ││
│  └──────────────┴──────────────┴──────────────┴────────────┘│
│                                                               │
│  🔍 Quick Actions                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  [+ Create Job Post]  [📋 View All Jobs]  [👥 Workers]  ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  📅 Today's Schedule                                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 09:00 - 17:00  │ Sunbeam Care Home  │ PC8 │ ✓ Assigned  ││
│  │ 15:00 - 23:00  │ Golden Age Center  │ B   │ ⚠ Unfilled  ││
│  │ 07:00 - 15:00  │ Harmony Villa      │ A   │ ✓ Assigned  ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  🚨 Alerts & Notifications                                    │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ • 3 jobs unfilled for tomorrow                           ││
│  │ • 5 new worker applications pending review               ││
│  │ • Worker W123 cancelled job at Golden Age (tomorrow)     ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

**Wireframe 2: Create Job Post (Quick Entry Form)**

```
┌─────────────────────────────────────────────────────────────┐
│ ← Back to Dashboard          Create New Job Post             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Facility *                                                   │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ [Select facility...                            ▼]        ││
│  └─────────────────────────────────────────────────────────┘│
│    (Type to search by code or name)                          │
│                                                               │
│  Service Date *                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ [2025-11-25                                 📅]          ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  Shift Type *                                                 │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ [PC8 - 8 Hour Day Shift                     ▼]          ││
│  └─────────────────────────────────────────────────────────┘│
│    Options: PC8, A, B, C, D, N                               │
│                                                               │
│  ┌──────────────────────────┬──────────────────────────────┐│
│  │ Start Time *             │ End Time *                    ││
│  │ [09:00          ▼]      │ [17:00          ▼]           ││
│  └──────────────────────────┴──────────────────────────────┘│
│    Working Hours: 8.0 hours (auto-calculated)                │
│                                                               │
│  Workers Needed *                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ [1                                           ▼]          ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  Special Requirements (Optional)                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                                                           ││
│  │  (Enter any special notes or requirements)               ││
│  │                                                           ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  [Save as Draft]           [Post Job Now]                ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

**Wireframe 3: Job List View (Staff)**

```
┌─────────────────────────────────────────────────────────────┐
│ ← Dashboard                   All Jobs                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  🔍 [Search jobs...]              [+ Create Job]             │
│                                                               │
│  Filters: [All Status ▼] [All Facilities ▼] [Date Range ▼]  │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ JOB #1234  │  Sunbeam Care Home  │  2025-11-25          ││
│  │ PC8 09:00-17:00  │  ✓ Assigned (1/1)  │  [View Details] ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ JOB #1235  │  Golden Age Center  │  2025-11-25          ││
│  │ B 15:00-23:00  │  ⚠ Unfilled (0/2)  │  [View Details]   ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ JOB #1236  │  Harmony Villa  │  2025-11-26              ││
│  │ A 07:00-15:00  │  📝 3 Pending Apps  │  [Review Apps]   ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  Showing 3 of 24 jobs      [< Previous]  [1] 2 3  [Next >]  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Worker Interface - Job Browsing Flow

**Wireframe 4: Worker Home Screen**

```
┌─────────────────────────────────────────────────────────────┐
│                      Available Jobs                    [👤]  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Your Status: 🟢 Available                                    │
│                                                               │
│  ⭐ Preferred Facilities                                      │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  📍 Sunbeam Care Home                                    ││
│  │  Kwun Tong District                                      ││
│  │  Tomorrow, 09:00 - 17:00 (8 hrs)                         ││
│  │  [Apply Now]                                             ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  📍 Harmony Villa                           ⭐           ││
│  │  Tsuen Wan District                                      ││
│  │  Nov 26, 15:00 - 23:00 (8 hrs)                           ││
│  │  [Apply Now]                                             ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  All Available Jobs                                           │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  📍 Golden Age Center                                    ││
│  │  Sham Shui Po District                                   ││
│  │  Nov 25, 15:00 - 23:00 (8 hrs)                           ││
│  │  [View Details]                                          ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  [Load More Jobs]                                             │
│                                                               │
│  ───────────────────────────────────────────────────────────│
│  [🏠 Jobs]  [📋 My Applications]  [👤 Profile]  [⚙️ Settings] │
└─────────────────────────────────────────────────────────────┘
```

**Wireframe 5: Job Detail View (Worker)**

```
┌─────────────────────────────────────────────────────────────┐
│ ← Back to Jobs                Job Details                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📍 Sunbeam Care Home                              ⭐        │
│  Kwun Tong District                                           │
│                                                               │
│  📅 Date & Time                                               │
│  November 25, 2025                                            │
│  09:00 - 17:00 (8 hours)                                      │
│                                                               │
│  💰 Pay Information                                           │
│  HK$ 150/hour (Total: HK$ 1,200)                              │
│                                                               │
│  📝 Job Requirements                                          │
│  • Arrive 15 minutes before shift start                      │
│  • Report to Reception Desk                                  │
│  • Wear uniform provided by agency                           │
│  • Bring valid work permit and ID                            │
│                                                               │
│  ─────────────────────────────────────────────────────────  │
│                                                               │
│  📋 Facility Terms & Conditions                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ [Image: Facility rules document]                         ││
│  │                                                           ││
│  │ (Scrollable area showing facility-specific policies)     ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  ☑ I have read and accept the terms and conditions           │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              [Confirm Application]                        ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

**Wireframe 6: My Applications Screen (Worker)**

```
┌─────────────────────────────────────────────────────────────┐
│                    My Applications                      [👤]  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Tabs: [Pending] [Confirmed] [Completed]                     │
│                                                               │
│  ⏳ Pending Applications (2)                                  │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  📍 Golden Age Center                                    ││
│  │  Nov 25, 15:00 - 23:00                                   ││
│  │  Applied: Nov 23, 2:30 PM                                ││
│  │  Status: ⏳ Waiting for confirmation                     ││
│  │  [Withdraw Application]                                  ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  📍 Harmony Villa                          ⭐            ││
│  │  Nov 26, 09:00 - 17:00                                   ││
│  │  Applied: Nov 24, 10:15 AM                               ││
│  │  Status: ⏳ Waiting for confirmation                     ││
│  │  [Withdraw Application]                                  ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  ✅ Confirmed Jobs (1)                                        │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  📍 Sunbeam Care Home                      ⭐            ││
│  │  Tomorrow, 09:00 - 17:00                                 ││
│  │  Status: ✅ Confirmed                                    ││
│  │  Report to: Reception Desk, 3/F                          ││
│  │  [View Full Details]  [Get Directions]                   ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  ───────────────────────────────────────────────────────────│
│  [🏠 Jobs]  [📋 My Applications]  [👤 Profile]  [⚙️ Settings] │
└─────────────────────────────────────────────────────────────┘
```

### 7.3 Worker Search Interface (Staff)

**Wireframe 7: Worker Search and Assignment**

```
┌─────────────────────────────────────────────────────────────┐
│ ← Back to Job                Assign Worker to Job #1235      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Job Details: Golden Age Center | Nov 25 | B Shift (15-23)   │
│  Workers Needed: 2  |  Current Applications: 3                │
│                                                               │
│  🔍 Search Workers                                            │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ [Search by name, staff no, or phone...               🔍] ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  Suggested Workers (Based on availability & preferences)      │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  👤 Wong Siu Ming - A123  │  🟢 Available                ││
│  │  📞 9123 4567  │  📍 Currently: Kwun Tong               ││
│  │  ⭐ Preferred facility  │  Last worked: Nov 20           ││
│  │  [Assign to Job]                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  👤 Chan Tai Man - B456  │  🟢 Available                 ││
│  │  📞 9234 5678  │  📍 Currently: Tsuen Wan                ││
│  │  Recent: Golden Age Center (Nov 22)                      ││
│  │  [Assign to Job]                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  👤 Lee Mei Ling - C789  │  🔴 On Job                    ││
│  │  📞 9345 6789  │  📍 Currently: Sunbeam (until 17:00)   ││
│  │  [View Profile]                                          ││
│  └─────────────────────────────────────────────────────────┘│
│                                                               │
│  Pending Applications (3)  [View All →]                       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 7.4 User Flow Diagrams

**Flow 1: Staff Creates Job Post**

[Staff Login] → [Dashboard] → [Click "Create Job"] →
[Fill Form: Facility, Date, Shift] →
[Auto-populate times from shift type] →
[Add special requirements (optional)] →
[Click "Post Job Now"] →
[Job created, workers notified] →
[Return to Dashboard]

**Flow 2: Worker Applies for Job**

[Worker Login] → [Browse Jobs] →
[Filter: Preferred facilities first] →
[Click job card] → [View full details] →
[Read facility terms] →
[Check "I accept terms"] →
[Click "Confirm Application"] →
[Application submitted] →
[Confirmation screen] →
[Return to "My Applications"]

**Flow 3: Staff Assigns Worker**

[Staff views job with pending applications] →
[Click "Review Applications"] →
[View worker profiles and availability] →
[Select best-fit worker] →
[Click "Assign to Job"] →
[Confirm assignment] →
[Worker notified via SMS/Push] →
[Job status updated to "Assigned"]

---

## 8. Non-Functional Requirements

### 8.1 Performance Requirements

| Metric | Target | Measurement |
|--------|--------|-------------|
| Page Load Time | < 2 seconds | First contentful paint |
| API Response Time | < 500ms | 95th percentile |
| Search Results | < 1 second | Autocomplete suggestions |
| Concurrent Users | 200+ | Staff + workers simultaneous access |
| Database Query Time | < 100ms | Complex queries |
| Mobile App Responsiveness | 60 FPS | UI animations and scrolling |

### 8.2 Scalability Requirements

- **User Growth:** Support 500 workers in Phase 1, scalable to 2,000 within 12 months
- **Job Volume:** Handle 100+ job posts per day, 50 concurrent applications
- **Data Storage:** Plan for 3 years of historical data retention
- **Geographic Expansion:** Architecture supports multi-region deployment (future)

### 8.3 Availability and Reliability

- **Uptime Target:** 99.5\% uptime (excluding planned maintenance)
- **Planned Maintenance:** Weekly maintenance window Sundays 02:00-04:00 HKT
- **Backup Frequency:** Daily full backups, hourly incremental backups
- **Disaster Recovery:** RPO (Recovery Point Objective) < 1 hour, RTO (Recovery Time Objective) < 4 hours
- **Monitoring:** 24/7 system health monitoring with automated alerts

### 8.4 Security and Compliance

- **Data Protection:** Comply with Hong Kong Personal Data (Privacy) Ordinance
- **Password Policy:** Minimum 6 characters for workers, 8 characters for staff with complexity requirements
- **Session Management:** Auto-logout after 4 hours inactivity (staff), 24 hours (workers)
- **Audit Trail:** Log all authentication attempts, data modifications, admin actions
- **Data Encryption:** TLS 1.3 in transit, AES-256 at rest for sensitive fields
- **Penetration Testing:** Annual third-party security assessment

### 8.5 Usability Requirements

- **Training Time:** Staff productive within 30 minutes of training
- **Mobile Optimization:** Touch-friendly interface, minimum 44x44px tap targets
- **Language Support:** Interface available in English and Traditional Chinese
- **Accessibility:** WCAG 2.1 Level AA compliance for key workflows
- **Browser Support:** Chrome 100+, Safari 15+, Firefox 100+, Edge 100+

### 8.6 Maintainability Requirements

- **Code Documentation:** Inline comments for complex logic, API documentation using OpenAPI/Swagger
- **Version Control:** Git-based workflow with feature branches and code reviews
- **Deployment:** Automated CI/CD pipeline for testing and deployment
- **Monitoring:** Application logging using structured format (JSON), centralized log aggregation
- **Configuration:** Environment-based configuration (dev, staging, production)

---

## 9. Implementation Plan

### 9.1 Development Phases

**Phase 1: Core Platform (Weeks 1-8)**

| Sprint | Duration | Deliverables |
|--------|----------|--------------|
| Sprint 1 | Week 1-2 | Database design, API skeleton, authentication |
| Sprint 2 | Week 3-4 | Staff interface: Job posting, worker search |
| Sprint 3 | Week 5-6 | Worker interface: Job browsing, applications |
| Sprint 4 | Week 7-8 | ERP integration, notifications, testing |

**Phase 2: Enhancement Features (Weeks 9-12)**

- QR code system implementation
- Worker preference management
- Advanced reporting and analytics
- Performance optimization
- User acceptance testing

**Phase 3: Production Launch (Weeks 13-14)**

- Staff training sessions
- Data migration from existing systems
- Soft launch with limited user group
- Monitor and fix critical issues
- Full production rollout

### 9.2 Milestones and Deliverables

| Milestone | Target Date | Deliverables |
|-----------|-------------|--------------|
| Requirements Approval | Week 1 | Signed specification document |
| Design Completion | Week 2 | UI mockups, API specs approved |
| Alpha Release | Week 6 | Core features functional (internal testing) |
| Beta Release | Week 10 | Full features (user acceptance testing) |
| Production Launch | Week 14 | System live with all users |
| Post-Launch Review | Week 18 | Performance review, feedback integration |

### 9.3 Resource Requirements

**Development Team:**

- 1 × Full-Stack Developer (Lead)
- 1 × Frontend Developer
- 1 × Backend Developer (part-time for API integration)
- 1 × UI/UX Designer (Weeks 1-4)
- 1 × QA Engineer (Weeks 8-14)

**Client Resources:**

- 1 × Project Manager / Product Owner (weekly meetings)
- 2-3 × Agency Staff for UAT and feedback
- 5-10 × Healthcare workers for beta testing
- IT contact for ERP integration access

### 9.4 Risk Management

| Risk | Likelihood | Mitigation Strategy |
|------|------------|---------------------|
| ERP integration delays | Medium | Start integration early, have fallback manual entry option |
| Worker adoption resistance | Medium | Conduct training, provide SMS/phone support |
| Scope creep | High | Strict change control process, prioritize Phase 2 features |
| Performance issues under load | Low | Load testing in Week 10, optimize before launch |
| Data migration errors | Medium | Thorough testing, staged migration approach |

---

## 10. Testing Strategy

### 10.1 Testing Levels

**Unit Testing:**

- Target: 80\%+ code coverage for backend business logic
- Tools: JUnit (Java), Jest (JavaScript)
- Focus: Data validation, calculation logic, API endpoints

**Integration Testing:**

- API endpoint testing (Postman/Newman)
- Database transaction testing
- ERP integration testing (mock and real endpoints)

**User Acceptance Testing (UAT):**

- Conduct with 3 agency staff members (Week 10)
- Beta testing with 10 healthcare workers (Week 11-12)
- Test realistic scenarios from start to finish
- Collect feedback using structured questionnaire

**Performance Testing:**

- Load testing: Simulate 100 concurrent users (Week 10)
- Stress testing: Find breaking point of system
- Database query optimization based on results

### 10.2 Test Scenarios

**Critical User Scenarios:**

1. Staff creates job post in under 2 minutes
2. Worker browses and applies for job successfully
3. Staff searches and assigns worker to job
4. Worker receives notifications and confirms job
5. ERP integration imports jobs and exports assignments
6. Multiple workers apply for same job simultaneously
7. Worker withdraws application before assignment
8. Staff cancels job with assigned workers

### 10.3 Acceptance Criteria

**System Ready for Launch When:**

- All critical user scenarios pass UAT
- Zero critical bugs, < 5 high-priority bugs
- Performance targets met (page load < 2s, API < 500ms)
- Staff training completed, 90\%+ satisfaction rating
- Data migration successful with < 1\% error rate
- ERP integration tested with real data
- Documentation complete (user guides, admin manual)

---

## 11. Training and Support

### 11.1 Staff Training Plan

**Training Sessions:**

- Session 1: System overview and job posting (45 minutes)
- Session 2: Worker search and assignment (30 minutes)
- Session 3: Reports and troubleshooting (30 minutes)

**Training Materials:**

- Video tutorials (5-10 minutes each)
- Step-by-step user guide (PDF)
- Quick reference card (laminated, desktop)
- In-app help tooltips and tutorials

### 11.2 Worker Onboarding

**Onboarding Process:**

1. Worker registers via iPad at agency office
2. Staff creates account and demonstrates app usage (10 minutes)
3. Worker receives SMS with login credentials
4. Worker completes profile setup (preferences, availability)
5. In-app tutorial guides through first job application

**Support Materials:**

- Video tutorial in Cantonese (5 minutes)
- WhatsApp support group for questions
- FAQ document covering common issues

### 11.3 Ongoing Support

**Support Channels:**

- **Level 1:** Phone/WhatsApp support (agency staff) - Business hours
- **Level 2:** Email support (development team) - Response within 24 hours
- **Level 3:** Critical issues (on-call support) - Response within 2 hours

**Post-Launch Support:**

- Weeks 1-4: Daily check-ins with agency staff
- Weeks 5-8: Weekly review meetings
- Month 3+: Monthly performance review and feedback sessions

---

## 12. Assumptions and Constraints

### 12.1 Assumptions

1. ERP system has accessible API endpoints for integration
2. Staff have iPads with internet connectivity
3. Workers have smartphones with data plans
4. Facility contact information is accurate and up-to-date
5. Workers are comfortable using mobile apps with minimal training
6. SMS gateway service available in Hong Kong
7. Agency can provide facility shift configurations

### 12.2 Constraints

**Technical Constraints:**

- Must integrate with existing ERP system (cannot replace)
- Initial deployment limited to Hong Kong region
- Mobile web app (not native iOS/Android apps in Phase 1)
- Data storage subject to Hong Kong data privacy laws

**Business Constraints:**

- Budget: [To be defined by client]
- Timeline: 14-week development + 4-week post-launch support
- Staff availability: Limited to weekly meetings and UAT sessions
- Worker participation: Voluntary adoption in Phase 1

**Operational Constraints:**

- Cannot disrupt existing WhatsApp-based workflow during transition
- Must maintain manual backup process for first 3 months
- Facility portal (Phase 2) dependent on Phase 1 success

### 12.3 Out of Scope

**Not Included in Phase 1:**

- Facility self-service portal
- Payment processing and commission calculations
- Worker performance ratings and reviews
- GPS tracking and geofencing
- Advanced analytics and business intelligence dashboards
- Mobile native applications (iOS/Android)
- Multi-language support beyond English/Chinese
- Integration with third-party background check services

---

## 13. Approval and Sign-Off

### 13.1 Document Review

This Product Specification Document requires review and approval from the following stakeholders:

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Agency Director | [Name] |  |  |
| Operations Manager | [Name] |  |  |
| IT Manager | [Name] |  |  |
| Project Manager | [Name] |  |  |
| System Analyst | [Name] |  |  |

### 13.2 Change Management Process

**After Approval:**

1. Any changes to requirements must be submitted as formal change request
2. Change requests evaluated for impact on timeline, budget, scope
3. Major changes require stakeholder meeting and re-approval
4. Minor changes (UI tweaks, text changes) can be approved by Project Manager
5. All changes documented in revision history

### 13.3 Next Steps

**Upon Approval of This Document:**

1. Finalize project budget and resource allocation
2. Schedule kickoff meeting with development team
3. Begin detailed UI mockup design (Week 1)
4. Set up development environment and repository
5. Schedule weekly status meetings (every Monday 10:00 AM)
6. Begin Sprint 1: Database design and authentication (Week 1-2)

---

## Appendices

### Appendix A: Future Enhancements - QR Code System

**Deferred to Version 2.0+ (Post-MVP)**

**QR-001: Facility QR Code Generation**

- **Description:** Generate unique QR codes for each facility for identification and attendance tracking
- **QR Code Contents:** Facility ID + Validation token + Timestamp
- **Use Cases:**
  1. **Facility Identification:** Workers scan QR code to auto-fill facility info in job applications
  2. **Attendance Tracking:** Workers scan QR code when arriving at shift for automated clock-in
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
  - Supports facility self-service portal (Phase 2)
- **Requirements:**
  - QR code printing and display at facilities
  - Camera/scanning capability on worker devices
  - Real-time validation infrastructure
- **Estimated Timeline:** Version 2.0 (Months 4-6 post-launch)
- **Priority:** OPTIONAL - Deferred to future release

### Appendix B: Glossary of Terms

| Term | Definition |
|------|------------|
| 配對系統 | Matching System - core platform name |
| 姐姐 | Healthcare workers (frontline care staff) |
| 院舍 | Care facilities (elderly homes, hospitals) |
| PC8 | Standard 8-hour day shift (09:00-17:00) |
| ERP | Enterprise Resource Planning system |
| UAT | User Acceptance Testing |
| API | Application Programming Interface |
| JWT | JSON Web Token (authentication method) |

### Appendix C: Reference Documents

1. Meeting Minutes - Prestige Health Care Agency Ltd (Nov 24, 2025)
2. Existing ERP System Documentation
3. Facility Master List and Shift Codes
4. Current WhatsApp Workflow Screenshots
5. Hong Kong Personal Data (Privacy) Ordinance Guidelines

### Appendix D: Contact Information

**Project Team:**

- Project Manager: [Name, Email, Phone]
- System Analyst: [Name, Email, Phone]
- Lead Developer: [Name, Email, Phone]

**Client Contacts:**

- Agency Director: [Name, Email, Phone]
- Operations Manager: [Name, Email, Phone]
- IT Contact: [Name, Email, Phone]

---

## Document End

**Total Pages:** [Page count]  
**Word Count:** [Approximate word count]  
**Last Updated:** November 24, 2025
