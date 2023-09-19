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