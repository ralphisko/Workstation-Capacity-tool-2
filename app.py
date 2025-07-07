import streamlit as st

# Workstation process times (in minutes)
process_times = {
    "NP3": {"picking": 15, "assembly": 35, "inspection": 15},
    "C3": {"picking": 18, "assembly": 35, "inspection": 15},
    "C4": {"picking": 18, "assembly": 35, "inspection": 15},
    "TC-L": {"picking": 18, "assembly": 35, "inspection": 15},
    "DP3": {"picking": 20, "assembly": 40, "inspection": 15},
    "E410": {"picking": 15, "assembly": 35, "inspection": 15},
}

transformer_times = {"picking": 5, "assembly": 15, "inspection": 5}
transformer_required = ["NP3", "DP3", "C3", "C4"]

effective_hours = 6.5
picker_efficiency = 0.60

st.title("📊 Workstation Capacity Planner")

st.header("🛠 Production Plan")
plan = {}
for ws in process_times:
    plan[ws] = st.number_input(f"Units of {ws}", min_value=0, value=0)

st.header("👷‍♂️ Available Operators")
people = {
    "pickers": st.number_input("Workstation Pickers", min_value=0, value=3),
    "assemblers": st.number_input("Workstation Assemblers", min_value=0, value=4),
    "inspectors": st.number_input("Workstation Inspectors", min_value=0, value=2),
    "transformer_operators": st.number_input("Transformer Operators", min_value=0, value=2),
    "transformer_inspectors": st.number_input("Transformer Inspectors/Testers", min_value=0, value=1),
}

def calculate_total_minutes(plan):
    totals = {
        "picking": 0,
        "assembly": 0,
        "inspection": 0,
        "transformer_picking": 0,
        "transformer_assembly": 0,
        "transformer_inspection": 0,
    }

    for ws_type, qty in plan.items():
        if ws_type not in process_times:
            continue
        ws = process_times[ws_type]
        totals["picking"] += ws["picking"] * qty
        totals["assembly"] += ws["assembly"] * qty
        totals["inspection"] += ws["inspection"] * qty

        if ws_type in transformer_required:
            totals["transformer_picking"] += transformer_times["picking"] * qty
            totals["transformer_assembly"] += transformer_times["assembly"] * qty
            totals["transformer_inspection"] += transformer_times["inspection"] * qty

    return totals

def calculate_capacity(people):
    return {
        "picking": people.get("pickers", 0) * effective_hours * 60 * picker_efficiency,
        "assembly": people.get("assemblers", 0) * effective_hours * 60,
        "inspection": people.get("inspectors", 0) * effective_hours * 60,
        "transformer_picking": people.get("transformer_operators", 0) * effective_hours * 60,
        "transformer_assembly": people.get("transformer_operators", 0) * effective_hours * 60,
        "transformer_inspection": people.get("transformer_inspectors", 0) * effective_hours * 60,
    }

def evaluate_plan(plan, people):
    totals = calculate_total_minutes(plan)
    capacity = calculate_capacity(people)
    utilisation = {
        k: (totals[k] / capacity[k] * 100) if capacity[k] > 0 else 0 for k in totals
    }
    return utilisation, totals, capacity

if st.button("Calculate Utilisation"):
    utilisation, totals, capacity = evaluate_plan(plan, people)

    st.subheader("📦 Required Time (minutes)")
    st.write(totals)

    st.subheader("📈 Available Capacity (minutes)")
    st.write(capacity)

    st.subheader("📊 Utilisation (%)")
    for k, v in utilisation.items():
        color = "🟢"
        if v > 100:
            color = "🔴"
        elif v > 80:
            color = "🟠"
        st.write(f"{k}: {v:.1f}% {color}")
