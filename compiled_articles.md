# Compiled Articles

## src/content/docs/index.mdx

---
title: ""
description: Personal Page
template: splash
hero:
  title: "Evo's Page"
  tagline: Ego ergo sum codice
  image:
    alt: A glittering, brightly colored logo
    file: ../../assets/logo.svg
  actions:
    - text: Resume
      link: /resume/
      icon: right-arrow
      variant: primary
    - text: Side Projects
      link: /projects/home
      icon: external
---

## src/content/docs/projects/Astro/folder.md

---
title: Folder Game
description: Version History
---

The game is [here](/folder)

# Version History

## 1. Initial Implementation (v0.1)

**Features:**

- Office-themed hidden object game
- Static folders with:
  - Department labels (HR, Finance, Engineering)
  - Document types (CONFIDENTIAL, Q4 REPORT)
- Rectangular click detection
- Life system (3 lives)

## 2. Draggable Folders (v0.2)

**Changes:**

- Added drag-and-drop functionality
- Folders scramble on new rounds
- Drop verification zone (bottom-right)
- Removed click penalties (only drop-zone checks)
- Issues:
  - `preventDefault` console warnings
  - Inconsistent drop detection

## 3. Circular Drop Detection (v0.3)

**Fixes/Improvements:**

- Replaced rectangular detection with **radius-based check**:
  ```javascript
  const distance = Math.sqrt(Math.pow(xDist, 2) + Math.pow(yDist, 2));
  ```
- Visual upgrades:

  - Circular drop zone (rounded-full)

  - Drag highlight effects

- Better mobile touch support

## Passive Event Fix (v0.4)

**Technical Improvements:**

- Fixed Chrome passive event warnings:

```javascript
window.addEventListener("touchmove", handler, { passive: false });
```

- Added CSS:

````css
touch-action: none;
Unified mouse/touch event handling```
````

## Proper Drop Zone Alignment (v0.5)

**Critical Fixes:**

- Corrected bottom-right positioning:

```javascript
left: 100 - zoneWidth; // True right-edge
top: 100 - zoneHeight; // True bottom-edge
```

- Fixed coordinate math:

- Container offset compensation

- Pixel/percentage conversion

- Enhanced visual feedback

## src/content/docs/projects/Astro/guide.md

---
title: Astro as a simple website
description: A reference page in my new Starlight docs site.
---
Easiest method would be to clone my repo and fork it or you can follow these steps

## Steps

### Create a github repo with your username
The repo name should be `<YOUR_GITHUB_NAME>.github.io` for example in my case the repo name will be `evotianusx.github.io`

### Clone the repo
After that open it in your favorite IDE / Text Editor

### Initialize Astro Starlight Project
```sh
npm create astro@latest -- --template starlight
```
This will create a few files for you, navigate to the `/src/content/docs/index.md`

### Start your development server
Run the `npm run dev` inside the project directory, it will spin up a webserver usually at `http://localhost:4321/`

### Start Development
Start by editing the `index.mdx` file inside the `/src/content/docs/index.md`

## src/content/docs/projects/Astro/sveltereact.md

---
title: Svelte and React in one project
description: The power of using both Svelte and React in a single Astro project
lastUpdated: 2024-07-25
---

Astro's ability to seamlessly integrate multiple frontend frameworks like Svelte and React into a single project is a game-changer for web development. This flexibility offers significant advantages, particularly when it comes to building and scaling teams.

### The Best of Both Worlds

Svelte, with its compiler-based approach, is renowned for its performance and small bundle sizes. It's an excellent choice for building highly interactive and performant components. React, on the other hand, has a massive ecosystem, a vast talent pool, and a proven track record in building complex applications.

By using both, you can leverage the strengths of each framework where it makes the most sense. For instance, you could use Svelte for performance-critical UI elements and React for more complex components that benefit from its extensive library support.

### A Wider Talent Pool

One of the most significant benefits of this multi-framework approach is the ability to tap into a much larger talent pool. You are no longer restricted to hiring developers with expertise in a single framework. This opens up a world of possibilities for finding the right people for your team.

### Flexibility for the Company

For the company, this means greater flexibility in hiring and project allocation. You can build teams with a mix of Svelte and React developers, fostering a more diverse and collaborative environment. This also future-proofs your technology stack, as you're not locked into a single framework's ecosystem.

