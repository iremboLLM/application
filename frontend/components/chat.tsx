"use client";

import { cn } from "@/lib/utils";
import { ChatList } from "@/components/chat-list";
import { ChatPanel } from "@/components/chat-panel";
import { EmptyScreen } from "@/components/empty-screen";
import { useLocalStorage } from "@/hooks/use-local-storage";
import { useEffect, useState } from "react";
import { Message, Session } from "@/lib/types";
import { usePathname } from "next/navigation";
import { useScrollAnchor } from "@/hooks/use-scroll-anchor";
import { useChatContext } from "@/context/Chat.context";

export interface ChatProps extends React.ComponentProps<"div"> {
  initialMessages?: Message[];
  id?: string;
  session?: Session;
}

export function Chat({ id, className, session }: ChatProps) {
  //   const router = useRouter();
  const path = usePathname();
  const [input, setInput] = useState("");
  const {
    messages,
    isLoading,
    tasksToComplete,
    options,
    forms,
    responses,
    citations,
  } = useChatContext();

  const [chatId, setNewChatId] = useLocalStorage("newChatId", id);

  console.log(chatId);

  useEffect(() => {
    if (session?.user) {
      if (!path.includes("chat") && messages.length === 1) {
        window.history.replaceState({}, "", `/chat/${id}`);
      }
    }
  }, [id, path, session?.user, messages]);

  useEffect(() => {
    setNewChatId(id);
  });

  const { isAtBottom, scrollToBottom } = useScrollAnchor();

  return (
    <div className="group w-full overflow-auto pl-0 peer-[[data-state=open]]:lg:pl-[250px] peer-[[data-state=open]]:xl:pl-[300px]">
      <div className={cn("pb-[200px] pt-4 md:pt-10", className)}>
        {messages.length ? (
          <ChatList
            isLoading={isLoading}
            messages={messages}
            isShared={false}
            session={session}
            tasksToComplete={tasksToComplete}
            options={options}
            responses={responses}
            forms={forms}
            citations={citations}
          />
        ) : (
          <EmptyScreen />
        )}
        <div className="w-full h-px" />
      </div>
      <ChatPanel
        id={id}
        input={input}
        setInput={setInput}
        isAtBottom={isAtBottom}
        scrollToBottom={scrollToBottom}
      />
    </div>
  );
}
