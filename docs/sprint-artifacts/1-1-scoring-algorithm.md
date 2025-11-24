# Story 1.1: Implement Scoring Algorithm

Status: drafted

## Story

As a System/backend,
I want Implement scoring algorithm,
so that Enable merit-based fair allocation.

## Acceptance Criteria

1. Score updates automatically on attendance verification
2. ERP synced in real-time via API
3. Score floor enforced at -10
4. Manual override requires reason field
5. Staff can view current score and history
6. Tier classification works (Gold/Silver/Bronze/Under Review)

## Tasks / Subtasks

- [ ] Create Score entity/model (AC: 1, 5, 6)
  - [ ] Define Score entity with fields: staff_id, current_score, tier, created_at, updated_at
  - [ ] Create ScoreHistory entity for audit trail
  - [ ] Add database schema migrations
- [ ] Implement score calculation logic (AC: 1, 3, 6)
  - [ ] Create ScoreCalculatorService with scoring rules
  - [ ] Attend: +1 point implementation
  - [ ] Cancel: -1 point, -100 HKD penalty implementation
  - [ ] No-show: -2 points, -100 HKD penalty implementation
  - [ ] Starting score: 5 points implementation
  - [ ] Score floor enforcement at -10
  - [ ] Tier classification logic (Gold 20+, Silver 10-19, Bronze 0-9, Under Review <0)
- [ ] Create score update service (AC: 1, 5)
  - [ ] Implement score update on attendance events
  - [ ] Create score history tracking
  - [ ] Add score viewing endpoint for staff
- [ ] Implement ERP sync for scores (AC: 2)
  - [ ] Create ScoreSyncService for real-time ERP integration
  - [ ] Implement API calls to ERP system
  - [ ] Add retry logic and error handling
- [ ] Create manual override endpoint (AC: 4)
  - [ ] Implement admin endpoint for score override
  - [ ] Add reason field validation
  - [ ] Create audit logging for manual changes
- [ ] Add audit logging (AC: 4)
  - [ ] Implement audit trail for all score changes
  - [ ] Add user tracking for manual overrides
- [ ] Write unit tests (AC: All)
  - [ ] Test score calculation logic
  - [ ] Test tier classification
  - [ ] Test score floor enforcement
  - [ ] Test manual override functionality
- [ ] Write integration tests (AC: All)
  - [ ] Test ERP sync integration
  - [ ] Test score update flow end-to-end
  - [ ] Test audit logging integration

## Dev Notes

### Technology Stack
- **Backend:** Spring Boot 3.5.7 LTS, Java 21
- **Database:** MySQL 8.4.7 LTS
- **Patterns:** Service layer, Repository pattern
- **Testing:** JUnit 5, Mockito
- **Security:** Audit logging required for all score changes

### Architecture Patterns
- **ScoreCalculatorService:** Central service for all score calculations
- **ScoreSyncService:** Handles real-time ERP synchronization
- **Repository Pattern:** Data access layer with Spring Data JPA
- **Audit Trail:** All score changes tracked in score_history table

### Implementation Details
- Score floor of -10 enforced at service level
- Tier classification calculated dynamically based on current score
- Real-time ERP sync triggered within 1 minute of score change
- Manual overrides require mandatory reason field with audit logging
- Starting score of 5 for new staff members

### Project Structure Notes
- Score entities: `backend/src/main/java/com/phc/model/`
- Score services: `backend/src/main/java/com/phc/service/`
- Score repositories: `backend/src/main/java/com/phc/repository/`
- Database migrations: `backend/src/main/resources/db/migration/`
- Unit tests: `backend/src/test/java/com/phc/service/`

### References
- [Source: docs/product-requirements-document.md#FR-1: Scoring Algorithm]
- [Source: docs/architecture.md#Merit-Based Scoring Pattern]
- [Source: docs/architecture.md#Technology Stack Details]
- [Source: docs/architecture.md#Data Architecture]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

claude-sonnet-4-5-20250929

### Debug Log References

### Completion Notes List

### File List