### The Astro Advantage

On top of the framework flexibility, Astro itself brings a host of benefits to the table:

*   **Performance by Default:** Astro's island architecture means that you ship zero JavaScript by default. Components are rendered to HTML at build time, and JavaScript is only loaded for the interactive components (islands) that you explicitly define. This results in incredibly fast load times and a great user experience.
*   **Content-Focused:** Astro is designed for content-rich websites. It has built-in support for Markdown, MDX, and content collections, making it easy to manage and organize your content.
*   **Developer Experience:** Astro offers a fantastic developer experience with features like a fast development server, a simple and intuitive project structure, and excellent documentation.

### The Winning Combination

By combining Astro's performance and content-focused architecture with the power and flexibility of Svelte and React, you get a development stack that is truly greater than the sum of its parts. You can build fast, content-rich websites with a rich, interactive user experience, all while leveraging a diverse and talented team of developers.

In conclusion, Astro's multi-framework capability is more than just a technical feat; it's a strategic advantage that can help you build better products, attract top talent, and create a more resilient and adaptable development team.

## src/content/docs/projects/Fertilizer-Calculator/index.md

---
title: "Fertilizer Calculator: A Deep Dive"
description: "An overview of the features, development, and future of the smart fertilizer calculator."
---

This article provides a comprehensive overview of the **Fertilizer Calculator**, a smart tool designed to help farmers and gardeners optimize their fertilizer usage for better crop yields.

## Background

The inspiration for this project comes from a real-world need. It was initially developed to help my father plan the fertilization for his durian garden. The goal was to create a simple tool that could take the guesswork out of calculating fertilizer needs, ensuring the trees get the right nutrients at the right time.

A key consideration in the calculator's logic is the concept of **fertilizer efficiency**. Not all the nutrients in a fertilizer are absorbed by the plant. The actual percentage of nutrient uptake can vary significantly based on factors like soil type, application method, and environmental conditions. For example, research on Nitrogen Use Efficiency (NUE) for cereal crops often shows that only about 30-35% of the applied nitrogen is actually used by the plants.

While this calculator uses a simplified model for efficiency, it highlights the importance of accounting for this factor to avoid both under-fertilization (which can lead to poor yield) and over-fertilization (which can harm the environment and waste money).

## Core Functionality

The calculator is built with a focus on scientific accuracy and user-friendliness.

- **Nutrient Requirement Calculation**: Determines the precise nutrient needs based on fruit yield and established scientific data.
- **Fertilizer Dose Calculation**: Calculates the exact amount of each fertilizer required per application.
- **Real-time Recalculation**: All calculations update instantly as you adjust inputs like fruit yield or application frequency.
- **Insufficient Nutrient Detection**: If the selected fertilizers don't meet the crop's needs, the tool alerts you and provides actionable advice.
- **Smart Suggestions**: To address nutrient gaps, the calculator intelligently recommends additional fertilizers.

## User Interface

The user interface is designed to be intuitive and efficient.

- **Interactive Inputs**: Sliders and input fields for fruit yield and application frequency allow for dynamic recalculations.
- **Chip-based Selection**: A modern, easy-to-use chip interface for selecting fertilizers.
- **Visual Feedback**: Clear color-coding and a responsive design provide at-a-glance information about nutrient levels.
- **Comprehensive Results**: The tool presents a detailed breakdown of nutrient requirements and a clear fertilizer application plan.

## The Development Journey

The project evolved through several phases, from a basic script to a full-featured web application.

### Phase 1: Basic Implementation

The initial phase focused on porting the core logic from a Python script to TypeScript. This involved creating the fundamental calculation functions for nutrient needs and building a simple user interface for input and output.

### Phase 2: Interface Enhancement

In the second phase, the user interface was upgraded. Checkboxes were replaced with modern, chip-based selection components. Real-time calculation triggers were added to provide instant feedback, and the overall styling and responsiveness were improved.

### Phase 3: Feature Refinement

This phase saw the addition of more advanced features. The display of total annual nutrient requirements was enhanced, and calculations for total and per-application fertilizer weights were added. The crucial features of insufficient nutrient detection and smart suggestions were also implemented.

### Phase 4: Final Polish

The final phase focused on refining the user experience. The layout was optimized, comprehensive error handling was added, and mobile responsiveness was improved. Visual feedback and user guidance were also enhanced to make the tool as intuitive as possible.

