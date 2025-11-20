# PostgreSQL Transaction ID (XID) Wraparound Simulator

This project is an educational tool designed to visualize the **PostgreSQL Transaction ID (XID) Wraparound** problem and demonstrate the critical importance of the **Vacuum Freeze** mechanism.

Built with Python and Matplotlib, this simulation models the PostgreSQL 32-bit transaction ID cycle as a radar (polar) chart, visually explaining MVCC (Multiversion Concurrency Control) visibility rules and how data loss occurs when the transaction counter wraps around without freezing.

## 🚀 Features

* **Circular XID Visualization:** Models the 4 Billion XID space on a polar coordinate system.
* **Visibility Window:** Dynamically shows the "Visible Past" versus the "Future/Invisible" transaction space.
* **Data Loss Simulation:** Demonstrates how old tuples (rows) disappear from view (wraparound failure) if not properly vacuumed.
* **Vacuum Freeze Mechanism:** Simulates the `VACUUM FREEZE` process, showing how tuples are marked as "frozen" to ensure permanent data safety.

## Installation

You need **Python 3** and the following libraries to run this simulation.
    ```bash
    pip install matplotlib numpy
    ```

## Visual Legend

| Element | Color | Description |
| :--- | :--- | :--- |
| **Rotating Line** | 🔴 Red | **Current XID:** The database's current time. |
| **Background** | 🟢 Green | **Visible Past:** The valid visibility window. |
| **Dot** | 🟢 Green | **Safe Tuple:** A normal row within safe window. |
| **Dot** | 🔴 Red | **Data Loss:** A tuple outside visibility window. |
| **Dot** | 🔵 Blue | **Frozen Tuple:** Permanently safe tuple. |
