# Specification Document Alignment - Changes Required
**Date:** 2025-11-24
**Status:** CRITICAL MISALIGNMENTS IDENTIFIED

---

## 🚨 CRITICAL ISSUES FOUND

### 1. Technology Stack Mismatch (REJECTED BY PRD)

**Specification Document (WRONG):**
- Line 595: Backend Framework: Spring Boot 3.x (Java 17+)
- Line 599: Database: MySQL 8.0+ or PostgreSQL 15+

**PRD (CORRECT - From PM Decision):**
- Backend: Java Spring Boot 2.7+ (NOT 3.x)
- Database: MySQL 8+ (primary), Redis 6+ (caching)

**❌ BANNED:** Cannot use "or" in technology decisions. Architect must be specific.
**❌ BANNED:** Version conflicts - PM specified 2.7+, not 3.x

**Action Required:** Update to match PRD exactly

---

### 2. Notification Method Completely Wrong (MAJOR ARCHITECTURAL MISMATCH)

**Specification Document (WRONG):**
- Lines 492-498: SMS Gateway: Twilio or local HK provider for worker notifications
- Lines 492, 494: Push notifications mentioned generically

**PRD (CORRECT - From PM Decision):**
- WhatsApp (manual template-based) + Firebase Cloud Messaging
- NO SMS as primary channel
- NO generic "push notification" ambiguity

**❌ BANNED:** Specifying technology that contradicts PM decision
**❌ BANNED:** Vague notification approach (SMS vs Push unclear priority)

**Impact:** System won't meet user needs (staff use WhatsApp, not SMS)

**Action Required:** Complete rewrite of notification architecture section

---

### 3. Time Estimates Present (ARCHITECT BAN)

**Specification Document (VIOLATION):**
- Line 1435: Video tutorials (5-10 minutes each)
- Line 1449: Worker onboarding (10 minutes)
- Line 1429: Staff training sessions (45 minutes, 30 minutes, 30 minutes)

**Architecture Rule:** ⚠️ ABSOLUTELY NO TIME ESTIMATES - NEVER mention hours, days, weeks, months

**❌ BANNED:** Architects must NEVER give time estimates
**Reason:** AI has changed development speed - time estimates are obsolete and misleading

**Action Required:** Remove all time-based language

---

### 4. Scoring Algorithm Missing (CRITICAL FUNCTIONAL GAP)

**Specification Document (MISSING):**
- No mention of scoring system
- No merit-based allocation logic
- No points system (+1 attend, -1 cancel, -2 no-show)

**PRD (REQUIRED - FR-1):**
- Scoring algorithm is core feature (P0)
- Gold/Silver/Bronze tiers
- Score floor = -10
- Real-time ERP sync

**❌ CRITICAL GAP:** Missing entire P0 functional requirement

**Action Required:** Add comprehensive scoring algorithm section

---

### 5. Matching Engine Missing (CRITICAL FUNCTIONAL GAP)

**Specification Document (MISSING):**
- No automated matching logic
- No ranking algorithm
- No filter by availability, documents, blacklist

**PRD (REQUIRED - FR-2):**
- Matching engine is P0 feature
- Filter by availability, documents, blacklist, fair sharing
- Rank by underlist, score tier, work history
- Match in <5 minutes

**❌ CRITICAL GAP:** Core automation feature missing

**Action Required:** Add matching engine architecture section

---

### 6. Penalty Management Missing (CRITICAL FUNCTIONAL GAP)

**Specification Document (MISSING):**
- No automatic penalty application
- No financial penalties (-100 HKD)
- No warning system

**PRD (REQUIRED - FR-7):**
- Cancellation: -1 score, -100 HKD
- No-show: -2 score, -100 HKD
- Warning displayed before cancellation
- ERP deduction

**❌ CRITICAL GAP:** Financial penalty system missing

**Action Required:** Add penalty management section

---

### 7. QR Code Method Not Aligned (DECISION NEEDED)

**Specification Document (AMBIGUOUS):**
- Lines 468-481: QR code for facility identification
- Lines 212-214: QR code OR supervisor verification

**PRD (REQUIRES DECISION):**
- Option A: QR code (staff scans)
- Option B: Supervisor manual verification
- Decision not finalized

**❌ BANNED:** Cannot implement both without decision
**❌ BANNED:** Ambiguity in primary attendance method

**Action Required:** Coordinate with PM to finalize decision before implementation

---

### 8. Inconsistent User Personas

**Specification Document (Generic):**
- Lines 44-47: Agency Staff, Healthcare Workers, Facility Admins
- No specific personas or pain points

**PRD (DETAILED):**
- Ah Mui, 48, Nursing Assistant (15 years experience)
- Ms. Wong, 52, Care Home Supervisor (20 years)
- Jason, Admin Manager (data-driven)
- Detailed pain points and goals for each

**❌ MISALIGNMENT:** Personas don't match - different market segments?

**Action Required:** Align user personas or clarify if different projects

---

### 9. Project Scope Mismatch

**Specification Document (Phase 1-3):**
- 14-week development + 4-week post-launch
- Facility portal in Phase 2
- QR codes, advanced analytics

