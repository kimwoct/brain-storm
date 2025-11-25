# Product Requirements Document (PRD) Summary
**Prestige Health Dispatch System (PHC)**

**Version:** 1.0
**Date:** 2025-11-24
**Type:** Product Overview (Executive Summary)

---

## 1. PRODUCT OVERVIEW

### 1.1 Product Name
**Prestige Health Dispatch System (PHC)** - "Uber for Healthcare Staffing"

### 1.2 Product Vision

**Vision Statement:**
Transform Prestige Health from manual coordination to intelligent automated staffing, reducing unfilled shifts by 80% and coordinator workload by 75% within 6 months.

**Elevator Pitch:**
PHC automatically matches nursing assistants to care home shifts based on performance scores, availability, and preferences—eliminating manual coordination and creating a fair, transparent merit-based system.

### 1.3 Target Users

| User Segment | Size | Primary Need | Key Pain Point |
|--------------|------|--------------|----------------|
| **Nursing Assistants** | 500+ | Get shift assignments | Want fair, transparent selection |
| **Care Home Supervisors** | 100+ | Verify attendance | Manual verification is time-consuming |
| **PHC Administrators** | 5-10 | Monitor & manage | Need visibility into all operations |
| **ERP Admin** (Backend) | 2-3 | Master data control | Need single source of truth |

---

## 2. PRODUCT SCOPE

### 2.1 In Scope (v1.0)

**Core Features:**
✅ Four-stage workflow automation (Registration, Job Posting, Matching, Settlement)
✅ Scoring system (+1 attend, -1 cancel)
✅ Financial penalties (−300 HKD for cancellation/no-show)
✅ Firebase web push notifications and confirmations
✅ Admin portal for monitoring and overrides
✅ Emergency file upload and distribution
✅ 13 API endpoints for ERP integration
✅ Attendance tracking (QR code OR supervisor verification)
✅ Simple score-rules

**Technical Features:**
✅ Web-based admin portal (React.js)
✅ JavaSpring Boot 2.7+ backend
✅ mySQL database
✅ Bi-directional ERP integration
✅ Web Push Notification with firebase

### 2.2 Out of Scope (v1.0)

**Deferred Features:**
❌ Automated matching algorithm (score-based)
❌ Geographic intelligence (distance-based matching)
❌ Automated fair sharing (manual ERP control)
❌ Mobile app (WhatsApp-only interface for staff)
❌ Advanced ML predictions
❌ Automated emergency triggers
❌ Billing/invoicing beyond penalties (ERP handles)
❌ S3/Azure Blob file storage
❌ Redis caching

**Future Enhancements:**
- Distance-based matching (v2.0)
- Prediction model for demand (v2.0)
- Native mobile app (v2.0)
- Advanced fair sharing algorithm (v2.0)

---

## 3. PRODUCT FEATURES

### 3.1 Feature 1: Scoring & Performance System

**What it is:**
A transparent, merit-based scoring system that rewards reliability and penalizes unreliability.

**How it works:**
- Base score: 5 points for new staff
- Attend: +1 point
- Cancel with notice: -1 point, −100 HKD
- No-show: -2 points, −100 HKD

**Tiers:**
- Gold (20+): First priority
- Silver (10-19): Second priority
- Bronze (0-9): Third priority
- Under Review (<0): Manual review

**User Stories:**
- US-NA-01: View my score
- US-NA-02: Score increases when I attend
- US-NA-03: Penalties for cancellation
- US-NA-04: Penalties for no-show

**Business Value:**
- Fair, transparent allocation
- Self-correcting system
- Motivates reliable behavior

**Effort:** 8 man-days (algorithm + UI)

**Priority:** P0 (Critical)

---

### 3.2 Feature 2: Intelligent Matching Engine

**What it is:**
Algorithm that automatically selects best staff for each shift based on multiple criteria.

**Matching Criteria (Priority Order):**
1. Underlist (previous work history)
2. Score Tier (Gold → Silver → Bronze)
3. Availability (from ERP)
4. Certificate validity
5. Blacklist exclusion
6. Fair sharing limit (from ERP)
7. Manual override (admin)

**User Stories:**
- US-NA-01: Receive assignment notification
- US-NA-02: Confirm assignment
- US-CS-01: View assigned staff
- US-ADM-01: View matching metrics

**Business Value:**
- Reduces fill time from 2-3 hours to 15 minutes
- Eliminates human bias
- Considers multiple factors
- 98% fill rate (vs 85% current)

**Effort:** 12 man-days

**Priority:** P0 (Critical)

---

### 3.3 Feature 3: WhatsApp Integration

