---
title: "LoreBinders"
description: "AI-assisted worldbuilding, character relationship tracking, and chapter management platform for fiction authors."
order: 1
tags: ["Python", "Architecture", "AI/LLM", "FastAPI"]
repoUrl: "https://github.com/ashlynn"
featured: true
status: "Active"
role: "Creator & Lead Developer"
---

## Overview

**LoreBinders** is a structured narrative management system designed to solve complex continuity challenges in large fiction projects. Born out of the practical challenges of writing across multiple pen names and series, LoreBinders manages deep lore, character relationship graphs, scene progression, and AI context grounding.

### Key Highlights

- **Object-Oriented Domain Model**: Transformed from early functional prototypes into a decoupled architecture with dedicated managers (`EmailManager`, `RateLimitManager`, `AIModelRegistry`).
- **Comprehensive Unit Testing**: Rigorous test suites built with `pytest` ensuring high reliability across stateful narrative transforms.
- **Modern Type Safety**: Built from the ground up leveraging Python's modern typing system (`from __future__ import annotations`, Pydantic models).
- **Vision & Text AI Integration**: Multi-provider AI orchestration supporting dynamic prompts and context-aware outline generation.
