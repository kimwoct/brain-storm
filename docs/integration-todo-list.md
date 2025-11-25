# ERP Integration Implementation Checklist

**Project:** Prestige Health Dispatch System (PHC)
**Document Version:** 1.5 (Human Screening Workflow)
**Last Updated:** 2025-11-25
**Status:** Updated for v1.5 PRD - Application/Approval Workflow

---

## 🎯 Executive Summary

This checklist outlines the step-by-step implementation plan for integrating PHC with the existing ERP system across the 4 main business flows.

**Critical Path:** Master Data Sync → Job Posting → **Staff Application & Admin Screening (v1.5)** → Assignment → Settlement

**⚠️ v1.5 MAJOR WORKFLOW CHANGE:**
- **From:** Automated matching with staff confirmation
- **To:** Staff application with admin screening/approval
- **Impact:** FR-2 becomes recommendation engine (not auto-assignment), new application workflow UIs required, assignment API triggered by admin approval (not system matching)

---

## 🔄 v1.5 Workflow Changes - Implementation Impact

### Critical Changes from v1.0 to v1.5

#### 1. Assignment Workflow Paradigm Shift
- **OLD (v1.0):** System matches staff → Staff confirms/rejects → ERP updated
- **NEW (v1.5):** Staff applies → Admin screens → Admin approves → ERP updated

#### 2. FR-2 Matching Engine Redefined
- **OLD:** Auto-assignment based on rules
- **NEW:** Ranking/recommendation engine to assist admin screening
- **Implementation:** Keep scoring/filtering logic, remove auto-assignment trigger

#### 3. New UI Components Required
- [ ] Staff application interface (browse and apply for shifts)
- [ ] Admin screening dashboard (pending applications queue)
- [ ] Admin approval workflow (approve/reject with reasons)
- [ ] Application status tracking (applied → approved/rejected → confirmed)

#### 4. ERP API Timing Changes
- **OLD:** API 3.1 (POST assignments) triggered by system matching
- **NEW:** API 3.1 triggered by **admin approval action**
- **NEW Status:** "applied" state added (before "approved")

#### 5. Notification Flow Updates
- **Added:** "Shift available - apply now" notification
- **Added:** "Application received" confirmation
- **Added:** "Application approved" notification
- **Added:** "Application rejected" notification
- **Changed:** Confirmation notification now sent **after** admin approval

### Implementation Priority Updates

#### High Priority (Blocking MVP):
- [ ] **Update workflow appendices** - Cv1, Cv2, B documents need v1.5 rewrite
- [ ] **Build application UIs** - Staff application + admin screening interfaces
- [ ] **Refactor matching engine** - From auto-assignment to recommendation
- [ ] **Update API triggers** - Assignment creation now admin-driven

#### Medium Priority:
- [ ] **Update terminology** - "match" → "recommend", "confirm" → "apply/approve"
- [ ] **Notification templates** - Add application-related notifications
- [ ] **Status tracking** - Expand to include application states

### Workflow Documentation Alignment

#### Documents Requiring Updates:
- [ ] `06 - Appendix Cv1 - Matching & Confirmation Flow.md` - Rewrite for human screening
- [ ] `06 - Appendix Cv2 - Matching & Confirmation Flow.md` - Fair sharing now manual admin control
- [ ] `05 - Appendix B - Job Posting flow.md` - Change "grab shift" to "apply for shift"
- [ ] `07 - Appendix Dv1 - Cancellation flow.md` - Minor terminology updates
- [ ] `08 - Appendix E - Push Notification Flow.md` - Add application notifications

#### Documents Already Aligned:
- [x] `Product Specification Document ALIGNED Revised.md` (v1.5) - Updated
- [x] `dataflow-phc-erp-integration.excalidraw` - Shows human screening workflow
- [x] `04 - Appendix A - Registration flow.md` - No workflow dependency

---

## 📋 Pre-Implementation Requirements

