## Healthcare Worker Matching System (配對系統)
### Prestige Health Care Agency Ltd

**Document Version:** 1.0  
**Date:** November 24, 2025  
**Project Manager:** [Name]  
**System Analyst:** [Name]  
**Status:** Draft for Client Approval

---

## Document Control

\begin{table}
\begin{tabular}{|l|l|l|l|}
\hline
\textbf{Version} & \textbf{Date} & \textbf{Author} & \textbf{Changes} \\
\hline
1.0 & 2025-11-24 & System Analyst & Initial draft for client review \\
\hline
\end{tabular}
\caption{Document revision history}
\end{table}

---

## Executive Summary

This document specifies the functional and technical requirements for the Healthcare Worker Matching System (配對系統), a web-based platform designed to streamline job posting, worker assignment, and facility coordination for Prestige Health Care Agency Ltd.

**Project Objectives:**

\begin{itemize}
\item Reduce manual data entry time by 60-70\% through automation
\item Enable staff to handle 2-3x current order volume without additional headcount
\item Improve job posting speed from 5-10 minutes to under 2 minutes per post
\item Create scalable foundation for future facility self-service portal
\item Integrate seamlessly with existing ERP system
\end{itemize}

**Target Users:**

\begin{enumerate}
\item Agency Staff (Primary Phase 1 users) - Job posting and worker management
\item Healthcare Workers (Phase 1) - Job browsing and application
\item Facility Administrators (Phase 2) - Self-service job posting
\end{enumerate}

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

\begin{figure}
\centering
\textbf{System Context Diagram}
\begin{itemize}
\item \textbf{External Systems:} Existing ERP System (Primary data source)
\item \textbf{Primary Users:} Agency Staff, Healthcare Workers
\item \textbf{Future Integration:} Facility Portal (Phase 2)
\end{itemize}
\caption{High-level system architecture and external interfaces}
\end{figure}

### 1.3 System Boundaries

**In Scope:**

\begin{itemize}
\item Staff interface for job posting and worker assignment
\item Worker mobile interface for job browsing and applications
\item ERP integration for job data synchronization
\item User authentication and authorization
\item Job matching logic based on preferences and availability
\item Notification system (SMS/Email/Push)
\item QR code generation for facility identification
\item Basic reporting and analytics
\end{itemize}

**Out of Scope (Phase 1):**

\begin{itemize}
\item Facility self-service portal
\item Payment processing and commission calculation
\item Worker rating and performance management
\item Advanced analytics and business intelligence
\item Mobile native applications (iOS/Android)
\end{itemize}

---

## 2. User Roles and Permissions

### 2.1 User Role Definitions

\begin{table}
\begin{tabular}{|p{3cm}|p{5cm}|p{5cm}|}
\hline
\textbf{Role} & \textbf{Description} & \textbf{Key Permissions} \\
\hline
System Administrator & Full system access, configuration management & All permissions, user management, system settings \\
\hline
Agency Staff & Daily operations, job posting, worker assignment & Create/edit/delete jobs, assign workers, view all data \\
\hline
Healthcare Worker & Browse jobs, submit applications, view assignments & View available jobs, apply for jobs, view own profile \\
\hline
Facility Admin (Phase 2) & Self-service job posting & Create job posts, view own facility data \\
\hline
\end{tabular}
\caption{User roles and access levels}
\end{table}

### 2.2 Permission Matrix

\begin{table}
\begin{tabular}{|l|c|c|c|c|}
\hline
\textbf{Function} & \textbf{Admin} & \textbf{Staff} & \textbf{Worker} & \textbf{Facility} \\
\hline
View Dashboard & ✓ & ✓ & ✓ & ✓ \\
Create Job Post & ✓ & ✓ & ✗ & ✓ (Phase 2) \\
Edit Job Post & ✓ & ✓ & ✗ & ✓ (own only) \\
Delete Job Post & ✓ & ✓ & ✗ & ✗ \\
Assign Worker & ✓ & ✓ & ✗ & ✗ \\
Apply for Job & ✗ & ✗ & ✓ & ✗ \\
View All Workers & ✓ & ✓ & ✗ & ✗ \\
Edit Worker Profile & ✓ & ✓ & ✓ (own only) & ✗ \\
Generate Reports & ✓ & ✓ & ✗ & ✓ (own data) \\
System Configuration & ✓ & ✗ & ✗ & ✗ \\
\hline
\end{tabular}
\caption{Detailed permission matrix by role}
\end{table}

---

## 3. Functional Requirements

### 3.1 User Authentication (FR-AUTH)

**FR-AUTH-001: Worker Login**

\begin{itemize}
\item \textbf{Description:} Healthcare workers log in using phone number and password
\item \textbf{Rationale:} Most accessible credential for workers who may not have email
\item \textbf{Acceptance Criteria:}
  \begin{enumerate}
  \item System accepts 8-digit Hong Kong phone numbers (no country code required)
  \item Password must be minimum 6 characters
  \item System remembers device for 30 days (optional)
  \item "Forgot Password" sends SMS verification code
  \item Maximum 5 failed login attempts before 15-minute lockout
  \end{enumerate}
\item \textbf{Priority:} MUST HAVE
\end{itemize}

**FR-AUTH-002: Staff Login**

\begin{itemize}
\item \textbf{Description:} Agency staff log in using email and password
\item \textbf{Acceptance Criteria:}
  \begin{enumerate}
  \item Email validation follows RFC 5322 standard
  \item Password complexity: 8+ characters, 1 uppercase, 1 number
  \item Session timeout after 4 hours of inactivity
  \item Audit log records all login attempts
  \end{enumerate}
\item \textbf{Priority:} MUST HAVE
\end{itemize}

**FR-AUTH-003: Phone Number Updates**

