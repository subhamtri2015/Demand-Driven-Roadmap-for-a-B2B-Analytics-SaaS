# Risk Log

**Planned, not executed.** Risks and mitigations are proposed; no risk reviews have occurred.

| Risk | Likelihood / impact (assumptions) | Mitigation | Owner (proposed) |
|---|---|---|---|
| Ambiguous precedence produces inconsistent themes | Medium / High | Specify conflict rules and validate in test matrix. | SDK engineering + PM |
| Host CSS affects embedded rendering | Medium / High | Define isolation boundary and test representative collisions. | SDK engineering |
| Arbitrary values reduce legibility | Medium / Medium | Document contrast guidance and validate design constraints. | Design |
| Public demand proxy does not represent customers | High / High | Conduct interviews and validate with product usage evidence. | PM |
| Proposed events capture sensitive data | Low / High | Minimize payloads; privacy review; never send raw values. | PM + engineering |