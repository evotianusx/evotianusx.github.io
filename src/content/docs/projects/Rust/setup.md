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


        
