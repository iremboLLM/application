import mongoose, { Schema, Model } from "mongoose";

const { DB_URL } = process.env;

if (!DB_URL) {
  throw new Error("DB_URL environment variable is not defined");
}

// Define the database connection function with serverless optimization
if (!global.mongoose) {
  global.mongoose = { conn: null, promise: null };
}

export async function connectDB() {
  if (global.mongoose.conn) {
    return global.mongoose.conn;
  }

  if (!global.mongoose.promise) {
    global.mongoose.promise = mongoose
      .connect(DB_URL as string, {})
      .then((mongoose) => mongoose.connection); // Return the connection object
  }

  global.mongoose.conn = await global.mongoose.promise;
  return global.mongoose.conn;
}

// Define the message schema
const messageSchema = new Schema(
  {
    role: { type: String, enum: ["Human", "AI"], required: true }, // Role of the message sender
    content: { type: String, required: true }, // Message content
    timestamp: { type: Date, default: Date.now }, // Timestamp for when the message was sent
  },
  { _id: false } // No need for a separate _id for each message
);

// Define the chat thread schema
const chatThreadSchema = new Schema(
  {
    thread_id: { type: String, unique: true, required: true }, // Unique ID for the chat thread
    messages: [messageSchema], // Array of messages
    created_at: { type: Date, default: Date.now }, // Timestamp for thread creation
    metadata: { type: Object, default: {} }, // Optional metadata for the thread
  },
  { timestamps: true } // Adds createdAt and updatedAt fields automatically
);

// Create the ChatThread model
const ChatThread: Model<Document> =
  mongoose.models.ChatThread || mongoose.model("ChatThread", chatThreadSchema);

connectDB();

export { ChatThread };
