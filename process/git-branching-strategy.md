# Git Branching Strategy

*Lightweight branch management for agile development*

## Overview

GitHub Flow remains the human collaboration transport, subordinate to the root [Semantic Engineering Protocol](./semantic-engineering-protocol.md).

**Core principles**:
- `main` represents the admitted release line for the repository;
- every non-trivial change binds an exact base SHA and one canonical WorkOrder subject;
- branches/PRs are projections of work, not authority;
- exact-head CI is evidence, not truth;
- merge is a consequential DO and requires explicit project/operator authority.

A moved base is new evidence. Never silently rebase the claimed subject and preserve its old standing.

> **When compound-engineering is in use**: see [`process/compound-engineering-integration.md`](./compound-engineering-integration.md) for branch-naming carve-outs (CE's `lfg`/`ce-work` autonomous flows) and the AI-review discipline that complements branch protection.

### Workflow Diagram

```text
gitGraph
    commit id: "initial"
    commit id: "stable"
    branch "1-add-user-auth"
    checkout "1-add-user-auth"
    commit id: "add login"
    commit id: "add tests"
    checkout main
    merge "1-add-user-auth" tag: "v1.1.0"
    commit id: "hotfix" type: HIGHLIGHT
    branch "2-add-notifications"
    checkout "2-add-notifications"
    commit id: "email notifs"
    checkout main
    merge "2-add-notifications" tag: "v1.2.0"
```

## Guiding Principles

1. **Exact base first** — record repository + immutable base SHA before implementation.
2. **One semantic subject** — bind branch, PR, checks, receipts, and projections to the same WorkOrder.
3. **Main stays admissible** — do not knowingly land a broken or unqualified release-line consequence.
4. **Issues are projections** — use them for navigation; in Semantic Work Mode they do not own work truth.
5. **Small coherent branches** — one independently verifiable semantic consequence per branch.
6. **Draft PR is the default publication boundary** — publication enables review/CI without granting merge.
7. **Exact-head evidence** — only evidence for the current head supports the current subject.
8. **Explicit merge authority** — CI, approval, proof, or plan does not independently authorize merge.

---

## Branch Types

### `main` - The Production Branch

**Purpose**: Represents deployable production-ready code

**Rules**:
- Always deployable and passing all tests
- Protected - requires pull request + review to merge
- No direct commits (except initial setup)
- Tagged with version numbers for releases

### Feature Branches

**Purpose**: Develop features, fix bugs, implement technical work

**Naming Convention**: Use GitHub's auto-generated branch names from issues

**Format**: `{issue-number}-{slugified-issue-title}`

**Examples**:
- Issue #1: "Write branching strategy standards doc" → `1-write-branching-strategy-standards-doc`
- Issue #42: "Fix login timeout error" → `42-fix-login-timeout-error`
- Issue #137: "Add email notifications" → `137-add-email-notifications`

**How to create**: Use GitHub's "Create a branch" feature directly from the issue

**Type classification**: Use issue labels instead of branch name prefixes. [`process/issue-tracking.md`](./issue-tracking.md#label-strategy) defines the set. `feature` and `refactor` are not in it: use `enhancement` and `tech-debt`.

**Lifecycle**:
1. Create issue, assign labels
2. Create branch from issue (GitHub auto-names it)
3. Develop and commit iteratively
4. Open pull request when ready (auto-links to issue)
5. Merge to `main` when approved and CI passes
6. GitHub auto-closes issue and deletes branch

---

## Workflow

For detailed mechanics, see [GitHub Flow documentation](https://docs.github.com/en/get-started/using-github/github-flow).

### Starting Work

1. Resolve repository and exact base SHA.
2. Resolve or create the canonical WorkOrder. In Documentation Mode, a GitHub issue may be the practical work record.
3. Record acceptance, constraints, falsifiers, verification court, dependencies, and authority ceiling.
4. Create the work branch without moving the admitted base silently.
5. Materialize only the source needed for the claimed boundary and start work.

### Keeping Branches Current

If `main` advances while working, sync your branch:

```bash
git fetch origin
git rebase origin/main  # or: git merge origin/main
git push --force-with-lease  # if rebased
```

Choose rebase (cleaner history) or merge (preserves history) and use consistently per project.

**Force push safety**:
- Always use `--force-with-lease` instead of `--force` (prevents overwriting others' work)
- Never force push to `main` (should be prevented by branch protection)
- Coordinate with teammates if sharing a feature branch

### Merging to Main

1. Open a draft pull request and record WorkOrder + exact base/head identities.
2. Run the narrowest repository-native court and exact-head CI.
3. Resolve review findings and classify unrelated/pre-existing/environmental failures separately.
4. Establish the project-required merge authority. Approval/CI are evidence inputs, not authority by themselves.
5. Merge only when explicitly authorized; squash-and-merge remains a reasonable repository policy where desired.
6. Re-observe the resulting main SHA and seal the mutation/verification receipt.
7. Project issue/ticket closure from the admitted consequence; closure does not itself create ALIVE standing.

**Note on squash merging**: When you squash and merge, all individual commits on the branch are combined into a single commit. This means:
- Individual commit messages are preserved in the squashed commit body
- The PR title is what GitHub builds the final commit message summary from (see [PR Title](#pr-title))
- Write clear, incremental commits during development for your own tracking
- Write the PR title to the format in [Commit Messages](#commit-messages); [PR Title](#pr-title) covers exactly how it reaches `main`

---

## Commit Messages

### Format

```
<type>: <summary in present tense>

[optional body: context, reasoning, references]
```

Scope is optional. When it tells the reader something the summary does not, add it to the type:

```
<type>(<scope>): <summary in present tense>
```

### Types

Common types (simplified subset of [Conventional Commits](https://www.conventionalcommits.org)):

- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code restructuring
- `docs:` - Documentation changes
- `test:` - Test additions/updates
- `perf:` - Performance improvements
- `chore:` - Build, dependencies, tooling
- `ci:` - CI/CD pipeline changes

### Examples

```
feat: add email notification preferences

Implements notification preferences UI and API endpoint
for users to configure email notification settings.

Refs: #137, docs/engineering/designs/notification-system.md
```

```
fix: prevent login timeout on slow connections

Increase timeout from 5s to 30s and add retry logic.

Fixes: #42
```

### Guidelines

- Use present tense: "add feature" not "added feature"
- Keep the whole first line to 72 characters or fewer, counting any `type(scope): ` prefix. That is [`gitlint`](https://jorisroovers.com/gitlint/latest/rules/builtin_rules/#t1-title-max-length)'s default `title-max-length`, and it sits under the [Linux kernel](https://www.kernel.org/doc/html/latest/process/submitting-patches.html)'s ceiling of no more than 70-75 characters for a patch summary. Git's own documentation suggests 50 for the whole summary line; this standard relaxes that to 72 to leave room for the type prefix. Note that in the widely cited 50/72 pair the 72 is the body wrap width, not a subject limit
- The limit applies to the subject as authored. GitHub appends ` (#<number>)` when it squashes, and that suffix is not counted against it
- Reference issue number and specs when applicable
- Explain why, not what (code shows what)

See [Conventional Commits](https://www.conventionalcommits.org) for more details.

---

## Pull Request Guidelines

### PR Title

A PR title must satisfy [Commit Messages](#commit-messages) above. Squash and merge is the recommended default, and GitHub builds the squash subject from the PR title, appending ` (#<number>)` to it, so a PR title that ignores the commit format lands on `main` as a commit that violates it:
- ✅ `feat: add user notification preferences UI`
- ✅ `fix: prevent login timeout on slow connections`
- ❌ `Add user notification preferences UI` (no type prefix)
- ❌ `Updates` (too vague, and no type prefix)

### PR Description

```markdown
## What
Brief description of the change

## Why
User/business value or problem being solved (link to issue/spec)

## How
Implementation approach (reference design doc if applicable)

## Subject
WorkOrder IRI/ID, repository, exact base SHA, candidate/head SHA

## Evidence ceiling
What this PR can and cannot establish

## Testing
Commands/courts, exits, exact-head CI, falsifiers exercised

## Receipt / standing
Observed consequence, replay evidence, bounded standing

## Related
- Closes: #123
- Spec: docs/engineering/designs/feature-name.md (if applicable)
```

### PR Size

Size by **semantic coherence and verification surface**, not a line-count quota. Prefer the smallest diff that closes one independently verifiable consequence while preserving required context. Generated projections do not count as design complexity, but their source/generator/receipt identity must be visible.

Split work when separate subjects, authority domains, falsifiers, or verification courts can stand independently. Do not split one atomic semantic change merely to satisfy a line target.

---

## Release and Versioning

### Semantic Versioning

Follow [semver](https://semver.org): `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Tagging Releases

```bash
git checkout main
git pull origin main
git tag -a v1.2.0 -m "Release 1.2.0: Add notification system"
git push origin v1.2.0
```

Maintain `CHANGELOG.md` or use [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github).

---

## Common Scenarios

### Hotfix for Production Bug

1. Create urgent issue with `bug` and `priority:high` labels (defined in [`process/issue-tracking.md`](./issue-tracking.md#label-strategy))
2. Branch from `main`: `45-fix-critical-auth-bug`
3. Fix with minimal changes, add test
4. Expedited PR review and merge
5. Tag as patch release (e.g., v1.2.1), deploy immediately

### Long-Running Feature

**Problem**: Feature takes 2+ weeks, don't want stale branch

**Solution**:
- Break into multiple issues/sub-features
- Each gets own branch and PR (keep each under 1 week)
- Use feature flags to hide incomplete UI
- Merge small increments continuously

### Experimental Work

1. Create issue labeled `spike` (defined in [`process/issue-tracking.md`](./issue-tracking.md#label-strategy))
2. Document in `docs/experiments/feature-name.md`, the location [`process/documentation-standards.md`](./documentation-standards.md#optional-directories-add-as-needed) declares
3. Develop on branch, timebox the exploration
4. **If successful**: Clean up, merge to `main`
5. **If unsuccessful**: Record findings in the brief, close the issue without merging

---

## Anti-Patterns

### ❌ Long-Lived Feature Branches

**Problem**: Diverge from `main`, painful merges, integration issues

**Solution**: Break work into smaller increments, merge frequently (max 1 week per branch)

### ❌ Direct Commits to Main

**Problem**: Skips review and CI validation

**Solution**: Protect `main` branch, require PRs (configure in repository settings)

### ❌ Large, Multi-Purpose PRs

**Problem**: Hard to review, slow feedback, risky merges

**Solution**: One issue per PR, use feature flags for incremental merges

### ❌ Branches Without Issues

**Problem**: No context, hard to track, unclear purpose

**Solution**: Create issue first (even for small fixes), use issue-based branching

**Exception**: When compound-engineering is in use, `lfg` and `ce-work` autonomous flows may produce topic-style branches (`feat/...`, `fix/...`) without a parent issue. File an issue retroactively only if review surfaces something worth tracking. See [`process/compound-engineering-integration.md`](./compound-engineering-integration.md).

### ❌ Stale Branches Not Synced

**Problem**: Merge conflicts, integration problems discovered late

**Solution**: Rebase/merge from `main` regularly (daily for active branches)

---

## Integration with AI Development

This strategy works well with AI-assisted development:

**Agents benefit from admitted context**:
- the root/project semantic graph defines stable subject identity and constraints;
- issues/specs are human projections of that context;
- branch and PR identities bind the same WorkOrder;
- receipts and falsifiers prevent narrative self-promotion.

**Best practices with AI tools**:
- Provide issue description and specs as context to AI
- Keep branches focused so AI maintains context
- Generate code in small increments (commit frequently)
- Always review and test AI-generated code before pushing
- Document AI-generated approaches in commit messages

**Example**: When asking AI to implement a feature, reference the issue number and include links to relevant specs from `docs/` directory.

---

## Branch Protection Configuration

Configure these rules for `main` branch in repository settings:

- ✅ Require pull request before merging
- ✅ Require at least 1 approval
- ✅ Require status checks to pass (CI/tests)
- ✅ Require branches to be up to date before merging
- ✅ Delete head branches automatically after merge

**When compound-engineering is in use**: the "Require at least 1 approval" rule has a process-level complement — the AI-review **discipline** (`ce-code-review` + `ce-doc-review`) defined in [`process/compound-engineering-integration.md`](./compound-engineering-integration.md). The discipline is process-level, not enforced by repo configuration; the standards' approval rule re-engages when a human reviewer onboards.

See [GitHub branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches) for setup details.

---

## When to Deviate

This strategy assumes:
- Continuous delivery model
- Small to medium team
- Web services / cloud deployments

**Consider alternatives if**:
- Multiple production versions maintained simultaneously → Use [GitFlow](https://nvie.com/posts/a-successful-git-branching-model/)
- Regulated deployments with long certification cycles → Add release branches
- Very large team (100+ developers) → May need coordination branches

Document deviations and rationale in project README.

---

## References

- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Creating branches from issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-a-branch-for-an-issue)
- [Semantic Versioning](https://semver.org)
- [Conventional Commits](https://www.conventionalcommits.org)

---

## Status

**Draft** - This standard is in active development and subject to revision based on practical experience.
