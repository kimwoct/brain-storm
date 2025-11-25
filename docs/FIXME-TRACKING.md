# [FIXME] Tracking Document

**Project:** Prestige Health Dispatch System (PHC)
**Document Version:** 1.5
**Date:** November 25, 2025
**Status:** Management Review Required

---

## 🚨 Critical [FIXME] Items

### CRITICAL #1: Security - TLS Version
**Location:** Section 9.3 Security
**Issue:** TLS 1.1 is deprecated and insecure
**Required Action:** Change to TLS 1.3 before implementation
**Priority:** BLOCKING - Must resolve before development starts
**Owner:** Security Team / Infrastructure Team
**Deadline:** Before Phase 1 Week 1

**Current State:**
```
TLS 1.1 or higher (HTTPS)
```

**Required State:**
```
TLS 1.3 (HTTPS)
```

**Impact:** Security vulnerability, compliance failure, potential data breach
**Blocker:** YES - Cannot proceed to development without this fix

---

## 📋 High Priority [FIXME] Items

### HIGH #1: User Roles Definition
**Location:** Section 1.2 System Context
**Content:** "Nursing assistants (recipients of assignments), different roles, such as...[fixme]"
**Required Action:** Define all nursing assistant role types
**Priority:** HIGH - Needed for user management and permissions
**Owner:** HR Department / Product Owner
**Estimated Effort:** 2 hours (meeting with HR)
**Deadline:** Phase 1 Week 1

**Questions to Answer:**
- What are the different nursing assistant role types? (e.g., RN, EN, HCA, PCA)
- Do different roles have different permission levels?
- Do roles affect matching priority or scoring?
- Are there role-specific shift requirements?

---

### HIGH #2: WhatsApp Template Format
**Location:** Section 3.3 (FR-3) Notifications
**Content:** "Template Format: [fixme]"
**Required Action:** Finalize WhatsApp message template format
**Priority:** HIGH - Required for notification implementation
**Owner:** Product Owner / Operations Team
**Estimated Effort:** 4 hours (template design + approval)
**Deadline:** Phase 1 Week 3

**Decisions Needed:**
- Exact message format (currently draft provided)
- Character limits (WhatsApp has limits)
- Bilingual format (English + Traditional Chinese)
- Template variables and formatting
- Emoji usage approval
- Link shortening strategy

**Draft Template (Needs Approval):**
```
🩺 Prestige Health Assignment
📅 Date: {date}
🏥 Location: {location_name}
⏰ Shift: {start_time} - {end_time}
👤 Contact: {contact_person} ({phone})

Please confirm: {confirmation_link}

⚠️ Confirm within 2 hours to secure this shift
```

---

### HIGH #3: Dashboard Widget Specifications
**Location:** Section 3.4 (FR-4) Admin Dashboard
**Content:** "Dashboard Widgets: [fixme]"
**Required Action:** Define specific dashboard widgets and layout
**Priority:** HIGH - Required for UI/UX design
**Owner:** Product Owner / UX Designer
**Estimated Effort:** 8 hours (wireframe + approval)
**Deadline:** Phase 1 Week 2

**Decisions Needed:**
- Which widgets to show on main dashboard?
- Widget priority and layout (grid positions)
- Drill-down capabilities
- Refresh frequencies
- Mobile responsiveness requirements

**Suggested Widgets (Needs Confirmation):**
- Total active assignments
- Pending confirmations
- Unfilled jobs (by urgency)
- Staff availability summary
- Score distribution
- Recent penalties
- System health status
- ERP sync status

---

### HIGH #4: Dashboard Features Priority
**Location:** Section 3.4 (FR-4) Admin Dashboard - Export and Filter
**Content:** 
- "Color-coded status (green/yellow/red) [fixme]"
- "Export to PDF/Excel for management reports [fixme]"
- "Filter by date range, facility, shift type [fixme]"

**Required Action:** Prioritize dashboard features for MVP vs v2.0
**Priority:** HIGH - Affects development scope
**Owner:** Product Owner / Project Manager
**Estimated Effort:** 2 hours (prioritization meeting)
**Deadline:** Phase 1 Week 2

