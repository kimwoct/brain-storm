# Technical Design Document (TDD)
**Prestige Health Dispatch System (PHC)**

**Version:** 1.0
**Date:** 2025-11-24
**Author:** Technical Lead
**Status:** Draft

---

## 1. ARCHITECTURE OVERVIEW

### 1.1 System Stack

```
┌──────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                   │
├──────────────────────────────────────────────────────────────┤
│ React.js (Admin Portal)          │ WhatsApp Business API     │
│ Tailwind CSS                                                 │
│ Responsive Design                                            │
├──────────────────────────────────────────────────────────────┤
│                          API GATEWAY                         │
├──────────────────────────────────────────────────────────────┤
│  Express.js (Node.js)  │  Rate Limiting │ Auth Middleware    │
├──────────────────────────────────────────────────────────────┤
│                        APPLICATION LAYER                     │
├──────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Matching     │  │ Scoring      │  │ Notification │        │
│  │ Engine       │  │ Service      │  │ Service      │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Attendance   │  │ Penalty      │  │ Sync         │        │
│  │ Service      │  │ Service      │  │ Orchestrator │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
├──────────────────────────────────────────────────────────────┤
│                        DATA LAYER                            │
├──────────────────────────────────────────────────────────────┤
│                           mySQL                              |
├──────────────────────────────────────────────────────────────┤
│                      INTEGRATION LAYER                       │
├──────────────────────────────────────────────────────────────│
│  ERP REST APIs  │ WhatsApp API  │ Cron Jobs  │ Webhooks │    │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 Technology Stack

**Frontend:**
- Framework: React.js 18+ (Vite build tool)
- Styling: TailwindCSS 3+
- State Management: Redux Toolkit + RTK Query
- Forms: React Hook Form + Zod validation
- Charts: Recharts for metrics
- Testing: Jest + React Testing Library

**Backend:**
- Runtime: Java 11+ 
- Framework: Java Spring Framework 2.7+
- Language: Java 11+ 
- Authentication: JWT + bcrypt
- API Docs: Swagger/OpenAPI 3.0
- Validation: Joi/Express-validator

**Database:**
- Primary: mySQL

**File Storage:**
- Emergency Files: In existing server
- Certificates/Documents: In existing server

**Queue/Job Processing:**
- BullMQ (Redis-based) for background jobs
- Scheduled jobs via node-cron

**External Services:**
- Firebase: Firebase Cloud Messaging (FCM) for web push notifications
- ERP Integration: RESTful APIs with OpenAPI/Swagger

---

### 1.3 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Client Layer                                 │
├─────────────────────────────────────────────────────────────────┤
│  Admin Portal (React)      │   Staff Portal (React)             │
│  - Desktop/Mobile          │   - Mobile-First Web App           │
│  - Dashboards              │   - Dashboard, Shifts, Profile     │
│                            │                                    │
│                            │   WhatsApp (Business API)          │
│                            │   - Notifications                  │
│                            │   - Confirmations                  │
└─────────────────────────────────────────────────────────────────┘
                                 ▲
                                 │ HTTPS/TLS
┌────────────────────────────────┴────────────────────────────────┐
│              API Gateway (Express.js)                           │
├─────────────────────────────────────────────────────────────────┤
│  ├─ Auth Middleware (JWT)                                       │
│  ├─ Rate Limiter (Redis)                                        │
│  ├─ Request Validator                                           │
│  ├─ Error Handler                                               │
│  └─ Logger (Winston)                                            │
└─────────────────────────────────────────────────────────────────┘
                                 │
┌────────────────────────────────┴────────────────────────────────┐
│              Application Services                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐      ┌──────────────────┐                 │
│  │ Assignment       │      │ Matching         │                 │
│  │ Controller       │─────▶│ Engine           │                 │
│  └──────────────────┘      └──────────────────┘                 │
│         │                         │                             │
│         ▼                         ▼                             │
│  ┌──────────────────┐      ┌──────────────────┐                 │
│  │ Attendance       │      │ Scoring          │                 │
│  │ Controller       │      │ Service          │                 │
│  └──────────────────┘      └──────────────────┘                 │
│         │                         │                             │
│         ▼                         ▼                             │
│  ┌──────────────────┐      ┌──────────────────┐                 │
│  │ Penalty          │      │ Sync             │                 │
│  │ Service          │      │ Orchestrator     │                 │
│  └──────────────────┘      └──────────────────┘                 │
│         │                         │                             │
│         ▼                         ▼                             │
│  ┌──────────────────┐      ┌──────────────────┐                 │
│  │ Notification     │      │ Report           │                 │
│  │ Service          │      │ Generator        │                 │
│  └──────────────────┘      └──────────────────┘                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                                 │
┌────────────────────────────────┴────────────────────────────────┐
│              Data Layer                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐                                           │
│  │ PostgreSQL       │─ Table: staff, locations, assignments,    │
│  │ (Primary DB)     │   attendance, penalties, scores, etc.     │
│  └──────────────────┘                                           │
│                                                                 │
│  ┌──────────────────┐                                           │
│  │ Redis Cache      │─ Session storage, API rate limiting,      │
│  │                  │   Job queue, Caching                      │
│  └──────────────────┘                                           │
│                                                                 │
│  ┌──────────────────┐                                           │
│  │ S3/Azure Blob    │─ Emergency files, certificates            │
│  │ (File Storage)   │                                           │
│  └──────────────────┘                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                                 │
┌────────────────────────────────┴────────────────────────────────┐
│              External Integrations                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐      ┌──────────────────┐                 │
│  │ ERP System       │◄────▶│ axios HTTP       │                 │
│  │ - Staff data     │      │ client           │                 │
│  │ - Locations      │      └──────────────────┘                 │
│  │ - Demands        │            ▲                              │
│  │ - Assignments    │            │                              │
│  │ - Settlements    │            │ ERP API calls                │
│  └──────────────────┘            │                              │
│                                  │                              │
│  ┌──────────────────┐            │                              │
│  │ WhatsApp         │◄───────────┘                              │
│  │ Business API     │      Webhook notifications (inbound)      │
│  │                  │                                           │
│  └──────────────────┘                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. DATABASE SCHEMA

### 2.1 Entity Relationship Diagram

```
┌─────────────────┐        ┌──────────────────┐
│     Staff       │        │   Location       │
├─────────────────┤        ├──────────────────┤
│ PK staff_id     │        │ PK location_id   │
│     erp_staff_id│        │     erp_loc_id   │
│     name_zh     │        │     name_zh      │
│     name_en     │        │     name_en      │
│     hkid        │        │     address      │
│     phone       │        │     region       │
│     whatsapp    │        │     district     │
│     email       │        │     contact_name │
│     bank_code   │        │     contact_phone│
│     bank_account│        │     status       │
│     status      │        │     created_at   │
│     score       │        │     updated_at   │
│     tier        │        └────────┬─────────┘
│     created_at  │                 │
│     updated_at  │                 │
└────────┬────────┘                 │
         │                          │
         │                          │
         │     ┌───────────────────┘
         │     │
         ▼     ▼
