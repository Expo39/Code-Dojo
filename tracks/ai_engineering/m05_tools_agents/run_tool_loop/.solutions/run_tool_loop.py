def run_tool_loop(model, tools, question, max_steps):
    if max_steps < 1:
        raise ValueError("max_steps must be at least 1")
    messages = [{"role": "user", "content": question}]
    for step in range(1, max_steps + 1):
        reply = model(messages)
        if "final" in reply:
            return {"answer": reply["final"], "steps": step, "stopped": "final", "messages": messages}
        name = reply["tool"]
        if name not in tools:
            content = f"error: unknown tool {name}"
        else:
            try:
                content = str(tools[name](**reply.get("args", {})))
            except Exception as error:
                content = f"error: {error}"
        messages.append({"role": "tool", "name": name, "content": content})
    return {"answer": None, "steps": max_steps, "stopped": "step limit", "messages": messages}
