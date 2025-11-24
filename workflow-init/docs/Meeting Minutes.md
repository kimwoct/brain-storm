## Prestige Health Care Agency Ltd

**Date:** [Meeting Date from transcript context]  
**Location:** [Meeting Location]  
**Attendees:** System Analyst/Developer, Agency Management Team, Operations Staff

---

## Executive Summary

This meeting focused on developing a digital matching system (配對系統) to streamline the process of connecting healthcare workers with care facilities. The discussion covered system requirements, workflow optimization, data integration with existing ERP systems, and user interface design considerations.

---

## 1. System Overview and Objectives

### 1.1 Project Name Change
- **Decision:** Renamed from "預約系統" (Booking System) to "配對系統" (Matching System)
- **Rationale:** Better reflects the core function of matching healthcare workers with facility needs

### 1.2 Primary Goals
- Reduce manual data entry workload for staff
- Enable faster job posting and worker assignment
- Improve operational efficiency during high-volume periods
- Create foundation for potential future self-service portal for care facilities

---

## 2. User Registration and Authentication

### 2.1 Login Credential Discussion

**Challenge Identified:** Healthcare workers (姐姐) may not have email addresses

**Solutions Discussed:**

\begin{itemize}
\item \textbf{Phone Number as Login ID} (Primary recommendation)
  \begin{itemize}
  \item Most accessible option for workers
  \item Concern raised: Workers may change phone numbers
  \item Mitigation: Workers typically notify agency when changing WhatsApp numbers
  \end{itemize}
\item \textbf{Staff Number} (Alternative considered but rejected)
  \begin{itemize}
  \item Workers may not remember staff numbers initially
  \item Only assigned after formal employment begins
  \end{itemize}
\end{itemize}

**Decision:** Proceed with phone number as primary login identifier, with provisions for updating when numbers change

### 2.2 Account Creation Process

1. Worker completes initial registration via iPad
2. Data captured and transferred to matching system
3. System automatically creates account with:
   - Login ID (phone number)
   - Password
   - Basic profile information

---

## 3. Search and Staff Identification System

### 3.1 Current Workflow Analysis

**Staff Search Methods Used:**

\begin{table}
\begin{tabular}{|l|l|l|}
\hline
Method & Priority & Notes \\
\hline
Staff Number & Primary & Modified WhatsApp contact names \\
Phone Number & Secondary & Used when staff number unavailable \\
Name & Tertiary & Multiple workers may share names \\
\hline
\end{tabular}
\caption{Staff identification methods in current workflow}
\end{table}

**Key Insight:** Staff modify WhatsApp contact names to show employee numbers, enabling quick identification during communication

### 3.2 System Design Implications

**UI Requirements:**
- Support multiple search methods (staff number, phone, name)
- Implement autocomplete/suggestion functionality
- Display: Name + Staff Number + Current Location
- Screenshot of current interface requested for reference

---

## 4. Job Posting Workflow

### 4.1 Data Input Interface Design Philosophy

**Core Principle:** Prioritize speed and accuracy over aesthetics

**Approach Discussion:**

\begin{itemize}
\item \textbf{Dropdown Selection vs. Text Input}
  \begin{itemize}
  \item For facility names: Dropdown preferred (approximately 20 major facilities)
  \item For shift codes: Currently uses shorthand codes (e.g., "013" = specific facility, "A82" = staff ID)
  \item Staff are highly familiar with facility codes
  \end{itemize}
\item \textbf{Time Entry Automation}
  \begin{itemize}
  \item Shift type selection (e.g., PC8 = 8-hour shift) auto-populates time ranges
  \item End time automatically calculated from start time
  \item Manual override capability maintained for exceptions
  \end{itemize}
\end{itemize}

### 4.2 Facility-Specific Configuration

**Requirement:** Each facility has unique shift patterns and time requirements

**Proposed Solution:**

\begin{enumerate}
\item Facilities provide template with shift codes and corresponding time ranges
\item System pre-configures shift codes during facility setup
\item When shift code selected, system auto-populates:
  \begin{itemize}
  \item Start time
  \item End time
  \item Working hours
  \end{itemize}
\item Staff can adjust times manually if needed (late arrivals, early departures)
\end{enumerate}

**Calculation Logic:**
- Final working hours calculated from actual start/end times entered
- Preset shift hours serve as default template only
- Manual adjustments take precedence for billing purposes

---

## 5. ERP Integration Strategy

### 5.1 Current Architecture

