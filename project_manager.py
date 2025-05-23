import uuid
from datetime import datetime, timezone

# In-memory storage for projects
# The key is the project_id (string UUID), and the value is the project dictionary.
_projects_db: dict[str, dict] = {}

def create_project(name: str, problem_statement: str) -> dict:
    """
    Creates a new project with a unique ID and stores it in memory.

    Args:
        name: The name of the project.
        problem_statement: A brief description of the project's problem statement.

    Returns:
        A dictionary representing the newly created project.
    """
    project_id = str(uuid.uuid4())  # Generate a unique string ID
    creation_date = datetime.now(timezone.utc) # Record creation date with timezone

    project = {
        "project_id": project_id,
        "name": name,
        "problem_statement": problem_statement,
        "creation_date": creation_date.isoformat(), # Store as ISO format string for consistency
    }
    _projects_db[project_id] = project
    return project

def get_project(project_id: str) -> dict | None:
    """
    Retrieves a specific project by its ID.

    Args:
        project_id: The unique ID of the project to retrieve.

    Returns:
        The project dictionary if found, otherwise None.
    """
    return _projects_db.get(project_id)

def list_projects() -> list[dict]:
    """
    Returns a list of all projects currently stored in memory.

    Returns:
        A list of project dictionaries.
    """
    return list(_projects_db.values())

# Example Usage (can be removed or commented out for production/import)
if __name__ == "__main__":
    print("Project Management System - In-Memory")

    # Create a couple of projects
    project1 = create_project(
        name="AI-Powered BA/SA Platform",
        problem_statement="To develop an AI assistant that helps Business and System Analysts."
    )
    print(f"\nCreated Project 1: {project1['name']} (ID: {project1['project_id']})")

    project2 = create_project(
        name="E-commerce Recommendation Engine",
        problem_statement="To build a system that suggests products to users based on their behavior."
    )
    print(f"Created Project 2: {project2['name']} (ID: {project2['project_id']})")

    # List all projects
    all_projects = list_projects()
    print("\nAll Projects:")
    for p in all_projects:
        print(f"- {p['name']} (Created: {p['creation_date']})")

    # Get a specific project
    retrieved_project = get_project(project1["project_id"])
    if retrieved_project:
        print(f"\nRetrieved Project by ID ({project1['project_id']}): {retrieved_project['name']}")
    else:
        print(f"\nCould not find project with ID: {project1['project_id']}")

    # Try to get a non-existent project
    non_existent_project = get_project("invalid-id")
    if non_existent_project:
        print(f"\nRetrieved Non-existent Project: {non_existent_project['name']}") # Should not happen
    else:
        print(f"\nAttempt to retrieve non-existent project (ID: invalid-id) correctly returned None.")

    # Show the internal database content
    # print("\nInternal DB state:")
    # for pid, pdata in _projects_db.items():
    #     print(f"{pid}: {pdata}")
