Based on the **original handwritten/printed requirements** and the detailed **3-hour meeting transcript**, I have compiled a comprehensive **User & Product Requirements Specification (URS/PRS)**.

This document bridges the gap between the client's high-level wish list and the technical realities/workflows discussed in the meeting.

---

# **Project: Health Helper Dispatch Sub-System (App & Web Portal)**
**Version:** 1.0 (Post-Meeting Analysis)
**Date:** November 25, 2025

## **1. Executive Summary**
The system is a **middleware solution** (Mobile App for Workers + Web Portal for Admins) that sits on top of the client’s existing **Master ERP**. It aims to digitize the job dispatching process, reduce manual WhatsApp communication, and enforce attendance rules.

**Core Philosophy:**
*   **ERP is Master:** The ERP owns the data (Workers, Jobs, Pay).
*   **Sub-System is for Operations:** It handles the "Marketplace" logic (Job posting, Grabbing, Notifying).
*   **Hybrid Automation:** While the goal is automation, the client retains manual control over *when* jobs are released and *who* gets priority.

---

## **2. System Architecture & Integration**

### **2.1 Data Synchronization Strategy**
*   **Direction:** Primarily **One-Way (ERP → Sub-System)** for core data.
*   **Sync Frequency:** Periodic API calls (e.g., daily at 5:00 PM or hourly) rather than real-time streaming, to avoid overloading the ERP.
*   **Write-Back (Sub-System → ERP):**
    *   **Safe Mode:** For critical actions (Cancellations, Penalties), the system will **not** directly modify ERP data to prevent corruption. Instead, it will generate a **"To-Do List" / "Action Report"** for Admins to manually update the ERP.
    *   **Job Confirmation:** If the ERP API allows, confirmed jobs can be written back. If not, a confirmation list is generated.

### **2.2 Defined Interfaces**
*   **Worker Auth:** Login via **Phone Number** (mapped to ERP Staff ID). No email required.
*   **Job Data Ingestion:** The system pulls: `Job ID`, `Date`, `Time`, `Venue Code`, `Job Type (RN, EN, HW, PCW)`, `Salary`, `Address` (See 4.2 for logic).

---

## **3. User Roles & Permissions**

1.  **Health Worker (App User):** Can view jobs, grab jobs, view schedule, receive notifications, view payslip (link).
2.  **Agency Admin (Web Portal):** Can import jobs from ERP, curate job lists, release jobs (publish), manage cancellations, manage "Priority Lists."
3.  **Care Home (Client):** *Limited Scope in Phase 1.* They do not have a login yet. They interact via WhatsApp/Email confirmations sent by the Agency.

---

## **4. Functional Requirements: Mobile App (Worker Side)**

### **4.1 Onboarding & Login**
*   **Account Creation:** Workers do not "Sign Up" freely. Their accounts are generated based on the ERP Employee List.
*   **Profile Management:**
    *   Users can view their details.
    *   **Document Update:** Users can upload renewed licenses/certificates (e.g., SCCN, First Aid).
    *   **Expiry Logic:** System checks expiry dates imported from ERP. If a license is expired, the user is **blocked** from seeing/accepting relevant jobs.

### **4.2 Job Listing & "The Market"**
*   **View Modes:**
    *   **Priority View:** Jobs explicitly targeted to them (because they are on a "Preferred List").
    *   **Public Sea (公海):** General jobs available to all qualified staff.
    *   **Job Grouping:** Users see grouped jobs (e.g., "Haven of Hope - Nov"). They click in to select specific dates/shifts.