### ERP Team Coordination (Must Complete First)
- [ ] Schedule kickoff meeting with ERP team
- [ ] Obtain complete API documentation (Swagger/OpenAPI format preferred)
- [ ] Secure access to ERP test/sandbox environment
- [ ] Receive API credentials (API keys, OAuth tokens)
- [ ] Confirm API rate limits (requests per minute/hour)
- [ ] Define SLA (target response times)
- [ ] Get escalation contacts (technical & business)
- [ ] Establish communication channel (Slack/Teams)
- [ ] Confirm webhook capability and obtain webhook documentation
- [ ] Schedule weekly sync meetings during implementation

**Estimated Time:** 1 week
**Owner:** Project Manager
**Dependencies:** ERP team availability
**Deliverable:** API access and documentation

---

## 🔷 Phase 1: Core Integration (Weeks 1-4) - CRITICAL PATH

### Week 1: API Foundation & Authentication

#### Authentication Setup
- [ ] Set up API authentication (OAuth 2.0 or API keys)
- [ ] Configure secure credential storage (encrypted)
- [ ] Implement token refresh logic (if using OAuth)
- [ ] Create API health check endpoint
- [ ] Test connectivity to ERP test environment
- [ ] Implement API request/response logging
- [ ] Set up error tracking and alerting

**Owner:** Backend Developer
**Review:** Security audit of credential storage
**Deliverable:** Secure API connection established

### Week 2: Master Data Sync - Staff & Locations

#### Staff Synchronization
- [ ] Implement API 1.1 (GET /api/v1/staff/active) - Staff list sync
- [ ] Create daily staff sync job (run at 02:00 AM)
- [ ] Build staff data validation (HKID format, contact numbers)
- [ ] Implement duplicate detection logic (by erp_staff_id)
- [ ] Handle new staff onboarding (create PHC accounts)
- [ ] Handle staff status changes (active/inactive)
- [ ] Alert admin for validation failures
- [ ] Create staff sync monitoring dashboard

**Owner:** Backend Developer
**Test:** Verify staff sync with 100+ test records
**Deliverable:** Automated staff sync operational

#### Staff Availability
- [ ] Implement API 1.2 (GET /api/v1/staff/availability)
- [ ] Map availability data to PHC shift calendar
- [ ] Handle availability conflicts (already assigned shifts)
- [ ] Create availability validation rules
- [ ] Test multi-day availability sync (7+ days)

**Owner:** Backend Developer
**Test:** Availability accuracy verification
**Deliverable:** Daily availability sync working

#### Location Synchronization
- [ ] Implement API 2.1 (GET /api/v1/locations/active)
- [ ] Create daily location sync job (run at 03:00 AM)
- [ ] Build location data validation
- [ ] Implement duplicate detection (by erp_location_id)
- [ ] Handle new locations (auto-create in PHC)
- [ ] Handle location status changes
- [ ] Create location sync monitoring

**Owner:** Backend Developer
**Test:** Location sync accuracy
**Deliverable:** Automated location sync operational

#### Location Preferences
- [ ] Implement API 2.3 (GET /api/v1/locations/{id}/preferences)
- [ ] Sync underlist staff (priority list)
- [ ] Sync blacklisted staff
- [ ] Map special requirements to PHC
- [ ] Test preference filtering in matching

**Owner:** Backend Developer
**Test:** Preference-based matching accuracy
**Deliverable:** Location preferences integrated

### Week 3: Job Demand Integration

#### Demand Polling
- [ ] Implement API 2.2 (GET /api/v1/jobs/demands)
- [ ] Create demand polling job (every 15 minutes)
- [ ] Filter demands by status (open/unfilled)
- [ ] Map demand fields to PHC job postings
- [ ] Handle new demands (auto-create postings)
- [ ] Handle demand updates (priority changes, counts)
- [ ] Handle demand cancellations (close postings)
- [ ] Validate shift times and required counts
- [ ] Create demand sync monitoring

**Owner:** Backend Developer
**Test:** Demand sync latency (< 15 min target)
**Deliverable:** Job demands syncing automatically

