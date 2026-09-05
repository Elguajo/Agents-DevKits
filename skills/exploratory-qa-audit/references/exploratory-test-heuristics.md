# Exploratory Test Heuristics

A catalogue of variation ideas. Select what fits the charter and the flow; running every item everywhere wastes the session and buries real defects.

## Input variation
Empty, minimum, maximum, far beyond maximum, whitespace only, leading/trailing whitespace, duplicate of an existing value, invalid format, wrong type, Unicode and non-Latin text, right-to-left text, emoji-length grapheme clusters, pasted rather than typed, special and quoting characters, values changed rapidly, and two fields set to conflicting values.

Do not send destructive or abusive payloads to production or third-party systems.

## Action variation
Double click, rapid repeated submit, submit before async work finishes, cancel then retry, undo and redo, open and close repeatedly, change selection quickly, repeat an already completed action, navigate away mid-operation, and use a keyboard path where a pointer path was assumed.

## Navigation variation
Browser back, browser forward, refresh mid-flow, direct URL and deep link into a mid-flow state, a link to a resource the user cannot access, a stale link to a deleted resource, opening a second tab, returning to a stale tab, switching routes rapidly, and reopening the product after closing it.

## State variation
First-time, returning, empty, populated, very large data set, loading, success, validation error, server or network error, partial data, stale data, disabled, permission-limited, and expired or lost session.

## Time and interruption
Slow responses, retry after failure, temporary offline, refresh during a mutation, navigation during save, cancellation mid-request, timeouts, background/foreground transitions, and resuming after an interruption.

Do not claim a condition was tested when the environment could not produce it.

## Persistence
For user-visible durable state, check that it survives reload and navigation, does not silently disappear, does not duplicate, does not revert to an older value, that deletion actually persists, that editing one record does not corrupt an adjacent one, and that previously created data is still readable.

Deeper durable-data concerns belong to `data-storage-review`; a format or schema transition belongs to `data-migration`.

## Multi-context
Two tabs on the same account, two windows, a session change made in another tab, a record edited in both places, and concurrent-looking actions on the same resource.

When a reproducible failure appears to depend on interleaving or shared state, record the user-observable defect first, then hand the mechanism to `concurrency-review`.

## Runtime signals
Uncaught exceptions, unhandled promise rejections, failed requests, unexpectedly repeated requests, mishandled response statuses, requests that never resolve, unexpected reloads or remounts, and errors that appear only on a second attempt.

A warning is not a defect by itself. Tie every signal to an exercised flow and a user-visible consequence before reporting it.
