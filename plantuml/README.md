# How to create a PlantUML architecture diagram with ChatGPT

[PlantUML](https://plantuml.com/) supports [architecture diagrams](https://plantuml.com/archimate-diagram) suited for cloud architecture. It also includes [cloud icons](https://github.com/plantuml/plantuml-stdlib).

To guide ChatGPT (or any LLM) to create a PlantUML architecture diagram, you can start with the code or an explanation.

To start with the code, use [files-to-prompt](https://github.com/simonw/files-to-prompt):

```bash
uvx files-to-prompt --cxml README.md ... | xclip -selection clipboard
```

Paste it and add this prompt for a PlantUML diagram:

> Based on this, create a PlantUML component diagram to describe the technical architecture.
> Read these files for cloud icons. For EVERY cloud component use the icon macro ONLY from these files:
>
> - https://github.com/sanand0/tutorials/releases/plantuml/main/AWS.puml
> - https://github.com/sanand0/tutorials/releases/plantuml/main/Azure.puml
> - https://github.com/sanand0/tutorials/releases/plantuml/main/GCP.puml

- [Sample conversation](https://chatgpt.com/share/68312df6-a134-800c-9a9c-80d39b41ffcc)
- [PlantUML output](https://editor.plantuml.com/uml/ZLBDRjiy4BphAJO-10aGMy1tpE53dBW_1kpKhPBsM53asc93KGftcTHz-YvDAq6DnkXDMixC3cTuHQm2nzOL9mRNrYDCVyM0Avb0mzpJPLa6zJpPM6vY7Gc3xZoZvudksh9toYVocDWuMvSxxdYLflVBHTagOWobiSJ5YVNQHOCnkDSLcN3JjMtd9xqCte1zmteFdTqUmrNS1RN1ZBrsNRqV7EF8zZxodlC-Uitsk9dfVAbqOpqkK0Ll_MQunSPRjazOONYo6kcOnaongXKXPMxrw8R9FyLGoMRT78FE3NgslCtugKx6PZQWba2sr__TP6wXqZ_S4mPG1B4e3fCxm--r_5t0g6B5LiEK29b6huDdhCaoGjCHInYZys9eIhZQU47k1Y2JHFiWSih1_Xb1UXp1rZ6bFd275aHWBPz9OJM7QwKVq9kaSTiPdFmWE8NLbflEGuYUROia2dylGwGwPL-yVEhHJ-T9Qh5OWlLh3EWr2lsm3o7IenFW4baP6S9mCdfHgpulCdDe9f5s7m99S4A6V998B-RsCzblyASelD6LgAd8IMjNr5I-KxbQfOnUNKnd862HAIACn__3BdsuX8ztTwkpwXm2FaOafY8VP4WgLp1VK4f0SKIvrBLrI8DGRY6XtbLtaAhGoZc2izYxJfaB4DsmlO1cstTYZP3EYymvNA9C-Hmi8sGc6Z0v7VgJ85K9VkwVkWU4r93ksjvXkky1KheHP7giM8RX4krGrIcGRh1L1voSkYn8kPSxzuEHFU5WYugSy5-Liu8J-wa75dDYvmgzYQtx3G00)
