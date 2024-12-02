import { Separator } from "@/components/ui/separator";
// import { UIState } from "@/lib/chat/actions";
import {
  Message,
  Session,
  TasksToComplete,
  USERS,
  TextResponse,
  Options,
  Citation,
} from "@/lib/types";
// import { Icon } from "lucide-react";
import Link from "next/link";
import { BotMessage, SpinnerMessage, UserMessage } from "./messages";
import TaskListContainer from "./TaskListContainer";
import OptionContainer from "./option-container";

export interface ChatList {
  messages: Message[];
  session?: Session;
  isShared: boolean;
  isLoading: boolean;
  tasksToComplete: { created_at: Date; tasks: [] }[];
  options: { options: string[]; created_at: Date }[];
  forms: { form: string; created_at: Date }[];
  responses: { response: string; created_at: Date }[];
  citations: Citation[];
}

export function ChatList({
  messages,
  session,
  isShared,
  isLoading,
  tasksToComplete,
  responses,
  options,
  citations,
}: ChatList) {
  if (!messages.length) {
    return null;
  }

  const mergedResponses = [
    ...messages,
    ...tasksToComplete,
    ...responses,
    ...options,
    ...citations,
  ];

  const sortedMergedResponses = mergedResponses.sort(
    (
      a: Message | TasksToComplete | TextResponse | Options | Citation,
      b: Message | TasksToComplete | TextResponse | Options | Citation
    ) =>
      new Date(a?.created_at as Date).getTime() -
      new Date(b?.created_at as Date).getTime()
  );

  console.log(sortedMergedResponses);

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
        (
          message:
            | Message
            | TasksToComplete
            | TextResponse
            | Options
            | Citation,
          index
        ) => (
          <div key={index}>
            {((message as Message)?.role === USERS.SYSTEM ||
              (message as Message)?.role === USERS.AI) && (
              <BotMessage content={(message as Message)?.content} />
            )}
            {(message as TextResponse)?.role === USERS.RESPONSE && (
              <BotMessage content={(message as TextResponse)?.response} />
            )}

            {(message as Options)?.options && (
              <OptionContainer options={(message as Options)?.options} />
            )}

            {(message as TasksToComplete)?.tasks && (
              <TaskListContainer
                tasks={(message as TasksToComplete).tasks}
                intent={""}
                goal={""}
              />
            )}

            {(message as Message)?.role === USERS.USER && (
              <UserMessage>{(message as Message)?.content}</UserMessage>
            )}

            {(message as Citation)?.citation && (
              <p className="text-sm text-muted-foreground mt-3">
                Source: {(message as Citation)?.citation}
              </p>
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
