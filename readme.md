# AI Agents 101: Build Your First Agent with Google ADK

A beginner-friendly workshop exploring how AI agents answer questions, use tools, search the web, and perform useful actions.

Developed for **GDG Cloud Port Harcourt**, **GDG Pretoria**, and **GDG Kisii**.

**Facilitator:** Dr Philip Obiorah — Google Developer Expert, Cloud AI

## What you will learn

- Define an agent using Google’s Agent Development Kit.
- Guide agent behaviour through instructions.
- Register Python functions as tools.
- Use Google Search for current information.
- Call a specialist agent through `AgentTool`.
- Parse expense details and save validated records to CSV.
- Inspect tool calls, handle errors, and verify results.
- Distinguish conversation context from persistent storage.

## Workshop progression

| Stage | Folder | What it demonstrates |
|---|---|---|
| 1 | `my_first_agent` | A general-purpose assistant without tools |
| 2 | `general_assistant_agent` | A custom function that retrieves the current time |
| 3 | `general_assistant_search_agent` | A search specialist called through `AgentTool` |
| 4 | `learning_assistant` | A computing tutor with teaching instructions and search |
| 5 | `expense_agent` | A custom tool that validates and records expenses |

Each folder is a separate checkpoint. Later examples introduce new concepts without replacing the earlier projects.

## Requirements

- Python 3.10 or later
- A terminal and code editor, such as VS Code
- Internet access
- A Gemini API key
- Access to a Gemini model compatible with the tools used

For the guided notebook, use Jupyter or the Jupyter extension in VS Code.

Model and Google Search access depend on your account, selected model, quota, and billing configuration.

## Installation

### 1. Download the project

Clone this repository using its GitHub clone URL, then open the repository folder in your terminal.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Use `python3` if your system does not recognise `python`.

Activate the environment.

**macOS/Linux:**

```bash
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install google-adk python-dotenv tzdata
```

Alternatively, if the repository includes `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

### 4. Configure your API key

Create a Gemini API key through [Google AI Studio](https://aistudio.google.com/apikey).

Create a `.env` file inside each agent folder you intend to run:

```dotenv
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
AGENT_MODEL=gemini-flash-latest
USER_TIMEZONE=Africa/Lagos
```

If an `.env.example` is provided, copy it to `.env` and replace the placeholders.

Use a model you have verified is available to your project. Some original checkpoints specify the model directly in `agent.py`; update those definitions if necessary. The notebook-generated versions use `AGENT_MODEL`.

Examples of user timezones:

- `Africa/Lagos`
- `Africa/Johannesburg`
- `Africa/Nairobi`
- `Europe/London`

Keep `.env` files private and exclude them from version control.

## Running the agents

From the directory containing the agent folders, run:

```bash
adk web --port 8000
```

Open:

```text
http://localhost:8000
```

Select the agent package you want to try.

Restart the server after changing the code and begin a new session when switching checkpoints.

ADK Web is intended for development and debugging.

You can also run a checkpoint in the terminal:

```bash
adk run my_first_agent
```

## Checkpoint 1: General-purpose assistant

**Folder:** `my_first_agent`

This agent introduces the core configuration:

- Model
- Name
- Description
- Instruction
- `root_agent`

It has no tools for retrieving current information or writing files.

### Try it

```text
Explain an AI agent using an everyday example.
```

```text
Write a Python function that adds two numbers.
```

```text
What time is it in Port Harcourt right now?
```

For the final question, discuss whether the answer is supported by a clock lookup. A fluent response is not proof of current information.

## Checkpoint 2: Current-time tool

**Folder:** `general_assistant_agent`

This checkpoint adds:

```python
get_current_time(timezone)
```

The model selects an IANA timezone, and Python retrieves the current date and time using `datetime` and `ZoneInfo`.

### Try it

```text
What time is it in Port Harcourt?
```

```text
What time is it in Pretoria and Kisii?
```

Inspect the tool arguments and returned results.

This demonstrates the difference between generating an answer and executing a function.

## Checkpoint 3: Search specialist

**Folder:** `general_assistant_search_agent`

This checkpoint contains:

- A current-time function.
- A specialist agent with Google Search.
- A root agent that calls the specialist through `AgentTool`.

The root can answer directly, retrieve the time, or delegate a search request.

### Try it

```text
Find the official Google ADK Python quickstart and include its source.
```

```text
What time is it in Nairobi?
```

```text
Explain what a Python function is.
```

Compare which capabilities are used for each request.

Inspect available grounding information and verify that sources support the answer. Search attribution may appear differently when returned through a specialist.

## Checkpoint 4: Learning assistant

**Folder:** `learning_assistant`

This agent uses instructions to act as a patient computing tutor.

It should:

- Establish the learner’s level when a request is broad.
- Explain manageable concepts.
- Use examples and exercises.
- Check understanding.
- Search for relevant external resources.

This checkpoint uses Google Search directly. It does not retain the time tool or specialist wrapper.

### Try it

```text
Teach me Python. I am a beginner and want to analyse data.
```

```text
Give me a small exercise.
```

```text
Find an official resource where I can practise this.
```

Changing the instructions customises behaviour; it does not retrain the model.

## Checkpoint 5: Personal expense recorder

**Folder:** `expense_agent`

The expense agent turns a natural-language receipt into structured arguments for:

```python
log_expense(
    location,
    total,
    description,
    expense_date,
    expense_type,
    attendees="",
    currency="GBP",
)
```

The model extracts the fields. Python validates them and appends a CSV row.

### Recorded fields

| Column | Description |
|---|---|
| `id` | Generated record identifier |
| `location` | Merchant or location |
| `total` | Positive amount with at most two decimal places |
| `currency` | GBP in the current implementation |
| `description` | Expense description |
| `date` | Date stored as `YYYY-MM-DD` |
| `attendees` | Optional attendee details |
| `type` | Expense type supplied by the user |

### Try a complete receipt

```text
Please record this practice expense:

