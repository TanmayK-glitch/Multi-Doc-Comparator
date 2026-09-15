# Function Calling with the Gemini API

Function calling lets you connect Gemini models to external tools and APIs. Instead of generating text responses, the model determines when to call specific functions and provides the necessary parameters to execute real-world actions.

This allows the model to act as a bridge between natural language and real-world actions and data.

## Primary Use Cases

Function calling has three primary use cases:

### 1. Take Actions

Interact with external systems using APIs, such as:

* Scheduling appointments
* Creating invoices
* Sending emails
* Controlling smart home devices

### 2. Augment Knowledge

Access information from external sources such as:

* Databases
* APIs
* Knowledge bases

### 3. Extend Capabilities

Use external tools to perform computations and extend the limitations of the model, such as:

* Using a calculator
* Creating charts

---

# Examples

## Schedule Meeting

This example defines a function that schedules a meeting with attendees at a specific time, allowing the model to parse user requests and return structured arguments to trigger actions in external systems.

```python
from google import genai

schedule_meeting_function = {
    "type": "function",
    "name": "schedule_meeting",
    "description": "Schedules a meeting with specified attendees at a given time and date.",
    "parameters": {
        "type": "object",
        "properties": {
            "attendees": {"type": "array", "items": {"type": "string"}},
            "date": {"type": "string", "description": "Date (e.g., '2024-07-29')"},
            "time": {"type": "string", "description": "Time (e.g., '15:00')"},
            "topic": {"type": "string", "description": "The meeting topic."},
        },
        "required": ["attendees", "date", "time", "topic"],
    },
}

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Schedule a meeting with Bob and Alice for 03/14/2025 at 10:00 AM about Q3 planning.",
    tools=[{"type": "function", **schedule_meeting_function}],
)

for step in interaction.steps:
    if step.type == "function_call":
        print(f"Function to call: {step.name}")
        print(f"Arguments: {step.arguments}")
```

---

## Get Weather

This example defines a function that retrieves temperature data for a location, enabling the model to call external APIs to answer queries requiring real-time or external information.

```python
from google import genai

weather_function = {
    "type": "function",
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. San Francisco",
            },
        },
        "required": ["location"],
    },
}

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="What's the temperature in London?",
    tools=[weather_function],
)

for step in interaction.steps:
    if step.type == "function_call":
        print(f"Function to call: {step.name}")
        print(f"Arguments: {step.arguments}")
```

---

## Create Chart

This example defines a function that generates a bar chart from structured data, demonstrating how the model can use external tools to perform computations or create visual assets.

```python
from google import genai

create_chart_function = {
    "type": "function",
    "name": "create_bar_chart",
    "description": "Creates a bar chart given a title, labels, and values.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "The title for the chart."},
            "labels": {"type": "array", "items": {"type": "string"}},
            "values": {"type": "array", "items": {"type": "number"}},
        },
        "required": ["title", "labels", "values"],
    },
}

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Create a bar chart titled 'Quarterly Sales' with Q1: 50000, Q2: 75000, Q3: 60000.",
    tools=[create_chart_function],
)

for step in interaction.steps:
    if step.type == "function_call":
        print(f"Function to call: {step.name}")
        print(f"Arguments: {step.arguments}")
```

---

# How Function Calling Works

Function calling involves a structured interaction between your application, the model, and external functions.

## Function Calling Flow

1. **Define Function Declaration**

   * Define the function's name, parameters, and purpose to the model.

2. **Call LLM with Function Declarations**

   * Send the user's prompt along with the function declaration(s) to the model.

3. **Execute Function Code**

   * The model does **not** execute the function itself.
   * Extract the function name and arguments.
   * Execute the function in your application.

4. **Create User-Friendly Response**

   * Send the function result back to the model.
   * The model generates a final user-friendly response.

This process can be repeated over multiple turns.

Gemini supports:

* Multiple functions in a single turn (**parallel function calling**)
* Functions called sequentially (**compositional function calling**)

---

# Step 1: Define a Function Declaration

A function declaration tells the model what function is available, what it does, and what parameters it accepts.