**Decisions Needed:**
- Which features are MVP (v1.0) vs future (v2.0)?
- Color coding: What thresholds for green/yellow/red?
- Export formats: PDF only, Excel only, or both?
- Filter combinations: Which filters are most critical?

---

## 📅 Medium Priority [FIXME] Items

### MED #1: ERP Sync Schedules
**Location:** Section 3.5 (FR-5) ERP Integration - Multiple APIs
**Content:** Multiple sync timing markers
**Required Action:** Confirm all ERP sync schedules with ERP team
**Priority:** MEDIUM - Can adjust during development
**Owner:** Backend Developer / ERP Team
**Estimated Effort:** 2 hours (coordination meeting)
**Deadline:** Phase 1 Week 2

**Sync Schedules to Confirm:**

| API | Current Schedule | Needs Confirmation |
|-----|------------------|-------------------|
| GET /api/v1/staff/active | Daily 02:00 AM | ✓ |
| GET /api/v1/staff/availability | Daily 02:30 AM | ✓ |
| GET /api/v1/staff/{id}/documents | Weekly | ✓ (which day/time?) |
| GET /api/v1/locations/active | Daily 03:00 AM | ✓ |
| GET /api/v1/locations/{id}/preferences | Daily 03:30 AM | ✓ |
| GET /api/v1/jobs/demands | Every 15 min (09:00-22:00) | ✓ |
| GET /api/v1/settlements/{id} | Monthly (1st of month) | ✓ (what time?) |
| POST /api/v1/jobs/assignments | Real-time | ✓ |

---

### MED #2: Notification Trigger Timings
**Location:** Section 3.3 (FR-3) Notifications
**Content:** Multiple notification timing markers
**Required Action:** Confirm exact notification trigger times
**Priority:** MEDIUM - Can adjust after initial testing
**Owner:** Product Owner / Operations Team
**Estimated Effort:** 1 hour
**Deadline:** Phase 1 Week 3

**Timings to Confirm:**

| Notification Type | Current Timing | Needs Confirmation |
|-------------------|----------------|-------------------|
| Assignment notification | Immediately after coordinator marks sent | ✓ |
| Pending confirmation reminder | 2 hours after assignment (if not confirmed) | ✓ |
| Day-before reminder | 24 hours before shift start | ✓ |
| Admin confirmation notification | Staff applies shift | ✓ |
| Scheduled reminders | 2h and 24h intervals | ✓ |

---

### MED #3: Attendance Field Requirements
**Location:** Section 3.6 (FR-6) Attendance Tracking
**Content:** 
- "Fields: assignment_id, staff_id, location_id, actual_hours, status [fixme]"
- "Status: completed, partial [fixme]"

**Required Action:** Finalize attendance data fields and status values
**Priority:** MEDIUM - Needed before Phase 2
**Owner:** Product Owner / ERP Team
**Estimated Effort:** 2 hours
**Deadline:** Phase 1 Week 4

**Decisions Needed:**
- Complete list of required fields
- Status values: just "completed" and "partial" or more?
- How to handle early departure/late arrival?
- Verification method tracking requirements

**Current v1.5 Note:** Clock_in/clock_out removed, only actual_hours and status

---

### MED #4: Emergency File Regions Configuration
**Location:** Section 3.8 (FR-8) Emergency File Upload
**Content:** "Regions (Optional): HKI/KLN/NT (select multiple) [fixme]"
**Required Action:** Confirm region configuration requirements
**Priority:** MEDIUM - Feature for v1.0 but not critical path
**Owner:** Product Owner / Operations Team
**Estimated Effort:** 1 hour
**Deadline:** Phase 2 Week 5

**Decisions Needed:**
- Is region filtering required for MVP?
- Region abbreviations correct? (HKI/KLN/NT = Hong Kong Island/Kowloon/New Territories)
- Should this be multi-select or single select?
- Default behavior if no region selected (all regions?)

---

## 📝 Low Priority [FIXME] Items (Can Defer)

### LOW #1: Data Model Validation
**Location:** Section 4. Data Model [FIXME]
**Required Action:** Complete data model review and validation
**Priority:** LOW - Model is functional, just needs formal review
**Owner:** Database Architect / Backend Lead
**Estimated Effort:** 4 hours
**Deadline:** Phase 1 Week 3