┌──────────────────────────────────────────┐
│          Assignment                      │
├──────────────────────────────────────────┤
│ PK assignment_id                         │
│     phc_assignment_id                    │
│     erp_assignment_id (nullable)         │
│ FK erp_demand_id                         │
│ FK staff_id                              │
│ FK location_id                           │
│     assignment_date                      │
│     shift_start                          │
│     shift_end                            │
│     assigned_by (system/manual)          │
│     assigned_timestamp                   │
│     status (pending/confirmed/cancelled) │
│     confirmed_timestamp (nullable)       │
│     cancelled_timestamp (nullable)       │
│     cancellation_reason (nullable)       │
│     created_at                           │
│     updated_at                           │
└────────┬─────────────────────────────────┘
         │
         │
         ▼
┌────────────────┐        ┌────────────────┐
│  Attendance    │        │    Penalty     │
├────────────────┤        ├────────────────┤
│ PK attend_id   │        │ PK penalty_id  │
│ FK assignment_id│       │ FK assignment_id│
│ FK staff_id    │        │ FK staff_id    │
│     clock_in   │        │     penalty_type│
│     clock_out  │        │     amount     │
│     actual_hours│       │     currency   │
│     status     │        │     reason     │
│     verified_by│        │     score_impact│
│     created_at │        │     applied_at │
└────────────────┘        │     status     │
                          │     erp_synced │
                          │     created_at │
                          └────────────────┘

┌────────────────┐
│  ScoreHistory  │
├────────────────┤
│ PK history_id  │
│ FK staff_id    │
│     score_change│
│     new_score  │
│     reason     │
│     created_at │
└────────────────┘

┌────────────────┐
│  EmergencyFile │
├────────────────┤
│ PK file_id     │
│     title      │
│     description│
│     file_url   │
│     priority   │
│     regions    │ # JSON array
│     uploaded_by│
│     created_at │
│     updated_at │
└────────────────┘

┌────────────────┐
│   Underlist    │
├────────────────┤
│ PK id          │
│ FK location_id │
│ FK staff_id    │
│     priority   │ # 1,2,3...
│     created_at │
└────────────────┘

┌────────────────┐
│   Blacklist    │
├────────────────┤
│ PK id          │
│ FK location_id │
│ FK staff_id    │
│     reason     │
│     created_at │
│     created_by │
└────────────────┘
```

### 2.2 Table Details

#### Table: `staff`
```sql
CREATE TABLE staff (
    staff_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    erp_staff_id VARCHAR(50) UNIQUE NOT NULL,  -- ERP unique ID
    name_zh VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    hkid VARCHAR(20) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    whatsapp VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    bank_code VARCHAR(10),
    bank_account VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',  -- active, inactive, suspended
    score INTEGER DEFAULT 5,  -- Initial score for new staff
    tier VARCHAR(20) DEFAULT 'Bronze',  -- Gold, Silver, Bronze, UnderReview
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT chk_hkid CHECK (hkid ~ '^[A-Z]{1,2}[0-9]{6}[0-9A]$'),
    CONSTRAINT chk_phone CHECK (phone ~ '^[0-9]{8}$'),
    CONSTRAINT chk_status CHECK (status IN ('active', 'inactive', 'suspended'))
);

CREATE INDEX idx_staff_erp_id ON staff(erp_staff_id);
CREATE INDEX idx_staff_score ON staff(score DESC);
CREATE INDEX idx_staff_tier ON staff(tier);
```

#### Table: `location`
```sql
CREATE TABLE location (
    location_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    erp_location_id VARCHAR(50) UNIQUE NOT NULL,
    location_code VARCHAR(50) NOT NULL,
    name_zh VARCHAR(200) NOT NULL,
    name_en VARCHAR(200) NOT NULL,
    address TEXT NOT NULL,
    region VARCHAR(10) NOT NULL,  -- HKI, KLN, NT
    district VARCHAR(100),
    contact_name VARCHAR(100),
    contact_phone VARCHAR(20),
    service_type VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT chk_region CHECK (region IN ('HKI', 'KLN', 'NT')),
    CONSTRAINT chk_loc_status CHECK (status IN ('active', 'inactive'))
);

CREATE INDEX idx_location_erp_id ON location(erp_location_id);
CREATE INDEX idx_location_region ON location(region);
```

#### Table: `assignment`
```sql
CREATE TABLE assignment (
    assignment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phc_assignment_id VARCHAR(50) UNIQUE NOT NULL,
    erp_assignment_id VARCHAR(50),  -- After ERP confirmation
    erp_demand_id VARCHAR(50) NOT NULL,
    staff_id UUID NOT NULL REFERENCES staff(staff_id),
    location_id UUID NOT NULL REFERENCES location(location_id),
    assignment_date DATE NOT NULL,
    shift_start TIME NOT NULL,
    shift_end TIME NOT NULL,
    assigned_by VARCHAR(50) NOT NULL,  -- system_auto, manual_admin
    assigned_timestamp TIMESTAMP DEFAULT NOW(),
    status VARCHAR(30) DEFAULT 'pending_confirmation',
    confirmed_timestamp TIMESTAMP,
    cancelled_timestamp TIMESTAMP,
    cancellation_reason TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT chk_shift_time CHECK (shift_end > shift_start),
    CONSTRAINT chk_assigned_by CHECK (assigned_by IN ('system_auto', 'manual_admin')),
    CONSTRAINT chk_assignment_status CHECK (status IN ('pending_confirmation', 'confirmed', 'cancelled', 'no_show'))
);