```python
set_light_values_declaration = {
    "type": "function",
    "name": "set_light_values",
    "description": "Sets the brightness and color temperature of a light.",
    "parameters": {
        "type": "object",
        "properties": {
            "brightness": {
                "type": "integer",
                "description": "Light level from 0 to 100",
            },
            "color_temp": {
                "type": "string",
                "enum": ["daylight", "cool", "warm"],
                "description": "Color temperature",
            },
        },
        "required": ["brightness", "color_temp"],
    },
}


def set_light_values(brightness: int, color_temp: str) -> dict:
    """Set the brightness and color temperature of a room light."""
    return {"brightness": brightness, "colorTemperature": color_temp}
```

---

# Step 2: Call the Model with Function Declarations

```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Turn the lights down to a romantic level",
    tools=[set_light_values_declaration],
)

fc_step = next(s for s in interaction.steps if s.type == "function_call")
print(fc_step)
```

The model returns a **`function_call`** step with:

* `type`
* `name`
* `arguments`

Example:

```text
type='function_call'
name='set_light_values'
arguments={'color_temp': 'warm', 'brightness': 25}
```

The important point is that the model is returning a **request to call the function**, not executing the function itself.

---

# Step 3: Execute the Function

The application is responsible for executing the function.

```python
fc_step = next(s for s in interaction.steps if s.type == "function_call")

if fc_step.name == "set_light_values":
    result = set_light_values(**fc_step.arguments)
    print(f"Function execution result: {result}")
```

The application receives the function name and arguments from the model, validates them, and executes the corresponding function.

---

# Step 4: Send the Result Back to the Model

After executing the function, send its result back to Gemini.

```python
final_interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input=[
        {
            "type": "function_result",
            "name": fc_step.name,
            "call_id": fc_step.id,
            "result": [{"type": "text", "text": json.dumps(result)}],
        }
    ],
    tools=[set_light_values_declaration],
    previous_interaction_id=interaction.id,
)

print(final_interaction.output_text)
```

The model can then use the function result to generate the final response to the user.

---

# Stateless Function Calling

Function calling can also be used in stateless mode by managing the conversation history on the client side and setting:

```python
store=False
```

In stateless mode, the full conversation history must be passed in the `input` field of every subsequent request.

The history must include:

1. The initial `user_input` step.
2. All model-generated steps returned in Turn 1, including:

   * `thought`
   * `function_call`
3. The `function_result` step containing the output of the executed function.

## Example

```python
from google import genai
import json

client = genai.Client()

history = [
    {
        "type": "user_input",
        "content": [
            {
                "type": "text",
                "text": "Turn the lights down to a romantic level",
            }
        ],
    }
]

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    store=False,
    input=history,
    tools=[set_light_values_declaration],
)

for step in interaction.steps:
    history.append(step.model_dump())

fc_step = next(s for s in interaction.steps if s.type == "function_call")

if fc_step.name == "set_light_values":
    result = set_light_values(**fc_step.arguments)

history.append({
    "type": "function_result",
    "name": fc_step.name,
    "call_id": fc_step.id,
    "result": [{"type": "text", "text": json.dumps(result)}],
})

final_interaction = client.interactions.create(
    model="gemini-3.8-flash",
    store=False,
    input=history,
    tools=[set_light_values_declaration],
)

print(final_interaction.output_text)
```

---

# Function Declarations

A function declaration is passed as a tool and includes the following fields:

| Field         | Type   | Description                                         |
| ------------- | ------ | --------------------------------------------------- |
| `type`        | string | Must be `"function"` for custom functions.          |
| `name`        | string | Unique function name. Use underscores or camelCase. |
| `description` | string | Clear explanation of the function's purpose.        |
| `parameters`  | object | Input parameters the function expects.              |

## Parameters Object

The `parameters` object contains:

| Field        | Type   | Description                                            |
| ------------ | ------ | ------------------------------------------------------ |
| `type`       | string | Overall data type, such as `"object"`.                 |
| `properties` | object | Individual parameters with their type and description. |
| `required`   | array  | Names of mandatory parameters.                         |

---

# Function Calling with Thinking Models

Gemini 3 series models use an internal **thinking** process that improves function calling.

The Gemini SDKs automatically handle **thought signatures**.

Relevant concepts:

* Thinking
* Thought signatures
* Function calling
* Multi-step reasoning

---

# Parallel Function Calling