**Review Points:**
- Field types and constraints correct?
- Relationships properly defined?
- Indexes sufficient for queries?
- Any missing fields or tables?

---

### LOW #2: Performance Requirements Validation
**Location:** Section 9.1 Performance [FIXME]
**Required Action:** Validate performance targets are realistic for MVP
**Priority:** LOW - v1.5 already adjusted to realistic targets
**Owner:** Technical Lead / DevOps
**Estimated Effort:** 2 hours
**Deadline:** Phase 1 Week 4

**Current v1.5 Adjusted Targets:**
- Page load: 30s (adjusted from 3s)
- API response: 5000ms (adjusted from 500ms)
- Matching: 10min (adjusted from 5min)
- DB query: 500ms (adjusted from 100ms)

**Validation:** Are these acceptable for MVP? Can we improve post-launch?

---

### LOW #3: Scalability Targets
**Location:** Section 9.2 Scalability [FIXME]
**Required Action:** Confirm scalability targets
**Priority:** LOW - v1.5 clarified 500+ initially, 5000+ scalable
**Owner:** Technical Lead / Infrastructure Team
**Estimated Effort:** 2 hours
**Deadline:** Phase 2 Week 6

**Current Targets:**
- Initial: 500+ nursing assistants
- Growth: Scalable to 5000+
- Future: 10,000+ (phase 2+)

**Validation:** Infrastructure plan to support growth path?

---

### LOW #4: Security Standards Review
**Location:** Section 9.3 Security [FIXME]
**Required Action:** Complete security review (after TLS fix)
**Priority:** LOW (except TLS 1.1 which is CRITICAL)
**Owner:** Security Team
**Estimated Effort:** 4 hours
**Deadline:** Phase 1 Week 4

**Review Points:**
- Authentication standards
- Authorization model
- Data encryption (at rest and in transit)
- Session management (JWT expiration now 8 hours - needs review)
- Audit logging requirements
- Compliance requirements (PDPO, etc.)

---

### LOW #5: Reliability Metrics
**Location:** Section 9.4 Reliability [FIXME]
**Required Action:** Define SLA targets and monitoring
**Priority:** LOW - Can define after MVP launch
**Owner:** DevOps / Operations Team
**Estimated Effort:** 2 hours
**Deadline:** Phase 3 Week 9

**Metrics to Define:**
- Uptime SLA (99%? 99.9%?)
- Mean time to recovery (MTTR)
- Mean time between failures (MTBF)
- Error rate thresholds
- Alerting rules

---

### LOW #6: Deployment Strategy
**Location:** Section 10. Deployment [FIXME]
**Required Action:** Finalize deployment plan
**Priority:** LOW - Can define during development
**Owner:** DevOps / Technical Lead
**Estimated Effort:** 4 hours
**Deadline:** Phase 3 Week 10

**Decisions Needed:**
- Cloud provider selection (if not decided)
- CI/CD pipeline setup
- Blue-green deployment strategy?
- Rollback procedures
- Database migration strategy

---

### LOW #7: Future Enhancement Prioritization
**Location:** Section 12. Future Enhancements [FIXME]
**Required Action:** Prioritize post-MVP enhancements
**Priority:** LOW - For v2.0 planning
**Owner:** Product Owner / Stakeholders
**Estimated Effort:** 4 hours (roadmap meeting)
**Deadline:** Before MVP launch (Week 11)

**Enhancements to Prioritize:**
- QR Code System (facility ID and attendance)
- Geographic intelligence (distance-based matching)
- WhatsApp Business API automation
- Predictive analytics
- Native mobile app
- Advanced fair sharing algorithm

---

## 📊 Summary Statistics

### By Priority
- **CRITICAL:** 1 item (TLS 1.3) ⚠️ BLOCKING
- **HIGH:** 4 items (roles, templates, dashboard, features)
- **MEDIUM:** 4 items (sync schedules, notifications, attendance, regions)
- **LOW:** 7 items (data model, performance, scalability, security, reliability, deployment, enhancements)

**Total:** 16 [FIXME] items

### By Owner
- **Security/Infrastructure Team:** 2 items (1 CRITICAL)
- **Product Owner:** 7 items
- **HR Department:** 1 item
- **Backend Developer/ERP Team:** 2 items
- **UX Designer:** 1 item
- **Database Architect:** 1 item
- **Technical Lead/DevOps:** 4 items

