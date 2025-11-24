# PHC System Technical Architecture

## Executive Summary

The PHC (Prestige Health Care) system is a merit-based healthcare worker dispatch platform that automates the assignment of nursing assistants to care home shifts. The architecture follows a modern web application pattern with React.js frontend, Spring Boot backend, MySQL database, and hybrid notification system combining WhatsApp (manual templates) with Firebase Cloud Messaging for web push notifications. The system prioritizes fair allocation through a scoring algorithm, real-time ERP integration, and mobile-first design for 500+ healthcare workers.

## Project Initialization

First implementation story should execute:
```bash
# Frontend initialization
npx create-react-app@latest phc-frontend --template typescript

# Backend initialization
spring init --dependencies=web,data-jpa,security,validation,actuator phc-backend
```

This establishes the base architecture with these decisions:
- React 18.3.1 with TypeScript for type safety
- Spring Boot 3.5.7 LTS for enterprise-grade backend
- Maven/Gradle build system with Spring Initializr
- Development server with hot reload capabilities

## Decision Summary

| Category | Decision | Version | Affects FRs | Rationale |
| -------- | -------- | ------- | ----------- | --------- |
| Frontend Framework | React.js | 18.3.1 | FR-3, FR-4 | Component-based architecture for complex UI states, excellent mobile support for field workers |
| Backend Framework | Spring Boot | 3.5.7 LTS | All FRs | Enterprise-grade Java framework with built-in security, validation, and ERP integration capabilities |
| Primary Database | MySQL | 8.4.7 LTS | FR-1, FR-2, FR-5 | ACID compliance for financial transactions, proven scalability for 500+ concurrent users |
| Cache/Session Store | Redis | 8.2.3 | FR-2, FR-3 | High-performance session management and real-time notification delivery |
| API Architecture | RESTful + WebSocket | Spring WebFlux | FR-2, FR-5 | Standardized ERP integration with real-time updates for urgent assignments |
| Authentication | JWT + Spring Security | 6.2.x | All FRs | Stateless authentication for mobile-first users, role-based access control |
| Notifications | WhatsApp Templates + Firebase FCM | Latest | FR-3 | Hybrid approach: WhatsApp for primary reach, FCM for portal alerts and reminders |
| File Storage | AWS S3 | Standard | FR-8 | Secure cloud storage for emergency protocols with encryption at rest |
| Deployment | Docker + Kubernetes | Latest | All FRs | Containerized deployment for scalability and reliability |
| Data Validation | Hibernate Validator | 8.0.x | FR-1, FR-5 | Server-side validation for HKID format, phone numbers, and business rules |

## Project Structure

```
phc-system/
├── phc-frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   ├── dashboard/
│   │   │   ├── assignments/
│   │   │   ├── attendance/
│   │   │   └── notifications/
│   │   ├── services/
│   │   │   ├── api.service.ts
│   │   │   ├── auth.service.ts
│   │   │   ├── notification.service.ts
│   │   │   └── firebase.service.ts
│   │   ├── store/
│   │   │   ├── auth/
│   │   │   ├── assignments/
│   │   │   └── notifications/
│   │   ├── utils/
│   │   ├── types/
│   │   └── App.tsx
│   ├── public/
│   └── package.json
├── phc-backend/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/
│   │   │   │   └── com/phc/
│   │   │   │       ├── config/
│   │   │   │       ├── controller/
│   │   │   │       ├── service/
│   │   │   │       ├── repository/
│   │   │   │       ├── model/
│   │   │   │       ├── security/
│   │   │   │       └── scheduler/
│   │   │   └── resources/
│   │   │       ├── application.yml
│   │   │       └── db/migration/
│   │   └── test/
│   └── pom.xml
├── phc-shared/
│   ├── src/
│   │   ├── types/
│   │   ├── constants/
│   │   └── utils/
│   └── package.json
├── docker-compose.yml
├── kubernetes/
│   ├── frontend-deployment.yaml
│   ├── backend-deployment.yaml
│   ├── mysql-deployment.yaml
│   └── redis-deployment.yaml
└── docs/
    ├── api/
    ├── architecture/
    └── deployment/
```

## FR to Architecture Mapping

