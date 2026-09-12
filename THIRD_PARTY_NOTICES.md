# Writing sources and licenses

The writing guide and review workflow adapt principles from [OMP Writing](https://github.com/bnivanov/omp-writing-skills), inspected at commit `8df095b5d9499f55e7f291bb53cbeb795cf1c397`. That version consolidates the earlier writing, voice and editing skills into `skills/writing`.

OMP Writing is copyright 2026 Bozhidar Ivanov & Contributors and distributed under the [MIT license](licenses/OMP-MIT.txt). Its craft reference credits [Anbeeld/WRITING.md](https://github.com/Anbeeld/WRITING.md), copyright 2026 Anbeeld, under the [MIT license](licenses/WRITING-MIT.txt). Its editing reference credits [Peter Yang's no-ai-slop](https://github.com/petergyang/no-ai-slop). This package contains an adapted writing guide rather than a copy of those complete skills.

The bundled `scripts/writing/cliche-lint.mjs` is copied unchanged from the inspected OMP commit. Its pattern-detection logic derives from [Simon Willison's LLM cliché highlighter](https://github.com/simonw/tools/blob/main/llm-cliche-highlighter.html), copyright Simon Willison, licensed under the [Apache License 2.0](licenses/APACHE-2.0.txt). OMP's CLI, code masking and line-reporting modifications use the MIT license above. The new cross-platform `lint.mjs` wrapper belongs to Image Gen Soul.

The optional AST pass installs [berelevant-ai/slopless](https://github.com/berelevant-ai/slopless) version 0.2.36 as a local dependency. Its implementation and dependencies are not bundled in the skill archive; the installed packages carry their own license notices.

No OMP installer, site artwork, credentials or external design skill is included.
