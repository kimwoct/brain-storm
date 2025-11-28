# User Stories

## US-NA-00: Staff Login
**As a** nursing assistant,
**I want** to log in to the PHC platform using my registered credentials (mobile number, username, or email),
**So that** I can access my dashboard and apply for shifts.

**Scenario - Login:**
```gherkin
Given: My staff account has been synced from ERP
When: I enter my mobile number, username, or email
And: I enter my password
Then: I am successfully logged in
And: I see my personal dashboard
```

**Acceptance Criteria:**
✅ Login supported via Mobile Number, Username, or Email
✅ Credentials validated against synced ERP data
✅ Account locked after 5 failed attempts
✅ "Forgot Password" flow via SMS/Email OTP
✅ Session timeout after 30 minutes of inactivity

**Priority:** Critical
