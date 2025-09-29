class ToolManagerRegistry:
    def __init__(self, managers=None):
        """
        - managers: list các instance của BaseToolsManager
        """
        self.managers = managers or []

    def register_manager(self, manager):
        """Đăng ký thêm một tool manager."""
        self.managers.append(manager)

    def get_all_tools(self) -> dict:
        """Trả về toàn bộ tool từ tất cả manager dưới dạng dict {name: tool}."""
        tools = {}
        for m in self.managers:
            manager_tools = m.get_tools()  # dict {name: tool}
            tools.update(manager_tools)    # gộp dict
        return tools

    def get_all_tools_text(self):
        """Ghép toàn bộ tool text từ tất cả manager để show cho LLM."""
        parts = []
        for m in self.managers:
            parts.append(m.get_tools_text())
        return "\n".join(parts)

if __name__ == "__main__":
    from .git_tools import GitHubToolsManager
    from .ask_user_tools import AskUserToolsManager

    # Khởi tạo registry
    registry = ToolManagerRegistry()

    # Đăng ký các manager
    registry.register_manager(GitHubToolsManager())
    registry.register_manager(AskUserToolsManager())

    # Lấy danh sách tool
    all_tools = registry.get_all_tools()
    print(type(all_tools))
    print(all_tools)
    print("📦 Tổng số tool:", len(all_tools))

    # Lấy mô tả tools text
    print("\n📌 Tools text cho LLM:\n")
    print(registry.get_all_tools_text())