### By Deadline
- **Phase 1 Week 1:** 2 items (including 1 CRITICAL)
- **Phase 1 Week 2:** 3 items
- **Phase 1 Week 3:** 3 items
- **Phase 1 Week 4:** 3 items
- **Phase 2 Week 5-6:** 2 items
- **Phase 3 Week 9-11:** 3 items

---

## 🎯 Resolution Workflow

### For Each [FIXME] Item:

1. **Identification** ✓ (Completed in this document)
2. **Assignment** - Assign to appropriate owner
3. **Scheduling** - Add to project timeline
4. **Resolution** - Owner completes decision/action
5. **Documentation** - Update PRD with final decision
6. **Validation** - Review and approve changes
7. **Closure** - Mark [FIXME] as resolved

### Tracking Status:

- [ ] **CRITICAL #1 - TLS 1.3:** ⏳ PENDING URGENT RESOLUTION
- [ ] **HIGH #1 - User Roles:** ⏳ Pending HR input
- [ ] **HIGH #2 - WhatsApp Template:** ⏳ Pending approval
- [ ] **HIGH #3 - Dashboard Widgets:** ⏳ Pending UX design
- [ ] **HIGH #4 - Dashboard Features:** ⏳ Pending prioritization
- [ ] **MED #1 - ERP Sync Schedules:** ⏳ Pending ERP team coordination
- [ ] **MED #2 - Notification Timings:** ⏳ Pending confirmation
- [ ] **MED #3 - Attendance Fields:** ⏳ Pending finalization
- [ ] **MED #4 - Emergency Regions:** ⏳ Pending confirmation
- [ ] **LOW #1 - Data Model:** ⏳ Can defer
- [ ] **LOW #2 - Performance:** ⏳ Can defer
- [ ] **LOW #3 - Scalability:** ⏳ Can defer
- [ ] **LOW #4 - Security Review:** ⏳ Can defer (after CRITICAL #1)
- [ ] **LOW #5 - Reliability:** ⏳ Can defer
- [ ] **LOW #6 - Deployment:** ⏳ Can defer
- [ ] **LOW #7 - Future Enhancements:** ⏳ Can defer

---

## 📧 Stakeholder Communication

### Immediate Actions Required

**To: Security Team / Infrastructure Team**
**Subject:** URGENT - TLS 1.1 Security Issue in PHC Specification
**Priority:** CRITICAL - BLOCKING

The PRD currently specifies TLS 1.1 which is deprecated and insecure. This must be changed to TLS 1.3 before development begins. Please confirm update by end of week.

---

**To: Product Owner + HR Department**
**Subject:** PRD Review Required - 4 High Priority Decisions Needed
**Priority:** HIGH - Needed for Phase 1

Please review and provide decisions on:
1. Nursing assistant role types definition
2. WhatsApp template format approval
3. Dashboard widget specifications
4. Dashboard feature prioritization (MVP vs v2.0)

Deadline: End of Phase 1 Week 2

---

**To: ERP Team**
**Subject:** ERP Sync Schedule Confirmation Required
**Priority:** MEDIUM

Please confirm the following sync schedules work for ERP system:
- Daily syncs: 02:00, 02:30, 03:00, 03:30
- Polling: Every 15 minutes (09:00-22:00)
- Real-time: Assignment submissions

Also need to finalize attendance field requirements.

Deadline: End of Phase 1 Week 2

---

## 📅 Next Review

**Review Meeting:** Phase 1 Week 1 - Kickoff
**Attendees:** Project Manager, Product Owner, Technical Lead, Security Team
**Agenda:**
1. Resolve CRITICAL #1 (TLS 1.3)
2. Assign owners for HIGH priority items
3. Set deadlines for MEDIUM priority items
4. Review overall [FIXME] resolution plan

**Next Review:** Phase 1 Week 4 - [FIXME] Resolution Progress Check

---

**Document Status:** ✅ COMPLETE - All [FIXME] items identified and categorized
**Next Action:** Distribute to stakeholders and schedule resolution meetings
**Owner:** Project Manager
**Last Updated:** November 25, 2025
