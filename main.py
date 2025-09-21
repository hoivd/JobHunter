from agent.conversation.agent import ConversationalAgent
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def main():
    agent = ConversationalAgent()
    print("🤖 Agent sẵn sàng! Bạn có thể chat, gõ 'cảm ơn' hay 'muốn dừng' để kết thúc.\n")
    
    while True:
        query = input("Bạn:")
        response = agent.chat(query)
        print(f"🤖 Agent: {response}\n")

if __name__ == "__main__":
    main()