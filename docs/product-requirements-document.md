# Product Requirements Document (PRD)
**Prestige Health Dispatch System (PHC)**

**Document Version:** 1.0
**Date:** 2025-11-24
**Product Owner:** [To be assigned]

---

## 📌 PRODUCT DEFINITION

### Product Name
**Prestige Health Dispatch System (PHC)**

### Product Tagline
"Intelligent Healthcare Staffing - Automated, Fair, Transparent"

### Problem Statement
Current manual coordination between care homes and nursing assistants is:
- **Inefficient:** 2-3 hours per shift to fill
- **Inconsistent:** Human bias in allocation
- **Unfair:** No transparency in selection process
- **Error-prone:** High no-show rate (5%)
- **Costly:** 3 FTE coordinators needed

### Solution
Automated dispatch system that:
- Uses scoring algorithm for merit-based allocation
- Integrates with ERP for real-time data sync
- Sends Firebase web push notifications for confirmations
- Provides web-based platform for staff and admin
- Handles emergencies via file upload and distribution

---

## 🎯 PRODUCT GOALS

### Primary Goals
1. **Increase fill rate** from 85% to 95%+ within 3 months
2. **Reduce coordinator time** by 75% (3 hours → 45 min/day)
3. **Decrease no-shows** from 5% to <2%
4. **Launch in 60 days** (1.5 months)

### Secondary Goals
5. Achieve 90% nursing assistant adoption rate
6. Maintain 99.5% system uptime
7. Process 500+ daily assignments
8. Generate HKD 1.74M in Year 1 value

### Success Metrics
See Executive Summary (Section 6)

---

## 👥 TARGET USERS

### Primary Users
1. **Nursing Assistants (500+)**
   - Age: 35-55
   - Tech level: Low-Medium
   - Primary device: Smartphone
   - Goal: Get fair shift assignments

2. **Care Home Supervisors (100+)**
   - Age: 40-60
   - Tech level: Medium
   - Primary device: Mobile/tablet
   - Goal: Verify attendance, manage shifts

3. **PHC Administrators (5-10)**
   - Tech level: High
   - Primary device: Desktop/laptop
   - Goal: Monitor operations, handle exceptions

4. **ERP Administrators (2-3)**
   - Tech level: High
   - Goal: Maintain master data in ERP

### User Personas

**Name:** Ah Mui, 48, Nursing Assistant
- **Background:** 15 years experience, working mother of 2
- **Tech:** Uses smartphone daily, comfortable with web apps
- **Pain Point:** Hates calling coordinator for shifts, feels it's unfair
- **Goal:** Get shifts based on her good attendance record

**Name:** Ms. Wong, 52, Care Home Supervisor
- **Background:** 20 years in healthcare, very experienced
- **Tech:** Uses computer daily, comfortable with web apps
- **Pain Point:** Spends too much time verifying attendance
- **Goal:** Quick way to confirm who's coming

**Name:** Jason, Admin Manager
- **Background:** Operations manager, data-driven
- **Tech:** Very comfortable with technology
- **Pain Point:** No visibility into staffing operations
- **Goal:** Dashboard with real-time metrics

---

## 📋 FEATURE REQUIREMENTS

### P0: Critical Features (Must-Have)

#### FR-0: Staff Login
**Description:** Secure login for nursing assistants using ERP credentials

**Requirements:**
- Login via Mobile Number only
- Validate against synced ERP data
- Account locking (5 failed attempts)
- Forgot Password flow (OTP)
- Session timeout (30 mins)

**Acceptance Criteria:**
✅ Login works with all credential types
✅ Invalid credentials rejected
✅ Account locked after 5 failures
✅ OTP sent for password reset

---

#### FR-1: Scoring Algorithm
**Description:** Merit-based scoring for fair allocation

**Requirements:**
- Attend: +1 point
- Cancel: -1 point, -100 HKD
- No-show: -2 points, -100 HKD
- Tiers: Gold (20+), Silver (10-19), Bronze (0-9), Under Review (<0)

**Acceptance Criteria:**
✅ Score updates automatically
✅ ERP synced in real-time
✅ Manual override with reason required
✅ Score floor = -10

---

