import json
from abc import ABC, abstractmethod


class BaseToolsManager(ABC):
    def __init__(self):
        # Lớp con phải hiện thực _build_tools và trả về dict {name: tool}
        self.tools = self._build_tools()

    @abstractmethod
    def _build_tools(self) -> dict:
        """Lớp con cần implement để trả về dict {tool_name: tool_object}."""
        pass

    def get_tools(self) -> dict:
        """Trả về dict tool {name: tool}."""
        return self.tools

    def get_tools_text(self) -> str:
        """Sinh chuỗi mô tả tools kèm input schema cho prompt."""
        tool_lines = []
        for name, t in self.tools.items():
            # Nếu là tool object của LangChain → có name & description
            if hasattr(t, "name") and hasattr(t, "description"):
                schema_text = ""
                if getattr(t, "args_schema", None):
                    schema_text = (
                        f"\n  Input schema: {json.dumps(t.args_schema.schema(), ensure_ascii=False, indent=2)}"
                    )
                tool_lines.append(f"- {t.name}: {t.description}{schema_text}")
            else:
                # Nếu chỉ là function → lấy docstring làm description
                desc = (t.__doc__ or "").strip()
                tool_lines.append(f"- {name}: {desc}")
        return "\n".join(tool_lines)
