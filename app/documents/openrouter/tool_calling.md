---

title: OpenRouter Tool Calling
topic: Tool Calling
provider: OpenRouter
api: Responses API
scope: Function calling, tool definitions, tool choice, tool responses, parallel calls, multimodal outputs, and streaming
-------------------------------------------------------------------------------------------------------------------------

# OpenRouter Tool Calling

OpenRouter's Responses API supports tool calling, allowing models to request external functions or tools during a response.

Tool calling can be used for:

* Calling application-defined functions
* Executing multiple tools
* Executing tools in parallel
* Returning tool results to the model
* Returning multimodal content such as images and files from tools
* Streaming tool calls and their arguments

OpenRouter uses an OpenAI-compatible function-calling format for defining and handling tools.

---

# Basic Tool Definition

Tools are defined using the function calling format.

A function tool contains:

| Field         | Description                                              |
| ------------- | -------------------------------------------------------- |
| `type`        | Must be `"function"`                                     |
| `name`        | Name of the function/tool                                |
| `description` | Description of what the tool does                        |
| `strict`      | Controls strict schema behavior; the examples use `null` |
| `parameters`  | JSON Schema describing the function arguments            |

Example:

```json
{
  "type": "function",
  "name": "get_weather",
  "description": "Get the current weather in a location",
  "strict": null,
  "parameters": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city and state, e.g. San Francisco, CA"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"]
      }
    },
    "required": ["location"]
  }
}
```

The tool is supplied to the Responses API through the `tools` field.

Example request:

```http
POST https://openrouter.ai/api/v1/responses
Authorization: Bearer YOUR_OPENROUTER_API_KEY
Content-Type: application/json
```

```json
{
  "model": "openai/o4-mini",
  "input": [
    {
      "type": "message",
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "What is the weather in San Francisco?"
        }
      ]
    }
  ],
  "tools": [
    {
      "type": "function",
      "name": "get_weather",
      "description": "Get the current weather in a location",
      "strict": null,
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA"
          },
          "unit": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"]
          }
        },
        "required": ["location"]
      }
    }
  ],
  "tool_choice": "auto",
  "max_output_tokens": 9000
}
```

---

# Tool Choice

The `tool_choice` parameter controls whether and how the model can call tools.

Supported options:

| `tool_choice`                               | Behavior                                 |
| ------------------------------------------- | ---------------------------------------- |
| `"auto"`                                    | The model decides whether to call a tool |
| `"none"`                                    | The model does not call tools            |
| `{"type": "function", "name": "tool_name"}` | Forces a specific function to be called  |

## Automatic Tool Selection

Use:

```json
{
  "tool_choice": "auto"
}
```

With `auto`, the model decides whether a tool is necessary based on the request and the available tool definitions.

---

## Force a Specific Tool

A specific function can be forced using:

```json
{
  "tool_choice": {
    "type": "function",
    "name": "get_weather"
  }
}
```

This instructs the model to call the specified function.

Example:

```json
{
  "model": "openai/o4-mini",
  "input": [
    {
      "type": "message",
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Hello, how are you?"
        }
      ]
    }
  ],
  "tools": [weather_tool],
  "tool_choice": {
    "type": "function",
    "name": "get_weather"
  },
  "max_output_tokens": 9000
}
```

---

## Disable Tool Calling

Use:

```json
{
  "tool_choice": "none"
}
```

to prevent the model from calling tools, even when tools are included in the request.

Example:

```json
{
  "model": "openai/o4-mini",
  "input": [
    {
      "type": "message",
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "What is the weather in Paris?"
        }
      ]
    }
  ],
  "tools": [weather_tool],
  "tool_choice": "none",
  "max_output_tokens": 9000
}
```

---

# Multiple Tools

Multiple tools can be supplied in a single request.

For example, an application could provide both:

* `get_weather`
* `calculate`

Example:

```json
{
  "tools": [
    {
      "type": "function",
      "name": "get_weather",
      "description": "Get the current weather in a location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string"
          }
        },
        "required": ["location"]
      }
    },
    {
      "type": "function",
      "name": "calculate",
      "description": "Perform mathematical calculations",
      "parameters": {
        "type": "object",
        "properties": {
          "expression": {
            "type": "string"
          }
        },
        "required": ["expression"]
      }
    }
  ],
  "tool_choice": "auto"
}
```

The model can select the appropriate tool based on the user's request.

---

# Parallel Tool Calls

The Responses API supports parallel tool calls.

For example, a user request could require both:

* A calculation
* A weather lookup

The request can provide both tools:

```json
{
  "model": "openai/o4-mini",
  "input": [
    {
      "type": "message",
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Calculate 10*5 and also tell me the weather in Miami"
        }
      ]
    }
  ],
  "tools": [
    "weather_tool",
    "calculator_tool"
  ],
  "tool_choice": "auto",
  "max_output_tokens": 9000
}
```