\begin{itemize}
\item \textbf{Description:} Workers can update phone numbers through staff assistance
\item \textbf{Process:} Worker contacts agency → Staff verifies identity → Updates phone number → System sends confirmation SMS to new number
\item \textbf{Priority:} MUST HAVE
\end{itemize}

### 3.2 Job Posting Management (FR-JOB)

**FR-JOB-001: Quick Job Creation**

\begin{itemize}
\item \textbf{Description:} Staff can create job posts in under 2 minutes
\item \textbf{Required Fields:}
  \begin{enumerate}
  \item Facility (dropdown selection)
  \item Service Date (date picker)
  \item Shift Type (dropdown with codes: PC8, A, B, C, D, N, etc.)
  \item Start Time (auto-populated from shift type, editable)
  \item End Time (auto-calculated, editable)
  \item Number of Workers Needed (numeric input, default 1)
  \item Special Requirements (optional text area)
  \end{enumerate}
\item \textbf{Auto-population Logic:}
  \begin{itemize}
  \item Selecting facility pre-fills location and contact info
  \item Selecting shift type (e.g., PC8) auto-sets:
    \begin{itemize}
    \item Start time: 09:00
    \item End time: 17:00
    \item Working hours: 8 hours
    \end{itemize}
  \item Manual time edits recalculate working hours automatically
  \end{itemize}
\item \textbf{Priority:} MUST HAVE
\end{itemize}

**FR-JOB-002: Batch Job Creation**

\begin{itemize}
\item \textbf{Description:} Create multiple jobs for same facility and date with different shifts
\item \textbf{Workflow:}
  \begin{enumerate}
  \item Select facility and date once
  \item Add multiple shift types (PC8, A, B)
  \item Specify worker count per shift
  \item System creates separate job posts for each shift
  \end{enumerate}
\item \textbf{Priority:} SHOULD HAVE
\end{itemize}

**FR-JOB-003: Job Post Editing**

\begin{itemize}
\item \textbf{Description:} Staff can edit job posts before worker assignment
\item \textbf{Restrictions:}
  \begin{itemize}
  \item Can edit unassigned jobs freely
  \item Editing assigned jobs requires confirmation and worker notification
  \item Cannot delete jobs with confirmed workers (must cancel instead)
  \end{itemize}
\item \textbf{Priority:} MUST HAVE
\end{itemize}

**FR-JOB-004: Job Status Workflow**

\begin{table}
\begin{tabular}{|l|l|p{5cm}|}
\hline
\textbf{Status} & \textbf{Description} & \textbf{Allowed Actions} \\
\hline
Draft & Created but not published & Edit, Delete, Publish \\
\hline
Open & Published, accepting applications & Edit (limited), Cancel, Assign \\
\hline
Assigned & Worker assigned & View, Cancel (with reason) \\
\hline
Confirmed & Worker confirmed attendance & View, Mark Complete \\
\hline
Completed & Job finished & View, Archive \\
\hline
Cancelled & Job cancelled & View only (archived) \\
\hline
\end{tabular}
\caption{Job post status lifecycle}
\end{table}

\begin{itemize}
\item \textbf{Priority:} MUST HAVE
\end{itemize}

### 3.3 ERP Integration (FR-ERP)

**FR-ERP-001: Job Data Import**

\begin{itemize}
\item \textbf{Description:} Import job data from ERP system to create matching system posts
\item \textbf{Import Method:} RESTful API endpoint or scheduled batch import
\item \textbf{Data Mapping:}
\end{itemize}

\begin{table}
\begin{tabular}{|l|l|l|}
\hline
\textbf{ERP Field} & \textbf{Matching System Field} & \textbf{Transformation} \\
\hline
FacilityCode & facility\_id & Lookup facility by code \\
ServiceDate & job\_date & ISO 8601 format \\
ShiftCode & shift\_type & Direct mapping \\
StartTime & start\_time & HH:MM format \\
EndTime & end\_time & HH:MM format \\
WorkerCount & positions\_needed & Integer \\
\hline
\end{tabular}
\caption{ERP to matching system data mapping}
\end{table}

\begin{itemize}
\item \textbf{Frequency:} Every 15 minutes during business hours (09:00-22:00)
\item \textbf{Error Handling:} Log failed imports, alert staff, continue processing remaining records
\item \textbf{Priority:} MUST HAVE
\end{itemize}

**FR-ERP-002: Worker Assignment Export**

\begin{itemize}
\item \textbf{Description:} Export confirmed job assignments back to ERP system
\item \textbf{Trigger:} When worker confirms job acceptance
\item \textbf{Data Sent:} Job ID, Worker ID, Confirmation timestamp, Actual start/end times (if modified)
\item \textbf{Priority:} MUST HAVE
\end{itemize}

**FR-ERP-003: Data Conflict Resolution**

\begin{itemize}
\item \textbf{Scenario:} Same job modified in both ERP and matching system
\item \textbf{Resolution Strategy:} ERP is source of truth, matching system changes flagged for staff review
\item \textbf{Priority:} SHOULD HAVE
\end{itemize}

### 3.4 Worker Search and Selection (FR-SEARCH)

**FR-SEARCH-001: Multi-Criteria Worker Search**

\begin{itemize}
\item \textbf{Description:} Staff can search workers using multiple criteria
\item \textbf{Search Fields:}
  \begin{enumerate}
  \item Staff Number (primary)
  \item Phone Number
  \item Name (partial match supported)
  \item Current Location
  \item Availability Status
  \end{enumerate}
\item \textbf{Search Behavior:}
  \begin{itemize}
  \item Auto-suggest as user types (minimum 2 characters)
  \item Display format: [Name] - [Staff No.] - [Location]
  \item Results sorted by: Availability → Last Active → Staff No.
  \end{itemize}
\item \textbf{Priority:} MUST HAVE
\end{itemize}

