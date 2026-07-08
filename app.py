import streamlit as st

from pawpal_system import Owner, Pet, Priority, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet-care planning assistant. Add pets and tasks, then generate a daily plan.")

# --- Application memory -------------------------------------------------------
# Streamlit reruns this whole script on every interaction, so we keep a single
# Owner object alive in st.session_state instead of recreating it each time.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
owner = st.session_state.owner

# --- Owner --------------------------------------------------------------------
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

# --- Add a pet ----------------------------------------------------------------
st.subheader("Add a Pet")
with st.form("add_pet", clear_on_submit=True):
    new_pet_name = st.text_input("Pet name", value="Mochi")
    new_species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        owner.add_pet(Pet(name=new_pet_name, species=new_species))
        st.success(f"Added {new_pet_name} the {new_species}!")

if not owner.pets:
    st.info("Add a pet to get started.")
    st.stop()

st.divider()

# --- Add a task ---------------------------------------------------------------
st.subheader("Add a Task")
with st.form("add_task", clear_on_submit=True):
    target_pet = st.selectbox("For which pet?", [pet.name for pet in owner.pets])
    task_title = st.text_input("Task", value="Morning walk")
    col1, col2 = st.columns(2)
    with col1:
        task_time = st.text_input("Time (HH:MM)", value="08:00")
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col2:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    if st.form_submit_button("Add task"):
        pet = next(pet for pet in owner.pets if pet.name == target_pet)
        pet.add_task(
            Task(
                task_title,
                int(duration),
                frequency,
                Priority[priority.upper()],
                time=task_time,
            )
        )
        st.success(f"Added '{task_title}' for {target_pet}!")

# --- Current tasks ------------------------------------------------------------
st.markdown("### Current tasks")
for pet in owner.pets:
    st.write(f"**{pet.name}** ({pet.species}) — {len(pet.tasks)} task(s)")
    if pet.tasks:
        st.table(
            [
                {
                    "time": task.time,
                    "task": task.description,
                    "min": task.duration_minutes,
                    "priority": task.priority.name.lower(),
                    "frequency": task.frequency,
                    "done": task.completed,
                }
                for task in pet.tasks
            ]
        )

st.divider()

# --- Build schedule -----------------------------------------------------------
st.subheader("Build Schedule")
budget = st.number_input("Available time (minutes)", min_value=10, max_value=600, value=60)

if st.button("Generate schedule"):
    scheduler = Scheduler(int(budget))
    scheduler.schedule_for_owner(owner)
    st.code(scheduler.explain_plan())

    conflicts = scheduler.detect_conflicts(owner.all_tasks())
    for warning in conflicts:
        st.warning(warning)