Parallel function calling allows Gemini to call multiple independent functions at once.

Use parallel function calling when the requested functions do not depend on one another.

For example, a user could ask to turn a location into a party, requiring:

* Powering a disco ball
* Starting music
* Dimming the lights

These operations can be requested together.

```python
power_disco_ball = {
    "type": "function",
    "name": "power_disco_ball",
    "description": "Powers the disco ball.",
    "parameters": {
        "type": "object",
        "properties": {
            "power": {"type": "boolean"}
        },
        "required": ["power"]
    }
}

start_music = {
    "type": "function",
    "name": "start_music",
    "description": "Play music.",
    "parameters": {
        "type": "object",
        "properties": {
            "energetic": {"type": "boolean"},
            "loud": {"type": "boolean"}
        },
        "required": ["energetic", "loud"]
    }
}

dim_lights = {
    "type": "function",
    "name": "dim_lights",
    "description": "Dim the lights.",
    "parameters": {
        "type": "object",
        "properties": {
            "brightness": {"type": "number"}
        },
        "required": ["brightness"]
    }
}

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Turn this place into a party!",
    tools=[power_disco_ball, start_music, dim_lights],
    generation_config={"tool_choice": "any"},
)

for step in interaction.steps:
    if step.type == "function_call":
        args = ", ".join(
            f"{key}={val}" for key, val in step.arguments.items()
        )
        print(f"{step.name}({args})")
```

---

# Compositional Function Calling

Compositional function calling chains multiple function calls together for complex requests.

One function call can provide information required by a later function call.

### Example

1. Get the user's location or another relevant location.
2. Get weather information for that location.
3. Use the weather result to decide whether to call another function.
4. Execute the resulting function.

Example:

```python
get_weather_forecast_declaration = {
    "type": "function",
    "name": "get_weather_forecast",
    "description": "Gets the current weather temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The location"
            },
        },
        "required": ["location"],
    },
}

set_thermostat_temperature_declaration = {
    "type": "function",
    "name": "set_thermostat_temperature",
    "description": "Sets the thermostat to a desired temperature.",
    "parameters": {
        "type": "object",
        "properties": {
            "temperature": {
                "type": "integer",
                "description": "The temperature in Celsius",
            },
        },
        "required": ["temperature"],
    },
}

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="If it's warmer than 20°C in London, set the thermostat to 20°C, otherwise 18°C.",
    tools=[
        get_weather_forecast_declaration,
        set_thermostat_temperature_declaration,
    ],
)

for step in interaction.steps:
    if step.type == "function_call":
        print(f"Function to call: {step.name}")
        print(f"Arguments: {step.arguments}")
    elif hasattr(step, "content") and step.content:
        for part in step.content:
            if hasattr(part, "text"):
                print(part.text)
```

---

# Function Calling Modes

The way Gemini uses tools can be controlled using **`tool_choice`** in **`generation_config`**.

## `auto`

Default mode.

The model decides whether to:

* Call a function
* Respond directly

## `any`

The model is constrained to always predict a function call.

## `none`

The model is prohibited from making function calls.

## `validated`

The model ensures function schema adherence.

### Example

```python
generation_config = {
    "tool_choice": {
        "allowed_tools": {
            "mode": "any",
            "tools": ["get_current_temperature"]
        }
    }
}
```

---

# Multi-Tool Use

Multiple tools can be enabled in the same request.

Gemini 3 models can combine built-in tools with custom function calling out-of-the-box in the Interactions API.

Passing **`previous_interaction_id`** automatically circulates the built-in tool context.

## Example

```python
from google import genai
import json

client = genai.Client()

get_weather = {
    "type": "function",
    "name": "get_weather",
    "description": "Gets the weather for a requested city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city and state, e.g. Utqiaġvik, Alaska",
            },
        },
        "required": ["city"],
    },
}

tools = [
    {"type": "google_search"},
    get_weather
]

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="What is the northernmost city in the United States? What's the weather like there today?",
    tools=tools
)

for step in interaction.steps:
    if step.type == "function_call":
        print(f"Function call: {step.name} (ID: {step.id})")

        result = {
            "response": "Very cold. 22 degrees Fahrenheit."
        }

        interaction_2 = client.interactions.create(
            model="gemini-3.8-flash",
            previous_interaction_id=interaction.id,
            tools=tools,
            input=[{
                "type": "function_result",
                "name": step.name,
                "call_id": step.id,
                "result": [
                    {
                        "type": "text",
                        "text": json.dumps(result)
                    }
                ]
            }]
        )

        print(interaction_2.output_text)
```