**Two-System Approach:**

\begin{figure}
\centering
\textbf{System Flow Diagram}
\begin{itemize}
\item \textbf{Phase 1:} ERP System → Data Export → Matching System → Auto-post Creation
\item \textbf{Future Phase 2:} Facility Portal → Direct Entry → Matching System → Pending Review → ERP Import
\end{itemize}
\caption{Proposed integration workflow between ERP and matching system}
\end{figure}

### 5.2 Data Synchronization

**Data Fields to Transfer:**

\begin{table}
\begin{tabular}{|l|c|l|}
\hline
Field & Required & Notes \\
\hline
Facility Name/Code & Yes & Primary identifier \\
Date & Yes & Service date \\
Shift Type & Yes & PC8, A, B, etc. \\
Start Time & Yes & Auto-calculated or manual \\
End Time & Yes & Auto-calculated or manual \\
Working Hours & Yes & Final calculation \\
Location/Address & Conditional & Discussed in detail below \\
\hline
\end{tabular}
\caption{Data mapping between ERP and matching system}
\end{table}

### 5.3 Integration Challenges

**Challenge:** ERP requires complete data fields for job entry, but matching system may post jobs with partial information

**Solution Approach:**
- Matching system creates jobs with available information
- API integration pulls data from ERP to create matching posts
- Pending order status for facility-initiated posts requiring staff review
- Staff completes missing fields before finalizing in ERP

**Decision:** Initial implementation focuses on ERP-to-Matching data flow; facility self-service portal development deferred to Phase 2

---

## 6. Location and Privacy Considerations

### 6.1 Address Display Policy

**Current Practice:**
- Job posts show: Facility name + District + Shift time
- Detailed address NOT displayed in initial posting
- Full address provided only after worker confirms acceptance

**Rationale:**
- Privacy protection for facilities
- Prevents workers from contacting facilities directly
- Reduces facility phone disruptions

### 6.2 Alternative Approach Discussed

**Proposal:** Display full address in job postings

**Concerns Raised:**
- Workers may contact facilities directly
- Facilities receive excessive phone calls
- Agency loses control of communication channel

**Counterarguments:**
- Workers can easily find facility addresses online via facility names
- Providing address upfront improves transparency
- Reduces back-and-forth communication

**Final Decision:** Maintain current practice of withholding detailed address until confirmation; revisit based on operational experience

---

## 7. QR Code Integration

### 7.1 Facility-Specific QR Codes

**Concept:** Each facility receives unique QR code linked to their profile

**Benefits:**
- Workers scan code to auto-populate facility information
- Eliminates manual facility selection step
- Facilitates potential future self-service model for facilities

**Use Case:**
- Facility manages 10 care homes → receives 10 unique QR codes
- Each QR code maps to specific location
- Scanning automatically sets facility context in matching system

**Decision:** Implement QR code system for facility identification

---

## 8. Worker Job Selection and Preferences

### 8.1 Facility Preference System

**Current Situation:**
- Workers develop preferences for specific facilities
- Some workers want to work only at familiar locations
- Others open to working at any facility

**Proposed Feature:** Facility Preference List

**Functionality:**

\begin{itemize}
\item Workers indicate preferred facilities during profile setup
\item System prioritizes showing jobs from preferred facilities
\item Two-tier posting system:
  \begin{enumerate}
  \item Jobs sent first to workers with facility on preference list
  \item If no matches, jobs opened to all available workers
  \end{enumerate}
\end{itemize}

### 8.2 Job Visibility Management

**Challenge:** How to manage job post visibility when many workers access system simultaneously

**Solution Options Discussed:**

\begin{table}
\begin{tabular}{|p{4cm}|p{4cm}|p{4cm}|}
\hline
\textbf{Approach} & \textbf{Pros} & \textbf{Cons} \\
\hline
Show all jobs to all workers & Transparent, democratic & Workers overwhelmed, causes confusion \\
\hline
Limit visible jobs per worker (5-6 at a time) & Manageable job list & May miss opportunities \\
\hline
Rotate job visibility periodically & Fair distribution & Requires constant app checking \\
\hline
Priority-based system (ratings/history) & Rewards reliable workers & May disadvantage new workers \\
\hline
\end{tabular}
\caption{Job visibility management strategies}
\end{table}

**Recommendation:** Implement hybrid approach combining preference matching with limited visibility window

---

## 9. Confirmation and Acknowledgment Process

### 9.1 Terms and Conditions Display

