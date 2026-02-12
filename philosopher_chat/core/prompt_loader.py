from pathlib import Path

import yaml


class PromptLoader:
    PROMPTS_DIR = "data"
    PROMPT_FILE = "prompt_template.yaml"

    def _load_templates(self) -> dict[str, str]:
        prompt_path = Path(__file__).parent.parent / self.PROMPTS_DIR / self.PROMPT_FILE
        data = yaml.safe_load(prompt_path.read_text(encoding="utf-8"))
        return data["prompt"]

    def load_prompts(self, input_text: str, philosopher: str) -> dict[str, str]:
        template_config = self._load_templates()
        format_args = {"input_text": input_text, "philosopher": philosopher}
        template_config = template_config.format(**format_args)
        return template_config