**FR-SEARCH-002: Worker Profile Quick View**

\begin{itemize}
\item \textbf{Description:} Click worker name to see profile sidebar
\item \textbf{Information Displayed:}
  \begin{itemize}
  \item Profile photo
  \item Staff number and phone
  \item Current status (Available / On Job / Unavailable)
  \item Preferred facilities (top 3)
  \item Recent job history (last 5 assignments)
  \item Current location
  \end{itemize}
\item \textbf{Priority:} SHOULD HAVE
\end{itemize}

### 3.5 Worker Job Browsing (FR-BROWSE)

**FR-BROWSE-001: Job Listing Display**

\begin{itemize}
\item \textbf{Description:} Workers view available jobs matching their profile
\item \textbf{Default View:} Card-based layout, 6 jobs per screen
\item \textbf{Job Card Information:}
  \begin{itemize}
  \item Facility name (bold, 18px)
  \item District (secondary text)
  \item Date and shift time
  \item Working hours
  \item Pay rate (if configured)
  \item "Apply" button (primary action)
  \end{itemize}
\item \textbf{Priority:} MUST HAVE
\end{itemize}

**FR-BROWSE-002: Preference-Based Filtering**

\begin{itemize}
\item \textbf{Description:} Show preferred facility jobs first
\item \textbf{Logic:}
  \begin{enumerate}
  \item Worker sets up to 5 preferred facilities in profile
  \item System prioritizes showing jobs from preferred facilities
  \item After 24 hours, if job unfilled, show to all workers
  \end{enumerate}
\item \textbf{Visual Indicator:} Star icon for preferred facility jobs
\item \textbf{Priority:} SHOULD HAVE
\end{itemize}

**FR-BROWSE-003: Job Detail View**

\begin{itemize}
\item \textbf{Description:} Click job card to view full details
\item \textbf{Information Displayed:}
  \begin{itemize}
  \item Facility name and full address (after application only)
  \item Contact person and phone
  \item Detailed shift time and break schedule
  \item Special requirements and dress code
  \item Facility-specific terms and conditions (images/PDFs)
  \item Map showing facility location
  \end{itemize}
\item \textbf{Priority:} MUST HAVE
\end{itemize}

### 3.6 Job Application Process (FR-APPLY)

**FR-APPLY-001: Application Submission**

\begin{itemize}
\item \textbf{Description:} Worker applies for job with terms acknowledgment
\item \textbf{Workflow:}
  \begin{enumerate}
  \item Worker clicks "Apply" on job card
  \item System displays full job details + facility terms (scrollable)
  \item Worker reviews all information
  \item Worker checks "I acknowledge and accept the terms" checkbox
  \item "Confirm Application" button becomes enabled
  \item Worker clicks to submit application
  \item System shows confirmation message
  \item Staff receives notification
  \end{enumerate}
\item \textbf{Audit Trail:} System logs application timestamp, IP address, device type
\item \textbf{Priority:} MUST HAVE
\end{itemize}

**FR-APPLY-002: Application Limits**

\begin{itemize}
\item \textbf{Description:} Prevent workers from over-applying
\item \textbf{Rules:}
  \begin{itemize}
  \item Maximum 5 pending applications at any time
  \item Cannot apply for overlapping shift times
  \item Cannot apply for same facility on same date (different shifts allowed)
  \end{itemize}
\item \textbf{Priority:} SHOULD HAVE
\end{itemize}

**FR-APPLY-003: Application Withdrawal**

\begin{itemize}
\item \textbf{Description:} Worker can cancel pending application before staff assignment
\item \textbf{Process:} Navigate to "My Applications" → Click "Withdraw" → Confirm → Application removed
\item \textbf{Restriction:} Cannot withdraw after staff assigns job
\item \textbf{Priority:} MUST HAVE
\end{itemize}

### 3.7 QR Code System (FR-QR)

**FR-QR-001: Facility QR Code Generation**

\begin{itemize}
\item \textbf{Description:} Generate unique QR codes for each facility
\item \textbf{QR Code Contents:} Facility ID + Validation token
\item \textbf{Usage:}
  \begin{enumerate}
  \item System administrator generates QR codes for all facilities
  \item QR codes provided as printable PDFs (A4 size)
  \item Facility displays QR code at reception area
  \item Workers scan QR code to auto-fill facility info in job applications
  \end{enumerate}
\item \textbf{Priority:} SHOULD HAVE (Future use for facility self-service)
\end{itemize}

### 3.8 Notification System (FR-NOTIF)

**FR-NOTIF-001: Worker Notifications**

\begin{table}
\begin{tabular}{|p{4cm}|p{4cm}|p{4cm}|}
\hline
\textbf{Event} & \textbf{Notification Type} & \textbf{Message Example} \\
\hline
New job posted (preferred facility) & Push + SMS & "New job at [Facility] on [Date] - Apply now!" \\
\hline
Application accepted & Push + SMS & "Job confirmed: [Facility] on [Date] at [Time]" \\
\hline
Job cancelled & Push + SMS & "Job cancelled: [Facility] on [Date]. Reason: [X]" \\
\hline
Job reminder (2 hours before) & Push + SMS & "Reminder: Report to [Facility] at [Time]" \\
\hline
\end{tabular}
\caption{Worker notification types and triggers}
\end{table}

\begin{itemize}
\item \textbf{Priority:} MUST HAVE
\end{itemize}

**FR-NOTIF-002: Staff Notifications**

\begin{itemize}
\item \textbf{Triggers:} New worker application, Worker confirms job, Worker withdraws application, Job unfilled 24 hours before shift
\item \textbf{Delivery:} In-app notification + Email
\item \textbf{Priority:} MUST HAVE
\end{itemize}

### 3.9 Facility Configuration (FR-FACILITY)

**FR-FACILITY-001: Facility Master Data**