#### Webhook Implementation (Optional but Recommended)
- [ ] Create webhook endpoint: POST /webhook/erp/job-demand
- [ ] Implement webhook authentication/validation
- [ ] Parse webhook payload
- [ ] Process demand in real-time (skip polling delay)
- [ ] Register webhook URL in ERP system
- [ ] Test webhook delivery
- [ ] Implement webhook failure handling
- [ ] Create webhook monitoring dashboard

**Owner:** Backend Developer
**Test:** Webhook latency (< 1 min)
**Deliverable:** Real-time demand processing via webhook

### Week 4: Assignment Management

#### Staff Application & Admin Screening (v1.5 Workflow)
- [x] **WORKFLOW CHANGE:** Staff now **apply** for shifts (not auto-assigned)
- [x] **WORKFLOW CHANGE:** Admin performs manual **screening/approval** (not automated matching)
- [ ] Build staff application interface (browse available shifts)
- [ ] Create application submission workflow
- [ ] Build admin screening dashboard (view all applications)
- [ ] Implement admin approval/rejection interface
- [ ] Create application queue management
- [ ] Build ranking/recommendation engine (FR-2) to assist admin screening
- [ ] Display underlist priority flag to admin during screening
- [ ] Show staff scores and history during screening
- [ ] Implement conflict checking during approval
- [ ] Create fair sharing alerts for admin (max 5 jobs per staff)

**Owner:** Backend + Frontend Developer
**Test:** Application workflow end-to-end
**Deliverable:** Human screening workflow operational

#### Assignment Submission to ERP
- [ ] Implement API 3.1 (POST /api/v1/jobs/assignments)
- [ ] Trigger API call when **admin approves** staff application (v1.5 change)
- [ ] Map PHC assignment to ERP format
- [ ] Handle successful submission (store ERP assignment_id)
- [ ] Handle conflict errors (staff unavailable)
- [ ] Implement re-notification to admin on conflict
- [ ] Create assignment submission logs

**Owner:** Backend Developer
**Test:** Assignment submission success rate > 99%
**Deliverable:** Approved assignments syncing to ERP in real-time

#### Assignment Status Updates
- [ ] Implement API 3.2 (PATCH /api/v1/jobs/assignments/{id})
- [ ] Update status: applied (staff submits application)
- [ ] Update status: approved (admin approves application)
- [ ] Update status: rejected (admin rejects application)
- [ ] Update status: confirmed (staff accepts approval)
- [ ] Update status: cancelled (staff cancels after approval)
- [ ] Include application timestamp
- [ ] Include approval/rejection timestamp
- [ ] Include confirmation timestamp
- [ ] Include cancellation reason
- [ ] Track complete application-to-assignment history

**Owner:** Backend Developer
**Test:** Status update accuracy
**Deliverable:** Assignment lifecycle tracking operational

#### Reconciliation
- [ ] Implement API 3.3 (GET assignment status verification)
- [ ] Create hourly reconciliation job
- [ ] Compare PHC vs ERP assignment status
- [ ] Flag discrepancies for review
- [ ] Auto-correct minor mismatches
- [ ] Alert admin for major discrepancies

**Owner:** Backend Developer
**Test:** Reconciliation accuracy 100%
**Deliverable:** Automated discrepancy detection

**Phase 1 Deliverable:** Core data flows operational (Staff, Locations, Demands, Assignments)
**Go/No-Go Criteria:** All critical APIs tested and working

---

## 🔷 Phase 2: Attendance & Settlement (Weeks 5-8) - HIGH PRIORITY

### Week 5: Attendance Tracking

#### Attendance Submission
- [ ] Implement API 4.1 (POST /api/v1/attendance)
- [ ] Build clock-in/out interface (QR code scanner)
- [ ] Create manual attendance entry (supervisor)
- [ ] Capture clock times and calculate hours
- [ ] Include verification method (QR/signature/manual)
- [ ] Submit attendance at shift completion
- [ ] Handle partial attendance (early leave/late arrival)
- [ ] Create attendance audit log

**Owner:** Backend + Frontend Developer
**Test:** Attendance accuracy and timing
**Deliverable:** Attendance tracking working