When appropriate, the model can request multiple independent tools as part of the same response.

Applications should design independent tools so that they can be executed in parallel when possible.

---

# Tool Call Response

When the model requests a function, the Responses API returns function-call information.

Example:

```json
{
  "id": "resp_1234567890",
  "object": "response",
  "created_at": 1234567890,
  "model": "openai/o4-mini",
  "output": [
    {
      "type": "function_call",
      "id": "fc_abc123",
      "call_id": "call_xyz789",
      "name": "get_weather",
      "arguments": "{\"location\":\"San Francisco, CA\"}"
    }
  ],
  "usage": {
    "input_tokens": 45,
    "output_tokens": 25,
    "total_tokens": 70
  },
  "status": "completed"
}
```

Important fields in a `function_call` object:

| Field       | Description                                                         |
| ----------- | ------------------------------------------------------------------- |
| `type`      | Always `"function_call"`                                            |
| `id`        | Identifier for the function-call object                             |
| `call_id`   | Identifier used to associate the tool result with the function call |
| `name`      | Name of the requested function                                      |
| `arguments` | JSON string containing the function arguments                       |

For example:

```json
{
  "type": "function_call",
  "id": "fc_abc123",
  "call_id": "call_xyz789",
  "name": "get_weather",
  "arguments": "{\"location\":\"Seattle, WA\"}"
}
```

The `arguments` value is a JSON string and should be parsed by the application before invoking the actual function.

---

# Returning Tool Results

After executing a requested function, the application sends the tool result back to the Responses API using a `function_call_output` object.

Example:

```json
{
  "type": "function_call_output",
  "call_id": "call_123",
  "output": "{\"temperature\": \"72°F\", \"condition\": \"Sunny\"}"
}
```

The important fields are:

| Field     | Description                           |
| --------- | ------------------------------------- |
| `type`    | Must be `"function_call_output"`      |
| `call_id` | Identifies the original function call |
| `output`  | Result returned by the tool           |

The `call_id` connects the tool result to the original `function_call`.

---

# `function_call_output.id`

The `id` field on a `function_call_output` object is optional.

Only these fields are required:

```text
type
call_id
output
```

The `call_id` is the field that pairs the tool output with its originating function call.

Example without `id`:

```json
{
  "type": "function_call_output",
  "call_id": "call_123",
  "output": "{\"temperature\": \"72°F\", \"condition\": \"Sunny\"}"
}
```

---

# Tool Responses in Conversation

Tool calls and their results can be included in subsequent Responses API requests as part of the `input` sequence.

A typical flow is:

1. User sends a request.
2. Model returns a `function_call`.
3. Application executes the requested function.
4. Application sends a `function_call_output`.
5. The conversation continues with the tool result available as context.

Example:

```json
{
  "model": "openai/o4-mini",
  "input": [
    {
      "type": "message",
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "What is the weather in Boston?"
        }
      ]
    },
    {
      "type": "function_call",
      "id": "fc_1",
      "call_id": "call_123",
      "name": "get_weather",
      "arguments": "{\"location\": \"Boston, MA\"}"
    },
    {
      "type": "function_call_output",
      "id": "fc_output_1",
      "call_id": "call_123",
      "output": "{\"temperature\": \"72°F\", \"condition\": \"Sunny\"}"
    }
  ],
  "max_output_tokens": 9000
}
```

The tool output becomes part of the conversation context that the model can use to produce its next response.

---

# Multimodal Tool Outputs

`function_call_output.output` can contain either:

1. A string
2. An array of input content parts

The array form can contain:

* `input_text`
* `input_image`
* `input_file`

This allows tools to return more than plain text.

Example:

```json
{
  "type": "function_call_output",
  "call_id": "call_123",
  "output": [
    {
      "type": "input_text",
      "text": "{\"results\":[{\"title\":\"Golden Gate Bridge\"}]}"
    },
    {
      "type": "input_image",
      "image_url": "https://example.com/image.jpg"
    }
  ]
}
```

Non-text content such as images and files is only forwarded to models that support the corresponding multimodal input.

---

# Streaming Tool Calls

Tool calls can be monitored in real time by enabling streaming:

```json
{
  "stream": true
}
```

With streaming enabled, the Responses API emits Server-Sent Events (SSE).

Applications can inspect streamed events to detect tool calls and tool arguments as they become available.

Important event types include:

```text
response.output_item.added
response.function_call_arguments.done
```

A `response.output_item.added` event can indicate that a function-call output item has been added.

A `response.function_call_arguments.done` event indicates that the function-call arguments are complete.

Example event-handling logic:

