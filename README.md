These tools require this wonderful [Python Wrapper for the Canvas API](https://github.com/ucfopen/canvasapi).

Replace the sample credentials in `config.json.sample` with your own and rename the file to `config.json`

## Hide Distribution Graphs
`hide_distribution_graphs.py`

Toggles on (or off) the Hide Distribution Graphs course setting for all courses in a hard-coded set of terms (given as term_ids)

## Update Notification Frequency for Observers
`update_observer_notification_preferences.py`

Currently this script changes observer notification preferences on every communication channel for every type of notification to "never" by hard-coding a course id.

#### Needs investigation

Two notification channels aren't changing:

* discussionentry (which shows as "discussion_entry" accessing raw data in browser bu is being read as "discussionentry" by hitting the endpoint `users/:user_id/communication_channels/:communication_channel_id/notification_preference_categories`)
* registration
