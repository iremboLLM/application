import { ChatThread } from "../db";

export async function saveChat(
  thread_id: string,
  messages: { role: string; content: string }[],
  metadata = {}
) {
  const chatThread = await ChatThread.findOneAndUpdate(
    { thread_id },
    {
      $setOnInsert: { thread_id, created_at: new Date(), metadata },
      $push: { messages: { $each: messages } },
    },
    { upsert: true, new: true } // Insert new if not exists, return updated document
  );

  return chatThread;
}
