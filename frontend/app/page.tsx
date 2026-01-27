"use client";

import { useEffect, useState } from "react";

interface Item {
  id: number;
  name: string;
  created_at: string;
}

export default function Home() {
  const [items, setItems] = useState<Item[]>([]);
  const [newItem, setNewItem] = useState("");
  const [loading, setLoading] = useState(true);

  const fetchItems = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/items");
      const data = await res.json();
      setItems(data);
    } catch (error) {
      console.error("Failed to fetch items:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const addItem = async () => {
    if (!newItem.trim()) return;
    try {
      await fetch("http://localhost:8000/api/items", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newItem }),
      });
      setNewItem("");
      fetchItems();
    } catch (error) {
      console.error("Failed to add item:", error);
    }
  };

  const deleteItem = async (id: number) => {
    try {
      await fetch(`http://localhost:8000/api/items/${id}`, {
        method: "DELETE",
      });
      fetchItems();
    } catch (error) {
      console.error("Failed to delete item:", error);
    }
  };

  return (
    <main style={{ padding: "2rem", fontFamily: "system-ui", maxWidth: "600px", margin: "0 auto" }}>
      <h1>SynnovatorZero</h1>
      <p style={{ color: "#666" }}>FastAPI + SQLite + Next.js</p>

      <div style={{ marginTop: "2rem" }}>
        <input
          type="text"
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && addItem()}
          placeholder="Add new item..."
          style={{ padding: "0.5rem", width: "70%", marginRight: "0.5rem" }}
        />
        <button onClick={addItem} style={{ padding: "0.5rem 1rem" }}>
          Add
        </button>
      </div>

      <div style={{ marginTop: "2rem" }}>
        {loading ? (
          <p>Loading...</p>
        ) : items.length === 0 ? (
          <p style={{ color: "#999" }}>No items yet. Add one above!</p>
        ) : (
          <ul style={{ listStyle: "none", padding: 0 }}>
            {items.map((item) => (
              <li
                key={item.id}
                style={{
                  padding: "0.75rem",
                  borderBottom: "1px solid #eee",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                <span>{item.name}</span>
                <button
                  onClick={() => deleteItem(item.id)}
                  style={{ color: "red", background: "none", border: "none", cursor: "pointer" }}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div style={{ marginTop: "3rem", color: "#999", fontSize: "0.875rem" }}>
        <p>Frontend: http://localhost:3000</p>
        <p>Backend: http://localhost:8000</p>
        <p>API Docs: http://localhost:8000/docs</p>
      </div>
    </main>
  );
}
