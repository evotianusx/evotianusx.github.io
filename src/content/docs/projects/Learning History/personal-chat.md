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
