"use client";

import { Session } from "@/lib/types";
import { redirect } from "next/navigation";
import { Chat } from "./chat";
import { nanoid } from "@/lib/utils";

export function PageContent({ id }: { id: string }) {
  const user = { id: nanoid() };
  const session = { user: { id: user?.id as string } } as Session;

  if (!session?.user) {
    redirect(`/sign-in`);
  }

  const chat = {
    id,
    messages: [],
  };

  return (
    <Chat id={chat.id} session={session} initialMessages={chat.messages} />
  );
}