#### Attendance Validation
- [ ] Validate clock-in time (not too early)
- [ ] Validate clock-out time (not too late)
- [ ] Calculate actual hours vs scheduled
- [ ] Flag significant deviations (> 1 hour)
- [ ] Require supervisor approval for deviations
- [ ] Create attendance reports

**Owner:** Backend Developer
**Test:** Deviation handling
**Deliverable:** Attendance validation rules implemented

### Week 6: Penalty Management

#### Penalty Calculation Engine
- [ ] Build penalty rules engine:
  - [ ] Cancellation (with notice): -1 score, -100 HKD
  - [ ] No-show (absent): -2 score, -100 HKD
- [ ] Create warning UI modal
- [ ] Warning message: "100HKD will be deducted when you apply AL within 48 hours before coming job!"
- [ ] Implement accept/reject buttons for cancellation
- [ ] Apply penalties immediately when accepted
- [ ] Queue penalty for batch processing
- [ ] Create penalty audit trail

**Owner:** Backend + Frontend Developer
**Test:** Penalty calculation accuracy
**Deliverable:** Penalty system operational

#### Penalty Submission to ERP
- [ ] Implement API 4.2 (POST /api/v1/penalties)
- [ ] Submit penalty when cancellation accepted
- [ ] Submit penalty when no-show recorded
- [ ] Include penalty reason and amount
- [ ] Track submission status
- [ ] Handle submission failures (retry logic)

**Owner:** Backend Developer
**Test:** 100% penalty submission success
**Deliverable:** Penalties syncing to ERP

#### Financial Deduction Integration
- [ ] **TBD API Specification** - Work with ERP team to define
- [ ] Implement financial deduction API call
- [ ] Trigger deduction when penalty applied
- [ ] Track deduction status
- [ ] Handle deduction failures
- [ ] Create deduction reports for finance

**Owner:** Backend Developer
**Dependencies:** ERP team to provide API spec
**Deliverable:** Financial deductions processed

### Week 7: Score Management

#### Score Tracking
- [ ] Implement API 4.4 (PATCH /api/v1/staff/{id}/score)
- [ ] Update score when:
  - [ ] Staff attends shift: +1
  - [ ] Staff cancels: -1
  - [ ] Staff no-show: -2
- [ ] Track score history (audit log)
- [ ] Calculate current score
- [ ] Determine tier (Gold/Silver/Bronze/Negative)
- [ ] Sync score to ERP in real-time

**Owner:** Backend Developer
**Test:** Score calculation accuracy
**Deliverable:** Score tracking operational

#### Score-Based Allocation
- [ ] Implement tier-based allocation priority:
  - [ ] Gold (20+): First priority
  - [ ] Silver (10-19): Second priority
  - [ ] Bronze (0-9): Third priority
  - [ ] Negative (< 0): Manual review
- [ ] Display staff tier in matching interface
- [ ] Sort candidate list by score (descending)
- [ ] Test allocation with various score scenarios

**Owner:** Backend Developer
**Test:** Tier-based allocation accuracy
**Deliverable:** Score-based matching implemented

#### Score Recovery
- [ ] Implement time decay (if applicable)
- [ ] Set minimum score floor (recommendation: -10)
- [ ] Create score boost for consistent attendance
- [ ] Build manual score adjustment (admin only)
- [ ] Create score reports for management

**Owner:** Backend Developer
**Test:** Score recovery scenarios
**Deliverable:** Score management complete

### Week 8: Settlement Reconciliation

#### Payment Reconciliation
- [ ] Implement API 4.3 (GET /api/v1/settlements/{id})
- [ ] Create monthly settlement job (1st of month)
- [ ] Pull settlement data from ERP
- [ ] Compare with PHC records
- [ ] Verify gross payment, hours, penalties
- [ ] Flag discrepancies for review
- [ ] Generate settlement reports

**Owner:** Backend Developer
**Test:** Reconciliation accuracy
**Deliverable:** Settlement reconciliation working