## Technology Stack

The application is built with a modern, reactive technology stack:

- **Svelte**: A reactive frontend framework for building fast and efficient user interfaces.
- **TypeScript**: For type-safe JavaScript, ensuring code quality and maintainability.
- **CSS3**: Modern styling with Flexbox and Grid for a responsive and flexible layout.
- **JSON**: Used for storing the fertilizer database.

## Future Roadmap

The future of the Fertilizer Calculator is exciting, with many potential improvements planned across several categories.

### 1. Enhancing the User Experience

- [ ] **Save/Load Presets**: Allow users to save fertilizer combinations for different crops.
- [ ] **Unit Conversion**: Support for different measurement units (lbs, acres, etc.).
- [ ] **Seasonal Planning**: Visual timeline showing application timing.
- [ ] **Cost Calculator**: Estimate total fertilizer costs based on local prices.

### 2. Adding Advanced Analytics

- [ ] **Nutrient Ratio Analysis**: Check if NPK ratios are optimal for fruit development.
- [ ] **Soil Deficiency Profiler**: Compare with common soil deficiency patterns.
- [ ] **Yield Projection**: Estimate potential yield based on nutrient plan.
- [ ] **Environmental Impact**: Calculate carbon footprint of fertilizer use.

### 3. Improving Data Management

- [ ] **Custom Fertilizer Database**: Allow users to add their own fertilizer formulations.
- [ ] **Export Options**: PDF, Excel, and CSV export for record keeping.
- [ ] **Batch Processing**: Calculate for multiple trees/areas at once.
- [ ] **History Tracking**: Save calculation history for future reference.

### 4. Building Educational Features

- [ ] **Nutrient Information**: Popups with information about each nutrient's role.
- [ ] **Best Practices Guide**: Tips for application timing and methods.
- [ ] **Crop-specific Recommendations**: Pre-loaded data for different fruit types.
- [ ] **Deficiency Symptoms**: Visual guide to nutrient deficiency signs.

### 5. Making Technical Enhancements

- [ ] **Offline Support**: PWA capabilities for field use.
- [ ] **Mobile Optimization**: Dedicated mobile app interface.
- [ ] **Multi-language Support**: Localize for different regions.
- [ ] **API Integration**: Connect to agricultural databases.

## src/content/docs/projects/Learning History/2024.mdx

---
title: '2024'
---

* Setup angular project
* Play around with angular material UI
* Learned about Angular Service
    - using http GET on resources
* Created Angular Component
    - First it was static component
* Read argument from URL
    - Dynamically fetch data based on the argument
* Learn to use AG - Grid
* Flex and Grid Display
* CSS styling on component


## src/content/docs/projects/Learning History/2025.mdx

---
title: '2025'
---

* Lots of angular stuff such as passing data to a new Mat Dialog
* Try out rust
    * Very painful to setup in windows, check this [article](/projects/rust/setup)

## src/content/docs/projects/Learning History/linkedin-scraping-adventures.md

---
title: "LinkedIn Scraping"
description: "The goal was simple: scrape LinkedIn for contract jobs. The execution? Not so much. A story of browsers, profiles, and blocked buttons."
pubDate: "Aug 26 2025"
---

## Automating LinkedIn Job Hunting: A Technical Adventure with Selenium and Chrome

Searching for contract work on LinkedIn can feel like an endless cycle: scroll, click, apply, repeat. Beyond the repetition, there’s also the challenge of keeping track of which roles you’ve applied for, which ones look promising, and which ones are already stale. As a developer, I saw an opportunity: Why not automate this? A scraper, purpose-built to collect job postings directly from LinkedIn, could save untold hours of effort and inject efficiency into the otherwise monotonous task of job-hunting.

The idea was simple—build a scraper that could:

* Collect LinkedIn job posts (particularly those advertising contracts).
* Allow me to quickly apply (or at least prepare for applying).
* Store the results in a structured format (eventually pushing them into a spreadsheet for tracking).

In theory, this would give me a personalized job-hunting dashboard. In practice, it became a crash course in browser automation, authentication quirks, and the invisible walls erected by modern web platforms.

### Step 1: First Attempt with Microsoft Edge

My first attempt was with Microsoft Edge, largely because it ships with Windows and has solid Selenium integration. The setup seemed straightforward: install msedgedriver, point Selenium to it, and open LinkedIn.