**What it is:**
Notification and confirmation system using WhatsApp Business API.

**User Flow:**
1. Assignment created → WhatsApp notification sent
2. Staff clicks "Confirm" or "Cancel"
3. System records response
4. Confirmed → Score increases
5. Cancelled → Warning + penalty applied

**User Stories:**
- US-NA-01: Receive assignment notification
- US-NA-02: Confirm via WhatsApp
- US-NA-03: Cancel with warning

**Business Value:**
- No mobile app needed (95% adoption)
- High engagement (95% open rate)
- Fast responses (2-hour confirmation window)
- Automatic reminders

**Effort:** 8 man-days

**Priority:** P0 (Critical)

---

### 3.4 Feature 4: Admin Portal

**What it is:**
Web-based dashboard for admins to monitor operations and handle exceptions.

**Dashboard Features:**
- Real-time metrics (jobs, confirmations, attendance, penalties)
- Manual assignment override
- System monitoring (API logs, sync status)
- Reporting (settlement, attendance, score reports)

**User Stories:**
- US-ADM-01: View dashboard
- US-ADM-02: Manual assignment
- US-ADM-03: View logs
- US-ADM-04: Upload emergency files
- US-ADM-05: Emergency job posting
- US-ADM-06: View reports

**Business Value:**
- 360° visibility into operations
- Handle exceptions manually
- Monitor system health
- Generate reports for management

**Effort:** 10 man-days

**Priority:** P0 (Critical)

---

### 3.5 Feature 5: Emergency Protocol Management

**What it is:**
Manual system for uploading and distributing emergency protocols.

**Capabilities:**
- Upload files (PDF, DOC, images) up to 10MB
- Set priority (Normal/High/Critical)
- Select regions (HKI/KLN/NT) or all
- Auto-notify affected staff via WhatsApp
- Track views and confirmations
- Emergency job posting (bypasses standard)

**User Stories:**
- US-ADM-04: Upload emergency file
- US-ADM-05: Distribute to staff
- US-ADM-06: Post emergency job

**Business Value:**
- Rapid response capability
- Documented compliance
- Real-time shortage dashboard
- Crisis management

**Effort:** 6 man-days

**Priority:** P1 (High)

---

### 3.6 Feature 6: ERP Integration

**What it is:**
13 API endpoints for bi-directional data sync with existing ERP.

**APIs Included:**

**From ERP → PHC:**
1. GET /api/v1/staff/active (daily sync)
2. GET /api/v1/staff/availability (daily)
3. GET /api/v1/staff/{id}/documents (weekly)
4. GET /api/v1/locations/active (daily)
5. GET /api/v1/locations/{id}/preferences (daily)
6. GET /api/v1/jobs/demands (every 15 min)
7. GET /api/v1/settlements/{id} (monthly)

**From PHC → ERP:**
8. POST /api/v1/jobs/assignments (real-time)
9. PATCH /api/v1/jobs/assignments/{id} (real-time)
10. POST /api/v1/attendance (post-shift)
11. POST /api/v1/penalties (real-time)
12. PATCH /api/v1/staff/{id}/score (real-time)
13. POST /api/v1/finance/deduction (TBD)

**User Stories:**
- US-ERP-01 through US-ERP-06 (system-to-system)

**Business Value:**
- Single source of truth maintained
- No duplicate data entry
- Automatic payroll processing
- Financial data stays in ERP

**Effort:** 12 man-days (all APIs)

**Priority:** P0 (Critical)

---

### 3.7 Feature 7: Attendance Tracking

**What it is:**
System to verify staff actually showed up for shifts.

**Options (to be decided):**
- **Option A:** QR code at location (staff scans with phone)
- **Option B:** Supervisor manual verification in portal

**Features:**
- Clock-in/out time recording
- Actual hours calculation
- Deviation alerts (>1 hour difference)
- No-show detection

**User Stories:**
- US-CS-02: Verify attendance
- US-CS-03: Mark no-shows

**Business Value:**
- Accurate payroll data
- No-show penalty enforcement
- Attendance verification

**Effort:** 6 man-days

**Priority:** P1 (High)

---

## 4. USER EXPERIENCE

### 4.1 Primary Flows

**Nursing Assistant Journey:**
1. **Receive Notification** → WhatsApp includes all shift details
2. **Confirm/Cancel** → One-tap confirmation or cancellation
3. **See Penalty** → Clear warning if cancelling
4. **Get Reminder** → Day before shift
5. **Clock In** → QR scan or supervisor verification
6. **Score Update** → After shift completion

**Admin Journey:**
1. **Dashboard** → See all key metrics at glance
2. **Monitor** → Real-time sync status, API health
3. **Override** → Manual assignment when needed
4. **Emergency** → Upload files or post urgent jobs
5. **Report** → Generate settlement summaries