```python
import requests
import json

response = requests.post(
    "https://openrouter.ai/api/v1/responses",
    headers={
        "Authorization": "Bearer YOUR_OPENROUTER_API_KEY",
        "Content-Type": "application/json",
    },
    json={
        "model": "openai/o4-mini",
        "input": [
            {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "What is the weather like in Tokyo, Japan? Please check the weather.",
                    }
                ],
            }
        ],
        "tools": [weather_tool],
        "tool_choice": "auto",
        "stream": True,
        "max_output_tokens": 9000,
    },
    stream=True,
)

for line in response.iter_lines():
    if not line:
        continue

    line_str = line.decode("utf-8")

    if line_str.startswith("data: "):
        data = line_str[6:]

        if data == "[DONE]":
            break

        try:
            parsed = json.loads(data)

            if (
                parsed.get("type") == "response.output_item.added"
                and parsed.get("item", {}).get("type") == "function_call"
            ):
                print(f"Function call: {parsed['item']['name']}")

            if parsed.get("type") == "response.function_call_arguments.done":
                print(
                    f"Arguments: {parsed.get('arguments', '')}"
                )

        except json.JSONDecodeError:
            continue
```

---

# Tool Call Validation

Applications should validate tool calls before executing functions.

A function call should contain the expected structure:

```json
{
  "type": "function_call",
  "id": "fc_abc123",
  "call_id": "call_xyz789",
  "name": "get_weather",
  "arguments": "{\"location\":\"Seattle, WA\"}"
}
```

Important fields include:

| Field       | Requirement                                                |
| ----------- | ---------------------------------------------------------- |
| `type`      | Must be `"function_call"`                                  |
| `id`        | Unique identifier for the function call object             |
| `call_id`   | Identifier used to associate the tool output with the call |
| `name`      | Should correspond to a defined tool                        |
| `arguments` | JSON string containing the function parameters             |

The application should parse and validate `arguments` before passing them to the actual tool implementation.

---

# Tool Calling Workflow

The overall tool-calling workflow is:

```text
User request
     |
     v
Responses API
     |
     v
Model decides whether a tool is needed
     |
     v
function_call
     |
     v
Application validates function name and arguments
     |
     v
Application executes the tool
     |
     v
function_call_output
     |
     v
Responses API
     |
     v
Model processes the tool result
     |
     v
Final response
```

For multiple independent tool requests, tools can be executed in parallel when appropriate.

---

# Tool Calling Best Practices

## 1. Use Clear Tool Descriptions

Provide detailed descriptions for:

* What the function does
* What each parameter means
* Expected parameter formats
* Important constraints

Clear descriptions help the model select and use the correct tool.

## 2. Use Valid JSON Schema

The `parameters` field should use a valid JSON Schema describing the expected function arguments.

Define:

* Parameter types
* Required parameters
* Allowed enum values
* Parameter descriptions
* Other applicable schema constraints

## 3. Validate Tool Calls Before Execution

Do not blindly execute a model-generated function call.

Validate:

* Tool name
* Argument structure
* Argument types
* Required parameters
* Application-specific authorization rules
* Any security or business constraints

## 4. Handle Tool Failures

Applications should handle situations where:

* A tool does not exist
* Arguments are invalid
* The tool fails
* The tool returns an error
* The model does not call a tool when one was expected

## 5. Use Parallel Execution When Appropriate

Independent tools can be designed for parallel execution when doing so improves performance.

Tools with dependencies on each other's results should instead be executed sequentially.

## 6. Preserve Conversation Context

Include function calls and their corresponding tool outputs in subsequent requests so that the model has the context required to continue the workflow.

## 7. Secure Tool Execution

Model-generated tool calls should be treated as **requests to perform an action**, not as authorization to perform that action.

Applications should enforce their own authorization, validation, and security policies before executing a tool.

---

# Key Concepts

| Concept                | Meaning                                                  |
| ---------------------- | -------------------------------------------------------- |
| Tool                   | An application-defined capability available to the model |
| Function tool          | A tool defined using the function-calling format         |
| `tools`                | Request field containing available tools                 |
| `tool_choice`          | Controls whether and which tool can be called            |
| `function_call`        | Model-generated request to execute a function            |
| `call_id`              | Identifier connecting a function call with its result    |
| `function_call_output` | Application-provided result of executing a function      |
| Parallel tool calls    | Multiple independent tool calls handled together         |
| Streaming tool calls   | Tool-call events delivered through SSE                   |
| Multimodal tool output | Tool output containing text, images, or files            |

---

# RAG Retrieval Keywords

OpenRouter tool calling, OpenRouter function calling, Responses API tools, OpenRouter Responses API tool calling, function_call, function_call_output, tool_choice, tool definition, tool schema, JSON Schema tools, automatic tool selection, force tool, disable tools, parallel tool calls, multiple tools, tool response, call_id, function arguments, multimodal tool output, input_image, input_file, streaming tool calls, SSE tool calls, response.output_item.added, response.function_call_arguments.done, tool validation, function execution, tool calling workflow.