| FR Category | Architecture Component | Implementation Location |
|-------------|----------------------|------------------------|
| FR-1: Scoring Algorithm | ScoreCalculatorService | backend/src/main/java/com/phc/service/ScoreCalculatorService.java |
| FR-2: Matching Engine | MatchingEngineService | backend/src/main/java/com/phc/service/MatchingEngineService.java |
| FR-3: WhatsApp + Firebase | NotificationService + FCMService | backend/src/main/java/com/phc/service/NotificationService.java |
| FR-4: Admin Dashboard | DashboardController + React Components | frontend/src/components/dashboard/ |
| FR-5: ERP Integration | ERPClientService + ScheduledJobs | backend/src/main/java/com/phc/service/ERPClientService.java |
| FR-6: Attendance Tracking | AttendanceService + QRCodeService | backend/src/main/java/com/phc/service/AttendanceService.java |
| FR-7: Penalty Management | PenaltyService | backend/src/main/java/com/phc/service/PenaltyService.java |
| FR-8: Emergency File Upload | FileStorageService + S3Integration | backend/src/main/java/com/phc/service/FileStorageService.java |
| FR-9: Emergency Job Posting | EmergencyJobService | backend/src/main/java/com/phc/service/EmergencyJobService.java |
| FR-10: Settlement Reconciliation | SettlementReconciliationService | backend/src/main/java/com/phc/service/SettlementReconciliationService.java |
| FR-11: Manual Assignment Override | AssignmentOverrideService | backend/src/main/java/com/phc/service/AssignmentOverrideService.java |
| FR-12: System Monitoring | MonitoringController + Actuator | backend/src/main/java/com/phc/controller/MonitoringController.java |
| FR-13: Reporting | ReportGenerationService | backend/src/main/java/com/phc/service/ReportGenerationService.java |

## Technology Stack Details

### Core Technologies

**Frontend Stack:**
- React 18.3.1 with TypeScript 5.x for type safety
- Redux Toolkit for state management
- React Router v6 for navigation
- Axios for API calls
- TailwindCSS for styling
- React Hook Form for form handling
- Recharts for dashboard visualizations
- Service Worker for offline notifications

**Backend Stack:**
- Spring Boot 3.5.7 LTS with Java 21
- Spring Security for authentication/authorization
- Spring Data JPA for database operations
- Spring WebFlux for reactive programming
- Spring Batch for scheduled jobs
- Hibernate Validator for input validation
- Jackson for JSON processing
- Logback for structured logging

**Database & Cache:**
- MySQL 8.4.7 LTS for primary data storage
- Redis 8.2.3 for session management and caching
- Flyway for database migrations
- Connection pooling with HikariCP

### Integration Points

**ERP System Integration:**
- RESTful API client with Spring WebClient
- OAuth 2.0 authentication with ERP
- Retry mechanism with exponential backoff
- Webhook support for real-time updates
- Data transformation layer for format compatibility

**WhatsApp Integration:**
- Manual template generation system
- Template storage and management
- Coordinator dashboard for sending
- Delivery tracking and confirmation

**Firebase Cloud Messaging:**
- Service worker registration
- Token management per device
- Topic-based messaging for user groups
- Delivery status tracking

## Novel Pattern Designs

### Merit-Based Scoring Pattern

**Purpose:** Ensure fair, transparent allocation based on reliability history rather than manual bias

**Components:**
- ScoreCalculatorService: Calculates scores based on attendance/cancellation history
- ScoreTierClassifier: Determines tier (Gold/Silver/Bronze/Under Review) from score
- ScoreHistoryRepository: Maintains audit trail of all score changes
- ScoreSyncService: Real-time synchronization with ERP system

**Data Flow:**
```
Attendance Event → PenaltyService → ScoreCalculatorService → ScoreTierClassifier → ScoreHistoryRepository → ScoreSyncService → ERP API
```

**Implementation Guide:**
- All score changes must go through ScoreCalculatorService
- Score floor (-10) enforced at service level
- Tier classification calculated dynamically, not stored
- Real-time sync triggered within 1 minute of change
- Manual overrides require audit trail with reason

### Hybrid Notification Pattern

**Purpose:** Combine WhatsApp reach with web portal engagement for optimal staff response

**Components:**
- NotificationService: Orchestrates notification delivery
- WhatsAppTemplateService: Generates message templates
- FCMService: Handles web push notifications
- NotificationTracker: Monitors delivery and engagement

