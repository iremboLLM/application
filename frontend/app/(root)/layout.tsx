import { UserButton } from "@clerk/nextjs";
import React from "react";
// import Sidebar from "@/components/Sidebar"; // Assuming Sidebar is in the same folder

export default function ChatLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="">
      {/* <Sidebar tasksToComplete={tasksToComplete.tasks} /> */}
      <div className="flex items-center justify-end px-10 py-4">
        <UserButton />
      </div>
      <div className="chat-content">{children}</div>
    </div>
  );
}
