from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from utils.tools import TOOLS
from utils.state import State
from utils.nodes import assistant

def create_agent():
    """Create and compile the agent executor"""
    # Create the graph
    graph = StateGraph(State)
    graph.add_node("assistant", assistant)
    graph.add_node("tools", ToolNode(TOOLS))
    
    # Set up the flow
    graph.set_entry_point("assistant")
    graph.add_conditional_edges("assistant", tools_condition)
    graph.add_edge("tools", "assistant")
    
    # Compile with memory
    memory = MemorySaver()
    agent_executor = graph.compile(checkpointer=memory)
    
    return agent_executor

def run_agent(agent_executor, user_input: str, thread_id: str = "default"):
    """Run the agent with user input"""
    try:
        config = {"configurable": {"thread_id": thread_id}}
        result = agent_executor.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config
        )
        return result["messages"][-1].content
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}. Please try asking your question again."

# if __name__ == "__main__":
#     print("Medical Assistant for Community Health Center Harichandanpur")
#     print("Ask me about hospital policies, procedures, visiting hours, or any medical questions!")
#     print("Type 'quit' to exit\n")
   
#     # Create the agent
#     agent_executor = create_agent()
#     thread_id = "main_conversation"
   
#     while True:
#         try:
#             user_input = input("You: ")
#             if user_input.lower() in ['quit', 'exit', 'bye']:
#                 print("Thank you for using our medical assistant. Take care!")
#                 break
           
#             if user_input.strip():
#                 response = run_agent(agent_executor, user_input, thread_id)
#                 print(f"\nAssistant: {response}\n")
#             else:
#                 print("Please enter a question or type 'quit' to exit.\n")
               
#         except KeyboardInterrupt:
#             print("\nGoodbye!")
#             break
#         except Exception as e:
#             print(f"An error occurred: {e}\n")