**Data Flow:**
```
Assignment Created → NotificationService → WhatsAppTemplateService (primary) → Coordinator Dashboard → Manual Send
                                    ↓
                                FCMService (secondary) → Web Push → Portal Alert
```

**Implementation Guide:**
- WhatsApp templates generated automatically with shift details
- Coordinator copy-paste workflow with one-click template copy
- FCM notifications sent immediately after WhatsApp marked sent
- 2-hour confirmation window with automatic reminders
- 24-hour advance reminder for confirmed shifts

### Multi-Method Attendance Pattern

**Purpose:** Support both QR code and supervisor verification methods with preference for supervisor verification

**Components:**
- QRCodeGeneratorService: Creates location-specific QR codes
- QRCodeValidatorService: Validates scanned codes
- SupervisorVerificationService: Handles manual verification
- AttendanceRecorderService: Records attendance regardless of method

**Data Flow:**
```
Staff Arrival → [QR Scan] → QRCodeValidatorService → AttendanceRecorderService
              ↓
              [Supervisor] → SupervisorVerificationService → AttendanceRecorderService
```

**Implementation Guide:**
- Supervisor verification is primary recommended method
- QR codes available as backup for tech-savvy facilities
- Both methods feed into unified attendance records
- Real-time sync to ERP within 1 hour
- Deviation detection for hours worked vs scheduled

## Implementation Patterns

### Naming Conventions

**REST API Endpoints:**
- Resource-based: `/api/v1/staff`, `/api/v1/assignments`
- Plural nouns: `/staff` not `/staffs`
- Hyphen-separated: `/job-demands` not `/job_demands`
- Versioned: `/api/v1/` prefix for all endpoints

**Database Tables:**
- Snake case: `staff_assignments`, `attendance_records`
- Singular entities: `staff` not `staffs`
- Foreign keys: `staff_id` not `staffId`
- Timestamp columns: `created_at`, `updated_at`

**Java Classes:**
- Service classes: `ScoreCalculatorService`
- Repository interfaces: `StaffRepository`
- Entity classes: `StaffEntity`
- DTO classes: `StaffResponseDTO`

**React Components:**
- PascalCase: `AssignmentCard`, `DashboardWidget`
- Feature folders: `components/assignments/`
- Service files: `api.service.ts`
- Hook files: `useAssignments.ts`

### Code Organization

**Backend Structure:**
```
com.phc/
├── config/          # Configuration classes
├── controller/      # REST endpoints
├── service/         # Business logic
├── repository/      # Data access
├── model/          # Entity classes
├── dto/            # Data transfer objects
├── security/       # Authentication/authorization
├── scheduler/      # Background jobs
└── exception/      # Custom exceptions
```

**Frontend Structure:**
```
src/
├── components/     # React components
├── services/      # API calls and external services
├── store/         # Redux store and slices
├── utils/         # Helper functions
├── types/         # TypeScript interfaces
├── hooks/         # Custom React hooks
└── assets/        # Static resources
```

### Error Handling

**API Error Response Format:**
```json
{
  "error": {
    "code": "STAFF_NOT_AVAILABLE",
    "message": "Staff member is not available for selected shift",
    "details": {
      "staffId": "12345",
      "conflictingAssignment": "67890"
    }
  },
  "timestamp": "2025-11-24T10:30:00Z",
  "path": "/api/v1/assignments"
}
```

**Error Codes:**
- `INVALID_HKID`: Hong Kong ID format validation failed
- `STAFF_NOT_AVAILABLE`: Conflicting assignment or unavailable
- `FACILITY_BLACKLIST`: Staff on facility blacklist
- `DOCUMENT_EXPIRED`: Required certificate expired
- `FAIR_SHARE_EXCEEDED`: Staff exceeded shift limit

### Logging Strategy

**Structured Logging Format:**
```json
{
  "timestamp": "2025-11-24T10:30:00.123Z",
  "level": "INFO",
  "service": "matching-engine",
  "traceId": "abc-123-def",
  "userId": "coordinator_001",
  "message": "Matching completed",
  "data": {
    "jobId": "JOB-2025-001",
    "candidatesFound": 5,
    "topScore": 18
  }
}
```