*   **Job Details Card:**
    *   Must show: Date, Time, District, Care Home Name.
    *   **Address Logic:**
        *   *Standard:* Shows Care Home address.
        *   *Escort/Home Care:* Must display the **"Service Address"** (patient's location), NOT the NGO's office address.
    *   **Special Notes:** Vital. Must include text + images (e.g., map photos, ward instructions) pulled from the Admin setup.

### **4.3 Job Application (The "Grabbing" Process)**
*   **Flow:** User selects Job $\rightarrow$ Views Details $\rightarrow$ Clicks "Apply" $\rightarrow$ **Mandatory Pop-up:** "Terms & Conditions / Cancellation Penalty Warning" $\rightarrow$ User Confirms.
*   **Logic:**
    *   **Scenario A (First-Come-First-Served):** If the post is set to FCFS, the first user to confirm gets it.
    *   **Scenario B (Application Mode):** Users apply, Admin selects the best candidate manually.
*   **Conflict Check:** System prevents users from booking overlapping shifts (e.g., taking a PM shift when they already have a PM shift).

### **4.4 My Schedule & History**
*   **Status Types:** "Pending Confirmation", "Confirmed", "Completed", "Cancelled".
*   **Payslip:** A button linking to the existing external PDF payslip system (no native payroll processing).

### **4.5 Notifications**
*   **Push Notifications:**
    *   New Job Alerts (Filtered by preferences).
    *   Confirmation Alerts.
    *   Reminder: 1 day before the shift.
    *   **Quiet Hours:** Logic to prevent notifications between e.g., 12:00 AM and 7:00 AM (unless urgent).

---

## **5. Functional Requirements: Admin Portal**

### **5.1 Job Dispatch Management (The "Control Tower")**
*   **Import from ERP:** Admin clicks "Sync". System fetches unfilled jobs.
*   **The "Pending" List:** Jobs do not go live immediately. They sit in a "Pending Release" bucket.
*   **Priority Logic (The "17 People" Rule):**
    *   Admin maintains a **"Preference List"** per Care Home (e.g., "Staff A, B, C are regulars at Home X").
    *   **Tier 1 Release:** Admin releases jobs *only* to the Preference List first.
    *   **Tier 2 Release:** If not filled after $X$ hours (or manually triggered), release to "Public Sea."
*   **Bulk Operations:**
    *   Admin sees a list of 200 shifts.
    *   Can "Select All" $\rightarrow$ "Publish".
    *   **"Next" Workflow:** When reviewing applications, Admin approves one, system auto-loads the next application (Speed processing).

### **5.2 Cancellation & Penalty Management (Critical)**
*   **The "48-Hour Rule":**
    *   If Worker cancels $>48h$ before shift: Standard cancellation. Job returns to "Vacant" pool automatically.
    *   If Worker cancels $<48h$ before shift:
        1.  App shows "Penalty Warning" ($300 deduction + Bonus forfeit).
        2.  Worker confirms cancellation.
        3.  **System Action:**
            *   Job becomes "Vacant" (re-released to pool).
            *   **Ticket Generation:** Creates an entry in the **"Penalty / Deduction List"**.
*   **Admin Action:** Admin reviews the Penalty List and updates the ERP manually (to deduct salary).

### **5.3 Attendance Logic**
*   **Passive Attendance:** No GPS/Check-in required.
*   **Assumption:** If the shift time passes and no cancellation is filed, the system marks it as "Completed" automatically.
*   **Exception Handling:** Admin can manually change status to "No Show" or "Late" based on complaints from Care Homes.

### **5.4 WhatsApp Integration**
*   **Triggers:** When a job is confirmed or a specific urgent notice is needed.
*   **Template:** Admin selects a template $\rightarrow$ System opens WhatsApp Web/API with pre-filled text $\rightarrow$ Admin hits send. (Avoids full API automation cost/complexity in Phase 1).

---

## **6. Business Logic & Rules (Extracted from Meeting)**

1.  **No Direct Write-Back for Money:** The system must *never* automatically deduct money in the ERP. It only alerts the Admin to do it.
2.  **The "Fill Rate" Backup:** If a worker cancels, the primary goal is to refill the shift. The system must immediately repost the job to the pool.
3.  **Multi-Application:** A worker can apply for 3 conflicting jobs. Once one is Confirmed, the other 2 pending applications are auto-retracted/hidden.
4.  **Rating System:**
    *   Workers start with a base score (e.g., 50).
    *   Good attendance = Points added (or maintenance).
    *   No Show / Late = Points deducted.
    *   *Usage:* Higher score = Access to better jobs or seen first in "Application Mode."

## **7. Deliverables Checklist**
*   **Workflow Diagram:** Visualizing the flow: ERP Import $\rightarrow$ Pending Pool $\rightarrow$ Priority Release $\rightarrow$ Public Release $\rightarrow$ Confirmation $\rightarrow$ Attendance.
*   **UI Mockups:** Specifically for the "Job List" (Worker) and "Batch Processing" (Admin).
*   **API Specification:** Definition of the JSON payloads for syncing "Jobs" and "Workers" from ERP.

## **8. Future Considerations (Phase 2)**
*   **Care Home Portal:** Allow clients to log in and request staff directly.
*   **Full WhatsApp Automation:** Bot-based responses.
*   **Smart AI Matching:** Auto-suggesting staff based on location/rating without Admin manual release.