**PRD (60-day MVP):**
- Launch in 60 days (not 14 weeks)
- 7 P0 features + 3 P1 features
- WhatsApp-based (not self-service portal focus)

**❌ CRITICAL:** Different timeline, scope, and priorities

**Question:** Is this the same project or a different system?

---

### 10. API Authentication Mismatch

**Specification Document (JWT):**
- Lines 186-189: Password complexity, session timeout 4 hours
- Line 641: JWT tokens with 4-hour expiration, 30-day refresh

**PRD (To be clarified):**
- No specific mention of JWT in FRs
- Line 382: JWT + Spring Security
- No session timeout requirements specified

**❌ BANNED:** Architect making decisions not in PRD
**Rule:** Architecture must implement PRD decisions, not add new ones

**Action Required:** Verify JWT is approved by PM, or align with implicit requirement

---

### 11. Missing Implementation Patterns

**Specification Document (Partial):**
- Some API endpoint structure (lines 618-624)
- Some standards (lines 629-634)

**PRD (Required from Architecture):**
- No implementation patterns documented
- No naming conventions for AI agents
- No file structure defined
- No error handling patterns

**❌ BANNED:** Architect must provide implementation patterns for AI agents

**Action Required:** Add comprehensive implementation patterns section

---

### 12. Database Schema Over-Specified

**Specification Document (Lines 655-758):**
- Complete table structures with field types
- MySQL-specific implementations

**Architecture Principle:**
- PRD doesn't require this level of detail
- Should be decided during implementation by development agents
- Database design is implementation detail, not architecture

**⚠️ WARNING:** May constrain implementation unnecessarily

**Action Required:** Consider moving to implementation phase or mark as "EXAMPLE ONLY"

---

### 13. Inconsistent Technology Justifications

**Specification Document (Lines 589-611):**
- "Your expertise, enterprise-grade" as rationale for Spring Boot
- No business value justification

**Architecture Principle:**
- Every decision must connect to business value and user impact
- Must be objective, not subjective

**❌ BANNED:** "Because I said so" or "Because we're familiar" as justification

**Action Required:** Rewrite rationale based on PRD requirements (60-day timeline, scalability needs)

---

### 14. Integration Details Premature

**Specification Document (Lines 762-790):**
- Detailed ERP integration workflow
- Polling frequency (every 15 minutes)
- Retry 3 times with exponential backoff

**PRD (Lines 177-186, 196-199):**
- ERP Integration as FR-5: 13 API endpoints
- Daily sync: staff, locations
- Every 15 min: job demands
- Real-time: assignments, penalties, scores

**❌ PARTIAL ALIGNMENT:** Details correct but should align with PRD structure

**Action Required:** Reference FR numbers in architecture documentation

---

### 15. Missing References to PRD

**Specification Document (Throughout):**
- No references to FR numbers
- No traceability to product requirements

**PRD (Lines 105-333):**
- 13 functional requirements (FR-1 through FR-13)
- All P0 features prioritized

**❌ BANNED:** Architecture must reference specific FRs it implements

**Action Required:** Add FR traceability throughout specification

---

## 📋 SUMMARY OF REQUIRED CHANGES

### High Priority (Must Fix Before Implementation):
1. ✅ Update technology stack to match PRD (Spring Boot 2.7+, MySQL 8+)
2. ✅ Rewrite notification architecture (WhatsApp + Firebase, NOT SMS)
3. ✅ Remove all time estimates (architect ban)
4. ✅ Add scoring algorithm (FR-1)
5. ✅ Add matching engine (FR-2)
6. ✅ Add penalty management (FR-7)
7. ✅ Finalize QR code vs supervisor verification decision
8. ✅ Align user personas with PRD
9. ✅ Verify if this is same project (scope mismatch)

### Medium Priority (Should Fix):
10. ⏳ Add implementation patterns for AI agents
11. ⏳ Connect decisions to business value
12. ⏳ Add FR traceability
13. ⏳ Reconcile terminology differences

### Low Priority (Nice to Have):
14. 💡 Consider simplifying database schema detail
15. 💡 Standardize document format (remove LaTeX, use markdown)

---

## 🎯 ESTIMATED EFFORT

**Time to Fix:** 8-12 hours (1.5 days)
- Technology alignment: 1 hour
- Notification rewrite: 3 hours
- Remove time estimates: 1 hour
- Add missing features: 3-4 hours
- Pattern documentation: 2 hours

**Complexity:** Medium
**Blockers:** None (all decisions documented in PRD)
**Next Step:** Update specification document with these changes

---

## 📝 CHANGE LOG

**Version 1.0 → 1.1 (2025-11-24)**
- [ ] Technology stack aligned with PRD (Spring Boot 2.7+, MySQL 8+)
- [ ] Notification architecture rewritten (WhatsApp + Firebase)
- [ ] Time estimates removed per architect standards
- [ ] Scoring algorithm added (FR-1)
- [ ] Matching engine added (FR-2)
- [ ] Penalty management added (FR-7)
- [ ] QR code decision documented
- [ ] User personas aligned with PRD
- [ ] Implementation patterns added
- [ ] FR traceability added

---

**Document Status:** ⚠️ REQUIRES REVISION
**Architecture Approval:** ⏳ PENDING CHANGES
**Next Review:** After changes implemented
