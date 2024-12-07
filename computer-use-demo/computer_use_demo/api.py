from fastapi import FastAPI, Request
from typing import Any, Dict
import httpx
import uvicorn
from typing import cast
from computer_use_demo.loop import sampling_loop, APIProvider
from computer_use_demo.tools import ToolResult

app = FastAPI()

@app.post("/run_sampling_loop")
async def run_sampling_loop(request: Request) -> Dict[str, Any]:
    # Parse the incoming JSON request
    data = await request.json()
    messages = data.get("messages", [{"role": "user", "content": "Hello"}])
    
    # Convert provider string to the corresponding APIProvider enum member
    model = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    system_prompt_suffix = data.get("system_prompt_suffix", "")
    only_n_most_recent_images = data.get("only_n_most_recent_images", 3)

    def _output_callback(message):
        print('_output_callback:\n\nmessage: ', message)

    def _tool_output_callback(
        tool_output: ToolResult, tool_id: str,
    ):
        print(f" _tool_output_callback:\n\ntool_id: {tool_id}\n\ntool_output: {tool_output}")

    def _api_response_callback(
        request: httpx.Request,
        response: httpx.Response | object | None,
        error: Exception | None,
    ):
        print(f"_api_response_callback")

    # Run the sampling loop
    updated_messages = await sampling_loop(
        system_prompt_suffix=system_prompt_suffix,
        model=model,
        provider=cast(APIProvider, APIProvider.BEDROCK),
        messages=messages,
        output_callback=_output_callback,
        tool_output_callback=_tool_output_callback,
        api_response_callback=_api_response_callback,
        api_key="", # only used with Anthropic provider
        only_n_most_recent_images=only_n_most_recent_images,
    )

    # Return the updated messages as a JSON response
    return {"messages": updated_messages}


@app.get("/ping")
async def ping() -> Dict[str, str]:
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run(app="api:app", host="0.0.0.0", reload=True)