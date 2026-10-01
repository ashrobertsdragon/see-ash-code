---
title: "ProsePal"
description: "An integrated author workspace and pipeline orchestrator managing creative workflows, services, and document tooling."
order: 2
tags: ["TypeScript", "Python", "Monorepo", "Turborepo", "Docker"]
repoUrl: "https://github.com/ashlynn"
featured: true
status: "In Development"
role: "Maintainer & Architect"
---

## Overview

**ProsePal** is an author workspace monorepo orchestrating administrative tooling, microservices, and user-facing author utilities. It serves as the unified umbrella bringing together narrative tools, web interfaces, and automated background jobs.

### Key Architecture Features

- **Monorepo Architecture**: Cohesive management of frontend web apps, API services (`lorebinders-api`), admin dashboards, and shared packages.
- **Microservice Orchestration**: Dedicated orchestrators handling long-running background document conversion and AI-assisted data transforms.
- **Modern CI/CD & Testing**: Automated linting, static type verification (TypeScript & MyPy), and end-to-end testing with Playwright.
