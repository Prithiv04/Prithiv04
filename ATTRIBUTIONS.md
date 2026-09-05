# ATTRIBUTIONS.md

This file records all third-party open-source components, techniques, and assets used in or referenced during construction of this GitHub profile README. Keeping provenance is good engineering practice.

---

## Components Used / Adapted

| Source | Component | License | Usage | Attribution Required? |
|---|---|---|---|---|
| [Platane/snk](https://github.com/Platane/snk) | Contribution snake SVG generator | MIT | Reused via GitHub Actions | Yes — license notice retained |
| [anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats) | GitHub stats cards | MIT | Linked via public API endpoint | Yes — license notice retained |
| [simple-icons/simple-icons](https://github.com/simple-icons/simple-icons) | Brand SVG icons | CC0-1.0 | Technology logos (if used locally) | Not required, but credited here |
| [tandpfun/skill-icons](https://github.com/tandpfun/skill-icons) | Skill badge icons | MIT | Skill display via API | Yes — license notice retained |

---

## Components Studied / Inspired By

The following open-source projects were studied for their architecture, animation techniques, and patterns. **No visual content was copied.** Design language, animation timing, and composition are original.

| Source | What Was Studied | License |
|---|---|---|
| [williamzujkowski/svg-terminal](https://github.com/williamzujkowski/svg-terminal) | Terminal SVG rendering, SMIL animation blocks, GitHub Action patterns | MIT |
| [navi3582/animated-github-profile](https://github.com/navi3582/animated-github-profile) | SMIL reveal technique, Python → SVG pipeline, Action refresh pattern | MIT |
| [DenverCoder1/readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg) | Typing animation logic, SVG generation concepts | MIT |
| [lowlighter/metrics](https://github.com/lowlighter/metrics) | GitHub metrics plugins and Action patterns | MIT |
| [github-readme-animated-chat-bubbles](https://github.com/uuu64/github-readme-animated-chat-bubbles) | Parameterized SVG template → generator → committed SVG architecture | MIT |
| [doyoon530/terminal-identity](https://github.com/doyoon530/terminal-identity) | Terminal identity + live GitHub data patterns | MIT |
| [GitHub/READMEForge](https://github.com/Nicconike/READMEForge) | SVG component generation, component APIs | MIT |
| [devicons/devicon](https://github.com/devicons/devicon) | Developer logos (SVG/font variants) | permissive |
| [n1shanthb/n1shanthb](https://github.com/n1shanthb/n1shanthb) | ASCII portrait SVG styling and textLength spacing concept | MIT |

---

## Custom-Built Components

The following are **entirely original** works created for this profile:

- `assets/hero/identity-hero.svg` — Custom animated Signature AI Engineering Identity Hero (SMIL)
- `assets/hero/identity-hero-static.svg` — Static dark identity hero variant
- `assets/hero/identity-hero-light.svg` — Static light mode identity hero variant
- `generators/hero/generate_identity_hero.py` — Identity hero SVG generator script
- `assets/hero/ascii-portrait.svg` — Custom animated terminal ASCII portrait (SMIL) generated from `hhgoa.jpeg`
- `assets/hero/ascii-portrait-static.svg` — Static dark variant
- `assets/hero/ascii-portrait-light.svg` — Static light mode variant
- `generators/hero/generate_ascii_portrait.py` — Reusable PIL/NumPy ASCII generator script
- `assets/hero/terminal-profile.svg` — Custom animated Terminal Profile Dossier (SMIL)
- `assets/hero/terminal-profile-static.svg` — Static dark profile dossier variant
- `assets/hero/terminal-profile-light.svg` — Static light mode profile dossier variant
- `generators/hero/generate_terminal_profile.py` — Terminal profile SVG generator script
- `assets/hero/ai-console.svg` — Custom animated Visual AI Systems Monitor (SMIL)
- `assets/hero/ai-console-static.svg` — Static dark visual monitor variant
- `assets/hero/ai-console-light.svg` — Static light mode visual monitor variant
- `generators/hero/generate_ai_console.py` — Visual AI Systems Monitor SVG generator script
- `assets/hero/whoami-editorial.svg` — Custom animated Editorial WhoAmI Typography (SVG)
- `assets/hero/whoami-editorial-static.svg` — Static dark editorial whoami variant
- `assets/hero/whoami-editorial-light.svg` — Static light mode editorial whoami variant
- `generators/hero/generate_whoami.py` — Editorial WhoAmI typography SVG generator script
- `assets/sections/selected-recognition.svg` — Custom Career Milestone Timeline SVG (SMIL)
- `assets/sections/selected-recognition-static.svg` — Static dark milestone timeline variant
- `assets/sections/selected-recognition-light.svg` — Static light mode milestone timeline variant
- `assets/sections/currently-engineering.svg` — Custom Directional Engineering Focus Map SVG (SMIL)
- `assets/sections/currently-engineering-static.svg` — Static dark engineering focus map variant
- `assets/sections/currently-engineering-light.svg` — Static light mode engineering focus map variant
- `generators/sections/generate_sections.py` — Milestones and engineering focus map SVG generator script
- `assets/github/activity.svg` — Custom animated Engineering Activity Visualizer (SMIL) powered by real GitHub contributions
- `assets/github/activity-static.svg` — Static dark engineering activity variant
- `assets/github/activity-light.svg` — Static light mode engineering activity variant
- `generators/github/fetch_contributions.py` — Real public GitHub contributions parser script
- `generators/github/generate_activity_svg.py` — Engineering Activity Visualizer SVG generator script
- `assets/github/languages.svg` — Custom animated Language Signal horizontal bar graph SVG (SMIL)
- `assets/github/languages-static.svg` — Static dark language signal variant
- `assets/github/languages-light.svg` — Static light mode language signal variant
- `generators/github/fetch_languages.py` — Real repository language distribution parser script
- `generators/github/generate_languages_svg.py` — Language Signal SVG generator script
- `generators/github/validate_svg.py` — Activity and Language SVG validation script
- `assets/icons/connect-*.svg` — Minimal self-contained SVG platform connect badges (dark & light variants)
- `generators/sections/generate_connect_badges.py` — Platform connect badges SVG generator script
- `assets/footer/terminal-footer.svg` — Terminal footer animation
- All project pipeline diagrams (`assets/projects/`)
- Overall README composition, visual identity, animation language, typography, and storytelling

---

## Notes

- All MIT-licensed components: original `LICENSE` and copyright notices are preserved in those repositories.
- CC0-licensed content (Simple Icons): no attribution required, but credited above for transparency.
- No proprietary images, stock illustrations, or copyrighted third-party artwork are used.
- No complete profile templates or complete visual designs were copied.
