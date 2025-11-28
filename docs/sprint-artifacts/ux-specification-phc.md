# PHC - Prestige Health Match or Dispatch System
## User Experience Specification Document

**Project:** PHC - Automated Staff Dispatch System
**Version:** 1.0
**Date:** 2025-11-24
**Status:** Draft - Design Thinking Phase
**Designer:** Sally (UX Designer)
**Stakeholder:** Kim (Project Owner)

---

## Executive Summary

PHC transforms Prestige Health's manual staff coordination process into an intelligent, merit-based dispatch system. The solution respects existing workflows while eliminating 75% of manual coordination time through human-in-the-loop automation.

**Core Value Proposition:** *"Intelligent suggestions, human approval, fair allocation"*

---

## 1. Problem Definition

### Current State Pain Points

**The 6:00 AM Crisis (happens daily across 50+ care homes):**
1. Staff calls in sick → Supervisor alerts coordinator
2. Coordinator spends **2-3 hours** manually calling through staff lists
3. **High no-show rate (5%)** - unreliable manual process
4. **No transparency** - allocation based on relationships, not merit
5. **Inconsistent coverage** - 85% fill rate leaves residents under-staffed
6. **Inefficient resource use** - 3 FTE coordinators managing chaos

**Technical Debt:**
- Custom-built ERP system is desktop-only, not mobile-friendly
- No integration between ERP and real-world coordination
- Staff (500 nursing assistants, 100 supervisors) have **zero system access**
- Only coordinators use ERP; everyone else works in "phone call world"

**Business Impact:**
- High operational costs: 3 coordinators × salary = significant expense
- Revenue loss: Unfilled shifts = unpaid care hours
- Quality risk: Inconsistent staffing affects resident care
- Scalability limit: Manual process can't support growth

---

## 2. User Personas

### 2.1 Nursing Assistant (Primary User)
**Name:** Wai-Ling Chan
**Age:** 47
**Tech Level:** Low-Medium
**Primary Device:** Smartphone (Android)

**Bio:**
- 12 years experience, single mother of two teenagers
- Works 5-6 shifts per week across 3 different care homes
- Lives paycheck to paycheck, every shift matters
- Tech-savvy enough for WhatsApp, Facebook, basic apps
- Frustrated by unfair shift allocation - "They always call the same people first"