#### Reporting
- [ ] Create settlement summary report
- [ ] Generate penalty summary report
- [ ] Build attendance summary report
- [ ] Create monthly summaries for finance
- [ ] Export to Excel/PDF
- [ ] Email reports to stakeholders

**Owner:** Backend + Frontend Developer
**Deliverable:** Reporting module complete

**Phase 2 Deliverable:** Complete attendance and settlement flow
**Go/No-Go Criteria:** Penalties and payments processing correctly

---

## 🔷 Phase 3: Automation & Monitoring (Weeks 9-10) - MEDIUM PRIORITY

### Week 9: Job Automation

#### Cron Jobs Setup
- [ ] Configure all scheduled jobs:
  - [ ] Staff sync: Daily 02:00
  - [ ] Location sync: Daily 03:00
  - [ ] Demand poll: Every 15 min
  - [ ] Assignment verification: Hourly
  - [ ] Settlement: Monthly 1st @ 02:00
- [ ] Set up job monitoring (success/failure)
- [ ] Create job failure alerts (email/Slack)
- [ ] Build job retry logic (exponential backoff)
- [ ] Create job dashboard (view all job statuses)

**Owner:** Backend Developer
**Deliverable:** All jobs running automatically

#### Retry Logic
- [ ] Implement retry for failed API calls:
  - [ ] Attempt 1: Immediate
  - [ ] Attempt 2: After 5 minutes
  - [ ] Attempt 3: After 15 minutes
- [ ] Log all retry attempts
- [ ] Alert if still failing after 3 attempts
- [ ] Create queue for failed jobs
- [ ] Manual retry interface for admins

**Owner:** Backend Developer
**Test:** Retry behavior with simulated failures
**Deliverable:** Resilient error handling

### Week 10: Monitoring & Alerting

#### API Monitoring
- [ ] Implement API health checks (every 5 minutes)
- [ ] Monitor API response times
- [ ] Alert if response time > 3 seconds
- [ ] Alert if API error rate > 5%
- [ ] Create API performance dashboard
- [ ] Generate weekly API performance reports

**Owner:** Backend Developer
**Deliverable:** API monitoring operational

#### Data Quality Monitoring
- [ ] Create data quality checks:
  - [ ] Staff completeness (all required fields)
  - [ ] Location completeness
  - [ ] Assignment status consistency
- [ ] Generate daily data quality reports
- [ ] Alert on data anomalies
- [ ] Create data correction workflows

**Owner:** Backend Developer
**Deliverable:** Data quality monitoring active

#### Alerting System
- [ ] Set up email notifications for:
  - [ ] Sync failures
  - [ ] API errors
  - [ ] Data quality issues
  - [ ] System errors
- [ ] Set up Slack integration (optional)
- [ ] Configure alert recipients
- [ ] Create alert severity levels (Info/Warning/Critical)

**Owner:** Backend Developer
**Test:** Alert delivery verification
**Deliverable:** Alerting system active

**Phase 3 Deliverable:** Automated monitoring and alerting
**Go/No-Go Criteria:** All jobs stable, alerts working

---

## 🔷 Phase 4: Optimization & Enhancement (Weeks 11-12) - LOW PRIORITY

### Week 11: Performance Optimization

#### Caching
- [ ] Implement Redis cache for:
  - [ ] Staff data (TTL: 1 hour)
  - [ ] Location data (TTL: 1 hour)
  - [ ] Demand data (TTL: 15 min)
- [ ] Build cache invalidation logic
- [ ] Monitor cache hit rates
- [ ] Optimize cache memory usage

**Owner:** Backend Developer
**Test:** Performance improvement measurement
**Deliverable:** Caching layer operational

#### Bulk Operations
- [ ] Implement bulk sync (batch multiple records)
- [ ] Reduce API call overhead
- [ ] Optimize database queries
- [ ] Performance testing (1000+ records)
- [ ] Measure sync time improvements

**Owner:** Backend Developer
**Deliverable:** Performance optimized

### Week 12: Documentation & Finalization

