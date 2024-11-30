module.exports = {
  apps: [
    {
      name: "irembo-frontend",
      script: "yarn",
      args: "start",
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
      ignore_watch: ["venv", "logs"], // Ignore unnecessary folders
    },
  ],
};