#### FR-2: Matching Engine
**Description:** Automated selection of best staff for each shift

**Requirements:**
- Filter by: availability, documents, blacklist, fair sharing
- Rank by: underlist, score tier, work history, seniority
- Automatic submission to ERP
- Re-match on conflict

**Acceptance Criteria:**
✅ Match in <5 minutes
✅ All filters applied correctly
✅ Underlist respected
✅ Re-matching triggered automatically

---

#### FR-3: WhatsApp + Firebase Hybrid Notifications
**Description:** WhatsApp for primary notifications (manual template-based) + Firebase web push for portal alerts and reminders

**Requirements:**

**WhatsApp Notifications (Primary):**
- System generates WhatsApp message templates
- Coordinator copies template and sends via WhatsApp
- Templates include: shift details, confirmation link, deadline
- Support for urgent shift notifications
- Bilingual templates (English + Traditional Chinese)

**Firebase Web Push (Secondary):**
- Send web push notifications to PHC portal
- Trigger: new assignment, pending reminder (2h), day-before reminder (24h)
- Alert coordinators when staff confirms
- Store and manage FCM tokens
- Handle token refresh gracefully

**Requirements:**
- Template generation for WhatsApp messages
- One-click copy button for coordinators
- Firebase push notification system
- Confirmation link with deep linking
- Reminder scheduling (2h, 24h)
- Delivery tracking for both channels

**Acceptance Criteria:**
✅ WhatsApp template generated < 5 seconds
✅ Firebase notification delivered < 30 seconds
✅ Coordinator can send WhatsApp in < 1 min
✅ Confirmation captured in web portal
✅ Reminders sent automatically at 2h and 24h
✅ Works on mobile and desktop browsers

---

#### FR-4: Admin Dashboard
**Description:** Real-time view of all operations

**Requirements:**
- Live metrics: jobs, confirmations, attendance, penalties, API health
- Auto-refresh every 30 seconds
- Drill-down to details
- Color-coded status

**Acceptance Criteria:**
✅ All metrics accurate
✅ No manual refresh needed
✅ Load time <3 seconds

---

#### FR-5: ERP Integration
**Description:** Bi-directional data sync with existing ERP

**Requirements:**
- 13 API endpoints (6 push, 7 pull)
- Daily sync: staff, locations
- Every 15 min: job demands
- Real-time: assignments, penalties, scores

**Acceptance Criteria:**
✅ All APIs tested and working
✅ Zero data loss
✅ Retry logic (3 attempts)
✅ Error logging and alerts

---

#### FR-6: Attendance Tracking
**Description:** Verify staff presence at shifts

**Requirements:**
- Option A: QR code (staff scans)
- Option B: Supervisor manual verification
- Clock-in/out time recording
- Deviation alerts (>1 hour)
- Automatic ERP sync

**Acceptance Criteria:**
✅ Attendance recorded accurately
✅ Deviation flagged
✅ No-show detected automatically
✅ Submitted to ERP within 1 hour

---

#### FR-7: Penalty Management
**Description:** Automatic penalty application for violations

**Requirements:**
- Cancellation: -1 score, -100 HKD
- No-show: -2 score, -100 HKD
- Warning displayed before cancellation
- ERP deduction (API TBD)

**Acceptance Criteria:**
✅ Warning displayed clearly
✅ Penalty applied immediately
✅ Score updated
✅ ERP penalty record created

---

### P1: High-Priority Features

#### FR-8: Emergency File Upload
**Description:** Upload and distribute emergency protocols

**Requirements:**
- Upload PDF/DOC/JPG/PNG (max 10MB)
- Title, description, priority, regions
- Secure storage (S3/Azure)
- Firebase push notification distribution
- In-app alerts for Critical priority
- Tracking (views, confirmations)

**Acceptance Criteria:**
✅ File uploaded successfully
✅ Notifications sent within 5 minutes
✅ Only affected staff notified
✅ In-app alert for Critical priority
✅ Tracking dashboard functional

---

#### FR-9: Emergency Job Posting
**Description:** Manual override for urgent staffing needs

**Requirements:**
- Bypass standard 15-min polling
- Immediate matching
- Urgent Firebase push notification with in-app alert
- "Accept Immediately" button in platform
- Real-time shortage dashboard
- Admin alert if unfilled after 30 min