CREATE INDEX idx_assignment_staff ON assignment(staff_id);
CREATE INDEX idx_assignment_location ON assignment(location_id);
CREATE INDEX idx_assignment_date ON assignment(assignment_date);
CREATE INDEX idx_assignment_status ON assignment(status);
CREATE UNIQUE INDEX idx_unique_demand_staff ON assignment(erp_demand_id, staff_id) WHERE status <> 'cancelled';
```

#### Table: `attendance`
```sql
CREATE TABLE attendance (
    attendance_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assignment_id UUID NOT NULL REFERENCES assignment(assignment_id),
    staff_id UUID NOT NULL REFERENCES staff(staff_id),
    clock_in TIMESTAMP,
    clock_out TIMESTAMP,
    actual_hours DECIMAL(5,2),  -- Calculated
    status VARCHAR(30) NOT NULL,  -- completed, partial, no_show
    verified_by VARCHAR(100),
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT chk_attendance_status CHECK (status IN ('completed', 'partial', 'no_show')),
    CONSTRAINT chk_clock CHECK (clock_out IS NULL OR clock_out > clock_in)
);

CREATE INDEX idx_attendance_assignment ON attendance(assignment_id);
CREATE INDEX idx_attendance_staff ON attendance(staff_id);
CREATE INDEX idx_attendance_date ON attendance((clock_in::DATE));
```

#### Table: `penalty`
```sql
CREATE TABLE penalty (
    penalty_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assignment_id UUID NOT NULL REFERENCES assignment(assignment_id),
    staff_id UUID NOT NULL REFERENCES staff(staff_id),
    penalty_type VARCHAR(50) NOT NULL,  -- cancellation, no_show
    amount DECIMAL(10,2) DEFAULT 100.00,
    currency VARCHAR(3) DEFAULT 'HKD',
    reason TEXT,
    score_impact INTEGER NOT NULL,  -- -1 or -2
    applied_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(30) DEFAULT 'pending_eru_sync',
    erp_synced BOOLEAN DEFAULT FALSE,
    erp_penalty_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT chk_penalty_type CHECK (penalty_type IN ('cancellation', 'no_show')),
    CONSTRAINT chk_amount CHECK (amount = 100.00)
);