### 4.2 Design Principles

- **Mobile-First:** Admin portal works on mobile/tablet
- **Speed:** All actions <3 seconds
- **Clarity:** Clear call-to-action buttons
- **Transparency:** Staff can see their score/history
- **Bilingual:** English + Traditional Chinese

---

## 5. IMPLEMENTATION

### 5.1 Technology Stack

**Frontend:**
- React.js 18+ (Vite)
- TailwindCSS
- Redux Toolkit
- Recharts for metrics

**Backend:**
- Java Spring Boot 2.7+
- Spring Security
- JWT Authentication

**Database:**
- MySQL 8+ (primary)
- Redis 6+ (cache, sessions)

**Infrastructure:**
- Cloud-hosted (AWS or Azure)
- S3/Azure Blob for file storage
- Docker containerization

**Integrations:**
- Firebase Cloud Messaging (web push)
- RESTful ERP APIs
- Spring Batch or Quartz (job scheduling)

### 5.2 Development Timeline

**Total: 60 man-days (1.5 months)**

Detailed breakdown in TDD and Integration To-Do List documents.

### 5.3 Team Structure

- **Backend Developers:** 2
- **Frontend Developer:** 1
- **QA/Testing:** 1
- **DevOps/Infrastructure:** 0.5
- **Project Manager:** 0.5 (shared)

**Note:** Backend requires Java Spring Boot expertise

---

## 6. SUCCESS METRICS

### 6.1 Launch Goals (Month 1)

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Shift Fill Rate | 85% | 95%+ | Daily reports |
| No-Show Rate | 5% | <2% | Attendance logs |
| Coordinator Hours/Day | 3 hours | <1 hour | Time tracking |
| System Uptime | N/A | 99.5% | Monitoring |
| Staff Satisfaction | 65% | 80%+ | Quarterly survey |

### 6.2 Adoption Goals (Month 3)

- 90% of staff using WhatsApp confirmations
- 95% of shifts filled within 30 minutes of posting
- 100% of penalties automatically applied
- 100% of attendance automatically synced to ERP

### 6.3 Business Goals (Year 1)

- **Revenue:** HKD 1.2M increase (from improved fill rate)
- **Cost Savings:** HKD 480K (coordinator time reduction)
- **ROI:** 118% (net benefit: HKD 940K)

---

## 7. RISKS & MITIGATION

### 7.1 High Risks

**Risk 1: ERP API delays**
- **Impact:** High
- **Likelihood:** Medium
- **Mitigation:** Parallel dev with mock APIs; manual data bridge

**Risk 2: Timeline overrun**
- **Impact:** High
- **Likelihood:** Medium
- **Mitigation:** Agile sprints; daily tracking; scope reduction if needed

**Risk 3: User adoption**
- **Impact:** Medium
- **Likelihood:** Low
- **Mitigation:** Change management; training; pilot with 50 staff

### 7.2 Medium Risks

**Risk 4: Webhook unreliability**
- **Mitigation:** Robust polling fallback

**Risk 5: Data quality issues**
- **Mitigation:** Strong validation; admin correction workflows

---

## 8. COMPETITIVE LANDSCAPE

### Competitor Analysis:

| Competitor | Approach | Strengths | Weaknesses |
|------------|----------|-----------|------------|
| **Traditional Agencies** | Manual phone calls | Personal touch | Slow, expensive, inconsistent |
| **Nurse Apps** | Mobile-first | Modern UX | Low adoption, fragmented market |
| **PHC (Our Solution)** | WhatsApp + Automation | High adoption (95%), automation, merit-based | New to market |

**Differentiation:**
- Uses WhatsApp (already adopted) vs forcing new app download
- Merit-based scoring vs random/manual assignment
- ERP integration vs standalone system
- 60-day implementation vs 6-12 months competitors

---

## 9. PRODUCT ROADMAP

### **Phase 1: MVP (v1.0) - 60 days**
- All 4 main flows
- Scoring algorithm
- WhatsApp integration
- Admin portal
- ERP integration (13 APIs)
- Emergency file upload

### **Phase 2: Enhanced (v2.0) - +30 days**
- Geographic intelligence (distance-based matching)
- Automated fair sharing algorithm
- Mobile app (optional)
- Predictive analytics (ML model)
- Real-time dashboard (WebSockets)

### **Phase 3: Scale (v3.0) - +30 days**
- Multi-language support (English + TC)
- Advanced reporting & BI
- Automated emergency triggers
- Integration with additional systems

---

## 10. INVESTMENT & ROI

