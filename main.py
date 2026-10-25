"""Interactive Chapter 15 demonstration for Visual Studio 2026."""
from agent import OfficeSupportAgent
from knowledge_base import KnowledgeBase
from settings import MODEL_NAME


def read_lines(prompt):
    print(prompt)
    print("Type END on its own line to finish.")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def main():
    print("CHAPTER 15 - OFFICE AND CUSTOMER SUPPORT AI AGENT")
    print("Model:", MODEL_NAME)
    print("Fictional policies only; no emails are sent or tickets submitted.")
    print("Do not enter confidential or sensitive customer information.")
    try:
        knowledge = KnowledgeBase()
        agent = OfficeSupportAgent()
    except (OSError, ValueError) as exc:
        print("Startup failed:", exc)
        return

    while True:
        print("\n1. Draft an office email")
        print("2. Summarize an office note")
        print("3. Answer a customer support question")
        print("4. Classify a support ticket")
        print("5. View FAQ questions")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        try:
            if choice == "1":
                audience = input("Intended recipient/audience: ").strip()
                purpose = read_lines("Enter email purpose and details:")
                print("\nDRAFT - REVIEW BEFORE SENDING\n")
                print(agent.draft_email(audience, purpose))
            elif choice == "2":
                note = read_lines("Enter the office note:")
                print("\nSUMMARY\n", agent.summarize_note(note))
            elif choice == "3":
                question = input("Customer question: ").strip()
                answer, sources = agent.support_answer(question, knowledge)
                print("\nDRAFT SUPPORT ANSWER\n", answer)
                print("FAQ sources:", ", ".join(sources) if sources else "none")
            elif choice == "4":
                ticket = read_lines("Enter the ticket description:")
                result = agent.classify_ticket(ticket)
                print("Category:", result["category"])
                print("Priority:", result["priority"])
                print("Reason:", result["reason"])
                print("A person must review the classification.")
            elif choice == "5":
                for item in knowledge.entries:
                    print(f"{item['id']}: {item['question']}")
            else:
                print("Choose a number from 0 to 5.")
        except (ValueError, OSError, ConnectionError, TimeoutError) as exc:
            print("Operation failed:", exc)
        except Exception as exc:
            print("AI service error:", exc)


if __name__ == "__main__":
    main()