**Acceptance Criteria:**
✅ No delay in posting
✅ Matching triggered instantly
✅ Dashboard updates in real-time
✅ Alert sent correctly

---

#### FR-10: Settlement Reconciliation
**Description:** Monthly settlement verification with ERP

**Requirements:**
- Fetch settlement data from ERP (1st of month)
- Compare PHC records
- Flag discrepancies
- Generate reports for finance

**Acceptance Criteria:**
✅ Completed by 3rd of month
✅ All discrepancies flagged
✅ Reports generated automatically
✅ Match rate >99%

---

### P2: Medium-Priority Features

#### FR-11: Manual Assignment Override
**Description:** Admin can manually assign staff

**Requirements:**
- Search staff by name, location, score
- Conflict warnings
- Reason required
- Audit log

**Acceptance Criteria:**
✅ Search works correctly
✅ Override logged with admin ID
✅ ERP updated

---

#### FR-12: System Monitoring
**Description:** View API logs and system health

**Requirements:**
- API logs (request/response)
- Sync status dashboard
- Error tracking
- Filter/search logs

**Acceptance Criteria:**
✅ Logs viewable with filters
✅ Critical errors trigger alerts
✅ 90-day retention

---

#### FR-13: Reporting
**Description:** Generate management reports

**Requirements:**
- Settlement reports
- Attendance reports
- Penalty reports
- Score reports
- Date range filter
- Export to Excel/PDF

**Acceptance Criteria:**
✅ All reports accurate
✅ Export works correctly
✅ Format suitable for management review

---

## 🎨 USER EXPERIENCE

### Primary User Journeys

#### Journey 1: Nursing Assistant Gets Assigned
1. ✅ Logs in to Staff Portal
2. ✅ Receives WhatsApp/Push Notification
3. ✅ Reviews shift details on Dashboard
4. ✅ Clicks "Confirm" (1 tap)
5. ✅ Gets confirmation message
6. ✅ Score increases (+1)

#### Journey 2: Admin Posts Emergency Job
1. ✅ Logs into portal
2. ✅ Clicks "Emergency Job"
3. ✅ Fills form (1 minute)
4. ✅ Submits
5. ✅ Job posted immediately
6. ✅ Staff notified (5 min)
7. ✅ Dashboard shows real-time progress

#### Journey 3: Supervisor Verifies Attendance
1. ✅ Opens portal on tablet
2. ✅ Views today's schedule
3. ✅ Confirms staff arrival (1 tap/staff)
4. ✅ Marks no-shows (if any)
5. ✅ Done (2 minutes total)

---

### Design Principles

- **Speed:** All actions <3 seconds
- **Mobile-First:** Works on phone/tablet/desktop
- **Clarity:** Clear buttons, labels, instructions
- **Transparency:** Staff can see their score history
- **Bilingual:** English + Traditional Chinese

---

## ⚙️ TECHNICAL REQUIREMENTS

### Technology Stack
- **Frontend:** React.js 18+, TailwindCSS, Redux
- **Backend:** Java Spring Boot 2.7+, Spring Security
- **Database:** MySQL 8+ (primary), Redis 6+ (caching, sessions)
- **Storage:** S3 or Azure Blob (for files)
- **Queue:** Spring Batch or Quartz (job processing)
- **Auth:** JWT + Spring Security
- **APIs:** 13 ERP integrations (REST)
- **Notifications:** WhatsApp (manual template-based) + Firebase Cloud Messaging (web push)
- **Hosting:** AWS or Azure (cloud)

### Architecture Principles
- **Microservices:** Separate services for matching, notifications, sync
- **Scalable:** Handles 1000+ staff, 500+ daily assignments
- **Resilient:** Retry logic, error handling, monitoring
- **Secure:** Encryption, RBAC, audit logging
- **Maintainable:** Java best practices, documentation, testing

---

## 📅 RELEASE PLAN

### Version 1.0 (60 days)
**Target Launch:** 2025-01-24

**Features:**
- All P0 features (7)
- P1: Emergency features (2)
- P1: Settlement reconciliation
- Basic reporting

