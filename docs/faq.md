---
layout: default
title: FAQ
---
# Frequently Asked Questions

**Q: How do I try MemoryCache?**

Right now (as of December 7, 2023), MemoryCache requires a few manual steps to set up the end to end workflow. There are three components: a) a Firefox extension, b) a local instance of privateGPT, and c) a symlinked folder between privateGPT and your local Downloads folder. There is also an optional configuration that can be done to a private build of Firefox to save files to your local machine as PDF files instead of HTML files. Check out the [GitHub repository](https://github.com/Mozilla-Ocho/Memory-Cache) for more detailed instructions. We are looking into ways to streamline the deployment of MemoryCache to require less manual configuration, but if you're here at this stage, you're at the very earliest stages of our explorations. 

**Q: Does MemoryCache send my data anywhere?**

No. One of the core principles of MemoryCache is that you have full control over the system, and that it all stays on your device. If you're a developer or someone who just likes to tinker with your computer applications, and you want to cloud-ify this, feel free! But we're looking to stay entirely local. 

**Q: Why is MemoryCache using an old language model and primordial privateGPT?**

MemoryCache is using an old language model ([Nomic AI's gpt4all-j v1.3 groovy.ggml](https://huggingface.co/nomic-ai/gpt4all-j)) and primordial privateGPT because right now, this combo is the one that passes our criteria for the type of responses that it generates. This tech is almost a year old, and there have been many advancements in local AI that we'll be integrating in over time, but we're a small team exploring a lot of different subsets of this problem space and the quality of the insight generated is a sweet spot that we want to preserve. This is a temporary tradeoff, but we want to be careful to keep a consistent benchmark for insight generation.

**Q: What kind of tasks would I use MemoryCache for?**

MemoryCache is ultimately leaning into the weird and creative parts of human insight. The goal with MemoryCache is to "learn what you learn", which is why you are in control of what you want files you want to augment the application with. This can be helpful for research, brainstorming, creative writing, and synthesis of new ideas to connect seemingly unrelated topics together to find new insights and learnings from the body of knowledge that matters most to you. 