\begin{itemize}
\item \textbf{Required Fields:}
  \begin{itemize}
  \item Facility Name (English + Traditional Chinese)
  \item Facility Code (3-digit alphanumeric, unique)
  \item District/Region
  \item Full Address
  \item Contact Person and Phone
  \item Operating Hours
  \end{itemize}
\item \textbf{Optional Fields:}
  \begin{itemize}
  \item Google Maps coordinates
  \item Facility photos
  \item Parking instructions
  \item Special requirements document (PDF)
  \end{itemize}
\item \textbf{Priority:} MUST HAVE
\end{itemize}

**FR-FACILITY-002: Shift Code Configuration**

\begin{itemize}
\item \textbf{Description:} Define facility-specific shift codes and time ranges
\item \textbf{Configuration Table:}
\end{itemize}

\begin{table}
\begin{tabular}{|l|l|l|l|}
\hline
\textbf{Shift Code} & \textbf{Start Time} & \textbf{End Time} & \textbf{Hours} \\
\hline
PC8 & 09:00 & 17:00 & 8 \\
A & 07:00 & 15:00 & 8 \\
B & 15:00 & 23:00 & 8 \\
C & 23:00 & 07:00 & 8 \\
N & 20:00 & 08:00 & 12 \\
\hline
\end{tabular}
\caption{Example shift code configuration}
\end{table}

\begin{itemize}
\item \textbf{Editing:} Admin can add/edit/delete shift codes per facility
\item \textbf{Priority:} MUST HAVE
\end{itemize}

---

## 4. Technical Architecture

### 4.1 System Architecture Overview

**Architecture Pattern:** Three-tier web application

\begin{figure}
\centering
\textbf{System Architecture Layers}
\begin{itemize}
\item \textbf{Presentation Layer:} Responsive web interface (React.js or Vue.js)
\item \textbf{Application Layer:} RESTful API backend (Spring Boot or Node.js)
\item \textbf{Data Layer:} Relational database (MySQL or PostgreSQL)
\end{itemize}
\caption{Three-tier architecture with clear separation of concerns}
\end{figure}

### 4.2 Technology Stack Recommendations

\begin{table}
\begin{tabular}{|l|l|p{5cm}|}
\hline
\textbf{Component} & \textbf{Recommended Technology} & \textbf{Rationale} \\
\hline
Frontend Framework & React.js 18+ or Vue.js 3+ & Component-based, mobile-responsive \\
\hline
Backend Framework & Spring Boot 3.x (Java 17+) & Your expertise, enterprise-grade \\
\hline
API Protocol & RESTful JSON over HTTPS & Standard, well-supported \\
\hline
Database & MySQL 8.0+ or PostgreSQL 15+ & Proven reliability, JSON support \\
\hline
Authentication & JWT with refresh tokens & Stateless, scalable \\
\hline
File Storage & AWS S3 or local filesystem & Store facility documents, photos \\
\hline
SMS Gateway & Twilio or local HK provider & Worker notifications \\
\hline
Hosting & AWS EC2/RDS or local server & Based on budget and requirements \\
\hline
\end{tabular}
\caption{Recommended technology stack}
\end{table}

### 4.3 API Design Principles

**REST Endpoints Structure:**

\begin{itemize}
\item \textbf{Jobs:} /api/v1/jobs (GET, POST, PUT, DELETE)
\item \textbf{Workers:} /api/v1/workers (GET, POST, PUT)
\item \textbf{Applications:} /api/v1/applications (GET, POST, DELETE)
\item \textbf{Facilities:} /api/v1/facilities (GET, POST, PUT)
\item \textbf{Authentication:} /api/v1/auth/login, /api/v1/auth/refresh
\item \textbf{ERP Integration:} /api/v1/erp/jobs/import, /api/v1/erp/assignments/export
\end{itemize}

**API Standards:**

\begin{enumerate}
\item All responses use standard HTTP status codes (200, 201, 400, 401, 404, 500)
\item JSON format for request/response bodies
\item Pagination for list endpoints (page, size, total)
\item Consistent error response structure
\item API versioning in URL path
\end{enumerate}

### 4.4 Security Architecture

**Security Layers:**

\begin{itemize}
\item \textbf{Transport Security:} TLS 1.3 for all connections
\item \textbf{Authentication:} JWT tokens with 4-hour expiration, 30-day refresh tokens
\item \textbf{Authorization:} Role-based access control (RBAC) on all endpoints
\item \textbf{Input Validation:} Server-side validation for all inputs, SQL injection prevention
\item \textbf{Data Encryption:} Passwords hashed with bcrypt (cost factor 12), sensitive data encrypted at rest
\item \textbf{Audit Logging:} All authentication attempts, data modifications logged
\end{itemize}

---

## 5. Data Model and Integration

### 5.1 Core Data Entities

**Entity: Users**

\begin{table}
\begin{tabular}{|l|l|l|p{4cm}|}
\hline
\textbf{Field} & \textbf{Type} & \textbf{Constraints} & \textbf{Description} \\
\hline
user\_id & INT & PRIMARY KEY, AUTO\_INCREMENT & Unique identifier \\
phone\_number & VARCHAR(20) & UNIQUE, NOT NULL & Login credential \\
email & VARCHAR(255) & UNIQUE, NULL & For staff only \\
password\_hash & VARCHAR(255) & NOT NULL & bcrypt hashed \\
full\_name & VARCHAR(255) & NOT NULL & English or Chinese \\
role & ENUM & NOT NULL & admin, staff, worker, facility \\
status & ENUM & NOT NULL & active, inactive, suspended \\
created\_at & TIMESTAMP & NOT NULL & Registration timestamp \\
last\_login & TIMESTAMP & NULL & Last successful login \\
\hline
\end{tabular}
\caption{Users table structure}
\end{table}

**Entity: Workers**