**Success Criteria:**
- 50 pilot staff operational
- 95% fill rate achieved
- System stable for 2 weeks

---

## 📊 SUCCESS CRITERIA

### Launch Success (30 days)
✅ 50+ staff using system
✅ 90+ assignments per day
✅ 95%+ fill rate
✅ <2% no-show rate
✅ 99.5% uptime

### Business Success (90 days)
✅ 200+ active staff
✅ 200 assignments/day
✅ HKD 300K revenue increase
✅ <1 hour coordinator time/day

### Strategic Success (365 days)
✅ 500+ active staff
✅ Full care home network
✅ HKD 1.2M revenue increase
✅ 1 FTE coordinator (vs 3)
✅ 118% ROI

---

## 🔒 RISKS & MITIGATION

### High Risks
1. **ERP API Delay**
   - Mitigation: Mock APIs, manual data bridge

2. **Timeline Risk**
   - Mitigation: Agile sprints, daily tracking, scope flexibility

3. **Adoption Risk**
   - Mitigation: Training, change management, pilot program

### Medium Risks
4. **Webhook Unreliability**
   - Mitigation: Polling fallback

5. **Data Quality**
   - Mitigation: Strong validation, admin correction workflows

---

## 💼 BUSINESS CASE

### Investment: HKD 800,000

**Breakdown:**
- Development (60 days): 600K (75%)
- ERP Integration: 80K (10%)
- Testing: 60K (7.5%)
- Infrastructure (Y1): 40K (5%)
- Training: 20K (2.5%)

### Return: HKD 1,740,000 (Year 1)

| Benefit | Year 1 | Monthly |
|---------|--------|---------|
| Revenue increase (5% fill rate) | 1,200,000 | 100,000 |
| Cost savings (2 FTE reduction) | 480,000 | 40,000 |
| Penalty collections | 60,000 | 5,000 |
| **Total** | **1,740,000** | **145,000** |

### ROI: 118%
**Payback Period:** 5.5 months

---

## 🚀 GO-TO-MARKET

### Launch Strategy
1. **Week 1-2:** Pilot with 50 staff (2 locations)
2. **Week 3-6:** Expand to 200 staff (10 locations)
3. **Week 7-8:** Full rollout (500+ staff, all locations)

### Change Management
- Town halls
- Hands-on training
- Dedicated helpdesk
- Weekly surveys
- Monthly business reviews

---

## 📚 DOCUMENTATION DELIVERED

✅ **Software Requirements Specification (SRS)** - Detailed functional requirements
✅ **Technical Design Document (TDD)** - Architecture, database, APIs
✅ **User Stories & Test Cases** - 20+ user stories, 20+ test cases
✅ **Executive Summary** - ROI, business case, stakeholder summary
✅ **Integration To-Do List** - 12-week implementation plan (condensed)
✅ **ERP API Specification** - 13 API endpoints

---

## ✅ APPROVAL STATUS

| Role | Name | Date | Status |
|------|------|------|--------|
| Product Owner | [To be assigned] |  | ⏳ Pending |
| Engineering Lead | [To be assigned] |  | ⏳ Pending |
| Operations Manager | [To be assigned] |  | ⏳ Pending |
| CFO | [To be assigned] |  | ⏳ Pending |
| CEO | [To be assigned] |  | ⏳ Pending |

**Target Approval Date:** December 15, 2025

---

## 🎯 RECOMMENDATION

**APPROVE** HKD 800K investment for PHC v1.0

**Rationale:**
- 118% ROI in Year 1
- 5.5 month payback
- Transformative operational impact
- Scalable for future growth
- Competitive advantage

**Next Steps:**
1. Obtain executive approval (Dec 15)
2. Form project team (Dec 16-20)
3. Kick-off meeting (Dec 23)
4. Start development (Jan 2)
5. Launch pilot (Feb 1)
6. Full launch (Mar 1)

---

## 📞 CONTACTS

**Document Owner:** [Product Manager to be assigned]
**Technical Contact:** [Engineering Lead to be assigned]
**Timeline:** 60 days from approval
**Budget:** HKD 800,000

---

**Last Updated:** 2025-11-24
**Version:** 1.0
**Status:** Ready for Approval
