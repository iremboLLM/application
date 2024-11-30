module.exports = {
  apps: [
    {
      name: "irembo-frontend",
      script: "npm",
      args: "run start",
      cwd: "./frontend", // Set the working directory
      watch: true, // Enable watch mode
      ignore_watch: ["node_modules", "logs"], // Ignore unnecessary folders
    },
    {
      name: "irembo-backend",
      script: "./start-prod.sh",
      cwd: "./backend", // Set the working directory
      interpreter: "bash", // Use bash for the script
      watch: true, // Enable watch mode
      ignore_watch: [
        "venv",
        "logs",
        "chroma_langchain_db",
        "graph_representation.png",
      ], // Ignore unnecessary folders
    },
  ],
};
