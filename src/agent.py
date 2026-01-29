import os

from dotenv import load_dotenv
import litellm

from a2a.server.tasks import TaskUpdater
from a2a.types import Message, Part, TaskState, TextPart
from a2a.utils import get_message_text, new_agent_text_message


load_dotenv()


SYSTEM_PROMPT = (
    "You are an expert Python developer. Your task is to solve the provided coding problem. "
    "Return ONLY the complete Python code, including any necessary imports. "
    "Do not include explanations, markdown formatting, or triple backticks unless specifically asked."
)


class Agent:
    def __init__(self):
        self.model = os.getenv("AGENT_LLM", "openai/gpt-4o")
        self.messages: list[dict[str, object]] = [{"role": "system", "content": SYSTEM_PROMPT}]

    async def run(self, message: Message, updater: TaskUpdater) -> None:
        input_text = get_message_text(message)

        await updater.update_status(TaskState.working, new_agent_text_message("Generating code..."))

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

        await updater.add_artifact(
            parts=[Part(root=TextPart(text=assistant_content))],
            name="CodeSubmission",
        )
