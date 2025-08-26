---
title: "My LinkedIn Scraping Saga: A Tale of Woe and... Well, More Woe"
description: "The goal was simple: scrape LinkedIn for contract jobs. The execution? Not so much. A story of browsers, profiles, and blocked buttons."
pubDate: "Aug 26 2025"
---

## The Great LinkedIn Scraping Adventure

So, I had this brilliant idea. I'm on the hunt for contract work, and LinkedIn is a goldmine. But manually searching and keeping track of which jobs I've applied for is a total drag. "I'm a developer!" I thought. "I can automate this!" The goal was simple: build a scraper to pull down posts from people advertising contract jobs. How hard could it be?

Famous last words, my friend.

### Round 1: Microsoft Edge

My first foray into this adventure was with Microsoft Edge. I figured, "Hey, it's a modern browser, it should work." Let's just say it... didn't go as planned. I'm not gonna bore you with the details, but it was a non-starter. Back to the drawing board.

### Round 2: Google Chrome, My Old Friend

Okay, on to Google Chrome. My thinking was, I'll just use my existing Chrome profile. That way, I'm already logged into LinkedIn, and I don't have to mess with all that pesky authentication stuff in my script.

Nope. Total failure. It just kept erroring out. It seems like programmatically firing up Chrome with your main profile isn't as straightforward as one might hope.

### Round 3: A Glimmer of Hope

Then, a lightbulb moment! What if I just *copy* my existing profile folder to a new, temporary location? I could then point my script's `user-data-dir` to this copied folder. It felt like a genius hack.

And you know what? It actually worked! The LinkedIn page loaded, and miracle of miracles, it recognized my Google profile. I could see my little profile picture in the corner. I was so close I could taste it.

### Round 4: The Inevitable Roadblock

But then, the final boss appeared. The "Sign in with Google" button. I clicked it, expecting sweet, sweet victory. Instead, LinkedIn, in its infinite wisdom, blocked the login. Just... nope. Denied.

Such is life, I guess. All that work, just to be thwarted by a single button.

So what's next? I'm not giving up. The next tool in my arsenal is the "undetectable chromedriver." It's supposed to be the answer to all my web-scraping prayers. We'll see.

Stay tuned for the next chapter in this ridiculous saga. Hopefully, it ends with a successfully scraped job post. A guy can dream, right?
