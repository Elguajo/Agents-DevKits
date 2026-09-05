# Usability Review Checklist

Use selectively. Do not force every item into every review.

## Orientation and hierarchy
- Can the user tell where they are?
- Is the purpose of the screen clear?
- Is the primary action visually and semantically obvious?
- Do secondary actions compete unnecessarily with the primary action?
- Is information ordered by user need rather than implementation structure?

## Navigation and information architecture
- Are labels understandable without insider knowledge?
- Can users predict where navigation items lead?
- Are related concepts grouped together?
- Is there a clear way back, out, or to a safe previous state?
- Are important destinations buried or duplicated?

## Interaction and affordance
- Do interactive elements look interactive?
- Are controls consistent with familiar platform/web conventions?
- Is current selection/state visible?
- Does every meaningful action receive feedback?
- Are destructive or irreversible actions protected appropriately?

## Forms and data entry
- Are labels persistent and specific?
- Are required/optional expectations clear?
- Is validation timely and actionable?
- Are errors placed near the cause and recovery path?
- Are defaults useful and safe?
- Are users asked for information earlier than necessary?

## System states
Check relevant:
- loading;
- skeleton/progress;
- empty;
- no results;
- success;
- error;
- offline/retry;
- disabled;
- active/selected;
- hover/focus;
- permission/authorization denial.

A missing state can be a usability defect even when the happy path works.

## Cognitive load and efficiency
- Is the user required to remember hidden context?
- Are repeated choices or steps avoidable?
- Are complex decisions broken into understandable chunks?
- Are frequent actions efficient for repeat users?
- Is information density appropriate for the task?

## Microcopy
- Use user language rather than internal implementation terms.
- Buttons should describe the action or outcome where practical.
- Error messages should explain recovery, not only failure.
- Avoid ambiguous labels such as “Continue” when a more specific action matters.

## Responsive usability
Do not only ask whether the layout fits.
Ask whether priority, tap targets, navigation, reading order, content density, dialogs, forms, and critical actions remain usable at smaller and larger viewports.

## Accessibility handoff signals
Hand off to `accessibility-review` when findings involve keyboard navigation, focus order/visibility, semantics, screen-reader behavior, contrast, target sizing, motion sensitivity, or other accessibility-specific criteria.
