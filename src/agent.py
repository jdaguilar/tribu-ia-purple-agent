import os
from typing import List, Dict
from dotenv import load_dotenv
import litellm

from a2a.server.tasks import TaskUpdater
from a2a.types import Message, Part, TaskState, TextPart
from a2a.utils import get_message_text, new_agent_text_message

load_dotenv()

class Agent:
    def __init__(self, model: str = "openai/gpt-4o"):
        self.model = os.getenv("AGENT_LLM", model)
        self.messages: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": (
                    "You are an expert Python developer specialized in solving coding "
                    "tasks for benchmarks like BigCodeBench. Your goal is to provide "
                    "ONLY the Python code requested. Do not include any explanations, "
                    "markdown formatting, or conversational text.\n\n"
                    "Crucial: If the task specifies a function name, use exactly that name. "
                    "If you are asked to provide a solution as 'task_func', ensure your "
                    "main function is named 'task_func'."
                ),
            }
        ]

    async def run(self, message: Message, updater: TaskUpdater) -> None:
        input_text = get_message_text(message)

        await updater.update_status(
            TaskState.working, new_agent_text_message("Generating code...")
        )

        self.messages.append({"role": "user", "content": input_text})

        try:
            completion = litellm.completion(
                model=self.model,
                messages=self.messages,
                temperature=0.0,
            )
            assistant_content = completion.choices[0].message.content or ""
        except Exception as e:
            assistant_content = f"# Error generating code: {e}"

        self.messages.append({"role": "assistant", "content": assistant_content})

        # Return the code as an artifact (for history)
        await updater.add_artifact(
            parts=[Part(root=TextPart(text=assistant_content))],
            name="CodeSubmission",
        )

        # CRITICAL: Also return the code as the final status message so the Green Agent can read it
        await updater.update_status(
            TaskState.completed, new_agent_text_message(assistant_content)
        )