\begin{table}
\begin{tabular}{|l|l|l|p{4cm}|}
\hline
\textbf{Field} & \textbf{Type} & \textbf{Constraints} & \textbf{Description} \\
\hline
worker\_id & INT & PRIMARY KEY & References user\_id \\
staff\_number & VARCHAR(20) & UNIQUE, NOT NULL & Agency staff number \\
preferred\_facilities & JSON & NULL & Array of facility IDs \\
availability\_status & ENUM & NOT NULL & available, on\_job, unavailable \\
current\_location & VARCHAR(255) & NULL & Last known location \\
\hline
\end{tabular}
\caption{Workers table structure}
\end{table}

**Entity: Facilities**

\begin{table}
\begin{tabular}{|l|l|l|p{4cm}|}
\hline
\textbf{Field} & \textbf{Type} & \textbf{Constraints} & \textbf{Description} \\
\hline
facility\_id & INT & PRIMARY KEY, AUTO\_INCREMENT & Unique identifier \\
facility\_code & VARCHAR(10) & UNIQUE, NOT NULL & 3-digit code \\
facility\_name & VARCHAR(255) & NOT NULL & English name \\
facility\_name\_zh & VARCHAR(255) & NULL & Traditional Chinese \\
district & VARCHAR(100) & NOT NULL & HK district \\
address & TEXT & NOT NULL & Full address \\
contact\_person & VARCHAR(255) & NULL & Primary contact \\
contact\_phone & VARCHAR(20) & NULL & Contact number \\
qr\_code\_token & VARCHAR(255) & UNIQUE, NULL & For QR code validation \\
shift\_config & JSON & NULL & Shift codes and times \\
\hline
\end{tabular}
\caption{Facilities table structure}
\end{table}

**Entity: Jobs**

\begin{table}
\begin{tabular}{|l|l|l|p{4cm}|}
\hline
\textbf{Field} & \textbf{Type} & \textbf{Constraints} & \textbf{Description} \\
\hline
job\_id & INT & PRIMARY KEY, AUTO\_INCREMENT & Unique identifier \\
facility\_id & INT & FOREIGN KEY, NOT NULL & References facilities \\
erp\_job\_id & VARCHAR(50) & UNIQUE, NULL & ERP system reference \\
job\_date & DATE & NOT NULL & Service date \\
shift\_type & VARCHAR(10) & NOT NULL & PC8, A, B, etc. \\
start\_time & TIME & NOT NULL & Shift start \\
end\_time & TIME & NOT NULL & Shift end \\
working\_hours & DECIMAL(4,2) & NOT NULL & Calculated hours \\
positions\_needed & INT & NOT NULL, DEFAULT 1 & Worker count \\
positions\_filled & INT & NOT NULL, DEFAULT 0 & Assigned count \\
status & ENUM & NOT NULL & draft, open, assigned, confirmed, completed, cancelled \\
special\_requirements & TEXT & NULL & Additional notes \\
created\_by & INT & FOREIGN KEY, NOT NULL & Staff user ID \\
created\_at & TIMESTAMP & NOT NULL & Creation timestamp \\
\hline
\end{tabular}
\caption{Jobs table structure}
\end{table}

**Entity: Applications**

\begin{table}
\begin{tabular}{|l|l|l|p{4cm}|}
\hline
\textbf{Field} & \textbf{Type} & \textbf{Constraints} & \textbf{Description} \\
\hline
application\_id & INT & PRIMARY KEY, AUTO\_INCREMENT & Unique identifier \\
job\_id & INT & FOREIGN KEY, NOT NULL & References jobs \\
worker\_id & INT & FOREIGN KEY, NOT NULL & References workers \\
status & ENUM & NOT NULL & pending, assigned, confirmed, withdrawn, rejected \\
applied\_at & TIMESTAMP & NOT NULL & Application timestamp \\
acknowledged\_terms & BOOLEAN & NOT NULL & Terms acceptance \\
acknowledgment\_ip & VARCHAR(45) & NULL & IP address \\
\hline
\end{tabular}
\caption{Applications table structure}
\end{table}

### 5.2 ERP Integration Data Flow

**Import Job Posts from ERP:**

\begin{enumerate}
\item ERP system exposes API endpoint: /api/export/jobs
\item Matching system polls endpoint every 15 minutes
\item Retrieves jobs created/modified since last sync
\item Validates required fields present
\item Creates job posts with status "open"
\item Logs import results (success/failure count)
\end{enumerate}

**Export Assignments to ERP:**

\begin{enumerate}
\item Worker confirms job application
\item Matching system updates job status to "confirmed"
\item System calls ERP API: POST /api/import/assignments
\item Sends: job\_id, erp\_job\_id, worker\_id, staff\_number, confirmed\_at
\item ERP acknowledges receipt
\item System logs export success
\end{enumerate}

**Error Handling:**

\begin{itemize}
\item Connection failures: Retry 3 times with exponential backoff
\item Data validation errors: Log error, alert staff, skip record
\item Duplicate records: Compare timestamps, keep latest
\end{itemize}

---

## 6. User Interface Specifications

### 6.1 Design Principles

**Core Principles:**

\begin{enumerate}
\item \textbf{Speed over Beauty:} Prioritize fast data entry and task completion
\item \textbf{Mobile-First:} Optimize for iPad (staff) and mobile phones (workers)
\item \textbf{Minimal Typing:} Use dropdowns, autocomplete, and pre-filled fields
\item \textbf{Clear Hierarchy:} Important actions prominent, secondary actions accessible
\item \textbf{Consistent Patterns:} Reuse UI components and interaction patterns
\end{enumerate}

### 6.2 Visual Design Guidelines

**Color Palette:**

