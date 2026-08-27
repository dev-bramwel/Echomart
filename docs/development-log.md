# Daily Development Log

Use one entry per developer per working day. Record decisions and behavior changes, not every command typed. Keep entries short enough to scan during standup and detailed enough for a later handoff.

## Entry template

Copy this block for a new entry and place the newest entry at the top of the team's shared log.

```markdown
## YYYY-MM-DD - Name

**Focus:** One sentence describing the day's goal.

**Changed**

- `path/to/file`: What was added, changed, or removed.
- `path/to/file`: Behavior or API change, including endpoint/model/component names when useful.

**Validated**

- Commands run: `make test`, `make lint`, or another relevant check.
- Result: pass, failure, or not run with the reason.

**Decisions**

- Important implementation or product decisions and their rationale.

**Blocked / risks**

- What is blocked, affected, or still uncertain.

**Next**

- The next concrete task or handoff action.

**Related**

- Branch, issue, PR, migration number, or design link.
```

## Example

```markdown
## 2026-08-27 - Developer Name

**Focus:** Connect the product list to the filtered API response.

**Changed**

- `vite-frontend/src/...`: Added loading and empty states for product results.
- `backend/products/...`: Added category filtering to the list endpoint.

**Validated**

- Commands run: `make test`, `make lint`.
- Result: pass.

**Decisions**

- Kept filtering server-side so pagination remains consistent.

**Blocked / risks**

- Product image placeholders need a design decision.

**Next**

- Add coverage for invalid category values.

**Related**

- Branch: `feature/product-filtering`
```

## Logging guidelines

- Use ISO dates: `YYYY-MM-DD`.
- Mention paths and symbols so another developer can find the change quickly.
- Separate completed work from plans and unresolved risks.
- Link migrations and PRs when they exist.
- Do not record secrets, access tokens, customer data, or payment details.
