# Feature: User Notification System

## Requirements

### User Stories

1. As a user, I want to receive in-app notifications when someone comments on my post
2. As a user, I want to configure which notification types I receive
3. As an admin, I want to broadcast notifications to all users

### Acceptance Criteria

**US-1: Comment Notifications**
- Given a user has a published post
- When another user comments on that post
- Then the post author receives an in-app notification within 5 seconds
- And the notification shows the commenter's name and a preview of the comment

**US-2: Notification Preferences**
- Given a user is on the settings page
- When they toggle notification categories on/off
- Then only enabled categories generate notifications going forward

### Non-Functional Requirements
- Notifications must be delivered within 5 seconds of the triggering event
- System must support 10,000 concurrent notification deliveries
- Notification history retained for 90 days