\begin{itemize}
\item \textbf{Primary:} Teal/Blue (\#32808D) - Primary actions, links
\item \textbf{Success:} Green (\#22C55E) - Confirmations, completed status
\item \textbf{Warning:} Orange (\#F97316) - Pending actions, attention needed
\item \textbf{Error:} Red (\#EF4444) - Errors, cancellations
\item \textbf{Neutral:} Gray scale - Text, backgrounds, borders
\end{itemize}

**Typography:**

\begin{itemize}
\item \textbf{Headings:} 24px bold for page titles, 18px bold for section headers
\item \textbf{Body Text:} 16px regular for content, 14px for secondary info
\item \textbf{Labels:} 14px medium for form labels
\item \textbf{Font Family:} System fonts (-apple-system, Roboto, sans-serif)
\end{itemize}

**Spacing and Layout:**

\begin{itemize}
\item Base spacing unit: 8px
\item Form field spacing: 16px vertical
\item Section spacing: 32px vertical
\item Container max-width: 1200px (desktop), 100\% (mobile)
\item Touch target minimum: 44x44px
\end{itemize}

### 6.3 Responsive Breakpoints

\begin{table}
\begin{tabular}{|l|l|l|}
\hline
\textbf{Device} & \textbf{Breakpoint} & \textbf{Layout Changes} \\
\hline
Mobile Phone & < 640px & Single column, full-width cards \\
\hline
Tablet (iPad) & 640px - 1024px & Two-column layout, side navigation \\
\hline
Desktop & > 1024px & Multi-column, expanded sidebar \\
\hline
\end{tabular}
\caption{Responsive design breakpoints}
\end{table}

---

## 7. Wireframes and Screen Flows

### 7.1 Staff Interface - Job Posting Flow

**Wireframe 1: Dashboard (Staff View)**

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

**Wireframe 2: Create Job Post (Quick Entry Form)**

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

**Wireframe 3: Job List View (Staff)**

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

### 7.2 Worker Interface - Job Browsing Flow

**Wireframe 4: Worker Home Screen**

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

**Wireframe 5: Job Detail View (Worker)**

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

**Wireframe 6: My Applications Screen (Worker)**

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

### 7.3 Worker Search Interface (Staff)

**Wireframe 7: Worker Search and Assignment**

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

\begin{table}
\begin{tabular}{|p{5cm}|p{3cm}|p{4cm}|}
\hline
\textbf{Metric} & \textbf{Target} & \textbf{Measurement} \\
\hline
Page Load Time & < 2 seconds & First contentful paint \\
\hline
API Response Time & < 500ms & 95th percentile \\
\hline
Search Results & < 1 second & Autocomplete suggestions \\
\hline
Concurrent Users & 200+ & Staff + workers simultaneous access \\
\hline
Database Query Time & < 100ms & Complex queries \\
\hline
Mobile App Responsiveness & 60 FPS & UI animations and scrolling \\
\hline
\end{tabular}
\caption{Performance targets and metrics}
\end{table}

### 8.2 Scalability Requirements

\begin{itemize}
\item \textbf{User Growth:} Support 500 workers in Phase 1, scalable to 2,000 within 12 months
\item \textbf{Job Volume:} Handle 100+ job posts per day, 50 concurrent applications
\item \textbf{Data Storage:} Plan for 3 years of historical data retention
\item \textbf{Geographic Expansion:} Architecture supports multi-region deployment (future)
\end{itemize}

### 8.3 Availability and Reliability

\begin{itemize}
\item \textbf{Uptime Target:} 99.5\% uptime (excluding planned maintenance)
\item \textbf{Planned Maintenance:} Weekly maintenance window Sundays 02:00-04:00 HKT
\item \textbf{Backup Frequency:} Daily full backups, hourly incremental backups
\item \textbf{Disaster Recovery:} RPO (Recovery Point Objective) < 1 hour, RTO (Recovery Time Objective) < 4 hours
\item \textbf{Monitoring:} 24/7 system health monitoring with automated alerts
\end{itemize}

### 8.4 Security and Compliance

\begin{itemize}
\item \textbf{Data Protection:} Comply with Hong Kong Personal Data (Privacy) Ordinance
\item \textbf{Password Policy:} Minimum 6 characters for workers, 8 characters for staff with complexity requirements
\item \textbf{Session Management:} Auto-logout after 4 hours inactivity (staff), 24 hours (workers)
\item \textbf{Audit Trail:} Log all authentication attempts, data modifications, admin actions
\item \textbf{Data Encryption:} TLS 1.3 in transit, AES-256 at rest for sensitive fields
\item \textbf{Penetration Testing:} Annual third-party security assessment
\end{itemize}

### 8.5 Usability Requirements

\begin{itemize}
\item \textbf{Training Time:} Staff productive within 30 minutes of training
\item \textbf{Mobile Optimization:} Touch-friendly interface, minimum 44x44px tap targets
\item \textbf{Language Support:} Interface available in English and Traditional Chinese
\item \textbf{Accessibility:} WCAG 2.1 Level AA compliance for key workflows
\item \textbf{Browser Support:} Chrome 100+, Safari 15+, Firefox 100+, Edge 100+
\end{itemize}

### 8.6 Maintainability Requirements

\begin{itemize}
\item \textbf{Code Documentation:} Inline comments for complex logic, API documentation using OpenAPI/Swagger
\item \textbf{Version Control:} Git-based workflow with feature branches and code reviews
\item \textbf{Deployment:} Automated CI/CD pipeline for testing and deployment
\item \textbf{Monitoring:} Application logging using structured format (JSON), centralized log aggregation
\item \textbf{Configuration:} Environment-based configuration (dev, staging, production)
\end{itemize}

---

## 9. Implementation Plan

### 9.1 Development Phases

**Phase 1: Core Platform (Weeks 1-8)**

\begin{table}
\begin{tabular}{|l|l|l|}
\hline
\textbf{Sprint} & \textbf{Duration} & \textbf{Deliverables} \\
\hline
Sprint 1 & Week 1-2 & Database design, API skeleton, authentication \\
\hline
Sprint 2 & Week 3-4 & Staff interface: Job posting, worker search \\
\hline
Sprint 3 & Week 5-6 & Worker interface: Job browsing, applications \\
\hline
Sprint 4 & Week 7-8 & ERP integration, notifications, testing \\
\hline
\end{tabular}
\caption{Phase 1 development sprints}
\end{table}

**Phase 2: Enhancement Features (Weeks 9-12)**

\begin{itemize}
\item QR code system implementation
\item Worker preference management
\item Advanced reporting and analytics
\item Performance optimization
\item User acceptance testing
\end{itemize}

**Phase 3: Production Launch (Weeks 13-14)**

\begin{itemize}
\item Staff training sessions
\item Data migration from existing systems
\item Soft launch with limited user group
\item Monitor and fix critical issues
\item Full production rollout
\end{itemize}

### 9.2 Milestones and Deliverables

\begin{table}
\begin{tabular}{|l|l|l|}
\hline
\textbf{Milestone} & \textbf{Target Date} & \textbf{Deliverables} \\
\hline
Requirements Approval & Week 1 & Signed specification document \\
\hline
Design Completion & Week 2 & UI mockups, API specs approved \\
\hline
Alpha Release & Week 6 & Core features functional (internal testing) \\
\hline
Beta Release & Week 10 & Full features (user acceptance testing) \\
\hline
Production Launch & Week 14 & System live with all users \\
\hline
Post-Launch Review & Week 18 & Performance review, feedback integration \\
\hline
\end{tabular}
\caption{Project milestones and timeline}
\end{table}

### 9.3 Resource Requirements

**Development Team:**

\begin{itemize}
\item 1 × Full-Stack Developer (Lead)
\item 1 × Frontend Developer
\item 1 × Backend Developer (part-time for API integration)
\item 1 × UI/UX Designer (Weeks 1-4)
\item 1 × QA Engineer (Weeks 8-14)
\end{itemize}

**Client Resources:**

\begin{itemize}
\item 1 × Project Manager / Product Owner (weekly meetings)
\item 2-3 × Agency Staff for UAT and feedback
\item 5-10 × Healthcare workers for beta testing
\item IT contact for ERP integration access
\end{itemize}

### 9.4 Risk Management

\begin{table}
\begin{tabular}{|p{4cm}|l|p{5cm}|}
\hline
\textbf{Risk} & \textbf{Likelihood} & \textbf{Mitigation Strategy} \\
\hline
ERP integration delays & Medium & Start integration early, have fallback manual entry option \\
\hline
Worker adoption resistance & Medium & Conduct training, provide SMS/phone support \\
\hline
Scope creep & High & Strict change control process, prioritize Phase 2 features \\
\hline
Performance issues under load & Low & Load testing in Week 10, optimize before launch \\
\hline
Data migration errors & Medium & Thorough testing, staged migration approach \\
\hline
\end{tabular}
\caption{Risk assessment and mitigation strategies}
\end{table}

---

## 10. Testing Strategy

### 10.1 Testing Levels

**Unit Testing:**

\begin{itemize}
\item Target: 80\%+ code coverage for backend business logic
\item Tools: JUnit (Java), Jest (JavaScript)
\item Focus: Data validation, calculation logic, API endpoints
\end{itemize}

**Integration Testing:**

\begin{itemize}
\item API endpoint testing (Postman/Newman)
\item Database transaction testing
\item ERP integration testing (mock and real endpoints)
\end{itemize}

**User Acceptance Testing (UAT):**

\begin{itemize}
\item Conduct with 3 agency staff members (Week 10)
\item Beta testing with 10 healthcare workers (Week 11-12)
\item Test realistic scenarios from start to finish
\item Collect feedback using structured questionnaire
\end{itemize}

**Performance Testing:**

\begin{itemize}
\item Load testing: Simulate 100 concurrent users (Week 10)
\item Stress testing: Find breaking point of system
\item Database query optimization based on results
\end{itemize}

### 10.2 Test Scenarios

**Critical User Scenarios:**

\begin{enumerate}
\item Staff creates job post in under 2 minutes
\item Worker browses and applies for job successfully
\item Staff searches and assigns worker to job
\item Worker receives notifications and confirms job
\item ERP integration imports jobs and exports assignments
\item Multiple workers apply for same job simultaneously
\item Worker withdraws application before assignment
\item Staff cancels job with assigned workers
\end{enumerate}

### 10.3 Acceptance Criteria

**System Ready for Launch When:**

\begin{itemize}
\item All critical user scenarios pass UAT
\item Zero critical bugs, < 5 high-priority bugs
\item Performance targets met (page load < 2s, API < 500ms)
\item Staff training completed, 90\%+ satisfaction rating
\item Data migration successful with < 1\% error rate
\item ERP integration tested with real data
\item Documentation complete (user guides, admin manual)
\end{itemize}

---

## 11. Training and Support

### 11.1 Staff Training Plan

**Training Sessions:**

\begin{itemize}
\item Session 1: System overview and job posting (45 minutes)
\item Session 2: Worker search and assignment (30 minutes)
\item Session 3: Reports and troubleshooting (30 minutes)
\end{itemize}

**Training Materials:**

\begin{itemize}
\item Video tutorials (5-10 minutes each)
\item Step-by-step user guide (PDF)
\item Quick reference card (laminated, desktop)
\item In-app help tooltips and tutorials
\end{itemize}

### 11.2 Worker Onboarding

**Onboarding Process:**

\begin{enumerate}
\item Worker registers via iPad at agency office
\item Staff creates account and demonstrates app usage (10 minutes)
\item Worker receives SMS with login credentials
\item Worker completes profile setup (preferences, availability)
\item In-app tutorial guides through first job application
\end{enumerate}

**Support Materials:**

\begin{itemize}
\item Video tutorial in Cantonese (5 minutes)
\item WhatsApp support group for questions
\item FAQ document covering common issues
\end{itemize}

### 11.3 Ongoing Support

**Support Channels:**

\begin{itemize}
\item \textbf{Level 1:} Phone/WhatsApp support (agency staff) - Business hours
\item \textbf{Level 2:} Email support (development team) - Response within 24 hours
\item \textbf{Level 3:} Critical issues (on-call support) - Response within 2 hours
\end{itemize}

**Post-Launch Support:**

\begin{itemize}
\item Weeks 1-4: Daily check-ins with agency staff
\item Weeks 5-8: Weekly review meetings
\item Month 3+: Monthly performance review and feedback sessions
\end{itemize}

---

## 12. Assumptions and Constraints

### 12.1 Assumptions

\begin{enumerate}
\item ERP system has accessible API endpoints for integration
\item Staff have iPads with internet connectivity
\item Workers have smartphones with data plans
\item Facility contact information is accurate and up-to-date
\item Workers are comfortable using mobile apps with minimal training
\item SMS gateway service available in Hong Kong
\item Agency can provide facility shift configurations
\end{enumerate}

### 12.2 Constraints

**Technical Constraints:**

\begin{itemize}
\item Must integrate with existing ERP system (cannot replace)
\item Initial deployment limited to Hong Kong region
\item Mobile web app (not native iOS/Android apps in Phase 1)
\item Data storage subject to Hong Kong data privacy laws
\end{itemize}

**Business Constraints:**

\begin{itemize}
\item Budget: [To be defined by client]
\item Timeline: 14-week development + 4-week post-launch support
\item Staff availability: Limited to weekly meetings and UAT sessions
\item Worker participation: Voluntary adoption in Phase 1
\end{itemize}

**Operational Constraints:**

\begin{itemize}
\item Cannot disrupt existing WhatsApp-based workflow during transition
\item Must maintain manual backup process for first 3 months
\item Facility portal (Phase 2) dependent on Phase 1 success
\end{itemize}

### 12.3 Out of Scope

**Not Included in Phase 1:**

\begin{itemize}
\item Facility self-service portal
\item Payment processing and commission calculations
\item Worker performance ratings and reviews
\item GPS tracking and geofencing
\item Advanced analytics and business intelligence dashboards
\item Mobile native applications (iOS/Android)
\item Multi-language support beyond English/Chinese
\item Integration with third-party background check services
\end{itemize}

---

## 13. Approval and Sign-Off

### 13.1 Document Review

This Product Specification Document requires review and approval from the following stakeholders:

\begin{table}
\begin{tabular}{|l|p{5cm}|l|l|}
\hline
\textbf{Role} & \textbf{Name} & \textbf{Signature} & \textbf{Date} \\
\hline
Agency Director & [Name] &  &  \\
\hline
Operations Manager & [Name] &  &  \\
\hline
IT Manager & [Name] &  &  \\
\hline
Project Manager & [Name] &  &  \\
\hline
System Analyst & [Name] &  &  \\
\hline
\end{tabular}
\caption{Stakeholder approval signatures}
\end{table}

### 13.2 Change Management Process

**After Approval:**

\begin{enumerate}
\item Any changes to requirements must be submitted as formal change request
\item Change requests evaluated for impact on timeline, budget, scope
\item Major changes require stakeholder meeting and re-approval
\item Minor changes (UI tweaks, text changes) can be approved by Project Manager
\item All changes documented in revision history
\end{enumerate}

### 13.3 Next Steps

**Upon Approval of This Document:**

\begin{enumerate}
\item Finalize project budget and resource allocation
\item Schedule kickoff meeting with development team
\item Begin detailed UI mockup design (Week 1)
\item Set up development environment and repository
\item Schedule weekly status meetings (every Monday 10:00 AM)
\item Begin Sprint 1: Database design and authentication (Week 1-2)
\end{enumerate}

---

## Appendices

### Appendix A: Glossary of Terms

\begin{table}
\begin{tabular}{|l|p{8cm}|}
\hline
\textbf{Term} & \textbf{Definition} \\
\hline
配對系統 & Matching System - core platform name \\
\hline
姐姐 & Healthcare workers (frontline care staff) \\
\hline
院舍 & Care facilities (elderly homes, hospitals) \\
\hline
PC8 & Standard 8-hour day shift (09:00-17:00) \\
\hline
ERP & Enterprise Resource Planning system \\
\hline
UAT & User Acceptance Testing \\
\hline
API & Application Programming Interface \\
\hline
JWT & JSON Web Token (authentication method) \\
\hline
\end{tabular}
\caption{Key terms and definitions}
\end{table}

### Appendix B: Reference Documents

\begin{enumerate}
\item Meeting Minutes - Prestige Health Care Agency Ltd (Nov 24, 2025)
\item Existing ERP System Documentation
\item Facility Master List and Shift Codes
\item Current WhatsApp Workflow Screenshots
\item Hong Kong Personal Data (Privacy) Ordinance Guidelines
\end{enumerate}

### Appendix C: Contact Information

**Project Team:**

\begin{itemize}
\item Project Manager: [Name, Email, Phone]
\item System Analyst: [Name, Email, Phone]
\item Lead Developer: [Name, Email, Phone]
\end{itemize}

**Client Contacts:**

\begin{itemize}
\item Agency Director: [Name, Email, Phone]
\item Operations Manager: [Name, Email, Phone]
\item IT Contact: [Name, Email, Phone]
\end{itemize}

---

**Document End**

**Total Pages:** [Page count]  
**Word Count:** [Approximate word count]  
**Last Updated:** November 24, 2025