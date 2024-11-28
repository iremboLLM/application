"use client";
import { nanoid } from "@/lib/utils";
import { Chat } from "@/components/chat";
import { Session } from "@/lib/types";

export default function IndexPage() {
  const id = nanoid();
  const user = { id: nanoid() };
  const session = { user: { id: user?.id as string } } as Session;

  return <Chat id={id} session={session} />;
}
