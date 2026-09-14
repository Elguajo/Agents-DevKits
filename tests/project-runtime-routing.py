#!/usr/bin/env python3
"""Exercise routing facts in one process to keep the runtime gate responsive."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ROOT = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("project_runtime", ROOT / "project.py")
if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load project runtime")
project = importlib.util.module_from_spec(spec)
spec.loader.exec_module(project)
REGISTRY, _ = project.paths()


def skills(task: str) -> set[str]:
    facts = project.task_facts(task, [], [])
    return set(project.resolve_route(REGISTRY, facts)["skills"])


def require(task: str, *expected: str) -> None:
    actual = skills(task)
    missing = set(expected) - actual
    if missing:
        raise AssertionError(f"{task!r}: expected {sorted(missing)}, got {sorted(actual)}")


def forbid(task: str, unexpected: str, message: str) -> None:
    if unexpected in skills(task):
        raise AssertionError(message)


for task, owner in (
    ("change the stored schema version and migrate old records", "data-migration"),
    ("could these two async saves race with each other", "concurrency-review"),
    ("add a trace id to every outbound request", "observability-review"),
    ("what will break if I change this persisted identifier", "change-impact-analysis"),
    ("audit how this app stores a growing history", "data-storage-review"),
    ("will a restart leave this half written", "reliability-review"),
    ("review what personal data our analytics sdk collects", "privacy-review"),
    ("the tracking cookie stores an advertising id", "privacy-review"),
    ("let users opt out of telemetry", "privacy-review"),
    ("we depend on a third-party api with a strict rate limit and cursor pagination", "api-integration-review"),
    ("reconcile this audit into the roadmap without implementing code", "project-state-change-adoption"),
    ("do an exploratory qa pass on the staging site", "exploratory-qa-audit"),
    ("find bugs nobody has reported yet in the checkout flow", "exploratory-qa-audit"),
    ("try to break the signup flow", "exploratory-qa-audit"),
    ("run a bug bash on the staging build", "exploratory-qa-audit"),
    ("there is a bug on the settings page, find the root cause", "debugging"),
    ("verify the checkout flow end-to-end in a real browser", "playwright-testing"),
    ("does this page match the design", "visual-qa"),
    ("check the visual regression on the pricing page", "visual-qa"),
    ("the settings screen is confusing and hard to use", "ux-usability-audit"),
    ("check keyboard navigation and screen reader labels", "accessibility-review"),
    ("add unit tests for the browser utils parser", "testing"),
    ("add structured logging to the worker", "observability-review"),
):
    require(task, owner)

require("исправь ошибку в авторизации", "debugging", "security-review")

for task, owner, message in (
    ("add a trace id to every outbound request", "privacy-review", "A diagnostic identifier alone must not select the privacy owner"),
    ("add product analytics for the onboarding funnel", "privacy-review", "A generic collection term without a personal-data subject must not select the privacy owner"),
    ("set up issue tracking for the backlog", "privacy-review", "A generic collection term without a personal-data subject must not select the privacy owner"),
    ("audit how this app stores a growing history", "api-integration-review", "Local storage work must not select the external API owner"),
    ("find bugs nobody has reported yet in the checkout flow", "debugging", "Discovery of an unknown defect must not also select the root-cause owner"),
    ("there is a bug on the settings page, find the root cause", "exploratory-qa-audit", "A reported defect must stay with debugging instead of the exploratory QA owner"),
    ("this page is broken after the last release", "exploratory-qa-audit", "A reported defect must stay with debugging instead of the exploratory QA owner"),
    ("verify the checkout flow end-to-end in a real browser", "testing", "A browser flow must select the browser owner instead of the non-browser test owner"),
    ("add unit tests for the browser utils parser", "playwright-testing", "The word browser alone must not select the browser owner"),
    ("check the visual regression on the pricing page", "debugging", "A visual regression is a fidelity concern, not a reported defect"),
    ("не трогай авторизацию, исправь опечатку", "security-review", "An explicitly excluded authentication surface must not select security-review"),
    ("the login page rejects valid users", "observability-review", "Whole-word matching must keep login and logic out of the observability fact"),
    ("the logic here is wrong", "observability-review", "Whole-word matching must keep login and logic out of the observability fact"),
    ("plan an information architecture for the settings sitemap", "solution-architecture", "Adjacent owners must stay separated by phrasing"),
    ("plan the user research and an interview guide for onboarding", "ux-usability-audit", "Adjacent owners must stay separated by phrasing"),
    ("sync figma variables with code connect", "figma-to-code", "Adjacent owners must stay separated by phrasing"),
    ("add product analytics for the onboarding funnel", "product-spec", "Adjacent owners must stay separated by phrasing"),
    ("what am i not thinking about as the product owner", "product-spec", "Adjacent owners must stay separated by phrasing"),
    ("audit the technical health of this whole repository", "codebase-explorer", "Adjacent owners must stay separated by phrasing"),
    ("this page is broken after the last release", "release-check", "Adjacent owners must stay separated by phrasing"),
    ("add a trace id to every outbound request", "concurrency-review", "Whole-word matching must keep trace out of the concurrency fact"),
    ("fix a readme typo", "__any__", "A documentation typo must not select a specialist skill"),
    ("audit the technical health of this whole repository", "project-audit", "Project audits must require an explicit user request"),
    ("audit the technical health of this whole repository", "interdisciplinary-project-audit", "Project audits must require an explicit user request"),
    ("what am i not thinking about as the product owner", "project-audit", "Project audits must require an explicit user request"),
    ("what am i not thinking about as the product owner", "interdisciplinary-project-audit", "Project audits must require an explicit user request"),
):
    if owner == "__any__":
        if skills(task):
            raise AssertionError(message)
    else:
        forbid(task, owner, message)

owners = {
    "debugging": "there is a bug on the settings page, find the root cause",
    "testing": "add regression coverage for the parser",
    "playwright-testing": "verify the checkout flow end-to-end in a real browser",
    "visual-qa": "does this page match the design",
    "accessibility-review": "check keyboard navigation and screen reader labels",
    "exploratory-qa-audit": "do an exploratory qa pass on the staging site",
    "data-storage-review": "audit how this app stores a growing history",
    "data-migration": "change the stored schema version and migrate old records",
    "concurrency-review": "could these two async saves race with each other",
    "reliability-review": "will a restart leave this half written",
    "observability-review": "add a trace id to every outbound request",
    "change-impact-analysis": "what will break if I change this persisted identifier",
    "privacy-review": "review what personal data our analytics sdk collects",
    "api-integration-review": "we depend on a third-party api with a strict rate limit and cursor pagination",
    "quality-constraints": "define an enforceable quality bar and quality constraints for this project",
    "adversarial-decision-review": "run an adversarial review before implementation for this authorization decision",
    "source-driven-implementation": "verify this version-sensitive implementation against the official docs",
    "deprecation-lifecycle": "retire the old service and migrate consumers to its replacement",
    "security-review": "rotate the oauth secret for the payment provider",
    "affine-notion-graph-sync": "turn this notion page into an affine edgeless canvas",
    "product-spec": "the requirements are vague, define the scope and acceptance criteria",
    "codebase-explorer": "help me understand the codebase before I touch the importer",
    "feature-development": "should we build a new feature for saved filters",
    "journey-mapping": "we need a customer journey map for the trial flow",
    "information-architecture": "plan an information architecture for the settings sitemap",
    "solution-architecture": "how should we structure the module boundaries for sync",
    "project-knowledge": "record the conventions in a knowledge pack",
    "roadmap-status": "show the roadmap status with checkboxes",
    "project-state-change-adoption": "reconcile this audit into the roadmap without implementing code",
    "ux-research": "plan the user research and an interview guide for onboarding",
    "ux-usability-audit": "run a usability audit on the dashboard",
    "frontend-design": "set the visual direction and look and feel for the marketing page",
    "apply-aesthetic": "this needs a stronger aesthetic and visual character",
    "design-system": "reuse the existing design system and component library",
    "design-tokens": "extend the semantic design token scale for dark mode",
    "token-build": "run the token build with style dictionary",
    "design-component": "write the component spec with variants and states",
    "design-code": "implement the component in react",
    "design-review": "do a design review and critique the mockup",
    "design-qa": "set up a design qa plan with ui evidence",
    "responsive-design": "fix the responsive breakpoint on mobile layout",
    "motion-design": "add a micro-interaction with easing to the menu",
    "apple-quality-interface-refinement": "polish the interface, it feels unfinished",
    "ux-writing": "rewrite the microcopy and button label",
    "figma-integration": "sync figma variables with code connect",
    "figma-to-code": "implement this screen from the figma file",
    "performance-review": "the dashboard is slow, check the bundle size",
    "code-review": "code review this change before merge",
    "release-check": "are we ready to ship this release",
}

for owner, task in owners.items():
    require(task, owner)

routable = {entry["name"] for entry in REGISTRY["skills"] if "model" in entry["invocation"]}
missing = sorted(routable - set(owners))
if missing:
    raise AssertionError("model-invocable owners no task description reaches: " + ", ".join(missing))