**Goals:**
- Fair access to shifts based on reliability, not relationships
- Control over her schedule - knows which days she's available
- Quick response - knows immediately if she gets a shift
- Transparent process - sees why she was (or wasn't) selected
- Maintain good performance score to get priority

**Pain Points:**
- No visibility into available shifts until coordinator calls
- Unclear why some people get called first
- Last-minute cancellations with no opportunity to pick up shifts
- No recognition for perfect attendance
- Anxiety about no-shows affecting her reputation

**Current Workflow:**
- Receives WhatsApp or phone call from coordinator (random times)
- Says "yes" or "no" immediately (no time to think)
- Remembers schedule in her head or paper calendar
- Shows up to shift → signs paper timesheet

**PHC Workflow:**
- Gets push notification/WhatsApp for available shifts matching her preferences
- Opens mobile web app → sees shift details + her performance score rank
- One-tap acceptance (or decline)
- Receives confirmation with QR code for attendance
- Can view her performance score and shift history

---

### 2.2 Care Home Supervisor (Secondary User)
**Name:** Mr. Wong
**Age:** 52
**Tech Level:** Medium
**Primary Device:** Tablet + Smartphone

**Bio:**
- 20 years in healthcare, 8 years as supervisor
- Manages 40 residents plus 15-20 nursing assistants
- Responsible for shift coverage 24/7
- Pragmatic, values reliability above all else
- Medium tech comfort - uses tablet for emails, reports, scheduling
- Frustrated by being understaffed, especially at 6am

**Goals:**
- Fill empty shifts FAST (within 30 minutes, not 3 hours)
- Get quality, reliable staff (not just warm bodies)
- Know WHO is coming (with confidence) before shift starts
- Reduce his "emergency coordinator calls"
- Track attendance and no-shows easily

**Pain Points:**
- 3-hour delay to fill shifts = stressed-out morning routine
- No-shows create crisis - last-minute scrambling
- No visibility into which staff are reliable vs. flakes
- Too many phone calls to coordinator (feels like begging)
- Paper timesheets and manual tracking = errors

**Current Workflow:**
- Staff calls sick → immediately calls coordinator
- Waits anxiously for coordinator to find replacement
- Sometimes has to provide care himself while waiting
- Staff arrives (or doesn't) → signs paper attendance

**PHC Workflow:**
- Staff calls sick → opens PHC supervisor app → marks shift "unfilled"
- Automatically triggers matching process (no phone call needed)
- Receives notification: "3 staff notified, 2 accepted, Chan Wai-Ling assigned"
- Can see staff profile with reliability score before they arrive
- QR code check-in confirms attendance → updates ERP automatically

---

### 2.3 Dispatch Coordinator (Power User)
**Name:** Emily Cheung
**Age:** 38
**Tech Level:** High
**Primary Device:** Desktop/Laptop (multiple monitors)

**Bio:**
- 5 years as coordinator, knows all 500 nursing assistants by name
- Works 8-hour shifts managing 50+ care homes
- Handles 30-40 staffing changes per day
- Expert at juggling phone calls, remembering preferences, negotiating
- Feels overwhelmed but takes pride in "never leaving a shift unfilled"
- Fears new system will replace her job

**Goals:**
- Fill shifts faster (from 3 hours to 45 minutes)
- Make fair, data-driven decisions (not just who she remembers)
- Reduce stress and phone tag
- Maintain human relationships with staff
- Prove her value beyond just making phone calls

**Pain Points:**
- Non-stop phone calls from supervisors (interruptions)
- Playing "phone tag" with 10+ staff to fill one shift
- Pressure to remember 500 people's preferences and availability
- Guilt about perceived favoritism (even when unintentional)
- Exhaustion from reactive firefighting (never proactive)

**Current Workflow:**
- Gets call from supervisor → opens ERP → sees empty shift
- Mentally reviews: "Who's available? Who's reliable? Who likes that location?"
- Makes 10-15 phone calls → leaves voicemails → waits for callbacks
- First person who answers gets the shift (speed over optimization)
- Updates timesheet/schedule manually in ERP

**PHC Workflow:**
- Supervisor marks shift "unfilled" in PHC → automatic matching triggers
- Receives notification: "Suggested 5 candidates, ranked by score"
- Reviews suggestions → approves/changes → one-click "notify selected staff"
- Staff responses appear in dashboard (real-time)
- Auto-assignment when acceptance received → syncs to ERP
- Focus shifts from "making calls" to "strategic oversight + exception handling"

---

### 2.4 PHC Administrator (System Admin)
**Name:** David Lau
**Age:** 45
**Tech Level:** High
**Primary Device:** Desktop/Laptop

**Bio:**
- Operations manager, responsible for system performance
- Monitors fill rates, no-show rates, costs
- Reports to leadership on ROI and efficiency
- Technical enough to understand APIs and data flows
- Needs reporting, analytics, and system oversight

**Goals:**
- Achieve 95%+ fill rate (from 85%)
- Reduce no-shows to <2% (from 5%)
- Demonstrate clear ROI on $1.5M investment
- Maintain system reliability and performance
- Ensure fair, transparent allocation process

**Pain Points:**
- No data-driven insights (manual process = no tracking)
- Can't prove ROI without metrics
- No visibility into coordinator decision-making
- ERP is siloed, no integration with operations
- Reporting requires manual data collection

**Current Workflow:**
- Monthly reports cobbled together from coordinator notes
- No real-time visibility into operations
- Reactive problem-solving (hears about issues too late)

**PHC Workflow:**
- Real-time dashboard: fill rates, no-shows, response times
- Automated reporting: ROI tracking, efficiency metrics
- Can drill down: which coordinators, which locations, which staff
- Merit system transparency: ensure fairness
- API monitoring: ensure ERP sync is working

---

## 3. Current State User Journey Mapping

### Journey 1: Nursing Assistant - "I need more shifts"

```
Current State (Manual):
Staff member needs more work
    ↓
Waits for coordinator to call (passive)
    ↓
May or may not get called
    ↓
If called: Immediate yes/no (no details)
    ↓
No visibility into why others got called first
    ↓
Frustration builds over time
```

**Pain Points:**
- Reactive, not proactive
- No control over schedule
- Lack of transparency
- Communication only one-way (coordinator → staff)

---

### Journey 2: Supervisor - "My staff called in sick"

```
Current State (Crisis Mode):
6:00 AM: Staff calls in sick
    ↓
Supervisor calls coordinator (interrupts coordinator's morning)
    ↓
Coordinator: "I'll take care of it"
    ↓
Supervisor waits anxiously (unknown timeline)
    ↓
Coordinator makes 10-15 phone calls over 2-3 hours
    ↓
Finally finds replacement (maybe)
    ↓
Supervisor briefs replacement (if they show up)
    ↓
Paper timesheet signed
```

**Pain Points:**
- Supervisor powerless during 2-3 hour wait
- No visibility into process
- Coordinator interruption-driven work
- No backup plan if coordinator can't fill
- High no-show rate (5%) = unreliable process

---

### Journey 3: Coordinator - "Fill this shift NOW"

```
Current State (Firefighting):
Receive call from supervisor (interrupt)
    ↓
Open ERP desktop → find shift details
    ↓
Mentally filter: Who's available? Who's qualified?
    ↓
Remember preferences (phone call to wrong person = frustration)
    ↓
Start making calls (first person who answers often wins)
    ↓
Leave voicemails, wait for callbacks (60-90 minutes)
    ↓
Maybe 2-3 callbacks out of 15 calls
    ↓
First positive response = shift filled (not necessarily best fit)
    ↓
Update ERP manually
    ↓
Next call comes in (reactive cycle continues)
    ↓
End of day: Exhausted, 30 shifts handled, no strategic work done
```

**Pain Points:**
- Constant interruptions (phone-driven, not system-driven)
- Relies on memory (500+ people, preferences change)
- Speed over optimization (first responder bias)
- Perceived favoritism (even when unintentional)
- No tracking → no data → no improvement
- Zero strategic capacity (always tactical)

---

## 4. Future State with PHC System

### Design Philosophy: "Intelligent Suggestions, Human Approval"

**Core Principles:**
1. **Human-in-the-loop:** System suggests, humans approve (never auto-assign)
2. **Transparent meritocracy:** Performance scores visible to all
3. **Mobile-first for staff:** 500 nursing assistants need smartphone access
4. **ERP as source of truth:** Read from ERP, write confirmations back only
5. **Incremental trust:** Start with suggestions, build toward more automation

---

### Journey 1: Nursing Assistant - "I want that shift!"

```
Future State (Application Workflow):
PHC System receives job demand from ERP
    ↓
System sends WhatsApp/Push Notification to eligible staff
    ↓
Nursing assistant receives notification
    ↓
Opens mobile web app → sees shift details
    ↓
Reviews: Location, time, rate, cancellation policy
    ↓
Clicks "Apply" (Status: Pending Approval)
    ↓
Admin reviews application (screens candidate)
    ↓
Admin approves application
    ↓
Nursing assistant receives: "Application Approved" + Confirmation
    ↓
Shows up → supervisor scans QR → attendance confirmed
    ↓
Performance score updates (+1 for attendance)
```

**Value Delivered:**
- **Fairness:** Admin screens candidates before assignment
- **Transparent:** Clear status updates (Pending -> Confirmed)
- **Control:** Apply for shifts that fit schedule
- **Mobile:** Works on their phone, no desktop needed

---

### Journey 2: Supervisor - "Shift filled automatically"

```
Future State (Automated Support):
6:00 AM: Staff calls in sick
    ↓
Supervisor updates ERP (or Admin posts Emergency Job)
    ↓
System syncs job demand (or Emergency Job triggers instantly)
    ↓
Notification sent to eligible staff
    ↓
Staff apply for the shift
    ↓
Admin reviews and approves best candidate
    ↓
Supervisor sees real-time dashboard: "Staff Assigned"
    ↓
Supervisor receives: "Chan Wai-Ling assigned, ETA 7:30 AM"
    ↓
7:30 AM: Chan arrives → QR code scanned → attendance confirmed
```

**Value Delivered:**
- **Visible:** Real-time status tracking
- **Reliable:** Admin screening ensures quality
- **Predictable:** Know WHO is coming, when
- **Accountable:** QR check-in proves attendance

---

### Journey 3: Coordinator - "Strategic oversight, not firefighting"

```
Future State (Screening & Approval):
System receives job demands from ERP
    ↓
Notifications sent to staff → Staff apply
    ↓
Coordinator opens "Job Applications" dashboard
    ↓
Sees list of applicants for each job
    ↓
Reviews: Performance scores, history, conflicts
    ↓
Makes human judgment: Approves best candidate
    ↓
System sends "Confirmed" notification to staff
    ↓
Auto-sync to ERP upon approval
    ↓
If no applicants: Coordinator uses "Manual Assignment"
    ↓
End of day: Reviews metrics dashboard
```

**Value Delivered:**
- **Control:** Human approval ensures right fit
- **Efficient:** Reviewing applications is faster than calling
- **Fair:** Data-driven selection from applicants
- **Trackable:** Every decision logged → analytics

---

## 5. Key Features by User Role

### 5.1 Nursing Assistant Mobile Interface

**Core Features:**
1. **Secure Login & Authentication**
   - Login via Mobile Number, Username, or Email
   - Password authentication with "Forgot Password" flow
   - Security: Account lockout after 5 failed attempts
   - Session: Auto-logout after 30 minutes of inactivity

2. **Notification Center**
   - WhatsApp + web push notifications
   - Shift opportunities matching preferences
   - Priority based on performance score

2. **Shift Details View**
   - Location, time, care home, supervisor
   - Hourly rate, shift duration
   - **Cancellation Penalty Warning** (if applicable)
   - "Apply for Shift" button (Status: Pending)

3. **Assignment Confirmation**
   - "Application Approved" notification
   - QR code for attendance check-in
   - Calendar integration
   - Directions to care home

4. **Performance Dashboard**
   - Current performance score
   - History: shifts completed, attendance record
   - Explanation of scoring: +1 attend, -1 cancel
   - Goal setting: "Attend 10 more shifts to reach 95 score"

5. **Profile & Preferences**
   - Availability calendar
   - Preferred locations
   - Specializations/qualifications
   - Contact information

6. **Shift History**
   - Past shifts with attendance record
   - Earnings tracking
   - Performance trends
   - Feedback from supervisors

**Design Considerations:**
- **Mobile-first:** Works perfectly on 5-6" Android phones
- **Low data usage:** Not everyone has unlimited data
- **Simple interface:** Large buttons, clear text, minimal steps
- **Bilingual:** Traditional Chinese + English
- **Offline capability:** View assignments without internet
- **Speed:** All actions < 3 seconds

---

### 5.2 Supervisor Mobile/Tablet Interface

**Core Features:**
1. **Shift Management**
   - View schedule for their care home
   - Real-time status: "Searching", "Staff Applied", "Assigned"
   - View assigned staff details

2. **Assignment Tracking**
   - Real-time dashboard: unfilled shifts
   - Staff application status
   - Staff profile preview: reliability score, history
   - ETA tracking for assigned staff

3. **Attendance Verification**
   - QR code scanner for check-in
   - Alternatives: manual verification, supervisor PIN
   - No-show flagging (triggers score penalty)
   - Early/late tracking

4. **Staff Performance View**
   - Staff assigned to their care home
   - Performance scores
   - Attendance history
   - Notes/feedback

5. **Communication Hub**
   - Message assigned staff
   - Broadcast to all staff at care home
   - Receive messages from staff

**Design Considerations:**
- **Tablet + phone:** Works on both devices
- **Offline mode:** Can mark shifts, syncs when connected
- **Urgency indicators:** Visual cues for time-sensitive needs
- **Quick actions:** Swipe gestures, large touch targets
- **Bilingual:** Traditional Chinese + English

---

### 5.3 Coordinator Desktop Interface

**Core Features:**
1. **Application Screening**
   - View all applications for each job
   - Applicant details: Score, History, Conflicts
   - Approve/Reject applications
   - Bulk approval capabilities

2. **Manual Assignment**
   - Search staff by name/score
   - Override system matching
   - Conflict warnings (e.g., double booking)
   - Audit log for manual overrides

3. **Job Posting Management**
   - View jobs synced from ERP
   - Post "Emergency Jobs" (bypasses sync)
   - Monitor fill rates in real-time

4. **Exception Management**
   - Complex shifts requiring human judgment
   - Last-minute unfilled shifts (no applicants)
   - Special requests from supervisors
   - Quality issues or complaints

5. **Staff Performance Management**
   - View all 500 staff performance scores
   - Trend analysis: improving/declining
   - Coaching opportunities: low-scoring staff
   - Recognition: high-performing staff

6. **Reporting & Analytics**
   - Fill rate by location, time period
   - Average time to fill shifts
   - No-show rate tracking
   - Coordinator performance metrics
   - Cost savings calculation

7. **System Configuration**
   - Matching algorithm parameters
   - Performance score calculation
   - Notification templates
   - Escalation rules

**Design Considerations:**
- **Multi-monitor support:** Dashboards, details, actions
- **Keyboard shortcuts:** Power user efficiency
- **Bulk operations:** Select multiple shifts, approve all
- **Filtering & search:** Find staff, shifts, locations quickly
- **Export capabilities:** Reports for leadership
- **Bilingual:** Traditional Chinese + English

---

### 5.4 Administrator Desktop Interface

**Core Features:**
1. **Executive Dashboard**
   - Fill rate: current, trend, target (95%)
   - No-show rate: current, trend, target (<2%)
   - Time-to-fill: average minutes per shift
   - Cost savings: coordinator hours saved
   - ROI tracking: system investment vs. returns

2. **Operations Analytics**
   - Heat map: which locations struggle most
   - Time-of-day patterns: morning, evening, weekend
   - Staff performance distribution
   - Coordinator productivity metrics
   - System health: API uptime, errors

3. **Financial Reporting**
   - Penalty deductions tracked: -300 HKD per late cancellation
   - Coordinator salary savings: hours × rate
   - Revenue protection: unfilled shifts prevented
   - ROI calculation: Year 1, Year 2 projections

4. **System Administration**
   - User management: 500 staff, 100 supervisors, 3 coordinators
   - Role-based permissions
   - API integration monitoring (13 endpoints)
   - ERP sync status
   - Notification service health

5. **Quality Assurance**
   - Merit system fairness audit
   - Complaint tracking
   - Staff satisfaction surveys
   - Performance score calibration

6. **Strategic Planning**
   - Capacity planning: growth scenarios
   - Hiring needs: based on fill rate gaps
   - Training priorities: low-scoring staff clusters
   - Shift pricing optimization

**Design Considerations:**
- **C-suite ready:** Charts, graphs, executive summaries
- **Drill-down capability:** Summary → details → raw data
- **Automated reporting:** Scheduled email reports
- **Bilingual:** Traditional Chinese + English
- **Mobile viewing:** Responsive for tablet access

---

## 6. Technical Integration Requirements

### 6.1 ERP Integration Strategy

**Data Flow Philosophy:**
- **ERP = Source of Truth** (custom-built system)
- **PHC = Intelligent Layer** (suggestions, automation, mobile)
- **Read from ERP frequently** (real-time sync)
- **Write to ERP carefully** (only confirmations, attendance)
- **DB admins handle ERP updates** (not PHC system)

**13 API Endpoints (Scope Definition Needed):**

**Reading from ERP (8-10 endpoints):**
1. GET /staff - Retrieve all nursing assistants + supervisors
2. GET /staff/{id} - Get staff details, qualifications, preferences
3. GET /shifts - Retrieve shift schedules for all locations
4. GET /shifts/{id} - Get shift details, requirements, status
5. GET /attendance - Retrieve attendance history
6. GET /locations - Get care home locations, addresses
7. GET /qualifications - Retrieve certification requirements
8. GET /pay-rates - Get hourly rates by location/role
9. GET /penalties - Retrieve penalty history (cancellations)
10. GET /availability - Get staff availability calendars

**Writing to ERP (3-5 endpoints):**
11. POST /attendance - Submit attendance confirmation (QR scan)
12. PUT /shifts/{id} - Update shift status (filled/unfilled/assigned)
13. POST /penalties - Submit late cancellation penalty (-300 HKD)
14. PUT /staff/{id}/performance - Update performance score (merit system)
15. POST /shift-history - Log matching/assignment history

**Integration Pattern:**
- **Frequency:** Real-time or near-real-time (5-minute sync)
- **Direction:** Mostly ERP → PHC (reads), selective PHC → ERP (writes)
- **Error handling:** Queue failed writes, alert administrators
- **Conflict resolution:** ERP wins (source of truth)

**New ERP Field Required:**
- **Shift Status:** "Filled", "Unfilled", "Pending", "Assigned"
- **(Currently missing, requires DB admin work)**
- **Purpose:** Trigger matching process when status = "Unfilled"

---

### 6.2 Performance Score (Merit System)

**Calculation Algorithm:**
```
Base Score: 80 points (starting/midpoint)

Scoring Events:
+1 point: Successfully attended shift
-1 point: Cancelled with notice (Early >48h)
-1 point: Late Cancellation (<48h) + 300 HKD Penalty
(No-show penalties removed in v1.2)

Score Range: 60-100 (with potential exceptions)

Ranking Weight: Higher score = priority matching

```

**Data Storage:**
- **Calculated in PHC system** (real-time)
- **Stored in PHC database only** (not written to ERP)
- **Used for matching/ranking only** (not payroll)
- **Visible to staff:** Show them their score (transparency)
- **Visible to coordinators:** Use for decision-making

**Rules:**
- Scores never go below 60 (poor performance) or above 100 (perfect)
- 3 late cancellations within 30 days = system flag for coordinator review
- Perfect attendance bonus: +5 after 20 consecutive shifts
- Trend indicator: Rising (improving) vs. Falling (declining)

**User Interface:**
- Staff see: "Your score: 86/100 (Rank: 45th out of 500)"
- Staff see: "Attend 4 more shifts to reach 90"
- Coordinators see: Score + trend + alerts for low performers

---

### 6.3 Notification System

**Hybrid Approach:**
1. **WhatsApp Business API** (primary for nursing assistants)
   - Familiar platform (already using it)
   - High open rate (90%+)
   - Template-based messages for consistency

2. **Firebase Web Push** (secondary/supplemental)
   - For staff who opt-in
   - Real-time notifications
   - Links directly to PHC mobile app

**Notification Types:**

**For Nursing Assistants:**
- "[URGENT] Shift available at Tseung Kwan O Care Home, 7am-3pm, $110/hr. Tap to Apply: [link]"
- "✅ Application Approved! Tseung Kwan O, 7am-3pm. Check-in QR: [link]"
- "⚠️ Penalty applied: Late Cancellation on March 15 = -1 pts, -300 HKD. Current score: 84"

**For Supervisors:**
- "✅ Shift filled! Chan Wai-Ling assigned. ETA: 7:20am. Score: 89/100"
- "⏰ 15 min warning: Staff not checked in for shift starting at 7am"

**For Coordinators:**
- "⚠️ New Applications: 3 shifts have pending applications"
- "📊 Daily report: 42 shifts filled, avg time 4.2 min, 1 escalation"
- "🚨 Escalation: Tseung Kwan O shift (7am) no applicants after 20 min"

**Delivery Rules:**
- Initial notification: Simultaneous to eligible candidates
- Escalation: If no applicants in 15 min, notify coordinator
- Reminder: 24 hours before shift (confirmation)
- Urgency: SMS fallback if critical and no response

---

### 6.4 Matching Algorithm

**Matching Criteria (Weighted):**

```
1. QUALIFICATIONS (Must Match - Binary)
   - Required certifications met
   - If NO: Exclude from pool
   - Weight: ∞ (hard requirement)

2. AVAILABILITY (Must Match - Binary)
   - Staff marked "available" for that time
   - If NO: Exclude from pool
   - Weight: ∞ (hard requirement)

3. PERFORMANCE SCORE (Primary Ranking - 40%)
   - Higher score = higher rank
   - Purpose: Reward reliability
   - Example: 95 score vs. 75 score = priority

4. LOCATION PREFERENCE (Secondary - 25%)
   - Staff marked "preferred location"
   - Calculate distance/travel time
   - Purpose: Short commute = more likely to show

5. SCHEDULE PATTERN (Tertiary - 20%)
   - Similar shifts in past (consistency)
   - Same day of week patterns
   - Purpose: Familiarity = reliability

6. FAIRNESS FACTOR (Balancing - 15%)
   - Hours worked this week/month (prevent burnout)
   - Recent assignments (prevent favoritism)
   - Purpose: Distribute opportunities

CALCULATION:
Final Score = (Performance × 0.4) + (Location × 0.25) +
              (Pattern × 0.20) + (Fairness × 0.15)

RANK: Top 5 candidates by Final Score
```

**Computation Time:** < 3 seconds (for 500 staff pool)

**Confidence Indicators:**
- **High match (85%+):** "Excellent fit - high likelihood of acceptance"
- **Medium match (70-84%):** "Good fit - likely to accept"
- **Low match (<70%):** "Available but not optimal - consider alternatives"

**Coordination Recommendations:**
- System suggests top 5 candidates with scores
- Coordinator can override based on human judgment
- Human override is logged (audit trail)

---

## 7. User Experience Principles

### 7.1 Design Philosophies

**1. Transparency Builds Trust**
- Show performance scores to staff (don't hide algorithm)
- Explain WHY someone was selected
- Display ranking: "You were #3 of 5 candidates"
- Merit system is transparent, not black box

**2. Mobile-First for Field Staff**
- 500 nursing assistants = smartphone primary
- Supervisors = tablet/mobile in care homes
- Desktop only for coordinators and admins
- Mobile experience can't be "desktop lite"

**3. Respect Existing Mental Models**
- Don't force complete behavior change
- Current workflow: Phone call → acceptance
- New workflow: Notification → acceptance (similar)
- Preserve "human approval" step (comfort with change)

**4. Speed is a Feature**
- All user actions < 3 seconds
- Matching computation < 3 seconds
- Notification delivery < 30 seconds
- Perceived speed = confidence in system

**5. Progressive Disclosure**
- Simple interface for low-tech users (nursing assistants)
- Advanced features for power users (coordinators)
- Don't overwhelm with options - show what's needed, when needed

**6. Error Prevention > Error Recovery**
- Late Cancellation penalty: Confirm cancellation 3 times before processing
- Double-booking prevention: Check availability before notification
- Fat finger protection: "Are you sure?" for consequential actions
- Undo capability within 60 seconds

**7. Bilingual by Default**
- All UI elements: English + Traditional Chinese
- Notifications: Language based on staff preference
- Support both character sets seamlessly
- Right context, not just translation

**8. Human-in-the-Loop**
- System suggests, humans approve (initial phase)
- Never fully auto-assign (builds trust)
- Coordinator retains final say (job security comfort)
- Logs all decisions (audit + learning)

---

### 7.2 Accessibility & Inclusion

**Digital Literacy:**
- Assume low-medium tech level for nursing assistants
- Large buttons, clear labels, minimal text
- Visual icons + text (not text-only)
- Video tutorials for critical flows

**Age Considerations:**
- Nursing assistants: 35-55 years old
- Supervisors: 40-60 years old
- Larger fonts (minimum 16px on mobile)
- High contrast mode for older eyes

**Device Diversity:**
- Android phones (primarily)
- iOS phones (some)
- Tablets (supervisors)
- Desktop/laptop (coordinators, admins)
- Test on mid-range devices (not just flagships)

**Language Accessibility:**
- Traditional Chinese primary (Hong Kong context)
- English for international staff/admin
- Clear, simple language (avoid jargon)
- Visual cues reduce language dependence

---

## 8. Success Metrics (KPIs)

### 8.1 Business Metrics

**Primary KPIs:**
1. **Fill Rate**
   - Current: 85%
   - Target: 95%+
   - Measurement: Shifts filled ÷ total shifts × 100
   - Frequency: Daily tracking, monthly reporting

2. **No-Show Rate**
   - Current: 5%
   - Target: <2%
   - Measurement: No-shows ÷ total assigned shifts × 100
   - Frequency: Real-time alerts, weekly trending

3. **Average Time to Fill**
   - Current: 2-3 hours (120-180 minutes)
   - Target: <45 minutes
   - Measurement: Time from "unfilled" to "assigned"
   - Frequency: Per shift tracking, daily average

4. **Coordinator Time Saved**
   - Current: 8 hours/day (3 coordinators × firefighting)
   - Target: 2 hours/day (strategic work)
   - Measurement: Hours spent on reactive tasks
   - Frequency: Daily logging, weekly analysis

**Secondary KPIs:**
5. **Staff Satisfaction (NPS)**
   - Target: >50 (promoters vs. detractors)
   - Survey: Monthly pulse survey
   - Questions: Fairness, transparency, ease of use

6. **Supervisor Satisfaction (NPS)**
   - Target: >50
   - Survey: Monthly pulse survey
   - Questions: Speed, quality of staff, reliability

7. **System Uptime**
   - Target: 99.5% uptime
   - Critical for morning shift matching (6am-8am)
   - Monitoring: 24/7 infrastructure health

8. **Mobile Adoption Rate**
   - Target: 80% of nursing assistants actively using mobile
   - Measurement: Monthly active users ÷ total staff
   - Engagement: Frequency of notification responses

---

### 8.2 Financial Metrics (ROI)

**Year 1 ROI Target: 118%**

**Cost Savings:**
1. **Coordinator Salary Reduction**
   - Current: 3 FTE coordinators = $XXX,XXX/year
   - Optimized: 2 FTE coordinators = $XXX,XXX/year
   - Savings: 1 FTE salary + benefits

2. **Cancellation Penalties**
   - Collected: -300 HKD per late cancellation
   - Reduced no-shows: 5% → 2% = 60% reduction
   - Additional revenue from penalties

3. **Revenue Protection**
   - Unfilled shifts = lost revenue
   - 85% → 95% fill rate = 10 percentage point improvement
   - Protected revenue per shift × additional filled shifts

4. **Productivity Gains**
   - Coordinators focus on strategic work
   - Reduced stress = lower turnover
   - Faster scaling without proportional staff increase

**Investment:**
- System development: $1,500,000 (Year 1)
- Monthly SaaS/operations: $XX,XXX
- Training: $XX,XXX

**ROI Calculation:**
```
ROI = (Total Savings - Total Investment) ÷ Total Investment × 100
    = ($XXX,XXX - $1,500,000) ÷ $1,500,000 × 100
    = 118% (target)
```

---

## 9. Technical Constraints & Decisions

### 9.1 Integration Architecture

**System Architecture:**
```
┌─────────────────────────────────────────────────┐
│   Mobile/Web User Interfaces                    │
│   (Nursing Assistants, Supervisors, Coordinators)│
└─────────────────────────────────────────────────┘
                          ↓ API calls
┌─────────────────────────────────────────────────┐
│   PHC Application Server                        │
│   - Matching Engine                             │
│   - Performance Scoring                         │
│   - Notification Service                        │
│   - Business Logic Layer                        │
└─────────────────────────────────────────────────┘
                          ↓ 13 APIs
┌─────────────────────────────────────────────────┐
│   PHC Database                                  │
│   - Staff performance scores                    │
│   - Matching history                            │
│   - Notification logs                           │
│   - Mobile session data                         │
└─────────────────────────────────────────────────┘
                          ↓ Integration layer
┌─────────────────────────────────────────────────┐
│   ERP Integration APIs (13 endpoints)           │
│   - Read: Staff, shifts, locations, attendance  │
│   - Write: Attendance, shift status, penalties  │
└─────────────────────────────────────────────────┘
                          ↓ Database sync
┌─────────────────────────────────────────────────┐
│   ERP Database (Custom-built)                   │
│   - Source of truth for all business data       │
│   - Updated by DB admins only                   │
│   - New field: Shift_Status (Filled/Unfilled)   │
└─────────────────────────────────────────────────┘
```

**Key Constraints:**
- ERP remains source of truth (custom-built system)
- PHC is intelligent layer, not replacement
- DB admins maintain ERP data integrity
- Performance scores stay in PHC (not ERP)
- Matching history logged in PHC, summary synced to ERP

---

### 9.2 Performance Requirements

**Matching Engine:**
- **Computation time:** < 3 seconds for 500 staff pool
- **Algorithm complexity:** O(n log n) acceptable, O(n²) too slow
- **Optimization:** Pre-filter by availability, then score
- **Caching:** Staff qualifications/preferences cached in PHC

**Notification Delivery:**
- **WhatsApp:** < 30 seconds to delivery
- **Firebase push:** < 5 seconds to delivery
- **Uptime:** 99.5% availability
- **Failover:** SMS backup for critical notifications

**API Performance:**
- **ERP reads:** < 2 seconds (cached where possible)
- **ERP writes:** < 3 seconds (asynchronous preferred)
- **Error rate:** < 1% (automatic retry on failure)
- **Rate limiting:** Respect ERP capacity (no overload)

**Mobile App:**
- **Page load:** < 2 seconds on 4G connection
- **Offline mode:** View assigned shifts without internet
- **Data usage:** < 10MB per day average
- **Battery:** Minimal background processing

---

### 9.3 Security & Compliance

**Data Protection:**
- Staff personal data: HIPAA-level protection (healthcare context)
- Phone numbers, addresses: Encrypted at rest and in transit
- API authentication: OAuth 2.0 or API keys
- Mobile app: TLS 1.3 encryption

**User Authentication:**
- Multi-identifier login (Mobile/User/Email)
- Brute-force protection: Lockout after 5 failed attempts
- Session management: 30-minute inactivity timeout
- Password recovery: Secure OTP/Email flow

**Access Control:**
- Nursing assistants: View own data only (mobile)
- Supervisors: View their location only (mobile)
- Coordinators: View all data, edit assignments (desktop)
- Administrators: Full system access (desktop)

**Audit Trail:**
- Log all shift assignments (who, when, why)
- Track all performance score changes
- Monitor human overrides of system suggestions
- Compliance reporting for labor regulations

**Bilingual Compliance:**
- Traditional Chinese: Primary language (Hong Kong)
- English: Secondary language
- Legal terms: Accurate translation
- Terms of service: Both languages, legally binding

---

## 10. Change Management & Adoption

### 10.1 Phased Rollout Strategy

**Phase 1: Pilot (30 days)**
- **Locations:** 2-3 care homes (volunteers)
- **Users:** 50 nursing assistants, 5 supervisors, 1 coordinator
- **Goal:** Validate workflow, identify issues
- **Success:** 90% fill rate, positive feedback

**Phase 2: Expansion (60 days)**
- **Locations:** 15-20 care homes (early adopters)
- **Users:** 200 nursing assistants, 30 supervisors, 2 coordinators
- **Goal:** Refine matching algorithm, scale infrastructure
- **Success:** 92% fill rate, <45 min avg time

**Phase 3: Full Launch (90 days)**
- **Locations:** All 50+ care homes
- **Users:** 500 nursing assistants, 100 supervisors, 3 coordinators
- **Goal:** Full adoption, monitor KPIs
- **Success:** 95% fill rate, <2% no-show, 118% ROI

---

### 10.2 Training Strategy

**Nursing Assistants (500 people, low-medium tech):**
- **Format:** Video tutorials (2-3 minutes each) + printed guides
- **Topics:**
  - How to respond to notifications
  - How to accept/decline shifts
  - How to view your performance score
  - How to check in with QR code
- **Support:** WhatsApp group for questions + in-person help sessions
- **Timeline:** 1 week before go-live, ongoing support

**Supervisors (100 people, medium tech):**
- **Format:** 1-hour group training (by location) + video library
- **Topics:**
  - How to mark shifts "unfilled"
  - How to view assignment status
  - How to scan QR codes
  - How to handle no-shows
- **Support:** Direct line to coordinator for help
- **Timeline:** 2 weeks before go-live, refresher sessions

**Coordinators (3 people, high tech):**
- **Format:** Full day training + ongoing system admin support
- **Topics:**
  - Dashboard navigation
  - Reviewing and approving suggestions
  - Exception handling
  - Reporting and analytics
  - System configuration
- **Support:** Technical support team + documentation
- **Timeline:** 3 weeks before go-live, advanced training

**Administrators (5-10 people, high tech):**
- **Format:** Half-day training + system access
- **Topics:**
  - Executive dashboard
  - Reporting and analytics
  - User management
  - System monitoring
- **Support:** Technical support team
- **Timeline:** 1 week before go-live

---

### 10.3 Communication Plan

**Pre-Launch (30 days before):**
- Announcement: "New system coming to streamline shift assignments"
- Video: "How PHC works for you" (role-specific versions)
- FAQ: Address concerns (fairness, transparency, job security)
- Town halls: Q&A sessions by role

**Launch Day:**
- Morning kickoff meetings at each care home
- Help desk: Extra staff available for support
- Monitoring: System health dashboard
- Celebration: Acknowledge first successful matches

**Post-Launch (30 days after):**
- Weekly feedback surveys
- Success stories: Share positive experiences
- Iteration: Quick wins based on feedback
- Recognition: Highlight staff with perfect attendance

---

## 11. UX Design Principles

### 11.1 Core Design Language

**Visual Identity:**
- **Color Palette:** Healthcare-friendly, calming
  - Primary: Deep blue (trust, reliability)
  - Secondary: Green (success, attend)
  - Accent: Orange (urgent, unfilled)
  - Alert: Red (no-show, penalty)

- **Typography:**
  - Headings: Bold, clear, Traditional Chinese + English
  - Body: Readable sans-serif (16px minimum)
  - Icons: Healthcare universally recognized symbols

- **Layout:**
  - Mobile: Single column, large touch targets (44px minimum)
  - Desktop: Multi-panel, information hierarchy
  - Tablet: Optimized two-column layouts

**Interaction Patterns:**
- **One-tap actions:** Accept, decline, approve
- **Swipe gestures:** Mobile navigation
- **Hover states:** Desktop information preview
- **Progress indicators:** Show matching in progress
- **Status badges:** Visual indicators (Filled, Pending, Unfilled)

---

### 11.2 Mobile Design Specifics (Nursing Assistants)

**Screen 0: Login**
- Input: Mobile / Username / Email
- Input: Password (masked)
- Action: "Login" button (Primary)
- Link: "Forgot Password?" (Secondary)
- Feedback: "Account locked after 5 failed attempts" (Error state)

**Screen 1: Notification (WhatsApp / Push)**
- Message: "[URGENT] Shift at Tseung Kwan O, 7am-3pm, $110/hr. Tap to Apply."

**Screen 2: Shift Details**
- Large text: "Tseung Kwan O Care Home"
- Time: "Today, 7:00 AM - 3:00 PM (8 hours)"
- Rate: "$110/hour = $880 total"
- Cancellation Policy: "Late cancel (<48h) = -300 HKD"
- Large buttons: "✅ Apply for Shift" / "❌ Not Interested"

**Screen 3: Confirmation**
- Success message: "Application Approved!"
- Details: Location, time, supervisor contact
- QR code: Large, scannable (for check-in)
- Add to calendar button

**Screen 4: Performance Dashboard**
- Score: Large number "86/100"
- Rank: "45th out of 500 staff"
- Recent history: Last 5 shifts (✓ ✓ ✓ ✗ ✓)
- Next milestone: "4 more shifts → 90 score"

---

### 11.3 Coordinator Dashboard Design

**Left Panel (1/3):** Job Postings Queue
- List: Location, time, urgency, applicant count
- Filter: By location, time, priority
- Sort: Newest, most applicants, urgent

**Center Panel (1/2):** Application Screening
- Shift info: Location, time, requirements
- Applicant List:
  - Name, photo, performance score, distance
  - History: "Worked this location 12 times, 100% attendance"
- Action: "Approve Application" / "Reject"

**Right Panel (1/6):** Application Status
- Live feed: New applications
- Icons: 📝 Applied | ✅ Approved | ❌ Rejected
- Timer: "Unfilled for 20 minutes"

**Bottom Panel (Full Width):** Daily Metrics
- Fill rate progress bar: "92% of 95% target"
- Avg time to fill: "38 minutes"
- Cancellation rate: "1.2% (target: <2%)"

---

## 12. Risks & Mitigations

### 12.1 Technical Risks

**Risk: ERP integration complexity**
- Impact: Medium
- Probability: High
- Mitigation: API contract defined early, sandbox testing, phased rollout

**Risk: Performance at scale**
- Impact: High
- Probability: Medium
- Mitigation: Load testing, caching strategy, optimized algorithms

**Risk: Mobile app adoption**
- Impact: High
- Probability: Medium
- Mitigation: User-friendly design, training, incentives for early adopters

**Risk: Notification delivery failures**
- Impact: High
- Probability: Low
- Mitigation: Multi-channel (WhatsApp + Push), SMS backup, monitoring

---

### 12.2 Adoption Risks

**Risk: Coordinator resistance (fear of job loss)**
- Impact: High
- Probability: Medium
- Mitigation: Position as "assistant" not "replacement", human-in-the-loop, retrain for strategic role

**Risk: Staff resistance to performance scores**
- Impact: Medium
- Probability: Medium
- Mitigation: Transparency, explain calculation, fairness audits, appeals process

**Risk: Supervisor reluctance to use mobile app**
- Impact: Medium
- Probability: Low
- Mitigation: Tablet alternative, training, prove time savings

**Risk: Perceived unfairness in algorithm**
- Impact: High
- Probability: Medium
- Mitigation: Transparency, human oversight, regular audits, adjust weights

---

### 12.3 Business Risks

**Risk: Fill rate doesn't improve to 95%**
- Impact: Critical
- Probability: Low
- Mitigation: Monitor closely, algorithm tuning, incentive programs, additional recruitment

**Risk: No-show rate remains high**
- Impact: High
- Probability: Low
- Mitigation: Strict penalty enforcement, performance score visibility, reminder system

**Risk: ROI doesn't meet 118% target**
- Impact: High
- Probability: Medium
- Mitigation: Track savings closely, adjust pricing, demonstrate value to leadership

**Risk: Timeline slip (60-day launch)**
- Impact: Medium
- Probability: Medium
- Mitigation: Agile development, MVP approach, phased rollout, scope management

---

## 13. Next Steps: UX Design Phase

### 13.1 Immediate Actions (Week 1-2)

1. **Validate User Personas**
   - [ ] Interview 3-5 nursing assistants (validate pain points)
   - [ ] Interview 2-3 supervisors (validate current workflow)
   - [ ] Shadow coordinator for 1 day (validate firefighting reality)
   - [ ] Review with administrators (validate business goals)

2. **Technical Architecture Review**
   - [ ] Confirm 13 API endpoints with ERP team
   - [ ] Review ERP database schema (identify all required fields)
   - [ ] Plan new "Shift_Status" field implementation
   - [ ] Define API authentication approach
   - [ ] Confirm read/write permissions and constraints

3. **Matching Algorithm Definition**
   - [ ] Finalize scoring criteria weights
   - [ ] Define performance score calculation logic
   - [ ] Create confidence indicators
   - [ ] Build simulation model (test with historical data)

4. **Notification Strategy**
   - [ ] Define WhatsApp message templates
   - [ ] Design push notification content
   - [ ] Create notification timing rules
   - [ ] Plan escalation workflows

---

### 13.2 Design Phase (Week 3-6)

1. **Wireframes & Prototypes**
   - [ ] Mobile interface for nursing assistants (low-fidelity)
   - [ ] Mobile/tablet interface for supervisors (low-fidelity)
   - [ ] Desktop dashboard for coordinators (low-fidelity)
   - [ ] Desktop analytics for administrators (low-fidelity)

2. **User Testing**
   - [ ] Test mobile prototype with 5 nursing assistants
   - [ ] Test supervisor interface with 3 supervisors
   - [ ] Test coordinator dashboard with 1 coordinator
   - [ ] Gather feedback, iterate designs

3. **Visual Design**
   - [ ] Define design system (colors, typography, components)
   - [ ] Create high-fidelity mockups
   - [ ] Design icons and illustrations
   - [ ] Bilingual UI specifications

4. **Design Documentation**
   - [ ] Component library
   - [ ] Interaction patterns
   - [ ] User flow diagrams
   - [ ] Bilingual copy deck (Chinese + English)

---

### 13.3 Development Phase (Week 7-12)

1. **MVP Development**
   - [ ] Core matching algorithm implementation
   - [ ] Mobile web app (nursing assistants)
   - [ ] Coordinator desktop dashboard
   - [ ] ERP API integration (critical endpoints)
   - [ ] Notification system (WhatsApp + Firebase)

2. **Pilot Preparation**
   - [ ] Select 2-3 pilot care homes
   - [ ] Recruit pilot users (50 staff, 5 supervisors, 1 coordinator)
   - [ ] Prepare training materials
   - [ ] Set up support channels

3. **Pilot Launch**
   - [ ] 30-day pilot program
   - [ ] Daily monitoring and support
   - [ ] Gather feedback continuously
   - [ ] Track metrics: fill rate, time to fill, user satisfaction

4. **Iteration**
   - [ ] Address pilot feedback
   - [ ] Refine algorithm based on real data
   - [ ] Fix UX issues discovered
   - [ ] Prepare for full rollout

---

## 14. Appendices

### Appendix A: Glossary

**ERP:** Enterprise Resource Planning (custom-built system)
**PHC:** Prestige Health Dispatch System (new intelligent layer)
**FTE:** Full-Time Equivalent employee
**NPS:** Net Promoter Score (satisfaction metric)
**API:** Application Programming Interface (system integration)
**QR Code:** Quick Response code for attendance check-in
**WhatsApp API:** Business messaging platform for notifications
**Firebase:** Google platform for web push notifications

---

### Appendix B: Assumptions

1. ERP data is accurate (cleansed by DB admins)
2. All nursing assistants have smartphones with internet
3. WhatsApp is primary communication channel (adoption)
4. Coordinators will embrace "strategic" vs. "reactive" role
5. Performance score system will be accepted as fair
6. Custom API development is feasible within timeline
7. 60-day launch is achievable with MVP scope
8. $1.5M budget covers development and Year 1 operations
9. Compliance requirements can be met (labor laws)
10. Pilot success will drive adoption in broader organization

---

### Appendix C: Open Questions

**For Kim/Stakeholders:**

1. **ERP Details:**
   - What database technology is ERP built on?
   - Current API infrastructure (if any)?
   - Who are the DB admins we need to coordinate with?

2. **Financials:**
   - What is current coordinator fully-loaded salary?
   - What is revenue per filled shift?
   - Confirm $1.5M total investment budget?

3. **Timeline:**
   - Is 60-day launch from today or from project kickoff?
   - What are the key milestones and gates?
   - Any hard deadlines (regulatory, seasonal)?

4. **User Validation:**
   - Can we interview actual nursing assistants and supervisors?
   - Who are the pilot location volunteers?
   - Who will participate in user testing?

5. **Technical:**
   - What are the 13 API endpoints specifically?
   - WhatsApp Business API account setup status?
   - Firebase/Google Cloud infrastructure decisions?

6. **Change Management:**
   - Who is the executive sponsor for this change?
   - What is communication plan to all staff?
   - How will job security concerns be addressed?

---

## 15. Approval & Sign-off

**Document Status:** DRAFT - Awaiting stakeholder review

**Prepared by:**
Sally, UX Designer
Date: 2025-11-24

**Reviewed by:**
Kim, Project Owner
Date: ___________

**Approved by:**
[Executive Sponsor - TBD]
Date: ___________

---

**Next Review:** After pilot program (30 days)
**Version History:**
- v1.0: Initial draft based on Design Thinking Workshop

---

*This document is the foundation for all UX design, development, and implementation work on the PHC project.*