CREATE INDEX idx_penalty_staff ON penalty(staff_id);
CREATE INDEX idx_penalty_applied ON penalty(applied_at);
```

#### Table: `score_history`
```sql
CREATE TABLE score_history (
    history_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    staff_id UUID NOT NULL REFERENCES staff(staff_id),
    old_score INTEGER NOT NULL,
    new_score INTEGER NOT NULL,
    score_change INTEGER NOT NULL,
    reason VARCHAR(200) NOT NULL,
    assignment_id UUID REFERENCES assignment(assignment_id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_score_staff ON score_history(staff_id);
CREATE INDEX idx_score_date ON score_history(created_at);
```

#### Table: `underlist`
```sql
CREATE TABLE underlist (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES location(location_id),
    staff_id UUID NOT NULL REFERENCES staff(staff_id),
    priority INTEGER NOT NULL,  -- 1 = highest
    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(location_id, staff_id),
    CHECK (priority > 0)
);

CREATE INDEX idx_underlist_location ON underlist(location_id);
CREATE INDEX idx_underlist_staff ON underlist(staff_id);
```

#### Table: `blacklist`
```sql
CREATE TABLE blacklist (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_id UUID NOT NULL REFERENCES location(location_id),
    staff_id UUID NOT NULL REFERENCES staff(staff_id),
    reason TEXT,
    created_by UUID REFERENCES staff(staff_id),
    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(location_id, staff_id)
);

CREATE INDEX idx_blacklist_location ON blacklist(location_id);
```

#### Table: `emergency_file`
```sql
CREATE TABLE emergency_file (
    file_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    file_url TEXT NOT NULL,
    file_type VARCHAR(50),
    file_size BIGINT,
    priority VARCHAR(20) DEFAULT 'Normal',
    regions JSONB,  -- ['HKI', 'KLN', 'NT'] or null for all
    uploaded_by UUID REFERENCES staff(staff_id),
    viewed_by JSONB DEFAULT '[]'::jsonb,  -- [staff_id1, staff_id2]
    confirmed_by JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_emergency_priority ON emergency_file(priority);
CREATE INDEX idx_emergency_created ON emergency_file(created_at);
```

#### Table: `api_log`
```sql
CREATE TABLE api_log (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    api_name VARCHAR(100) NOT NULL,
    endpoint VARCHAR(500),
    method VARCHAR(10),
    request_body JSONB,
    response_body JSONB,
    status_code INTEGER,
    error_message TEXT,
    duration_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_api_log_name ON api_log(api_name);
CREATE INDEX idx_api_log_date ON api_log(created_at);
```

---

## 3. CORE SERVICE DESIGNS

### 3.1 Scoring Service

```typescript
interface ScoringService {
  // Calculate current score for a staff member
  calculateScore(staffId: string): Promise<number>;

  // Update score based on action
  updateScore(
    staffId: string,
    action: 'attended' | 'cancelled' | 'no_show',
    assignmentId: string
  ): Promise<{ oldScore: number; newScore: number; change: number }>;

  // Get score history
  getScoreHistory(staffId: string, limit?: number): Promise<ScoreHistory[]>;

  // Manual score adjustment (admin only)
  manualAdjust(
    staffId: string,
    newScore: number,
    reason: string,
    adminId: string
  ): Promise<void>;

  // Calculate tier based on score
  calculateTier(score: number): 'Gold' | 'Silver' | 'Bronze' | 'UnderReview';
}

// Implementation
class ScoringServiceImpl implements ScoringService {
  async updateScore(staffId, action, assignmentId): Promise<any> {
    // Start transaction
    return await prisma.$transaction(async (tx) => {
      // Get current staff
      const staff = await tx.staff.findUnique({
        where: { staff_id: staffId },
        select: { score: true }
      });

      if (!staff) throw new Error('Staff not found');

      const oldScore = staff.score;
      let scoreChange: number;

      // Apply score change based on action
      switch (action) {
        case 'attended':
          scoreChange = 1;
          break;
        case 'cancelled':
          scoreChange = -1;
          break;
        case 'no_show':
          scoreChange = -2;
          break;
        default:
          throw new Error('Invalid action');
      }

      // Calculate new score (respect floor of -10)
      const newScore = Math.max(-10, oldScore + scoreChange);

      // Update staff score
      await tx.staff.update({
        where: { staff_id: staffId },
        data: {
          score: newScore,
          tier: this.calculateTier(newScore)
        }
      });

      // Create score history record
      const history = await tx.score_history.create({
        data: {
          staff_id: staffId,
          old_score: oldScore,
          new_score: newScore,
          score_change: scoreChange,
          reason: `${action.replace('_', ' ')} for assignment`,
          assignment_id: assignmentId
        }
      });

      // Also update ERP via API (async, non-blocking)
      this.updateERPScore(staffId, newScore, action, assignmentId).catch(err => {
        console.error('Failed to update ERP score:', err);
      });

      return {
        oldScore,
        newScore,
        change: scoreChange
      };
    });
  }

  private calculateTier(score: number): string {
    if (score >= 20) return 'Gold';
    if (score >= 10) return 'Silver';
    if (score >= 0) return 'Bronze';
    return 'UnderReview';
  }

  private async updateERPScore(
    staffId: string,
    newScore: number,
    action: string,
    assignmentId: string
  ) {
    const erpStaffId = await this.getERPStaffId(staffId);
    await axios.patch(
      `${ERP_BASE_URL}/api/v1/staff/${erpStaffId}/score`,
      {
        score_change: action === 'attended' ? 1 : (action === 'cancelled' ? -1 : -2),
        new_score: newScore,
        reason: action,
        assignment_id: assignmentId
      },
      { headers: { Authorization: `Bearer ${ERP_API_TOKEN}` } }
    );
  }
}
```

---

### 3.2 Matching Engine

```typescript
interface MatchingEngine {
  // Find best matches for a job demand
  findMatches(
    demandId: string,
    requiredCount: number
  ): Promise<Staff[]>;

  // Rank candidates based on criteria
  rankCandidates(
    candidates: Staff[],
    location: Location
  ): Promise<RankedCandidate[]>;
}

interface RankedCandidate {
  staff: Staff;
  score: number;      // Algorithm score (0-1)
  reasons: string[];  // Why this candidate was chosen
}

// Implementation
class MatchingEngineImpl implements MatchingEngine {
  async findMatches(demandId: string, requiredCount: number): Promise<Staff[]> {
    // Get demand details
    const demand = await this.getDemand(demandId);

    // Step 1: Get all available, eligible staff
    let candidates = await this.getEligibleCandidates(demand);

    // Step 2: Apply filters (availability, docs, blacklist)
    candidates = await this.applyFilters(candidates, demand);

    // Step 3: Rank candidates
    const ranked = await this.rankCandidates(candidates, demand.location);

    // Step 4: Select top N
    const selected = ranked.slice(0, requiredCount).map(r => r.staff);

    // Log matching decision
    await this.logMatchingDecision(demandId, selected, ranked);

    return selected;
  }

  private async getEligibleCandidates(demand: JobDemand): Promise<Staff[]> {
    const { date, shift_start, shift_end, location } = demand;

    // Basic query: staff available on date, active, documents valid
    return await prisma.staff.findMany({
      where: {
        status: 'active',
        // Availability check
        // Document validity check
      },
      include: {
        underlist: {
          where: { location_id: location.location_id }
        },
        blacklist: {
          where: { location_id: location.location_id }
        }
      },
      orderBy: [
        { score: 'desc' }  // Highest score first
      ]
    });
  }

  private async applyFilters(
    candidates: Staff[],
    demand: JobDemand
  ): Promise<Staff[]> {
    const filtered: Staff[] = [];

    for (const staff of candidates) {
      // 1. Check availability (from ERP data)
      const available = await this.checkAvailability(staff, demand.date);
      if (!available) continue;

      // 2. Check document validity
      const docsValid = await this.validateDocuments(staff, demand.requirements);
      if (!docsValid) continue;

      // 3. Check blacklist
      if (staff.blacklist.length > 0) continue;

      // 4. Check fair sharing limit (from ERP)
      const underLimit = await this.checkFairSharingLimit(staff, demand.date);
      if (!underLimit) continue;

      filtered.push(staff);
    }

    return filtered;
  }

  async rankCandidates(candidates: Staff[], location: Location): Promise<RankedCandidate[]> {
    const ranked: RankedCandidate[] = [];

    for (const staff of candidates) {
      let score = 0;
      const reasons: string[] = [];

      // 1. Underlist priority (50% weight)
      const underlist = staff.underlist[0];  // Assuming included
      if (underlist) {
        score += (11 - underlist.priority) * 0.5;  // Priority 1 = 5.0, 2 = 4.5, ...
        reasons.push(`Underlist priority ${underlist.priority}`);
      }

      // 2. Score tier (30% weight)
      const tierScore = this.getTierScore(staff.tier);
      score += tierScore * 0.3;
      reasons.push(`Score tier: ${staff.tier} (score: ${staff.score})`);

      // 3. Previous work history (10% weight)
      const workedBefore = await this.hasWorkedAtLocation(staff, location);
      if (workedBefore) {
        score += 0.1;
        reasons.push('Worked at this location before');
      }

      // 4. Seniority (10% weight)
      const seniority = await this.calculateSeniorityScore(staff);
      score += seniority * 0.1;

      ranked.push({
        staff,
        score,
        reasons
      });
    }

    // Sort by score descending
    ranked.sort((a, b) => b.score - a.score);

    return ranked;
  }
}
```

---

### 3.3 Notification Service

```typescript
interface NotificationService {
  // Send push notification via Firebase
  sendAssignmentNotification(
    assignment: Assignment,
    staff: Staff,
    fcmToken: string
  ): Promise<void>;

  // Send cancellation warning
  sendCancellationWarning(
    assignment: Assignment,
    staff: Staff,
    fcmToken: string
  ): Promise<string>;  // Returns notification ID

  // Send confirmation message
  sendConfirmationMessage(
    assignment: Assignment,
    staff: Staff,
    fcmToken: string
  ): Promise<void>;

  // Send emergency file notification
  sendEmergencyNotification(
    file: EmergencyFile,
    staff: Staff,
    fcmToken: string
  ): Promise<void>;
}

class FirebaseNotificationService implements NotificationService {
  private readonly firebaseConfig = {
    projectId: process.env.FIREBASE_PROJECT_ID,
    clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
    privateKey: process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, '\n')
  };

  private readonly firebaseAdmin = require('firebase-admin');

  constructor() {
    this.firebaseAdmin.initializeApp({
      credential: this.firebaseAdmin.credential.cert(this.firebaseConfig)
    });
  }

  async sendAssignmentNotification(
    assignment: Assignment,
    staff: Staff,
    fcmToken: string
  ): Promise<void> {
    const message = this.buildAssignmentMessage(assignment);

    const notification = {
      notification: {
        title: 'New Shift Assignment',
        body: message
      },
      data: {
        assignment_id: assignment.assignment_id,
        type: 'assignment_notification',
        click_action: 'FLUTTER_CLICK_ACTION'
      },
      token: fcmToken
    };

    try {
      const response = await this.firebaseAdmin.messaging().send(notification);
      console.log('Successfully sent message:', response);

      // Log notification
      await this.logNotification(staff.staff_id, 'assignment', message, fcmToken);
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  private buildAssignmentMessage(assignment): string {
    const location = assignment.location;
    const date = new Date(assignment.assignment_date);
    const dateStr = date.toLocaleDateString('zh-HK', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      weekday: 'short'
    });

    return `New shift assignment:\nDate: ${dateStr}\nLocation: ${location.name_zh}\nShift: ${assignment.shift_start} - ${assignment.shift_end}`;
  }

  async sendCancellationWarning(
    assignment: Assignment,
    staff: Staff,
    fcmToken: string
  ): Promise<string> {
    const message = `⚠️ Cancel shift? 100HKD will be deducted. Score: -1`;

    const notification = {
      notification: {
        title: 'Cancel Shift Confirmation',
        body: message
      },
      data: {
        assignment_id: assignment.assignment_id,
        type: 'cancellation_warning',
        requires_confirmation: 'true'
      },
      token: fcmToken
    };

    const response = await this.firebaseAdmin.messaging().send(notification);
    await this.logNotification(staff.staff_id, 'cancellation_warning', message, fcmToken);

    return response; // Return message ID
  }

  async sendConfirmationMessage(
    assignment: Assignment,
    staff: Staff,
    fcmToken: string
  ): Promise<void> {
    const message = `Shift confirmed successfully. Your score has increased by 1 point.`;

    const notification = {
      notification: {
        title: 'Shift Confirmed',
        body: message
      },
      data: {
        assignment_id: assignment.assignment_id,
        type: 'confirmation'
      },
      token: fcmToken
    };

    await this.firebaseAdmin.messaging().send(notification);
    await this.logNotification(staff.staff_id, 'confirmation', message, fcmToken);
  }

  async sendEmergencyNotification(
    file: EmergencyFile,
    staff: Staff,
    fcmToken: string
  ): Promise<void> {
    const message = `🚨 ${file.priority} Priority Alert: ${file.title}`;

    const notification = {
      notification: {
        title: 'Emergency Protocol',
        body: message
      },
      data: {
        file_id: file.file_id,
        type: 'emergency_notification',
        priority: file.priority
      },
      token: fcmToken
    };

    await this.firebaseAdmin.messaging().send(notification);
    await this.logNotification(staff.staff_id, 'emergency', message, fcmToken);
  }

  private async logNotification(
    staffId: string,
    type: string,
    message: string,
    fcmToken: string
  ): Promise<void> {
    // Store in database for audit
    await prisma.notification_log.create({
      data: {
        staff_id: staffId,
        notification_type: type,
        message: message,
        token: fcmToken,
        sent_at: new Date()
      }
    });
  }
}
```

---

### 3.4 Sync Orchestrator

```typescript
interface SyncOrchestrator {
  // Daily staff sync job
  syncStaff(): Promise<SyncResult>;

  // Daily location sync job
  syncLocations(): Promise<SyncResult>;

  // Polling for job demands
  pollDemands(): Promise<Demand[]>;

  // Submit assignment to ERP
  submitAssignment(assignment: Assignment): Promise<ERPResponse>;
}

class SyncOrchestratorImpl implements SyncOrchestrator {
  async syncStaff(): Promise<SyncResult> {
    logger.info('Starting staff sync job...');

    const result: SyncResult = {
      success: 0,
      failed: 0,
      errors: []
    };

    try {
      // Call ERP API
      const response = await axios.get(
        `${ERP_BASE_URL}/api/v1/staff/active`,
        {
          headers: { Authorization: `Bearer ${ERP_API_TOKEN}` },
          timeout: 30000
        }
      );

      const staffList = response.data.data;
      logger.info(`Received ${staffList.length} staff from ERP`);

      for (const staffData of staffList) {
        try {
          await this.upsertStaff(staffData);
          result.success++;
        } catch (error) {
          result.failed++;
          result.errors.push({
            staff_id: staffData.staff_id,
            error: error.message
          });
        }
      }

      logger.info(`Staff sync completed: ${result.success} success, ${result.failed} failed`);

      // If failures, queue for retry
      if (result.failed > 0) {
        await this.queueRetry('staff', result.errors);
      }

      return result;

    } catch (error) {
      logger.error('Staff sync job failed:', error);
      throw error;
    }
  }

  private async upsertStaff(staffData: any): Promise<void> {
    return await prisma.$transaction(async (tx) => {
      // Validate HKID
      if (!this.validateHKID(staffData.hkid)) {
        throw new Error(`Invalid HKID format: ${staffData.hkid}`);
      }

      // Upsert staff
      await tx.staff.upsert({
        where: {
          erp_staff_id: staffData.staff_id
        },
        update: {
          name_zh: staffData.name_chinese,
          name_en: staffData.name_english,
          hkid: staffData.hkid,
          phone: staffData.contact_number,
          whatsapp: staffData.whatsapp_number,
          email: staffData.email,
          bank_code: staffData.bank_account?.bank_code,
          bank_account: staffData.bank_account?.account_number,
          status: staffData.status,
          updated_at: new Date()
        },
        create: {
          erp_staff_id: staffData.staff_id,
          name_zh: staffData.name_chinese,
          name_en: staffData.name_english,
          hkid: staffData.hkid,
          phone: staffData.contact_number,
          whatsapp: staffData.whatsapp_number,
          email: staffData.email,
          bank_code: staffData.bank_account?.bank_code,
          bank_account: staffData.bank_account?.account_number,
          status: staffData.status
        }
      });
    });
  }

  private validateHKID(hkid: string): boolean {
    const pattern = /^[A-Z]{1,2}[0-9]{6}[0-9A]$/;
    return pattern.test(hkid.toUpperCase());
  }

  private async queueRetry(entity: string, errors: any[]): Promise<void> {
    // Add failed items to Redis queue for retry
    await redis.lpush(
      `retry_queue:${entity}`,
      ...errors.map(e => JSON.stringify(e))
    );

    // Set expiry (1 hour)
    await redis.expire(`retry_queue:${entity}`, 3600);
  }
}
```

---

## 4. API DESIGN

### 4.1 Internal APIs (Express.js)

#### POST /api/v1/assignments
**Create new assignment (manual by admin)**

```json
Request:
{
  "staff_id": "uuid",
  "location_id": "uuid",
  "assignment_date": "2025-11-25",
  "shift_start": "08:00",
  "shift_end": "20:00",
  "assigned_by": "manual_admin"
}

Response (201):
{
  "success": true,
  "data": {
    "assignment_id": "uuid",
    "phc_assignment_id": "PHC-001",
    "status": "pending_confirmation",
    "created_at": "2025-11-20T15:30:00Z"
  }
}
```

#### PATCH /api/v1/assignments/:id/status
**Update assignment status** (confirm/cancel)

```json
Request:
{
  "status": "confirmed",
  "confirmed_timestamp": "2025-11-20T16:00:00Z"
}

Response (200):
{
  "success": true,
  "data": {
    "assignment_id": "uuid",
    "status": "confirmed",
    "score_updated": true
  }
}
```

#### POST /api/v1/attendance
**Record attendance**

```json
Request:
{
  "assignment_id": "uuid",
  "clock_in": "2025-11-25T07:55:00Z",
  "clock_out": "2025-11-25T20:05:00Z",
  "verified_by": "supervisor_name"
}

Response (201):
{
  "success": true,
  "data": {
    "attendance_id": "uuid",
    "actual_hours": 12.17,
    "score_updated": true
  }
}
```

#### GET /api/v1/metrics/dashboard
**Get dashboard metrics**

```json
Response (200):
{
  "success": true,
  "data": {
    "today": {
      "total_jobs": 45,
      "jobs_filled": 42,
      "jobs_unfilled": 3,
      "confirmed_staff": 38,
      "pending_confirmations": 4
    },
    "attendance": {
      "completed": 35,
      "no_shows": 2
    },
    "penalties": {
      "cancellations": 1,
      "no_shows": 2
    }
  }
}
```

#### POST /api/v1/emergency/upload
**Upload emergency file**

```javascript
// Multipart form data
{
  file: File,  // PDF, DOC, DOCX, JPG, PNG (max 10MB)
  title: string,
  description: string,
  priority: 'Normal' | 'High' | 'Critical',
  regions: string[]  // ['HKI', 'KLN', 'NT'] or empty for all
}

Response (201):
{
  "success": true,
  "data": {
    "file_id": "uuid",
    "file_url": "https://...",
    "uploaded_at": "2025-11-20T16:00:00Z"
  }
}
```

---

### 4.2 Cron Jobs (Scheduled Tasks)

```javascript
// Using node-cron

// Staff sync: Daily 02:00 AM
cron.schedule('0 2 * * *', async () => {
  logger.info('Starting staff sync job...');
  await syncOrchestrator.syncStaff();
}, {
  timezone: 'Asia/Hong_Kong',
  name: 'staff-sync'
});

// Location sync: Daily 03:00 AM
cron.schedule('0 3 * * *', async () => {
  logger.info('Starting location sync job...');
  await syncOrchestrator.syncLocations();
}, {
  timezone: 'Asia/Hong_Kong',
  name: 'location-sync'
});

// Demand polling: Every 15 minutes
cron.schedule('*/15 * * * *', async () => {
  logger.info('Polling job demands...');
  const demands = await syncOrchestrator.pollDemands();

  for (const demand of demands) {
    // Trigger matching for each new demand
    await matchingEngine.findMatches(demand.id, demand.required_staff_count);
  }
}, {
  timezone: 'Asia/Hong_Kong',
  name: 'demand-poll'
});

// Assignment verification: Hourly
cron.schedule('0 * * * *', async () => {
  logger.info('Verifying assignment statuses...');
  await this.verifyAssignments();
}, {
  timezone: 'Asia/Hong_Kong',
  name: 'assignment-verify'
});
```

---

### 4.3 Environment Configuration

```bash
# Database
DATABASE_URL="postgresql://user:pass@host:5432/phc_db"

# Redis
REDIS_URL="redis://localhost:6379"

# ERP System
ERP_BASE_URL="https://erp.prestigehealth.com"
ERP_API_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
ERP_API_KEY="prod_api_key_xyz"

# WhatsApp Business API
WHATSAPP_PHONE_NUMBER_ID="123456789"
WHATSAPP_ACCESS_TOKEN="EAABwzLixnjYBOZ..."

# App URLs
APP_BASE_URL="https://phc.prestigehealth.com"

# Security
JWT_SECRET="your-super-secret-jwt-key-min-32-chars"
ENCRYPTION_KEY="32-char-key-for-data-encryption"

# File Storage
AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_S3_BUCKET="phc-emergency-files"
AWS_REGION="ap-southeast-1"

# Logging
LOG_LEVEL="info"
LOG_TO_FILE="true"
```

---

## 5. SECURITY DESIGN

### 5.1 Authentication Flow

**Staff Login:**
```
Login Request (Mobile/Email/Username + Password)
    ↓
POST /api/v1/auth/login
    ↓
Lookup user by identifier (Mobile OR Email OR Username)
    ↓
Validate Password (bcrypt)
    ↓
Check Account Status (Active/Locked)
    ↓
Generate JWT (access token + refresh token)
    ↓
Return tokens + User Role (Staff)
```

**Admin Login:**
```
Login Request (Email + Password)
    ↓
POST /api/v1/auth/login
    ↓
... (Same flow)
```

### 5.2 Role-Based Access Control (RBAC)

```typescript
enum Role {
  ADMIN = 'admin',
  SUPERVISOR = 'supervisor',
  STAFF = 'staff'
}

// Middleware
const requireRole = (roles: Role[]) => {
  return async (req, res, next) => {
    const user = req.user; // From JWT middleware

    if (!user || !roles.includes(user.role)) {
      return res.status(403).json({
        error: 'Forbidden',
        message: 'Insufficient permissions'
      });
    }

    next();
  };
};

// Usage
app.post('/api/v1/assignments',
  authenticate,
  requireRole([Role.ADMIN]),
  assignmentController.create
);

app.post('/api/v1/attendance',
  authenticate,
  requireRole([Role.ADMIN, Role.SUPERVISOR]),
  attendanceController.create
);
```

### 5.3 API Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';

const createRateLimiter = (windowMs, max, keyGenerator) => {
  return rateLimit({
    store: new RedisStore({
      client: redisClient,
      prefix: 'rl:',
      sendCommand: (...args) => redisClient.call(...args)
    }),
    windowMs: windowMs,
    max: max,
    keyGenerator: keyGenerator,
    standardHeaders: true,
    legacyHeaders: false,
    handler: (req, res) => {
      res.status(429).json({
        error: 'Too Many Requests',
        message: `Limit: ${max} requests per ${windowMs / 1000} seconds`
      });
    }
  });
};

// Apply rate limiting
app.use('/api/v1/assignments', createRateLimiter(
  60 * 1000,  // 1 minute
  100,        // 100 requests
  (req) => req.user?.staff_id || req.ip
));

app.use('/api/v1/auth', createRateLimiter(
  15 * 60 * 1000,  // 15 minutes
  5,               // 5 login attempts
  (req) => req.body.email || req.ip
));
```

---

## 6. ERROR HANDLING & LOGGING

### 6.1 Error Types

```typescript
enum ErrorCode {
  // Validation errors
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  INVALID_HKID = 'INVALID_HKID',
  INVALID_PHONE = 'INVALID_PHONE',

  // Not found errors
  STAFF_NOT_FOUND = 'STAFF_NOT_FOUND',
  ASSIGNMENT_NOT_FOUND = 'ASSIGNMENT_NOT_FOUND',

  // Conflict errors
  STAFF_UNAVAILABLE = 'STAFF_UNAVAILABLE',
  ASSIGNMENT_CONFLICT = 'ASSIGNMENT_CONFLICT',
  DOUBLE_BOOKING = 'DOUBLE_BOOKING',

  // API errors
  ERP_API_ERROR = 'ERP_API_ERROR',
  ERP_TIMEOUT = 'ERP_TIMEOUT',
  ERP_AUTH_FAILED = 'ERP_AUTH_FAILED',

  // Business logic errors
  DOCUMENT_EXPIRED = 'DOCUMENT_EXPIRED',
  STAFF_BLACKLISTED = 'STAFF_BLACKLISTED',
  FAIR_SHARING_EXCEEDED = 'FAIR_SHARING_EXCEEDED'
}

class AppError extends Error {
  constructor(
    public code: ErrorCode,
    public message: string,
    public statusCode: number = 400,
    public details?: any
  ) {
    super(message);
    this.name = 'AppError';
  }
}

// Error handler middleware
const errorHandler = (err, req, res, next) => {
  logger.error('Unhandled error:', err);

  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: err.code,
      message: err.message,
      details: err.details
    });
  }

  // Unknown error
  res.status(500).json({
    error: 'INTERNAL_SERVER_ERROR',
    message: 'An unexpected error occurred'
  });
};
```

### 6.2 Logging with Winston

```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'phc-dispatch-system' },
  transports: [
    // Error log
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error',
      maxsize: 5242880,  // 5MB
      maxFiles: 5
    }),
    // Combined log
    new winston.transports.File({
      filename: 'logs/combined.log',
      maxsize: 5242880,
      maxFiles: 5
    })
  ]
});

// Console in development
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.simple()
    )
  }));
}

export default logger;
```

---

## 7. TESTING STRATEGY

### 7.1 Unit Tests

```typescript
// Example unit test for scoring service
describe('ScoringService', () => {
  let service: ScoringService;

  beforeEach(() => {
    service = new ScoringServiceImpl();
  });

  it('should increase score by 1 when staff attends shift', async () => {
    const result = await service.updateScore('staff-123', 'attended', 'assignment-456');

    expect(result.change).toBe(1);
    expect(result.newScore).toBe(result.oldScore + 1);
  });

  it('should decrease score by 1 when staff cancels', async () => {
    const result = await service.updateScore('staff-123', 'cancelled', 'assignment-456');

    expect(result.change).toBe(-1);
    expect(result.newScore).toBe(result.oldScore - 1);
  });

  it('should not go below -10 score', async () => {
    // Set score to -10 first
    await prisma.staff.update({
      where: { staff_id: 'staff-123' },
      data: { score: -10 }
    });

    const result = await service.updateScore('staff-123', 'no_show', 'assignment-456');

    expect(result.newScore).toBe(-10);  // Floor at -10
  });
});

// Target: 80% code coverage
// Tools: Jest + Supertest (for API tests)
```

### 7.2 Integration Tests

```typescript
describe('Assignment End-to-End Flow', () => {
  it('should complete full assignment lifecycle', async () => {
    // Step 1: Create demand
    const demand = await createTestDemand();

    // Step 2: Run matching
    const matches = await matchingEngine.findMatches(demand.id, 1);
    expect(matches).toHaveLength(1);

    // Step 3: Staff confirms
    const assignment = await getAssignment(matches[0], demand);
    await confirmAssignment(assignment.id, 'whatsapp');

    // Step 4: Check score increased
    const staff = await getStaff(matches[0].staff_id);
    expect(staff.score).toEqual(expect.any(Number));

    // Step 5: Record attendance
    await recordAttendance(assignment.id, 12);

    // Step 6: Verify attendance submitted to ERP
    const erpCall = await getLastERPCall('POST', '/api/v1/attendance');
    expect(erpCall).not.toBeNull();
  });
});
```

### 7.3 Load Testing

```bash
# Using k6
# Script: load-test.js

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // 50 concurrent users
    { duration: '5m', target: 50 },   // sustain 50
    { duration: '2m', target: 100 },  // ramp up to 100
    { duration: '5m', target: 100 },  // sustain 100
    { duration: '2m', target: 0 },    // ramp down
  ],
  thresholds: {
    'http_req_duration': ['p(95)<2000'],  // 95% under 2s
    'http_req_failed': ['rate<0.01'],     // 1% failure rate
  }
};

export default function() {
  // Test assignment confirmation flow
  const assignmentId = getRandomAssignment();

  const res = http.post(
    `${BASE_URL}/api/v1/assignments/${assignmentId}/status`,
    JSON.stringify({ status: 'confirmed' }),
    { headers: { 'Content-Type': 'application/json' } }
  );

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 2s': (r) => r.timings.duration < 2000
  });
}
```

---

## 8. DEPLOYMENT

### 8.1 Docker Setup

```dockerfile
# Dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY dist/ ./dist/
COPY prisma/ ./prisma/
RUN npx prisma generate

EXPOSE 3000

CMD ["node", "dist/server.js"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/phc_db
      - REDIS_URL=redis://redis:6379
      - ERP_BASE_URL=https://erp.prestigehealth.com
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=phc_db
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

### 8.2 CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linting
        run: npm run lint

      - name: Run tests
        run: npm test -- --coverage
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/phc_test
          REDIS_URL: redis://localhost:6379

      - name: Build application
        run: npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to production
        run: |
          ssh deploy@prod-server "cd /app && git pull && docker-compose restart app"
        env:
          SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
```

---

## 9. MONITORING & ALERTING

### 9.1 Metrics Collection

```typescript
// Using prom-client for Prometheus metrics
import client from 'prom-client';

// Custom metrics
const apiRequestDuration = new client.Histogram({
  name: 'phc_api_request_duration_seconds',
  help: 'API request duration in seconds',
  labelNames: ['method', 'endpoint', 'status'],
  buckets: [0.1, 0.5, 1, 2, 5, 10]
});

const staffSyncSuccess = new client.Counter({
  name: 'phc_staff_sync_success_total',
  help: 'Total successful staff syncs'
});

const staffSyncFailure = new client.Counter({
  name: 'phc_staff_sync_failure_total',
  help: 'Total failed staff syncs'
});

// Middleware to track API metrics
const metricsMiddleware = (req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;

    apiRequestDuration.observe({
      method: req.method,
      endpoint: req.path,
      status: res.statusCode
    }, duration);
  });

  next();
};

// Health check endpoint
app.get('/health', (req, res) => {
  const healthCheck = {
    uptime: process.uptime(),
    message: 'OK',
    timestamp: Date.now(),
    database: this.checkDatabaseHealth(),
    redis: this.checkRedisHealth(),
    erp: this.checkERPHealth()
  };

  res.json(healthCheck);
});
```

### 9.2 Alerts (Prometheus + Alertmanager)

```yaml
# alert-rules.yml
groups:
  - name: phc-alerts
    rules:
      - alert: HighAPIErrorRate
        expr: rate(phc_api_request_duration_seconds_count{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High API error rate detected"

      - alert: StaffSyncFailed
        expr: phc_staff_sync_failure_total > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Staff sync job failed"

      - alert: DatabaseDown
        expr: up{job="postgres"} == 0
        for: 1m
        labels:
          severity: critical
```

---

## 10. POST-MVP ENHANCEMENTS

### 10.1 Future Features (Not in v1.0)

1. **Geographic Intelligence**
   - Distance-based matching
   - Transportation time API integration
   - Regional staff pooling

2. **Advanced Analytics**
   - Predictive staffing (ML model)
   - Demand forecasting
   - Optimal shift scheduling

3. **Mobile App**
   - Native iOS/Android app for staff
   - Push notifications
   - In-app clock-in/out

4. **Enhanced Fair Sharing**
   - Automated fair sharing algorithm
   - Machine learning-based optimization
   - Multi-criteria decision engine

5. **Real-time Features**
   - WebSocket for live updates
   - Live dashboard (no refresh)
   - Collaborative planning

---

**Document Version:** 1.0
**Last Updated:** 2025-11-24
**Next Review:** Before Phase 1 development