Instead of a smooth entry, though, I was greeted by an immediate crash. The browser session terminated before it could load a page, throwing errors about the DevTools port.

Lesson learned: not every browser is equally well-supported, and debugging setup issues can eat more time than it’s worth. At this point, Edge was out.

### Step 2: Reusing My Chrome Profile

Next, I turned to Chrome. The logic was appealing: my Chrome profile already had me logged into LinkedIn, so if I launched Selenium with that profile, I could bypass the login flow entirely. No fiddling with CAPTCHAs, no “Sign in with Google” dialogs—just straight to the content.

Here’s where theory met reality. Chrome refused to cooperate when asked to open my main profile under automation. The errors were cryptic, and the result was always the same: the browser launched but never successfully navigated to LinkedIn.

Lesson learned: Chrome is not designed to let you attach Selenium directly to your main user profile—it’s a security risk, and Google has deliberately made it difficult.

### Step 3: The Profile Duplication Trick

After a round of trial and error, I hit on an idea: copy my profile folder to a new temporary location and point Selenium’s --user-data-dir there.

Surprisingly, this worked. The browser launched, LinkedIn opened, and it recognized my Google profile. My profile picture even appeared in the top corner of the page. For the first time, I felt I was on the cusp of success.

At this point, I could scrape the page source and start parsing content with BeautifulSoup
This was the first real win in the project.

### Step 4: The Authentication Roadblock

And then came the final hurdle: authentication. Clicking Sign in with Google looked like it would complete the circle. Instead, LinkedIn promptly blocked the attempt. Google’s security checks identified the automated environment and refused to authenticate.

That was the end of the line for this iteration. The scraper could load LinkedIn while logged in, but any interaction requiring active authentication was stopped cold.

Lesson learned: platforms like LinkedIn invest heavily in anti-bot defenses. They don’t just check cookies—they monitor interaction patterns, headers, and even automation fingerprints.

![LinkedIn Failed Auth](../../../../assets/linkedin_fail_google.png)

## Where to Go From Here

At this stage, I had a partially functioning system: I could open LinkedIn in an automated browser session and see content. The missing piece was sustainability—being able to consistently log in, scrape posts, and track them without hitting roadblocks.

My next steps include:

Exploring undetectable ChromeDriver options, which aim to reduce the automation fingerprints that trigger platform defenses.

Building a pipeline to store scraped posts in a structured format (JSON, CSV, or directly into Google Sheets).

Adding logic to track whether I’ve already applied to a given post, so the system becomes a true job-application tracker, not just a data collector.

## A Note on Ethics and Practicality

Before closing, it’s important to acknowledge the elephant in the room: scraping LinkedIn is against their terms of service. The measures that blocked my automation aren’t arbitrary—they’re intentional safeguards.

For developers considering similar projects, there’s a balance to strike between technical exploration (learning Selenium, browser automation, and data pipelines) and respecting platform boundaries.

In my case, this project is primarily an exercise in technical learning. The long-term vision isn’t just scraping jobs blindly, but creating a workflow that helps me keep track of applications more effectively.

## Technical Roadmap

Here’s a possible milestone-based roadmap for turning this experiment into a more complete tutorial:

Milestone	Goal	Tools / Notes
1. ~~Basic Scraper	Launch Chrome, load LinkedIn, and parse job listings.	Selenium + BeautifulSoup~~
2. ~~Data Extraction	Extract relevant job details (title, poster, date).	XPath / CSS selectors~~
3. Storage	Save posts into CSV/JSON for persistence.	pandas or built-in csv
4. Application Tracking	Mark which posts I’ve already applied to.	Add status column in CSV/Sheets
5. ~~Sheets Integration	Push data into Google Sheets for real-time tracking.	gspread / Google Sheets API~~. Manual for now
6. ~~Automation Refinement	Experiment with stealthier drivers and better session management.	`undetectable-ChromeDriver`~~. DONE

## Final Code

