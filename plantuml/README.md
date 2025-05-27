# How to create a PlantUML architecture diagram with ChatGPT

[PlantUML](https://plantuml.com/) supports [architecture diagrams](https://plantuml.com/archimate-diagram) suited for cloud architecture. It also includes [cloud icons](https://github.com/plantuml/plantuml-stdlib).

To guide ChatGPT (or any LLM) to create a PlantUML architecture diagram, you can start with the code or an explanation.

**STEP 1a**: Write your instructions for the architecture and copy it.

**STEP 1b**: OR, copy your code via [files-to-prompt](https://github.com/simonw/files-to-prompt):

```bash
uvx files-to-prompt --cxml README.md ... | xclip -selection clipboard
```

**STEP 2**: Copy the icons list for your cloud environment:

- [AWS](AWS.puml)
- [Azure](Azure.puml)
- [GCP](GCP.puml)

These were generated via [`bash icons.sh`](icons.sh).

**STEP 3**: Copy this prompt to ChatGPT (or any LLM):

```
Create a PlantUML component diagram for the technical architecture based on the code/instructions below.

[Your code or instructions from STEP 1]

For EVERY cloud component use the icon macro ONLY from this list:

[Your .puml from STEP 2]

Here's an example with Azure icons. Use the icon macros from the list above.

<puml>
@startuml
' Replace AzurePuml with AWSPuml, GCPPuml, ...
!define AzurePuml https://...
!includeurl AzurePuml/...
...

actor User as u

' Define nodes with just the macro name without path/prefix/namespace
AzureBlobStorage(e_blob, "Static Assets", "Static website hosting")
AzureCDN(e_cdn, "Azure CDN", "Global content distribution")
...

' Add links
u --> e_cdn : HTTP(S) requests
e_cdn --> e_blob : Retrieve static files
...
@enduml
</puml>
```

**STEP 4**: Paste the PlantUML code into [PlantUML online editor](https://editor.plantuml.com/).

Here is an example with AWS:

- [ChatGPT chat](https://chatgpt.com/share/6835db24-5c60-800c-b978-0b239f75f7c6)
- [PlantUML output](https://editor.plantuml.com/uml/ZLBDRjiy4BphAJO-10aGMy1tpE53dBW_1kpKhPBsM53asc93KGftcTHz-YvDAq6DnkXDMixC3cTuHQm2nzOL9mRNrYDCVyM0Avb0mzpJPLa6zJpPM6vY7Gc3xZoZvudksh9toYVocDWuMvSxxdYLflVBHTagOWobiSJ5YVNQHOCnkDSLcN3JjMtd9xqCte1zmteFdTqUmrNS1RN1ZBrsNRqV7EF8zZxodlC-Uitsk9dfVAbqOpqkK0Ll_MQunSPRjazOONYo6kcOnaongXKXPMxrw8R9FyLGoMRT78FE3NgslCtugKx6PZQWba2sr__TP6wXqZ_S4mPG1B4e3fCxm--r_5t0g6B5LiEK29b6huDdhCaoGjCHInYZys9eIhZQU47k1Y2JHFiWSih1_Xb1UXp1rZ6bFd275aHWBPz9OJM7QwKVq9kaSTiPdFmWE8NLbflEGuYUROia2dylGwGwPL-yVEhHJ-T9Qh5OWlLh3EWr2lsm3o7IenFW4baP6S9mCdfHgpulCdDe9f5s7m99S4A6V998B-RsCzblyASelD6LgAd8IMjNr5I-KxbQfOnUNKnd862HAIACn__3BdsuX8ztTwkpwXm2FaOafY8VP4WgLp1VK4f0SKIvrBLrI8DGRY6XtbLtaAhGoZc2izYxJfaB4DsmlO1cstTYZP3EYymvNA9C-Hmi8sGc6Z0v7VgJ85K9VkwVkWU4r93ksjvXkky1KheHP7giM8RX4krGrIcGRh1L1voSkYn8kPSxzuEHFU5WYugSy5-Liu8J-wa75dDYvmgzYQtx3G00)

Here is an example with Azure:

- [ChatGPT chat](https://chatgpt.com/share/68312df6-a134-800c-9a9c-80d39b41ffcc)
- [PlantUML output](https://editor.plantuml.com/uml/ZLBDRjiy4BphAJO-10aGMy1tpE53dBW_1kpKhPBsM53asc93KGftcTHz-YvDAq6DnkXDMixC3cTuHQm2nzOL9mRNrYDCVyM0Avb0mzpJPLa6zJpPM6vY7Gc3xZoZvudksh9toYVocDWuMvSxxdYLflVBHTagOWobiSJ5YVNQHOCnkDSLcN3JjMtd9xqCte1zmteFdTqUmrNS1RN1ZBrsNRqV7EF8zZxodlC-Uitsk9dfVAbqOpqkK0Ll_MQunSPRjazOONYo6kcOnaongXKXPMxrw8R9FyLGoMRT78FE3NgslCtugKx6PZQWba2sr__TP6wXqZ_S4mPG1B4e3fCxm--r_5t0g6B5LiEK29b6huDdhCaoGjCHInYZys9eIhZQU47k1Y2JHFiWSih1_Xb1UXp1rZ6bFd275aHWBPz9OJM7QwKVq9kaSTiPdFmWE8NLbflEGuYUROia2dylGwGwPL-yVEhHJ-T9Qh5OWlLh3EWr2lsm3o7IenFW4baP6S9mCdfHgpulCdDe9f5s7m99S4A6V998B-RsCzblyASelD6LgAd8IMjNr5I-KxbQfOnUNKnd862HAIACn__3BdsuX8ztTwkpwXm2FaOafY8VP4WgLp1VK4f0SKIvrBLrI8DGRY6XtbLtaAhGoZc2izYxJfaB4DsmlO1cstTYZP3EYymvNA9C-Hmi8sGc6Z0v7VgJ85K9VkwVkWU4r93ksjvXkky1KheHP7giM8RX4krGrIcGRh1L1voSkYn8kPSxzuEHFU5WYugSy5-Liu8J-wa75dDYvmgzYQtx3G00)
