# How to Use Codex with VS Code and LLM Foundry

These are instructions to set up

- [Codex](https://openai.com/codex/)
- on [Visual Studio Code (VS Code)](https://code.visualstudio.com/) using
- in Windows 11
- using [LLM Foundry](https://llmfoundry.straive.com/), Straive's API router.

You don't need admin access or OpenAI API keys.

## 1. Install VS Code

Download [Visual Studio Code](https://code.visualstudio.com/) and install it.

[![How Install Visual Studio Code on Windows 11 (VS Code) - 6 min](https://i.ytimg.com/vi_webp/cu_ykIfBprI/sddefault.webp)](https://youtu.be/cu_ykIfBprI)

Then open any folder in VS Code.

![](vscode-open-folder.webp)

## 2. Install Codex

Select the Extensions icon in the sidebar. Search for "Codex" in the search bar and install the one by OpenAI.

![](vscode-extensions.webp)

**CAREFUL**! There are multiple Codex extensions. You want the [Codex - OpenAI's coding agent](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt).

[![How to Use OpenAI Codex in VSCode: Step-by-Step Beginner’s Guide (2025) - 1 min](https://i.ytimg.com/vi_webp/qAU-8kM5H2s/sddefault.webp)](https://youtu.be/qAU-8kM5H2s)

## 3. Log in with a dummy API key

Click on the Codex icon in the sidebar.

![](codex-sidebar.webp)

This should show 2 buttons:

![A "Sign in with ChatGPT" and a "Use API Key" button](codex-api-key.webp)

Click on **Use API Key** and type "ABCD" (or any other random string) in the API key field and click "OK". We will change this later.

![](codex-api-key-2.webp)

Press "Continue" when prompted.

![](codex-continue.webp)

## 4. Configure LLM Foundry

Click on the gear-like settings icon to the right of the Codex pane, then **Codex settings**, then **Open config.toml**.

![](codex-toml.webp)

Paste the following into the `config.toml` file and save it.

```ini
#
profile = "llmfoundry_azure"
# Alternate profiles:
# profile = "llmfoundry_gemini"
# profile = "llmfoundry_openai"
# profile = "llmfoundry_openrouter"

[profiles.llmfoundry_azure]
model_provider = "llmfoundry_azure"

[model_providers.llmfoundry_azure]
name = "LLM Foundry - Azure"
base_url = "https://llmfoundry.straive.com/azure/openai/deployments/gpt-5"
env_key = "LLMFOUNDRY_TOKEN"
wire_api = "chat"
query_params = { api-version = "2025-04-01-preview" }

[profiles.llmfoundry_gemini]
model_provider = "llmfoundry_gemini"
model = "gemini-2.5-flash"

[model_providers.llmfoundry_gemini]
name = "LLM Foundry - Gemini"
base_url = "https://llmfoundry.straive.com/gemini/v1beta/openai"
env_key = "LLMFOUNDRY_TOKEN"
wire_api = "chat"

[profiles.llmfoundry_openai]
model_provider = "llmfoundry_openai"

[model_providers.llmfoundry_openai]
name = "LLM Foundry - OpenAI"
base_url = "https://llmfoundry.straivedemo.com/openai/v1"
env_key = "LLMFOUNDRY_TOKEN"
wire_api = "responses"

[profiles.llmfoundry_openrouter]
model_provider = "llmfoundry_openrouter"
model = "openai/gpt-5-codex"

[model_providers.llmfoundry_openrouter]
name = "LLM Foundry - Gemini"
base_url = "https://llmfoundry.straive.com/openrouter/v1"
env_key = "LLMFOUNDRY_TOKEN"
wire_api = "chat"
```

Any changes to `config.toml` require a restart of VS Code.

## 5. Set your LLM Foundry API key

Visit [LLM Foundry](https://llmfoundry.straive.com/) and log in with your official Google account.

Then click on the "Code" tab.

![](llmfoundry-code.webp)

Copy the LLM Foundry token.

![](llmfoundry-token.webp)

Search for "Edit environment variables for your account" in the Windows search bar.

![](env-vars-search.webp)

Select "New" from the "User variables" section.

![](env-vars-list.webp)

Set the variable name to:

`LLMFOUNDRY_TOKEN`

**CAREFULLY**! Copy paste it. Or, if typing:

- Use **upper case** (it's `LLMFOUNDRY` not `llmfoundry`).
- Spell it **correctly** (it's `LLMFOUNDRY` not `LLMFOUNDARY`).
- Don't forget the underscore (it's `LLMFOUNDRY_TOKEN` not `LLMFOUNDRY TOKEN`).

Set the variable value to the token you copied from [LLM Foundry > Code](https://llmfoundry.straive.com/code).

[![How to Set Environment Variables in Windows 11 - 1 min](https://i.ytimg.com/vi_webp/wbUdbhf7HbI/sddefault.webp)](https://youtu.be/wbUdbhf7HbI)

## 6. Restart VS Code

Close VS Code.

Then re-open it.

## 7. Verify Codex is working with LLM Foundry

Click on the Codex icon in the sidebar.

![](codex-sidebar.webp)

Type "Hi" (or anything else) in the prompt box and press Enter.

![](codex-hi.webp)

lf goes well, you should see a response from Codex.

![](codex-success.webp)

## 8. Troubleshooting

If you see an error like this:

![](codex-stream-error.webp)

Try the following:

1. Check if [LLM Foundry is up](https://llmfoundry.site24x7statusiq.com/). If not, try later.
2. Check if your `LLMFOUNDRY_TOKEN` environment variable is correct. Re-add it and restart VS Code.

## 8. Try simple examples

You can now use Codex in VS Code with LLM Foundry. Here are a few simple things to try.

1. Copy **text** documents into the folder and prompt Codex to "Summarize these documents".
2. Copy **code** files into the folder and prompt Codex to "Explain this code".
3. Copy **Excel** files into the folder and prompt Codex to "Write code to analyze this data".

## 9. Install Python

Open the Windows search bar and search for "Python". Install any of the Python versions from the Microsoft Store. This will allow Codex to run Python code locally.

[![How to Install and Setup Python 3 13 on Windows 11 via the Microsoft Store - 3 min](https://i.ytimg.com/vi_webp/aX4KV5i-cd4/sddefault.webp)](https://youtu.be/aX4KV5i-cd4)

## 10. Usage tips

To avoid Codex asking for too many approvals, use the "Agent (full access)" mode.

![](codex-agent-full-access.webp)
