These tools require this wonderful [Python Wrapper for the Canvas API](https://github.com/ucfopen/canvasapi).

Replace the sample credentials in `config.json.sample` with your own and rename the file to `config.json`

## Hide Distribution Graphs
`hide_distribution_graphs.py`

This script toggles on (or off) the Hide Distribution Graphs course setting for all courses in a hard-coded set of terms (given as term_ids)

## Update Notification Frequency for Observers
`update_observer_notification_preferences.py`

Currently this one changes observer notification preferences on every communication channel to "never" by hard-coding a course id.

The script, takes a list of enrollment_term_ids as command line arguments, builds a list of all observers enrolled in all courses for the given terms. Then for each observer, all communication channels are looped through, and every communication notification frequency is set to "never," but of course this can be changed (hard-coded) to set all to another setting.