---

# Multimodal Function Responses

For Gemini 3 series models, multimodal content can be included in function response parts sent back to the model.

The model can process this multimodal content in its next turn to produce a more informed response.

To include multimodal data in a function response:

* Put one or more content blocks in the `result` field of the `function_result` step.
* Each content block must specify its `type`.

Examples of content types include:

* `"text"`
* `"image"`

## Example

```python
import base64
from google import genai
import requests

client = genai.Client()

tool_call = next(
    s for s in interaction.steps
    if s.type == "function_call"
)

image_path = "https://goo.gle/instrument-img"
image_bytes = requests.get(image_path).content

base64_image_data = base64.b64encode(image_bytes).decode("utf-8")

final_interaction = client.interactions.create(
    model="gemini-3.8-flash",
    previous_interaction_id=interaction.id,
    input=[
        {
            "type": "function_result",
            "name": tool_call.name,
            "call_id": tool_call.id,
            "result": [
                {
                    "type": "text",
                    "text": "instrument.jpg"
                },
                {
                    "type": "image",
                    "mime_type": "image/jpeg",
                    "data": base64_image_data,
                },
            ],
        }
    ],
)

print(final_interaction.output_text)
```

---

# Function Calling with Structured Output

For Gemini 3 series models, function calling can be combined with **structured output** for consistently formatted responses.

---

# Remote MCP (Model Context Protocol)

The Interactions API supports connecting to remote MCP servers to give the model access to external tools and services.

The server's:

* `name`
* `url`

are provided in the tools configuration.

## Remote MCP Constraints

### Server Types

Remote MCP only works with **Streamable HTTP** servers.

**SSE (Server-Sent Events) servers are not supported.**

### Naming

MCP server names should not contain the `-` character.

Use `snake_case` server names instead.

## MCP Server Configuration

| Field           | Type   | Required | Description                                                                                           |
| --------------- | ------ | -------- | ----------------------------------------------------------------------------------------------------- |
| `type`          | string | Yes      | Must be `"mcp_server"`.                                                                               |
| `name`          | string | No       | A display name for the MCP server.                                                                    |
| `url`           | string | No       | The full URL for the MCP server endpoint.                                                             |
| `headers`       | object | No       | Key-value pairs sent as HTTP headers with every request to the server, such as authentication tokens. |
| `allowed_tools` | array  | No       | Restricts which tools from the server the agent may call.                                             |

## Remote MCP Example

```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="Check the weather in San Francisco.",
    tools=[
        {
            "type": "mcp_server",
            "name": "weather",
            "url": "https://gemini-api-demos.uc.r.appspot.com/mcp",
        }
    ]
)
```

---

# Stream Tool Calls

When using tools with streaming, the model generates function calls as a sequence of **`step.delta`** events on the stream.

Tool arguments can be streamed as partial arguments using **`arguments`**.

The application must aggregate these deltas to reconstruct the complete tool calls before executing them.

## Example

```python
import json
from google import genai

client = genai.Client()

weather_tool = {
    "type": "function",
    "name": "get_weather",
    "description": "Gets the weather for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state"
            }
        },
        "required": ["location"]
    }
}

stream = client.interactions.create(
    model="gemini-3.8-flash",
    input="What is the weather in Paris?",
    tools=[weather_tool],
    stream=True
)

current_calls = {}
tool_calls = []

for event in stream:
    if event.event_type == "step.start":
        if event.step.type == "function_call":
            current_calls[event.index] = {
                "id": event.step.id,
                "name": event.step.name,
                "arguments": ""
            }

            if hasattr(event.step, "arguments") and event.step.arguments:
                if isinstance(event.step.arguments, dict):
                    current_calls[event.index]["arguments"] = json.dumps(
                        event.step.arguments
                    )
                else:
                    current_calls[event.index]["arguments"] = event.step.arguments

    elif event.event_type == "step.delta":
        if event.delta.type == "arguments":
            if event.index in current_calls:
                current_calls[event.index]["arguments"] += (
                    event.delta.partial_arguments
                )

        elif event.delta.type == "text":
            print(event.delta.text, end="", flush=True)

    elif event.event_type == "interaction.completed":
        for index, call in current_calls.items():
            args = call["arguments"]

            if args:
                args = json.loads(args)
            else:
                args = {}

            tool_calls.append({
                "type": "function_call",
                "id": call["id"],
                "name": call["name"],
                "arguments": args
            })

        print("\nFinal tool calls ready to execute:")
        print(json.dumps(tool_calls, indent=2))
```