**Log Levels:**
- ERROR: System failures, data corruption
- WARN: Business rule violations, retries
- INFO: Business events, user actions
- DEBUG: Detailed execution flow
- TRACE: API request/response bodies

## Data Architecture

### Core Entity Relationships

**Staff Entity:**
```sql
CREATE TABLE staff (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  staff_number VARCHAR(20) UNIQUE NOT NULL,
  phone_number VARCHAR(8) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE,
  full_name VARCHAR(255) NOT NULL,
  current_score INT DEFAULT 5,
  score_tier ENUM('gold', 'silver', 'bronze', 'under_review') NOT NULL,
  status ENUM('active', 'inactive') DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**Assignment Entity:**
```sql
CREATE TABLE assignments (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  erp_assignment_id VARCHAR(50) UNIQUE,
  staff_id BIGINT NOT NULL,
  location_id BIGINT NOT NULL,
  assignment_date DATE NOT NULL,
  shift_type ENUM('PC8', 'A', 'B', 'C', 'D', 'N') NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  status ENUM('pending', 'confirmed', 'cancelled', 'completed', 'no_show') DEFAULT 'pending',
  confirmation_deadline TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (staff_id) REFERENCES staff(id),
  FOREIGN KEY (location_id) REFERENCES locations(id)
);
```

**Score History Entity:**
```sql
CREATE TABLE score_history (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  staff_id BIGINT NOT NULL,
  score_change INT NOT NULL,
  new_score INT NOT NULL,
  reason ENUM('attendance', 'cancellation', 'no_show', 'manual_override') NOT NULL,
  assignment_id BIGINT,
  created_by VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (staff_id) REFERENCES staff(id),
  FOREIGN KEY (assignment_id) REFERENCES assignments(id)
);
```

## API Contracts

### Authentication
**POST /api/v1/auth/login**
```json
// Request
{
  "phoneNumber": "91234567",
  "password": "hashedPassword"
}

// Response
{
  "accessToken": "eyJhbGc...",
  "refreshToken": "eyJhbGc...",
  "expiresIn": 14400,
  "user": {
    "id": 12345,
    "staffNumber": "NA001",
    "fullName": "Chan Tai Man",
    "role": "worker",
    "currentScore": 15,
    "scoreTier": "silver"
  }
}
```

### Assignment Creation
**POST /api/v1/assignments**
```json
// Request
{
  "locationId": 456,
  "assignmentDate": "2025-11-25",
  "shiftType": "A",
  "startTime": "07:00",
  "endTime": "15:00",
  "positionsNeeded": 2,
  "urgency": "normal"
}

// Response
{
  "data": {
    "assignmentId": 789,
    "matchedStaff": [
      {
        "staffId": 123,
        "staffNumber": "NA001",
        "fullName": "Chan Tai Man",
        "score": 18,
        "tier": "silver",
        "confirmationStatus": "pending"
      }
    ],
    "whatsappTemplate": "🩺 Prestige Health Assignment\n📅 Date: 2025-11-25..."
  }
}
```

### Attendance Recording
**POST /api/v1/attendance**
```json
// Request
{
  "assignmentId": 789,
  "verificationMethod": "supervisor",
  "clockInTime": "2025-11-25T06:55:00Z",
  "supervisorId": 234
}

// Response
{
  "data": {
    "attendanceId": 567,
    "status": "completed",
    "scoreUpdated": true,
    "newScore": 19,
    "erpSyncStatus": "pending"
  }
}
```

## Security Architecture

### Authentication Flow
1. Phone number + password login
2. JWT token generation with 4-hour expiration
3. Refresh token rotation on each access
4. Role-based access control for all endpoints
5. Session management with Redis

### Authorization Matrix
| Endpoint | Worker | Supervisor | Admin | ERP |
|----------|--------|------------|-------|-----|
| GET /assignments | Own only | Facility only | All | All |
| POST /assignments | ✗ | ✗ | ✓ | ✓ |
| PATCH /assignments/* | Own only | ✗ | ✓ | ✗ |
| POST /attendance | ✗ | ✓ | ✓ | ✗ |
| GET /staff/score | Own only | Facility only | All | All |

### Data Protection
- TLS 1.3 for all connections
- AES-256 encryption for sensitive data at rest
- HKID validation without storage
- Audit logging for all data modifications
- Personal data retention policies

## Performance Considerations

### Database Optimization
- Indexed columns: staff_number, phone_number, assignment_date
- Composite indexes for common queries
- Query optimization for matching engine (< 5 minutes SLA)
- Connection pooling with HikariCP
- Read replicas for reporting queries

### Caching Strategy
- Redis cache for staff availability status
- Session data cached with 4-hour TTL
- Assignment templates cached for quick generation
- Score calculations cached with invalidation on changes

### API Performance
- Pagination for list endpoints (50 items per page)
- Response compression enabled
- CDN for static assets
- Lazy loading for dashboard widgets
- Background job processing for heavy operations

## Deployment Architecture

### Container Configuration
```dockerfile
# Backend Dockerfile
FROM openjdk:21-jre-slim
COPY target/phc-backend.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: phc-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: phc-backend
  template:
    spec:
      containers:
      - name: backend
        image: phc-backend:latest
        ports:
        - containerPort: 8080
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "production"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