**Requirement:** Workers must acknowledge facility-specific requirements before job confirmation

**Implementation:**

\begin{enumerate}
\item Worker selects job and clicks "Apply"
\item System displays:
  \begin{itemize}
  \item Facility policies and rules (images/documents)
  \item Start time and location confirmation
  \item Reporting instructions
  \end{itemize}
\item Worker must click "Acknowledge" checkbox
\item "Confirm Booking" button enabled only after acknowledgment
\item System logs acknowledgment timestamp and user ID
\end{enumerate}

**Rationale:** Creates clear record that worker received and accepted facility requirements

### 9.2 Final Confirmation Screen

**Information Displayed:**
- Facility name and address
- Shift date and time (start/end)
- Reporting location and instructions
- Working hours
- Special requirements or notes

**Action Required:**
- Worker reviews all details
- Checks confirmation box
- Clicks final confirmation button (terminology to be determined - not "booking")

**Terminology Discussion:**
- Avoid "預約" (booking) as job not guaranteed until agency assigns
- Consider "申請" (apply) or similar term
- Final wording to be determined based on operational context

---

## 10. Rating and Performance System (Future Consideration)

### 10.1 Worker Rating System

**Purpose:** Enable facilities to rate worker performance

**Potential Benefits:**
- Helps identify reliable workers for priority assignment
- Addresses facility requests for specific workers or quality standards
- Provides objective basis for worker recognition

**Facility Use Case:**
- Facility requests agency to send only workers meeting certain standards
- System can filter based on rating thresholds
- Poor-performing workers receive fewer opportunities

**Implementation Considerations:**
- Rating criteria to be defined
- Rating visibility (public vs. internal only)
- Appeal process for disputed ratings
- Integration with job assignment priority logic

**Status:** Concept discussed for future phases; not in initial scope

---

## 11. Automation and Time-Saving Goals

### 11.1 Business Objectives

**Primary Goal:** Enable staff to handle increased order volume without proportional staff increases

**Key Insight:** "不是省人手" (Not about reducing staff) - It's about maximizing capacity during peak periods

**Expected Benefits:**

\begin{itemize}
\item Faster job posting (reduced data entry time)
\item Automated matching based on worker preferences and availability
\item Reduced phone interruptions
\item Staff can focus on exception handling and customer service
\item Ability to serve more clients with existing team
\end{itemize}

### 11.2 UI/UX Design Principles

**Guiding Principle:** "不要靚,我們要快,要準" (Not about looking good, need fast and accurate)

**Implementation Approach:**
- Minimize typing through dropdowns and auto-complete
- Pre-populate fields based on facility profiles
- Use familiar codes and shortcuts staff already know
- Mobile-optimized interface (iPad primary device)
- Single-click actions wherever possible

---

## 12. Outstanding Questions and Future Discussions

### 12.1 Multiple Job Applications

**Question:** How to handle workers who apply for multiple jobs simultaneously?

**Scenarios:**
- Worker applies for many jobs, gets offered multiple
- Worker accepts multiple jobs then cancels later
- How to prevent job hoarding?

**Requires Further Discussion:**
- Application limits per worker
- Acceptance timeframes
- Cancellation policies and penalties
- Re-posting workflow for cancelled jobs

### 12.2 After-Hours Job Posting

**Scenario:** Facility submits job request after office hours (post-10 PM)

**Current Gap:** No staff available to review and approve posting

**Potential Solutions:**
- Automated posting with validation rules
- Delayed posting queue for next business day
- Emergency contact system for urgent requests
- Clear facility communication about posting SLAs

**Decision:** Define validation rules allowing automatic posting when all required fields complete; otherwise queue for staff review

### 12.3 Commission and Payment Handling

**Discussed But Deferred:**
- Variable commission rates by facility
- Special facility pricing configurations
- How pricing displayed to workers
- Commission calculation and disbursement timing

**Action:** Requires separate discussion with finance team to define pricing models and system requirements

---

## 13. Technical Implementation Notes

### 13.1 Development Approach

**Technology Stack:**
- Web-based system (accessible via browser)
- Mobile-responsive design (iPad optimized)
- API integration with existing ERP system

**Phased Rollout:**

\begin{enumerate}
\item Phase 1: Staff-facing interface for job posting and worker assignment
\item Phase 2: Worker-facing mobile app for job browsing and applications
\item Phase 3: Facility self-service portal (conditional on Phase 1/2 success)
\end{enumerate}

### 13.2 Data Requirements Gathering

