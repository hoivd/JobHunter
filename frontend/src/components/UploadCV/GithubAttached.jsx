import React, { useState } from "react";

const GithubAttached = () => {
  const [links, setLinks] = useState([]);
  const [newLink, setNewLink] = useState("");
  const [editIndex, setEditIndex] = useState(null);

  const handleAddOrUpdate = () => {
    if (!newLink.trim()) return;

    if (editIndex !== null) {
      // Update link
      const updatedLinks = [...links];
      updatedLinks[editIndex] = newLink.trim();
      setLinks(updatedLinks);
      setEditIndex(null);
    } else {
      // Add new link
      setLinks([...links, newLink.trim()]);
    }
    setNewLink("");
  };

  const handleEdit = (index) => {
    setNewLink(links[index]);
    setEditIndex(index);
  };

  const handleDelete = (index) => {
    const updatedLinks = links.filter((_, i) => i !== index);
    setLinks(updatedLinks);
    if (editIndex === index) {
      setEditIndex(null);
      setNewLink("");
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-semibold mb-4 text-[#19335a]">
        Attach Github Links
      </h1>

      {/* Input + Button */}
      <div className="flex gap-2 mb-4">
        <input
          type="url"
          placeholder="Paste link Github..."
          value={newLink}
          onChange={(e) => setNewLink(e.target.value)}
          onKeyDown={(e) => {
            e.key === "Enter" && handleAddOrUpdate();
          }}
          className="flex-1 px-3 py-2 border border-[#ccc] rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-0"
        />
        <button
          onClick={handleAddOrUpdate}
          className="px-4 py-2 bg-green-400 text-white rounded-lg hover:brightness-110 cursor-pointer font-semibold"
        >
          {editIndex !== null ? "Update" : "Add"}
        </button>
      </div>

      {/* Danh sách link */}
      <ul className="space-y-2">
        {links.map((link, idx) => (
          <li
            key={idx}
            className="flex justify-between items-center bg-gray-50 p-2 rounded"
          >
            <a
              href={link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              {link}
            </a>
            <div className="flex gap-2">
              <button
                onClick={() => handleEdit(idx)}
                className="px-3 py-1 text-sm bg-yellow-300 text-white rounded hover:bg-yellow-400 cursor-pointer"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(idx)}
                className="px-3 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600 cursor-pointer"
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default GithubAttached;
