# Scoring Algorithm & Penalties Specification

**Document Version:** 1.0
**Date:** 2025-11-24
**Project:** Prestige Health Dispatch System (PHC)
**Agent:** BMAD Analyst (Mary)

---

## 📊 Overview

This document specifies the scoring algorithm and penalty system for the Prestige Health Dispatch System's automatic nursing assistant allocation mechanism.

---

## 🎯 Scoring Algorithm Framework

### Base Score
- **Initial Score:** To be determined (recommendation: 5-10 points for new staff)
- **Purpose:** Enable new nursing assistants to receive initial assignments

### Score Components

#### 1. Attendance Tracking (Primary Factor)
| Action | Score Impact | Notes |
|--------|--------------|-------|
| **Attend (Present)** | +1 point | Successful shift completion |
| **Cancelled** | -1 point | Advance notice given |
| **Absent (No-show)** | -2 points | No notice, didn't attend |

#### 2. Score Tiers (Automatic Allocation Priority)
| Tier | Score Range | Priority Level | Allocation Strategy |
|------|-------------|----------------|-------------------|
| **Gold** | 20+ points | First Priority | Top of allocation list |
| **Silver** | 10-19 points | Second Priority | Secondary allocation |
| **Bronze** | 0-9 points | Third Priority | Fill remaining shifts |
| **Under Review** | < 0 points | Special Handling | Manual review required |

#### 3. Score Recovery Mechanism
- **Time Decay:** Older penalties matter less over time (to be defined)
- **Maximum Negative:** Score floor to be determined (recommendation: -10)
- **Recovery Actions:** Accepting shifts increases score over time

---

## 💰 Financial Penalty System

### Penalty Structure

#### Cancelled Shift (48 hours before shift with AL - Annual Leave)
| Penalty Type | Amount | Processing Method |
|--------------|--------|-------------------|
| **Score Penalty** | -1 point | Automatic system deduction |
| **Financial Penalty** | -100 HKD | ERP API integration |

#### No-Show (Absent without notice)
| Penalty Type | Amount | Processing Method |
|--------------|--------|-------------------|
| **Score Penalty** | -2 points | Automatic system deduction |
| **Financial Penalty** | -100 HKD | Automatic ERP processing |

---

## 🔧 Cancellation Workflow with ERP Integration

### User-Initiated Cancellation Flow

```
User clicks "Cancel Shift"
    ↓
System displays penalty warning
    ↓
User selects option:
├── [Accept Cancellation] → Process penalties → API to ERP → Confirmation
└── [Reject/Keep Shift] → Shift remains confirmed → User expected to attend
```

### Warning Message

**Text:** `"100HKD will be deducted when you apply AL within 48 hours before coming job!"`

**Display Location:**
- Modal/pop-up when user initiates cancellation
- Must appear BEFORE cancellation is processed

**User Options:**
- **Accept:** Proceed with cancellation, penalties applied
- **Reject:** Cancel the cancellation request, shift remains confirmed

### ERP API Integration (TBD - To Be Determined Before Development)

**API Details to be specified in development phase:**
- API endpoint URL
- Authentication method
- Request payload format
- Response handling (success/error)
- Retry mechanism for failed requests

**Required Data Fields:**
- Staff/Nursing Assistant ID
- Shift/Assignment ID
- Deduction amount (100 HKD)
- Deduction reason (code)
- Timestamp
- User who processed cancellation (if applicable)

---

## 🎚️ Bonus Opportunities (Future Enhancement)

Potential additional scoring factors for future iterations:

1. **Last-Minute Acceptance Bonus**
   - Accepting shift within 2 hours of start time
   - +2 points bonus

2. **Peak Period Bonus**
   - Working holidays, weekends, night shifts
   - +1 point per peak shift

3. **Difficult Location Bonus**
   - Working at hard-to-staff care homes
   - +1 point per assignment

4. **Positive Feedback Bonus**
   - High ratings from care homes
   - +1 to +3 points based on rating

5. **Certification Bonus**
   - Additional qualifications/certifications
   - +2 points per certification

---

## 📈 Score Management

### Manual Override
- **Authorized Users:** System administrators
- **Use Cases:** Exceptional circumstances, system errors, appeals
- **Audit Trail:** All manual changes logged with reason and user ID

### Score Visibility
- **For Nursing Assistants:** Can view own score (transparency recommended)
- **For Care Homes:** Can see scores of available staff (for trust)
- **For Administrators:** Full visibility with audit trail

### Reporting
- **Monthly Score Statements:** Automatic generation
- **Penalty Reports:** Track financial deductions
- **Trend Analysis:** Score changes over time

---

## ⚖️ Tie-Breaking Rules

When multiple nursing assistants have similar scores, allocation priority:

1. **Previous Work History:** Staff who've worked at that care home before
2. **Geographic Proximity:** Closer staff prioritized
3. **Seniority:** Longer tenure with Prestige Health
4. **First-Come-First-Served:** Order of application/availability

---

## 🚨 Emergency Override Protocols

### Manual Override Triggers
1. **Emergency Staffing:** Critical shortage situations
2. **System Errors:** Technical issues preventing automatic allocation
3. **VIP Care Homes:** Special priority clients (if applicable)

### Override Process
- Requires administrator authorization
- Must include documented reason
- Affects both scoring and financial penalties
- Audit log maintained for compliance

---

## 📋 Implementation Checklist

- [ ] Define initial base score for new staff
- [ ] Implement attendance tracking mechanism
- [ ] Build score calculation engine
- [ ] Create warning UI modal with accept/reject options
- [ ] Integrate ERP API (endpoint to be determined)
- [ ] Set up score tier system for allocation priority
- [ ] Create manual override interface for administrators
- [ ] Build reporting dashboards
- [ ] Implement audit logging
- [ ] Test tie-breaking rules
- [ ] Document appeal process for penalties

---

## 🤔 Open Questions for Further Discussion

1. **Maximum Negative Score:** Should there be a floor (e.g., -10) or can it go indefinitely negative?
2. **Score Recovery:** Should old penalties decay over time (e.g., absences older than 6 months count less)?
3. **Initial Score:** What starting score for new staff (recommendation: 5-10)?
4. **Grace Period:** Should new staff have a probation period with modified rules?
5. **Appeals Process:** How should staff contest penalties they believe are unfair?

---

## 📝 Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-24 | BMAD Analyst (Mary) | Initial specification created |

---

**Next Steps:**
- Review and validate specification with stakeholders
- Determine ERP API technical details before development
- Define initial score parameters
- Design UI/UX for warning messages
- Create administrator override interface specifications
