# SkyJob AutoApply 🚀

A Windows desktop MVP to search public Greenhouse/Lever job listings and assist with application form filling.

## Features
- Tkinter desktop UI
- Search configured Greenhouse and Lever job boards
- Filter by role keywords and selected locations (e.g. Mumbai)
- Opens job postings in visible Chromium
- Best-effort autofill name/email/phone and resume
- Tracks opened applications in applications.csv

## Setup (Windows)
1. Install Python 3.11+ (enable Add Python to PATH).
2. Run install.bat
3. Edit boards.json and replace example slugs with real Greenhouse/Lever company board slugs.
4. Run run.bat
5. Add your profile and resume path, then click Search & Assist Apply.

## Limitations / safety
- Board slugs in boards.json are placeholders.
- Application sites differ; autofill is best effort.
- Review each application and submit manually. CAPTCHA/OTP/final submit are not bypassed.
- Do not commit your personal resume or profile information to a public repository.