Location: GPU canteen
Total: 1.80
Currency: GBP
Description: lunch_item_at_GPU canteen_
Date: 21-May-2026
Attendees:
Type: LUNCH (Lunch)
```

Inspect the tool result and the CSV file to verify the saved record.

The original expense checkpoint writes to `expense_details.csv`. The guided notebook version uses `practice_expense_details.csv` to keep practice records separate.

### Try an incomplete request

```text
Record my lunch at GPU canteen.
```

The agent should ask for missing details rather than inventing them.

### Validation

The tool checks:

- Valid dates.
- Positive, finite amounts.
- No more than two decimal places.
- GBP currency.
- Required location, description, and expense type.
- Compatible CSV headers before appending.

Attendees may be blank.

When currency is absent, the configured GBP default should be disclosed.

### Current limitations

This checkpoint records expenses only. It does not implement:

- Spending summaries.
- Currency conversion.
- Editing or deleting expenses.
- Duplicate detection.
- Concurrent multi-user writes.
- Atomic multi-expense transactions.
- Receipt-image processing.

Repeating a successful recording request may create another row.

The CSV persists across conversations, but the agent has no reader tool to retrieve its contents.

## Guided student notebook

If included, open:

```text
AI_Agents_101_Guided_Student_Notebook.ipynb
```

Use a local Jupyter environment or VS Code notebook.

The notebook includes:

- Setup instructions.
- Annotated checkpoint code.
- Prediction questions.
- Live test prompts.
- Exercises.
- Isolated expense-validation tests.
- An optional session-state extension.

Run the cells in order. Start ADK Web in a separate terminal rather than a blocking notebook cell.

## Testing your agents

Inspect more than the final response:

1. Was the appropriate tool selected?
2. Were its arguments correct?
3. Did the operation succeed?
4. Does the response match the tool result?
5. Did the expected file change occur?

For the expense tool, test invalid dates, zero amounts, extra decimal places, unsupported currencies, and blank required fields.

Direct function tests verify Python behaviour. They do not prove that the model always extracts the correct information or chooses the correct tool.

## Context, state, and storage

| Concept | Meaning in this workshop |
|---|---|
| Conversation context | Messages and tool results available during the interaction |
| Session state | Structured session data; offered as an optional extension |
| Persistent storage | Expense records saved in CSV |

The expense instruction provider receives `ReadonlyContext`, but the supplied implementation does not explicitly write session state.

## Troubleshooting

| Problem | What to check |
|---|---|
| `adk` command unavailable | Activate the virtual environment and verify installation |
| Agent missing from the selector | Run from the parent folder and check `__init__.py` |
| Authentication failure | Check the API key and backend configuration |
| Model unavailable | Select a model accessible to your project |
| Search fails | Check model support, account access, quota, and returned errors |
| Incorrect time | Inspect the timezone argument |
| Expense save fails | Inspect the tool result, file permissions, and CSV header |
| Old behaviour appears | Restart ADK Web and begin a new session |

## Privacy and credentials

- Never commit API keys or `.env` files.
- Exclude personal expense CSVs from version control.
- Use non-sensitive practice receipts.
- Clear sensitive notebook outputs before sharing.
- Remember that prompts and receipt text are processed by the model.
- Revoke and replace any API key accidentally published.

## Possible extensions

After completing the core workshop:

- Add a Python-calculated spending summary.
- Filter expenses by date or type.
- Store the last recorded expense in session state.
- Add duplicate protection.
- Replace CSV storage with SQLite.
- Add currency conversion while preserving original amounts and rate metadata.

These are extension ideas, not features of the current expense checkpoint.

## Resources

- [Google ADK documentation](https://adk.dev/)
- [ADK Python quickstart](https://adk.dev/get-started/python/)
- [Function tools](https://adk.dev/tools-custom/function-tools/)
- [Google Search grounding](https://adk.dev/grounding/google_search_grounding/)
- [Session state](https://adk.dev/sessions/state/)
- [Google AI Studio](https://aistudio.google.com/)
- [Python downloads](https://www.python.org/downloads/)
- [VS Code downloads](https://code.visualstudio.com/download/)