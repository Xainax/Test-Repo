import os

# -----------------------------
# 1. INDIRECT TAINT THROUGH VARIABLES
# -----------------------------

def indirect_flow():
    user_input = input("cmd: ")

    # AST sees only variable assignments + os.system("x")
    # but DOES NOT know "cmd" is tainted
    cmd = user_input
    safe_cmd = cmd
    final_cmd = safe_cmd

    os.system(final_cmd)  # PyCFG must trace taint across multiple hops


# -----------------------------
# 2. TAINT THROUGH CONDITIONAL LOGIC
# -----------------------------

def conditional_flow(flag):
    user_input = input("data: ")

    result = "safe"

    if flag:
        result = user_input
    else:
        result = "echo safe"

    os.system(result)  # Only PyCFG knows which path is unsafe


# -----------------------------
# 3. LOOP-BASED PROPAGATION
# -----------------------------

def loop_propagation():
    user_input = input("cmd: ")

    cmd = "echo safe"

    for i in range(3):
        # overwrites safe value with tainted value in loop
        if i == 2:
            cmd = user_input

    os.system(cmd)  # requires CFG + loop reasoning


# -----------------------------
# 4. FUNCTION-LEVEL PROPAGATION (INTERPROCEDURAL)
# -----------------------------

def sink(x):
    os.system(x)


def caller():
    user_input = input("cmd: ")

    transformed = helper(user_input)
    sink(transformed)


def helper(x):
    return x + ""  # identity propagation (no obvious danger)


# -----------------------------
# 5. OBSCURED TAINT VIA DATA STRUCTURES
# -----------------------------

def list_flow():
    user_input = input("cmd: ")

    data = ["safe1", "safe2"]
    data.append(user_input)

    cmd = data[2]

    os.system(cmd)  # AST cannot resolve indexing flow


# -----------------------------
# 6. REASSIGNMENT OBSCURITY
# -----------------------------

def reassignment_flow():
    user_input = input("cmd: ")

    cmd = "safe"
    cmd = cmd + ""  # still looks safe transformation
    cmd = user_input  # final overwrite hidden in flow

    os.system(cmd)  # requires full CFG tracking


# -----------------------------
# 7. BRANCH MERGING FLOW (PATH DEPENDENT)
# -----------------------------

def merge_flow(flag):
    user_input = input("cmd: ")

    a = "safe"
    b = "safe"

    if flag:
        a = user_input
    else:
        b = "echo safe"

    cmd = a if flag else b

    os.system(cmd)  # AST cannot resolve path dependency


# -----------------------------
# 8. “LOOKS SAFE” BUT IS NOT
# -----------------------------

def fake_safe_wrapper():
    user_input = input("cmd: ")

    def wrapper(x):
        return x  # no visible danger

    cmd = wrapper(user_input)

    os.system(cmd)  # PyCFG needed to connect wrapper → sink