### 10.1 Investment: HKD 800,000

| Category | Amount | % |
|----------|--------|---|
| Development (60 days) | 600K | 75% |
| ERP Integration | 80K | 10% |
| Testing & QA | 60K | 7.5% |
| Infrastructure (Y1) | 40K | 5% |
| Training & Docs | 20K | 2.5% |

### 10.2 Return: HKD 1.74M (Year 1)

| Benefit | Amount |
|---------|--------|
| Revenue increase (better fill rate) | 1.2M |
| Cost savings (coordinator time) | 480K |
| Penalty collections | 60K |

### 10.3 Net Benefit: HKD 940K
**ROI: 118%**

**Payback Period:** 5.5 months

---

## 11. COMPETITIVE ADVANTAGES

### Why PHC Wins:

✅ **Speed to Market:** 60 days vs 6-12 months
✅ **Adoption:** WhatsApp (95%) vs new app (30-40%)
✅ **Fairness:** Merit-based scoring (transparent)
✅ **Integration:** ERP-connected (single source of truth)
✅ **Cost:** HKD 800K vs competitors HKD 1.5-2M)
✅ **ROI:** 118% in Year 1

---

## 12. TEAM & STAKEHOLDERS

### Core Team:
- **Product Owner:** [To be assigned]
- **Technical Lead:** [To be assigned]
- **Backend Developers:** 2
- **Frontend Developer:** 1
- **QA Engineer:** 1

### Stakeholders:
- **Executive Sponsor:** [C-level]
- **Operations Manager:** [To participate in weekly reviews]
- **ERP Team Lead:** [For API coordination]
- **Nursing Assistant Representative:** [For user feedback]

---

## 13. DECISIONS REQUIRED

**Immediate Decisions:**
1. ✅ Approve HKD 800K budget
2. ✅ Approve 60-day timeline
3. ✅ Assign Project Sponsor
4. ✅ Assign Product Owner
5. ✅ Form project team

**Technical Decisions:**
1. ✅ Clock-in method: QR code OR supervisor verification
2. ✅ Hosting provider: AWS or Azure
3. ✅ Frontend framework: React.js (decided)
4. ✅ Database: PostgreSQL (decided)

**Go-Live Decisions:**
1. ✅ Pilot group size (recommend: 50 staff)
2. ✅ Rollout strategy (big bang or phased)
3. ✅ Training schedule
4. ✅ Support model post-launch

---

## 14. ASSUMPTIONS

1. ✅ ERP API documentation available within 1 week
2. ✅ Test/sandbox environment available
3. ✅ API credentials provided within 1 week
4. ✅ ERP team responsiveness (questions answered within 2 days)
5. ✅ Project team dedicated (no competing priorities)
6. ✅ Overtime/workends acceptable during critical phases
7. ✅ WhatsApp Business API account available
8. ✅ 4-person team can be allocated

---

## 15. DEPENDENCIES

**External:**
- ERP API documentation (from ERP team)
- ERP test environment access
- WhatsApp Business API credentials

**Internal:**
- Project team allocation
- C-suite approval
- VPN/network access to ERP

---

## 16. GO-TO-MARKET STRATEGY

### Launch Timeline:
- **Week 1-2:** Pilot with 50 staff (1-2 locations)
- **Week 3-4:** Expand to 200 staff (5-10 locations)
- **Week 5-6:** Full rollout (500+ staff, 100+ locations)

### Change Management:
1. **Communication:** Town halls, email announcements
2. **Training:** Hands-on sessions for supervisors and admin
3. **Support:** Dedicated helpdesk for first 2 weeks
4. **Feedback:** Weekly surveys during rollout

### Success Metrics:
- Adoption rate (target: 90%)
- User satisfaction (target: 80%)
- System uptime (target: 99.5%)
- Support tickets (target: <5/day after Week 2)

---

## 17. CONCLUSION

**PHC is a critical investment that will:**

✅ **Increase Revenue:** HKD 1.2M (better fill rate)
✅ **Reduce Costs:** HKD 480K (efficiency gains)
✅ **Improve Quality:** 98% fill rate, 1% no-show
✅ **Scale Operations:** Handle 2x growth without additional coordinators
✅ **Enhance Brand:** Transparent, merit-based system attracts better staff

**Recommendation:**
**APPROVE** the HKD 800K investment for immediate project kickoff.

**Expected ROI:** 118% in Year 1
**Payback Period:** 5.5 months
**Strategic Value:** Transformative for operations

---

**Document Version:** 1.0
**Last Updated:** 2025-11-24
**Next Review:** After executive approval
**Owner:** Product Manager (to be assigned)