```python
import os
import time
import shutil
import tempfile
from pathlib import Path
from contextlib import suppress

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# --- CONFIG ---
CHROMEDRIVER_PATH = "./chromedriver.exe"
PROFILE_NAME = "Default"

# Build paths
user_data_dir = Path(os.environ["LOCALAPPDATA"]) / "Google" / "Chrome" / "User Data"
src_profile = user_data_dir / PROFILE_NAME

if not src_profile.exists():
    raise FileNotFoundError(f"Profile folder not found: {src_profile}")

# Create temporary user data directory and copy profile
temp_udd = Path(tempfile.mkdtemp(prefix="chrome-clone-"))
dst_profile = temp_udd / PROFILE_NAME
dst_profile.mkdir(parents=True, exist_ok=True)

# Directories to skip during copy
skip_dirs = {
    "Cache", "Code Cache", "GPUCache", "Service Worker", "IndexedDB", "File System",
    "Storage", "GrShaderCache", "Media Cache", "Network", "Crashpad", "DIPS",
    "OptimizationGuide", "Platform Notifications", "Reporting and NEL"
}

# Copy profile files
for item in src_profile.iterdir():
    if item.name in skip_dirs:
        continue
    dst = dst_profile / item.name
    try:
        if item.is_dir():
            shutil.copytree(item, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dst)
    except Exception:
        pass

# Remove Chrome lock files
for lock in ("SingletonLock", "SingletonCookie", "SingletonSocket"):
    with suppress(Exception):
        (dst_profile / lock).unlink()

# Setup Chrome options
options = Options()
options.add_argument(f"--user-data-dir={temp_udd}")
options.add_argument(f"--profile-directory={PROFILE_NAME}")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")

# Start driver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
driver.set_window_size(1280, 900)

# Navigate and print page title
driver.get("https://www.linkedin.com/")
time.sleep(2)

soup = BeautifulSoup(driver.page_source, "html.parser")
print("Title:", soup.title.get_text(strip=True) if soup.title else "(no title)")
```

## Update

### Using undetectable-chromedriver

Extracting Structured Data with GPT-5

Once I had a stable browser session and could reliably fetch the HTML source, the next challenge was making sense of the data. LinkedIn posts are wrapped in deeply nested markup, and manually untangling it was tedious.

Here’s where GPT-5 came in handy: I used it to help me map the raw HTML elements into a structured format. With its assistance, I extracted key fields like post ID, author details, job role, and engagement metrics into a tabular format that looks like this:

| post_id             | author_name  | author_headline                        | date_label | date_iso_guess      | job_position_guess                   | content                                                | likes | comments | reposts | timestamp                        |
| ------------------- | ------------ | -------------------------------------- | ---------- | ------------------- | ------------------------------------ | ------------------------------------------------------ | ----- | -------- | ------- | -------------------------------- |
| 7363923075957956608 | James Dryden | Principal Consultant at Hydrogen Group | 5d         | 2025-08-21T18:59:04 | Data Engineer (GCP/Python) — UK ONLY | 🚀 Contract Opportunity – Data Engineer (GCP/Python)... | 10    | 1.0      | 2.0     | 2025-08-26 11:59:04.894450+00:00 |
| 7365991455921762305 | Unnati Kumar | Senior Talent Acquisition Specialist   | 5h         | 2025-08-26T13:59:04 | Contract Role (Remote)               | 🚀 We’re Hiring! Remote – Contract Role 🚀 Looking...    | 10    | 2.0      | NaN     | 2025-08-26 11:59:04.897465+00:00 |
|                     |              |                                        |            |                     |                                      |                                                        |       |          |         |                                  |

With this structure in place, it becomes straightforward to:

* Save results into CSV/JSON.

* Push them into Google Sheets for real-time tracking.

* Add logic to check whether I’ve already applied to a given post.

## Final Thoughts

What began as a “simple” project to streamline job hunting became an unexpected deep dive into the realities of modern web automation. While I haven’t yet achieved a fully functioning system, the lessons along the way—about browsers, sessions, authentication, and platform defenses—have been invaluable.

The story isn’t over. The next chapter will focus on refining the approach, experimenting with stealthier automation tools, and ultimately integrating the results into a structured application-tracking pipeline.

Until then, the adventure continues.

But I think I can just go to linked in everyday,
1. scroll down a few pages down
2. Save as HTML
3. Run BS4 parser
4. Form the table above


## src/content/docs/projects/Learning History/personal-chat.md

---
description: More interactive way for HR to do preliminary interview
pubDate: September 3 2025
title: Resume Chat
---




## Personal Inquiry Agent
## Why I Built This

