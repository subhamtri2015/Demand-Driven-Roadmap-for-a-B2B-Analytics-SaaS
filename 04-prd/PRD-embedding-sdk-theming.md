# PRD: Embedding SDK theming with CSS variables

**Version:** v0.1 draft  
**Author:** [Your name]  
**Status:** Draft - portfolio case study  
**Date:** 2026-10-19

## Version history

| Version | Date | Change |
|---|---|---|
| v0.1 | 2026-10-19 | Initial proposed scope from public signals; requires discovery. |

## Problem

Public issue [#59237](https://github.com/metabase/metabase/issues/59237) requests CSS variables in SDK theming and is an open-request demand signal in the fetched data. Public reactions are not representative customer demand. Apache Superset PR [#40763](https://github.com/apache/superset/pull/40763) describes an SDK-set theme being ignored when a dashboard has its own theme and proposes a fix; status is not verified. This provides external context for precedence, not evidence about Metabase SDK behavior.

## Users

Hypothetical persona: an embedding developer integrating analytics into a B2B SaaS product, working with design-system tokens and needing predictable preview and release behavior. This persona is not based on interviews.

## Goals

- Specify an illustrative CSS-variable contract for key colors and typography.
- Specify deterministic precedence and host-style isolation behavior.
- Plan a preview and publish workflow with observable error reporting.

## Non-goals

- Claiming or changing current SDK support without engineering discovery.
- Replacing all product-level or report-level styling mechanisms.
- Building a complete theme editor or guaranteeing accessibility for arbitrary user values.

## Scope

Proposed: variable names, token mapping, precedence, font family/size behavior, isolation, dark-mode variables, documentation, instrumentation plan. Variable names below are illustrative only.

## User stories and acceptance criteria

### Story 1: Brand colors

As an embedding developer, I want to set brand colors with CSS variables so that embedded content can align with my product design system.

```gherkin
Given an embed configuration with illustrative variables --mb-brand-primary and --mb-brand-surface
When the embedded view is rendered
Then supported visual elements use those values
And unspecified variables use documented defaults
```

### Story 2: Precedence

As an embedding developer, I want precedence between a theme object and CSS variables to be explicit.

```gherkin
Given a theme object and CSS variables both define the same token
When the embed resolves its theme
Then the documented precedence rule is applied consistently
And the resolved source is inspectable in development diagnostics
```

### Story 3: Typography

As an embedding developer, I want font family and size controls so that embedded text fits my host product.

```gherkin
Given supported illustrative font variables are configured
When text is rendered in an embedded view
Then supported text uses the configured family and size
And missing or invalid values fall back safely
```

### Story 4: Style isolation

As an embedding developer, I want host CSS not to unintentionally alter embedded components.

```gherkin
Given host styles contain selectors that match common element names
When the embed renders
Then host selectors do not unintentionally change supported embedded styles
And the isolation boundary is documented
```

### Story 5: Dark mode

As an embedding developer, I want to configure a dark palette with variables.

```gherkin
Given a dark-mode variable set is configured
When the host selects dark mode
Then supported embedded surfaces use the dark values
And contrast constraints are documented for the integrator
```

## Functional specifications

- Define supported variables, value types, fallback behavior, and token-to-component mapping.
- Define precedence across defaults, theme object, and CSS variables through design and engineering review; no precedence rule is assumed by this draft.
- Define validation errors and non-sensitive diagnostics.
- Provide preview behavior and clear separation between draft configuration and publish action.

## Non-functional requirements

Targets below are assumptions to validate with SDK engineering: no material regression in embed initialization; deterministic results for identical configuration; no unbounded style leakage into the host page; accessible contrast guidance; no raw theme values in analytics payloads.

## Edge cases

Invalid CSS values; partial variable sets; late host stylesheet load; font unavailable; nested embeds; theme object conflict; dark-mode switch during a session; responsive layouts; unsupported variable names.

## Dependencies

SDK engineering feasibility review, design-system review, docs review, privacy review for proposed events, and user discovery. No dependency is confirmed.

## Assumptions and open questions

- Assumption: developers can provide CSS variables in their integration context.
- Open: what surfaces and component tokens matter most?
- Open: should CSS variables override a theme object, or should the SDK reject conflicts?
- Open: what isolation technology and browser constraints apply?
- Open: which users can safely preview and publish configuration?

## Rollout plan

Planned, not executed: flagged beta with opt-in feedback, followed by a GA decision after reliability and support criteria are reviewed. Align a release window to the observed npm minor-line cadence as context only; npm publish timestamps do not guarantee a delivery date.

## Success metrics

Plan, no results: publish rate, median minutes from configuration start to publish, and theme error rate as described in [metrics plan](../05-metrics/metrics-plan.md). Targets are assumptions and must be set after baseline instrumentation.

## Tracking plan

See [tracking plan](../05-metrics/tracking-plan.md). Events are proposed and not instrumented.

## RACI

See [stakeholder RACI](../07-stakeholders/raci.md); proposed ownership only.

## Risks

Ambiguous precedence; host-style leakage; arbitrary values reduce legibility; unsupported fonts; broad token surface increases maintenance; public reactions do not validate customer impact; scope may exceed release constraints.

## Glossary

- CSS variable: a custom property in CSS, written with a `--` prefix.
- Theme object: a structured configuration of visual tokens.
- Embed: analytics content integrated into a host application.
- Reach proxy: sum of 👍 on qualifying open public issues, not customer count.