---

# Best Practices

## Function and Parameter Descriptions

Be clear and specific when describing functions and their parameters.

## Naming

Use descriptive function names without spaces or special characters.

## Strong Typing

Use specific parameter types such as:

* `integer`
* `string`
* `enum`

## Tool Selection

Keep the active tool set to approximately **10–20 tools maximum**.

## Prompt Engineering

Provide sufficient context and instructions to the model.

## Validation

Validate function calls before executing them.

## Error Handling

Implement robust error handling for tool execution.

## Security

Use appropriate authentication for external APIs.

---

# Workarounds for Pre-Tool Text Requirements

## Issue

If the prompt requires the model to output structured text such as XML, YAML, JSON, or another structured format immediately before making a tool call, the tool call may occasionally fail with:

```text
Malformed_Function_Call
```

For example, a prompt might require:

```text
<UPDATE>...</UPDATE>
```

before every tool call.

## Solutions

The documented workarounds are:

1. **Preferred:** Instruct the model to put its pre-tool notes inside a dedicated `update()` function call instead of raw text.
2. Instruct the model to write notes as Markdown headers such as:

   * `# UPDATE`
   * `## PLAN`
3. Do not require the model to output text before tool calls.

---

# Preferred Workaround: Wrap Working Notes in a Dedicated Function Call

Instead of the original instruction:

```text
Before calling a tool, in every response you MUST first output a single <UPDATE> part as specified, don't skip this part or any of required sub-tags within <UPDATE>.
```

Use:

```text
Before calling any other tool, in every response you MUST first call update with all required parameters (previous_step, plan, next_step, external).
```

Update all references to the old `<UPDATE>` XML format in the customer request.

Then add the corresponding function declaration for the `update` function:

```json
{
  "name": "update",
  "description": "Update working notes (previous step analysis, plan, next step, external note).",
  "parameters": {
    "type": "OBJECT",
    "properties": {
      "previous_step": {
        "type": "STRING",
        "description": "Key findings and outcomes since the previous step."
      },
      "plan": {
        "type": "STRING",
        "description": "The current status of the plan."
      },
      "next_step": {
        "type": "STRING",
        "description": "Brief explanation of the immediate next action according to the plan."
      },
      "external": {
        "type": "STRING",
        "description": "A short, plain-language note shown to the User about what you are ABOUT TO DO next."
      }
    },
    "required": [
      "previous_step",
      "plan",
      "next_step",
      "external"
    ]
  }
}
```

The model will then make two calls in the same step:

1. The **`update()`** call that replaces the structured XML.
2. The actual function call it wants to make.

---

# Notes and Limitations

* Only a **subset of the OpenAPI schema** is supported.
* For **`any`** mode, the API may reject very large or deeply nested schemas.
* Supported parameter types in Python are limited.

---

# Key Concepts

For Gemini function calling, the core concepts are:

* **Function declaration** — Defines the function available to the model.
* **Tool** — The function declaration is passed to Gemini as a tool.
* **Function call** — The model requests that a specific function be executed with specific arguments.
* **Function execution** — Your application executes the requested function.
* **Function result** — Your application sends the execution result back to Gemini.
* **Parallel function calling** — Multiple independent functions can be requested in the same turn.
* **Compositional function calling** — Multiple function calls can be chained sequentially.
* **Tool choice** — Controls whether and how the model can use tools.
* **Multi-tool use** — Combines multiple tools, including built-in tools and custom functions.
* **Multimodal function response** — Function results can contain multimodal content such as images.
* **Remote MCP** — Connects Gemini to external tools through remote MCP servers.
* **Streaming tool calls** — Function calls and their arguments can be received incrementally through streaming events.
