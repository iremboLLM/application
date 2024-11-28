import { Separator } from "@/components/ui/separator";
// import { UIState } from "@/lib/chat/actions";
import { Message, Session, TasksToComplete, USERS } from "@/lib/types";
// import { Icon } from "lucide-react";
import Link from "next/link";
import { BotMessage, SpinnerMessage, UserMessage } from "./messages";
import TaskListContainer from "./TaskListContainer";

export interface ChatList {
  messages: Message[];
  session?: Session;
  isShared: boolean;
  isLoading: boolean;
  tasksToComplete: TasksToComplete[];
}

export function ChatList({
  messages,
  session,
  isShared,
  isLoading,
  tasksToComplete,
}: ChatList) {
  if (!messages.length) {
    return null;
  }

  const mergedResponses = [...messages, ...tasksToComplete];

  const sortedMergedResponses = mergedResponses.sort(
    (a: Message | TasksToComplete, b: Message | TasksToComplete) =>
      new Date(a?.created_at as Date).getTime() -
      new Date(b?.created_at as Date).getTime()
  );

  return (
    <div className="relative mx-auto max-w-2xl px-4">
      {!isShared && !session ? (
        <>
          <div className="group relative mb-4 flex items-start md:-ml-12">
            <div className="bg-background flex size-[25px] shrink-0 select-none items-center justify-center rounded-md border shadow-sm">
              {/* <Us /> */}
            </div>
            <div className="ml-4 flex-1 space-y-2 overflow-hidden px-1">
              <p className="text-muted-foreground leading-normal">
                Please{" "}
                <Link href="/login" className="underline">
                  log in
                </Link>{" "}
                or{" "}
                <Link href="/signup" className="underline">
                  sign up
                </Link>{" "}
                to save and revisit your chat history!
              </p>
            </div>
          </div>
          <Separator className="my-4" />
        </>
      ) : null}

      {sortedMergedResponses.map(
        (message: Message | TasksToComplete, index) => (
          <div key={index}>
            {((message as Message)?.role === USERS.SYSTEM ||
              (message as Message)?.role === USERS.AI) && (
              <BotMessage content={(message as Message)?.content}></BotMessage>
            )}

            {(message as Message)?.role === USERS.USER && (
              <UserMessage>{(message as Message)?.content}</UserMessage>
            )}

            {(message as TasksToComplete)?.tasks && (
              <TaskListContainer
                tasks={(message as TasksToComplete).tasks}
                intent={(message as TasksToComplete).intent}
                goal={(message as TasksToComplete).goal}
              />
            )}

            {index < messages.length - 1 && <Separator className="my-4" />}
          </div>
        )
      )}
      {isLoading && (
        <div className="mt-5">
          <SpinnerMessage />
        </div>
      )}
    </div>
  );
}