### Load Balancing
- NGINX ingress controller
- SSL termination at load balancer
- Health checks every 30 seconds
- Auto-scaling based on CPU/memory usage

## Development Environment

### Prerequisites
- Node.js 20.x and npm 10.x
- Java 21 and Maven 3.9.x
- Docker and Docker Compose
- MySQL 8.4+ and Redis 8.2+

### Setup Commands
```bash
# Clone and setup
git clone <repository-url>
cd phc-system

# Start infrastructure
docker-compose up -d mysql redis

# Backend setup
cd phc-backend
mvn clean install
mvn spring-boot:run

# Frontend setup
cd ../phc-frontend
npm install
npm start

# Run tests
mvn test                    # Backend tests
npm test                    # Frontend tests
```

### Environment Variables
```bash
# Backend (.env)
DATABASE_URL=mysql://localhost:3306/phc
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
ERP_API_URL=https://erp.prestigehealth.com/api
ERP_CLIENT_ID=your-client-id
ERP_CLIENT_SECRET=your-client-secret

# Frontend (.env)
REACT_APP_API_URL=http://localhost:8080/api
REACT_APP_FIREBASE_API_KEY=your-firebase-key
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
```

## Architecture Decision Records (ADRs)

### ADR-001: Supervisor Verification Preferred Over QR Codes
**Status:** Accepted
**Context:** Two attendance verification methods specified in FR-6
**Decision:** Implement supervisor verification as primary method, QR codes as backup
**Rationale:**
- Supervisor verification is more reliable for elderly care home environment
- No dependency on staff smartphone capabilities
- Faster verification process for large staff rosters
- Better audit trail with supervisor accountability
- QR codes remain available for facilities that prefer technological solution

### ADR-002: Manual WhatsApp Templates Over Business API
**Status:** Accepted
**Context:** FR-3 specifies WhatsApp notifications but budget constraints for MVP
**Decision:** Use manual template generation with coordinator copy-paste workflow
**Rationale:**
- Significant cost savings (HKD 8,000-15,000/month vs minimal development cost)
- Faster implementation for 60-day timeline
- Maintains personal touch with coordinator oversight
- Template generation system ready for future API integration
- Delivery confirmation tracked through coordinator workflow

### ADR-003: Spring Boot Over Node.js for Backend
**Status:** Accepted
**Context:** Technology choice for enterprise system with ERP integration
**Decision:** Use Spring Boot 3.5.7 LTS for backend services
**Rationale:**
- Proven enterprise integration capabilities with existing ERP systems
- Strong transaction management for financial penalties
- Built-in security features for healthcare data protection
- Excellent monitoring and logging capabilities
- Team expertise in Java ecosystem
- Better performance for complex matching algorithms

### ADR-004: MySQL Over PostgreSQL for Primary Database
**Status:** Accepted
**Context:** Database choice for transactional system
**Decision:** Use MySQL 8.4.7 LTS as primary database
**Rationale:**
- ACID compliance essential for financial transactions and penalty management
- Proven scalability for 500+ concurrent users
- Strong replication support for high availability
- Better integration with existing ERP systems
- Lower operational complexity than PostgreSQL
- Cost-effective for healthcare organization budget

---

*Generated by BMAD Decision Architecture Workflow v1.0*
*Date: November 24, 2025*
*For: PHC System Implementation*