#### Technical Documentation
- [ ] Document all API integrations
- [ ] Create runbook for operations team
- [ ] Document troubleshooting procedures
- [ ] Create API credential rotation procedure
- [ ] Document data mapping specifications
- [ ] Create deployment guide

**Owner:** Backend Developer
**Deliverable:** Complete technical documentation

#### User Documentation
- [ ] Create user guide for admin interface
- [ ] Document monitoring dashboard usage
- [ ] Create error resolution procedures
- [ ] Document reporting features
- [ ] Create training materials

**Owner:** Technical Writer
**Deliverable:** User documentation complete

**Phase 4 Deliverable:** System optimized and documented
**Go/No-Go Criteria:** All documentation complete, performance targets met

---

## 📊 Success Metrics

### Phase 1 Success Criteria
- [ ] Staff sync success rate: > 99%
- [ ] Location sync success rate: > 99%
- [ ] Demand sync latency: < 15 minutes
- [ ] Assignment submission success: > 99%
- [ ] API uptime: > 99%
- [ ] **v1.5:** Application submission success: > 99%
- [ ] **v1.5:** Admin screening interface response time: < 3 seconds

### Phase 2 Success Criteria
- [ ] Attendance submission success: > 99%
- [ ] Penalty calculation accuracy: 100%
- [ ] Score tracking accuracy: 100%
- [ ] Settlement reconciliation match: > 99%

### Overall Project Success
- [ ] All 4 main flows operational
- [ ] Zero critical data loss
- [ ] API response time: < 3 seconds average (< 30 seconds MVP target per v1.5 PRD)
- [ ] Monthly settlement processing: automated
- [ ] **v1.5:** Staff can browse and apply for shifts successfully
- [ ] **v1.5:** Admin can screen and approve applications efficiently
- [ ] **v1.5:** Application-to-assignment workflow < 2 hours (manual screening time included)

---

## 🚦 Go-Live Readiness Checklist

Before production launch:

### Technical Readiness
- [ ] All Phase 1 tasks complete
- [ ] All Phase 2 tasks complete
- [ ] All APIs tested and stable
- [ ] Monitoring and alerting operational
- [ ] Documentation complete
- [ ] Operations team trained
- [ ] Rollback plan documented
- [ ] Load testing passed
- [ ] Security audit passed
- [ ] User acceptance testing passed

### v1.5 Workflow Readiness
- [ ] Staff application interface tested and approved
- [ ] Admin screening dashboard tested and approved
- [ ] Application workflow end-to-end testing completed
- [ ] Admin team trained on screening process
- [ ] Workflow documentation updated (Appendices Cv1, Cv2, B)
- [ ] FR-2 recommendation engine validated by admins
- [ ] Application status tracking verified
- [ ] Notification templates approved (application/approval messages)

### Business Readiness
- [ ] Business stakeholders approval obtained
- [ ] Staff onboarding plan for application workflow
- [ ] Admin screening procedures documented
- [ ] Escalation procedures for edge cases defined
- [ ] Performance metrics baseline established

---

## 🔴 Risk Mitigation

### High Risk Items

1. **v1.5 Workflow Change Adoption**
   - Risk: Staff and admins may resist application/screening workflow
   - Mitigation: Clear communication, training, phased rollout
   - Contingency: Temporary admin auto-approval mode for familiar users

2. **ERP API not ready**
   - Mitigation: Parallel development with mock APIs
   - Contingency: Manual data entry bridge

3. **Webhook unreliable**
   - Mitigation: Robust polling fallback
   - Contingency: Increase polling frequency

4. **Data quality issues**
   - Mitigation: Strong validation rules
   - Contingency: Manual data correction workflows

5. **Performance issues**
   - Mitigation: Caching and optimization
   - Contingency: Scale infrastructure

6. **Admin screening bottleneck (v1.5)**
   - Risk: Manual screening may slow assignment process
   - Mitigation: Recommendation engine to assist, batch approval features
   - Contingency: Increase admin staffing during peak hours

---

**Next Review Date:** End of Phase 1 (Week 4)
**Checkpoint Meeting:** Weekly every Monday
**Document Owner:** BMAD Analyst (Mary)