**Action Items:**
- Agency to provide screenshot of current search interface
- Facility list with codes and shift configurations
- Sample data for system testing
- Current ERP data export format documentation

---

## 14. Training and Change Management

### 14.1 Staff Training Plan

**Approach:**
- Hands-on workshop format
- 30-minute training sessions
- Multiple sessions to accommodate schedules
- Focus on practical workflow scenarios

**Confidence:** Team expressed that training burden is manageable given simplicity of interface

### 14.2 Facility Onboarding (Future)

**When self-service portal launched:**
- Group training sessions for facility administrators
- Comprehensive user guides with step-by-step instructions
- Validation rules prevent incomplete submissions
- Helpdesk support during initial rollout

---

## 15. Action Items and Next Steps

\begin{table}
\begin{tabular}{|l|p{6cm}|l|l|}
\hline
\textbf{Item} & \textbf{Description} & \textbf{Owner} & \textbf{Timeline} \\
\hline
1 & Provide current UI screenshots & Agency & ASAP \\
\hline
2 & Compile facility list with codes & Agency & 1 week \\
\hline
3 & Document shift type configurations & Agency & 1 week \\
\hline
4 & Define ERP data export format & Agency IT & 2 weeks \\
\hline
5 & Design initial UI mockups & Developer & 2 weeks \\
\hline
6 & Define job posting validation rules & Joint & 2 weeks \\
\hline
7 & Clarify address display policy & Management & 1 week \\
\hline
8 & Design worker preference feature & Developer & 3 weeks \\
\hline
9 & Define rating system criteria & Management & Phase 2 \\
\hline
10 & Schedule follow-up requirements session & All & 2 weeks \\
\hline
\end{tabular}
\caption{Action items and responsibilities}
\end{table}

---

## 16. Decisions Made

\begin{enumerate}
\item \textbf{System Naming:} Adopt "配對系統" (Matching System) nomenclature
\item \textbf{Login Credentials:} Use phone numbers as primary login identifier
\item \textbf{Search Functionality:} Support multiple search methods (staff number priority, with phone/name alternatives)
\item \textbf{Time Entry:} Implement auto-calculation with manual override capability
\item \textbf{Integration Strategy:} Phase 1 focuses on ERP→Matching flow; facility portal deferred
\item \textbf{Address Display:} Maintain current practice of withholding until confirmation
\item \textbf{QR Codes:} Implement facility-specific QR code system
\item \textbf{Terms Acknowledgment:} Mandatory checkbox before job confirmation
\item \textbf{UI Philosophy:} Prioritize speed and accuracy over visual design
\item \textbf{Validation Rules:} Enable automatic posting when all required fields complete
\end{enumerate}

---

## 17. Open Issues Requiring Resolution

\begin{itemize}
\item Job application limits per worker
\item Job visibility rotation/refresh logic
\item Confirmation button terminology
\item Commission rate configuration by facility
\item After-hours posting approval workflow
\item Worker rating system design (Phase 2)
\item Facility self-service training approach (Phase 2)
\end{itemize}

---

## 18. Meeting Conclusion

The session successfully established foundational requirements for the matching system. Key focus areas identified include workflow optimization for current staff operations, sensible ERP integration strategy, and forward-looking design accommodating future facility self-service capability.

Next meeting scheduled for requirements validation and UI mockup review.

---

## Appendices

### Appendix A: Terminology Glossary

\begin{table}
\begin{tabular}{|l|l|l|}
\hline
\textbf{Chinese Term} & \textbf{English} & \textbf{Definition} \\
\hline
配對系統 & Matching System & Core platform matching workers with facilities \\
姐姐 & Healthcare Workers & Frontline care staff \\
院舍 & Care Facilities & Elderly care homes, hospitals, clinics \\
軟舍 & Facility Portal & Self-service interface for facilities (future) \\
PC8 & 8-Hour Shift & Standard 8-hour working shift \\
A間 & Shift Code A & Facility-specific shift designation \\
Post & Job Posting & Available work opportunity \\
\hline
\end{tabular}
\caption{Key terminology used in discussions}
\end{table}

### Appendix B: Reference Materials Requested

- Current staff search interface screenshot
- Facility master list with codes
- Shift type configuration table
- Sample ERP data export
- Current WhatsApp workflow documentation

---

**Minutes Prepared By:** [System Analyst Name]  
**Date Prepared:** [Current Date]  
**Distribution:** Meeting Attendees, Project Stakeholders, Management Team