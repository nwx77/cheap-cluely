#!/usr/bin/env python3
"""
Demo script for Cluely AI Assistant
Shows how the assistant works without requiring full setup
"""

import time
import threading
from typing import Optional

def simulate_screen_capture() -> str:
    """Simulate screen capture with sample text"""
    sample_texts = [
        "Project Status Meeting - Q4 2024",
        "Agenda: Budget Review, Team Updates, Next Quarter Planning",
        "Current Budget: $150,000 allocated, $120,000 spent",
        "Team Performance: 85% of goals met",
        "Next Steps: Finalize Q1 2025 roadmap",
        "Action Items: Schedule follow-up meeting, Review proposals"
    ]
    return "\n".join(sample_texts)

def simulate_audio_transcript() -> str:
    """Simulate audio transcript with sample conversation"""
    sample_conversation = [
        "John: Welcome everyone to our Q4 status meeting.",
        "Sarah: Thanks John. I'll start with the budget review.",
        "Mike: The development team has completed 85% of our sprint goals.",
        "Lisa: Marketing campaigns are performing above expectations.",
        "John: Great work everyone. Any concerns about Q1 planning?",
        "Sarah: We need to finalize the budget allocation by next week."
    ]
    return " ".join(sample_conversation)

def simulate_gemini_response(context: str, query: str) -> str:
    """Simulate Gemini API response"""
    # Simple rule-based responses for demo
    query_lower = query.lower()
    
    if "budget" in query_lower:
        return "Based on the meeting context, the current budget status shows $150,000 allocated with $120,000 spent, leaving $30,000 remaining. The team needs to finalize Q1 2025 budget allocation by next week."
    
    elif "team" in query_lower or "performance" in query_lower:
        return "The development team has achieved 85% of sprint goals, and marketing campaigns are performing above expectations. Overall team performance is strong with 85% of goals met."
    
    elif "meeting" in query_lower or "agenda" in query_lower:
        return "This is a Q4 2024 Project Status Meeting. The agenda includes: Budget Review, Team Updates, and Next Quarter Planning. Key action items are to schedule a follow-up meeting and review proposals."
    
    elif "next" in query_lower or "planning" in query_lower:
        return "For next steps, the team needs to finalize the Q1 2025 roadmap and budget allocation by next week. A follow-up meeting should be scheduled to review proposals."
    
    else:
        return f"I can see this is a Q4 project status meeting. The team is discussing budget review, team updates, and Q1 planning. How can I help you with this meeting context?"

def demo_assistant():
    """Run a demo of the assistant"""
    print("🤖 Cluely AI Assistant - Demo Mode")
    print("=" * 50)
    print("This demo simulates how the assistant works in a real meeting.")
    print("Press Ctrl+C to exit\n")
    
    # Simulate context gathering
    print("📱 Capturing screen content...")
    screen_context = simulate_screen_capture()
    print("✅ Screen content captured")
    print(f"   Content: {screen_context[:100]}...")
    print()
    
    print("🎤 Capturing meeting audio...")
    audio_context = simulate_audio_transcript()
    print("✅ Audio transcript captured")
    print(f"   Transcript: {audio_context[:100]}...")
    print()
    
    # Demo queries
    demo_queries = [
        "What's the budget status?",
        "How is the team performing?",
        "What's on the meeting agenda?",
        "What are the next steps?",
        "Summarize this meeting"
    ]
    
    print("💬 Demo Queries:")
    print("-" * 30)
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{i}. User: {query}")
        print("   Assistant: ", end="")
        
        # Simulate processing time
        time.sleep(1)
        
        response = simulate_gemini_response(screen_context + " " + audio_context, query)
        print(response)
        
        if i < len(demo_queries):
            time.sleep(2)
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")
    print("\nIn the real assistant:")
    print("• Screen capture happens automatically every 2 seconds")
    print("• Audio recording and transcription runs continuously")
    print("• AI responses are generated using Google's Gemini API")
    print("• The overlay UI appears in the top-right corner")
    print("• Use Ctrl+Alt+C to toggle the overlay")
    print("\nTo try the real assistant:")
    print("1. Set your GEMINI_API_KEY environment variable")
    print("2. Run: python cluely_assistant.py")

def interactive_demo():
    """Interactive demo where user can ask questions"""
    print("🤖 Cluely AI Assistant - Interactive Demo")
    print("=" * 50)
    print("Ask questions about the simulated meeting context.")
    print("Type 'quit' to exit\n")
    
    # Simulate context
    screen_context = simulate_screen_capture()
    audio_context = simulate_audio_transcript()
    
    print("📱 Screen context loaded")
    print("🎤 Audio context loaded")
    print("💬 Ready for questions!\n")
    
    while True:
        try:
            query = input("You: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                break
            
            if not query:
                continue
            
            print("Assistant: ", end="")
            response = simulate_gemini_response(screen_context + " " + audio_context, query)
            print(response)
            print()
            
        except KeyboardInterrupt:
            break
    
    print("\n👋 Demo ended. Thanks for trying!")

def main():
    """Main demo function"""
    print("Choose demo mode:")
    print("1. Automatic demo (shows all features)")
    print("2. Interactive demo (ask your own questions)")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter choice (1-3): ").strip()
            
            if choice == "1":
                demo_assistant()
                break
            elif choice == "2":
                interactive_demo()
                break
            elif choice == "3":
                print("👋 Goodbye!")
                break
            else:
                print("Please enter 1, 2, or 3")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
