# Lightweight stub for activity logging (LangSmith-compatible)
def log_agent_event(agent_name: str, input_data, output_data):
    try:
        print(f'[LANGSMITH-STUB] {agent_name} -> input_len={len(str(input_data))} output_len={len(str(output_data))}')
    except Exception:
        pass
