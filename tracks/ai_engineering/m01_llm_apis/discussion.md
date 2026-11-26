# Discussion questions: m01_llm_apis

Questions for a discussion drill: answer out loud, at your level, with a concrete
example; the tutor follows up (why? when would you not?) and judges against the read-first sources (track
README). No answers here on purpose.

1. What is actually sent to a chat model API in one request, and what comes back?
2. What is a token, and why are limits and prices counted in tokens rather than words?
3. The model is stateless. How does a chat application still feel like a conversation, and what does that cost?
4. A request fails with a rate-limit error, another with a bad-request error. How should your code treat each?
5. What do temperature and top-p change? When would you set temperature to 0, and what does that not guarantee?
6. Estimate the monthly cost of a feature that handles 50,000 requests a day with 1,200 input and 300 output tokens each. Which numbers do you need, and which do you assume?
7. The same prompt works on one provider and fails on another. What differs between providers' APIs, and how would you keep your code portable?
8. Why is a long, perfectly fitting prompt still followed less reliably than a short one?
9. What is the AI engineering stack, and how does an AI engineer's job differ from an ML engineer's and a full-stack engineer's?
10. What is the difference between pre-training and post-training, and which one do you control as an application builder?
11. How do you decide whether a use case is worth building with a foundation model, before writing code?
