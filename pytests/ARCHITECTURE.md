# Python Playwright Architecture

This document defines the intended architecture for the Python Playwright test framework.

## Layers

1. `pytests/config`
Runtime settings and environment parsing.

2. `pytests/components`
Reusable UI building blocks (navigation, footer/subscription, modal widgets).

3. `pytests/pages`
Page orchestration classes. Pages can compose components and expose business actions.

4. `pytests/data`
Static test data, factories, and environment-backed credential providers.

5. `pytests/specs`
Test scenarios and assertions. Specs should call page/component behavior, not duplicate locator logic.

6. `pytests/utils`
Cross-cutting helpers such as reporting, attachments, and diagnostics.

## Dependency Rules

- `specs` can depend on `pages`, `data`, `utils`, `config`.
- `pages` can depend on `components`, `config`, `utils`.
- `components` can depend only on Playwright and shared component/base abstractions.
- `data` should not depend on `pages` or `components`.
- `config` should not depend on test specs or page objects.

## Coding Rules

- Keep selectors in pages/components, not in specs.
- Prefer typed function signatures and explicit return types.
- Keep retry/fallback behavior inside base abstractions, not duplicated in each page.
- Preserve backward compatibility when refactoring shared page APIs used by many tests.
- Add new reusable UI behavior as components before adding page-specific duplicates.

## Migration Strategy

- Refactor feature-by-feature to avoid a big-bang migration.
- Validate every refactor with `pytest --collect-only pytests/specs -q`.
- Run at least smoke tests after each feature area migration.