Recruiters and HR professionals often want to get quick answers to basic
questions:\
- *"Can you walk me through your background?"*
- *"What kind of projects have you worked on?"*
- *"Are you open to relocation or remote?"*

Answering these repeatedly can feel like a loop. So, I decided to build
**Resume Chat**: an intelligent, interactive agent that represents me
online, answers career-related questions in real time, and even learns
from what it cannot answer yet.

You can try it live on my website: 👉
[evotianusx.github.io/chat](https://evotianusx.github.io/chat)

------------------------------------------------------------------------
## Setup
### How It Works

Under the hood, Resume Chat is a lightweight Python application that
combines **OpenAI's models**, **document parsing**, and a
**Gradio-powered interface**. It's essentially a "virtual me" that HR
can interact with---kind of like an AI-powered cover letter that talks
back.

Key features include:
- **Context-Aware Responses** -- It loads a detailed summary and my
LinkedIn export to generate personalized answers.
- **Feedback Loop** -- Unanswered questions are logged for me to refine
later.
- **Real-Time Alerts** -- Via Pushover, I get notified whenever a
recruiter leaves their details or asks something new
- **Interactive Web UI** -- A simple, clean Gradio chat interface that
embeds neatly into my personal site.

------------------------------------------------------------------------

### Technical Setup

#### 1. Environment Variables

All secrets are stored in a `.env` file (and ignored by Git):

```bash
OPEN_AI_KEY=your_openai_api_key
PUSHOVER_TOKEN=your_pushover_application_token
PUSHOVER_USER=your_pushover_user_key
```

#### 2. Context Files

The agent reads my background from local files:

```
│   app.py
│   README.md
│   requirements.txt
│
└───me
        linkedin.pdf
        projects.yaml
        summary.txt
```


### Installation
1. Clone
2. `uv pip install requirements.txt`
3. `uv run app.py`


This starts a Gradio web server at `http://127.0.0.1:7860`.

------------------------------------------------------------------------

### Deployment to Hugging Face Spaces

Since this is a static site add-on, I needed something free, simple, and
reliable. Hugging Face Spaces with Gradio turned out perfect.

Steps to deploy:

1.  **Install Gradio CLI**\
    ```bash pip install --upgrade gradio ```

2.  **Authenticate**\
    ```bash huggingface-cli login ```

3.  **Deploy**\
    ```bash gradio deploy app.py ```
    (Replace with your filename if different, e.g. `main.py`.)

4.  **Secrets**\
    Save your keys in `secrets.txt` (never commit!) and Hugging Face
    will handle encryption.

Once deployed, it's live at:

👉 `https://huggingface.co/spaces/<username>/<space-name>`

Mine lives here:
[evotianusx/evo_resume_chat](https://huggingface.co/spaces/evotianusx/evo_resume_chat).

Embedding it into my website was as simple as dropping an iframe.

------------------------------------------------------------------------

## Lessons Learned

-   Recruiter questions tend to repeat---a conversational agent really
    does cut down redundancy.\
-   Handling **context sources** cleanly (summary + LinkedIn + projects)
    is trickier than I expected. Prompt balance matters.\
-   Deployment on Spaces is smooth, but environment variables must be
    handled carefully.\
-   The feedback loop (logging unanswered questions) makes the system
    feel like it "improves" over time.

------------------------------------------------------------------------


🚀 For me, Resume Chat is more than a side project---it's a small
experiment in making the job hunt less repetitive and more interactive.

## src/content/docs/projects/Office/appscript.md

---
title: Google App Script
---

Needed to copy and rename a google sheet ? For example you have a template and needed to create a brand new instance each day

Can use the code snippet below

1. Open the template in google sheet
2. Go to Extensions -> App Script
3. Copy and paste the script into the box
   - You might need to create a project, just follow the steps
4. Hit Run and it will then create a duplicates of the template sheet

```js

# There is a +- 5 minutes run time, and each creation of sheet takes +- 5 seconds
# You might need to create
function myFunction() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  # Example duplicate the file 10 times, with an ascending counter
  duplicate = 10;
  for (var i = 0; i <= duplicate; i++) {
    # Here I pad the number to be 4 digits, but this can be changed as per requirement
    var new_sheet = ss.copy("Pohon-" + String(i).padStart(4, '0'));
    # It will then print the sheet URL into the log
    Logger.log(String(i) + "|" + new_sheet.getUrl());
  }
}
```

## src/content/docs/projects/Office/printing.md

---
title: Batch edit .docx files
---

## Background
There are times where you kept documents as seperate files, however you received notification that the Date format for all the document were to be changed from `dd-mm-yyyy` to `yyyy-mm-dd`. Or something like that, check out the guide below on how I used python to help solve this issue


## Setup
1. Install the package `!pip install python-docx`
2. Use glob to read the files
3. Open said document
4. Loop thru all the `paragraph` and replace as neccessary
5. Save document


## Code
```python
from glob import glob
from docx import Document

fl = glob('{YOUR_DIRECTORY}/*.docx')
for f in fl:
    doc = Document(f)
    for p in doc.paragraphs:
        # Here you add your logic,
        # for example I replace the G123 keyword to G234
        if 'G123' in p.text:
            p.text = p.text.replace('G123','G234')
    doc.save(f)
```

## src/content/docs/projects/Rust/setup.md

---
title: Setting Up Rust in windows
description: Tutorial on setting up rust env inside a wsl from a windows host to minimize install
banner:
  content: |
    Gemini helped with re-writing this
lastUpdated: 2025-01-10

---


**Hey there!**

I know setting up Rust on Windows can be a bit of a headache.  Those C++ build tools are huge – 6GB just to say hello to the world?  Ouch.

Here's a way to set things up a bit more smoother:

1. **Let's get Ubuntu WSL on your Windows machine.**  This will create a Linux environment that you can run right inside Windows.
2. **Install the VS Code extension for WSL.**  This will let you connect to your WSL environment from VS Code.
3. **Once you're connected to WSL, you'll need to install some things there.**  Don't worry, it'll be much lighter weight than the Windows setup.  Run the installation script inside WSL, and you'll be good to go.
4. **Fire up VS Code on your Windows machine.**
5. **Look down in the left corner of VS Code.**  See that WSL connection option?
6. **Now that you're connected to WSL inside VS Code, you'll need to install some extensions there.**  They're separate from the ones you have on Windows, but luckily they're much smaller.  Grab the `rust-analyzer` extension – that one's essential for Rust development.
7. **Let's make something awesome!**  Use the Cargo tool to create a new Rust project.
8. **Open your `main.rs` file in VS Code.**
9. **See that little hover  over your code?**  That might be an option to run your code.  Give it a try!  If not, you can always use the command palette `CTRL+SHIFT+P` and search for something like `rust-analyzer run`.




## src/content/docs/projects/Sveltekit/guide.md

---
title: Sveltekit Toy Project
description: A reference page in my new Starlight docs site.
---
Add in some github pages action

## src/content/docs/projects/home.md

---
title: Home
description: ""

sidebar:
  order: 1

---
Here are some of the side projects I worked on.

## src/content/docs/resume.mdx

---
title: Evotianus Benedicto - Software Engineer
description: Evotianus Benedicto's professional portfolio and resume, showcasing expertise in software engineering, infrastructure, and core banking systems.
---
# Evotianus Benedicto

import { Card, CardGrid } from "@astrojs/starlight/components";

<Card title="Contact">
  * Email: [evotianusx@gmail.com](mailto:evotianusx@gmail.com)
  * Phone: [+6281806060414](tel:+6281806060414)
</Card>

My name is Evotianus Benedicto. I am a results-oriented **Staff Software Engineer** with over **5 years of experience** in designing, developing, and deploying scalable backend systems, robust infrastructure, and secure core banking solutions. My expertise lies in leading complex technical projects, migrating legacy systems, and architecting for high availability and performance. I am adept at translating business requirements into innovative software solutions and have a strong commitment to data protection and regulatory compliance.

A proactive and collaborative leader, I thrive in fast-paced environments, consistently delivering high-quality results both independently and as part of a team. I am passionate about mentoring engineers and fostering a culture of technical excellence.

## Experience
### Nikel

#### Staff Engineer
##### June 2025 – Present (as of June 20, 2025)

* **Led the strategic rewrite of the core banking system** from Java/MongoDB to Python/Django, aimed at enhancing scalability, performance, and long-term maintainability.
* **Architected and directed the migration** from a legacy third-party core banking ledger to an interim in-house solution, ensuring uninterrupted business operations during the transition.
* **Partnered with product and business stakeholders** to define technical specifications and requirements for a new, high-performance in-house ledger system.
* **Acted as Lead Solutions Architect** for a collaborative fraud detection project, designing resilient, scalable solutions integrated with new and existing systems.
* **Mentored and guided junior and mid-level engineers**, fostering technical growth and establishing best practices in software architecture and development.

#### Software Engineer
##### June 2022 – June 2025

* **Spearheaded the accelerated deployment of a core banking ledger software within one month**, significantly enhancing the company's financial operational capacity.
* **Engineered and maintained complex Smart Contracts using a Python DSL**, developing sophisticated accounting flows for precise tracking of financial transactions throughout the contract lifecycle.
* **Launched a comprehensive Case Management Service**, improving operational workflow efficiency for customer and internal case handling.
* **Developed and implemented a robust Audit Trail System**, guaranteeing data integrity, adherence to financial regulations, and detailed traceability for all system actions.
* **Played a key role in designing and implementing critical Python-based backend microservices**, focusing on performance optimization and system reliability.

#### Cloud Engineer
##### September 2019 – June 2022

* **Engineered, maintained, and optimized highly available Kubernetes infrastructure** (including Kafka, PostgreSQL, MongoDB) to ensure robust data persistence and high-throughput messaging.
* **Provided critical support for the "Credit as a Service" product**, including initial cloud infrastructure setup (GCP/AWS), third-party dependency integration, and operational support for large-scale lending operations.
* **Managed complex Airflow data pipelines and developed essential helper scripts** to support key business functions, such as borrower exposure analysis and regulatory reporting (OJK - AFPI).
* **Championed Infrastructure-as-Code (IaC) principles using Terraform**, automating cloud resource provisioning and management for improved deployment speed and consistency.
* **Proactively monitored system performance, implementing scaling and optimization strategies** to maintain system stability and optimize costs.

### Rockwell Automation

#### Client Engineer
##### August 2018 – May 2019

* **Led the Multistrada MES project as Project Engineer**, overseeing successful implementation and on-time delivery.
* **Developed a production line monitoring dashboard**, enabling rapid identification and visualization of operational issues, thereby improving efficiency.
* **Delivered a machine learning workshop** for AHM, sharing expertise and fostering industry knowledge.
* **Created multiple AR/VR demonstrations** to showcase innovative applications of emerging technologies.

### Databot

#### Software Engineer
##### November 2016 – April 2018

* **Developed and trained Part-of-Speech (POS) and Named Entity Recognition (NER) tagging models** for advanced Natural Language Processing (NLP) applications.
* **Engineered data scraping solutions** to collect and process data from diverse news sources, creating comprehensive training datasets.
* **Built and implemented autocorrection and word stemming systems**, significantly enhancing text processing accuracy and efficiency.
* **Utilized Web3JS for development tasks**, focusing on data integration with the Ethereum blockchain.

---

## Projects

Explore my recent projects, including the development of this website, on my [GitHub Pages](https://evotianusx.github.io).

---

## Education

### University

#### XJTLU
* **Bachelor of Engineering - Computer Science and Technology**
* 2014-2016

### Courses

#### Udacity
* Project Management
* Self-Driving Car

### Certifications

#### Associate Cloud Engineer (ACE)
* [Verify Certification](https://www.credential.net/12e26e32-a9d7-496c-b097-59bd08f9d119?key=ca83e9caf44e71eab59220d64c06f715a17d8388ae309e5eb353cda5afdf55db)

---

## Skills

*   **Programming Languages & Frameworks:** Python (Django, Flask, PySpark), JavaScript
*   **Libraries & Tools:** Numpy, Pandas, Keras, Tensorflow
*   **Cloud Computing & DevOps:** GCP, AWS, Kubernetes, Docker, Terraform, Airflow
*   **Databases:** MongoDB, PostgreSQL
*   **Expertise:** Backend Development, Full-Stack Development, Cloud Architecture, Infrastructure Management, Data Pipelines, Solutions Architecture, Core Banking Systems, Smart Contracts, Microservices, Agile Methodologies

## src/content/docs/tools/home.md

---
title: Tools
description: ""

sidebar:
  order: 1
---


## Collection of small tools I built

*  [Bill Splitter](/split)
*  [Pesangon Calculator ](/severance)
*  [Fertilizer](/fertilizer)
*  [Resume Chat Bot](/chat)

## Game

*  [Find Files](/folder)
