"use client";
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
  Forms,
} from "@/lib/types";
// import { Icon } from "lucide-react";
import Link from "next/link";
import { BotMessage, SpinnerMessage, UserMessage } from "./messages";
import TaskListContainer from "./TaskListContainer";
import OptionContainer from "./option-container";
import DynamicForm from "./dynamic-form";
import { Loader2, ThumbsDown, ThumbsUp } from "lucide-react";
import { supabase } from "@/app/supabaseClient";
import { toast } from "@/hooks/use-toast";
import { useState } from "react";

export interface ChatList {
  messages: Message[];
  session?: Session;
  isShared: boolean;
  isLoading: boolean;
  tasksToComplete: { created_at: Date; tasks: [] }[];
  options: { options: string[]; created_at: Date }[];
  responses: { response: string; created_at: Date }[];
  citations: Citation[];
  forms: Forms[];
}

// const formData: DynamicFormData = JSON.parse(`{
//   "title": "User Feedback Form",
//   "fields": [
//     {
//       "label": "Full Name",
//       "type": "text",
//       "placeholder": "Enter your full name",
//       "required": true
//     },
//     {
//       "label": "Email Address",
//       "type": "email",
//       "placeholder": "Enter your email address",
//       "required": true
//     },
//     {
//       "label": "Phone Number",
//       "type": "tel",
//       "placeholder": "Enter your phone number",
//       "required": false
//     },
//     {
//       "label": "Feedback",
//       "type": "textarea",
//       "placeholder": "Enter your feedback",
//       "required": true
//     },
//     {
//       "label": "Would you recommend us?",
//       "type": "radio",
//       "placeholder": "",
//       "required": true,
//       "options": ["Yes", "No"]
//     },
//     {
//       "label": "Preferred Contact Method",
//       "type": "select",
//       "placeholder": "Choose an option",
//       "required": false,
//       "options": ["Email", "Phone", "Text"]
//     }
//   ]
// }`);

export function ChatList({
  messages,
  session,
  isShared,
  isLoading,
  tasksToComplete,
  responses,
  options,
  citations,
  forms,
}: ChatList) {
  const [isLoadingReaction, setIsLoading] = useState<boolean>(false);
  if (!messages.length) {
    return null;
  }

  const mergedResponses = [
    ...messages,
    ...tasksToComplete,
    ...responses,
    ...options,
    ...citations,
    ...forms,
  ];

  const sortedMergedResponses = mergedResponses.sort(
    (
      a: Message | TasksToComplete | TextResponse | Options | Citation | Forms,
      b: Message | TasksToComplete | TextResponse | Options | Citation | Forms
    ) =>
      new Date(a?.created_at as Date).getTime() -
      new Date(b?.created_at as Date).getTime()
  );

  const handleChatReaction = async (status: "like" | "dislike") => {
    if (isLoadingReaction) {
      return;
    }
    try {
      setIsLoading(true);
      const data = {
        conversation: JSON.stringify({ message: sortedMergedResponses }),
        status,
      };
      await supabase.from("reactions").insert(data);
      toast({
        title: "Success",
        description: "Your reaction has been recorded successfully",
        variant: "default",
      });
    } catch (error: unknown) {
      console.log(error);
      toast({
        title: "Error",
        description: "Failed to record your reaction",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

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
            | Citation
            | Forms,
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

            {(message as Forms)?.role === USERS.FORM && (
              <DynamicForm formData={JSON.parse((message as Forms)?.form)} />
            )}

            {(message as TasksToComplete)?.tasks && (
              <TaskListContainer
                tasks={(message as TasksToComplete).tasks}
                intent={""}
                goal={""}
              />
            )}

            {(message as Message)?.role === USERS.USER &&
              (message as Message).hidden === false && (
                <UserMessage>{(message as Message)?.content}</UserMessage>
              )}

            {(message as Citation)?.citation && (
              <p className="text-sm text-muted-foreground mt-1">
                Source: {(message as Citation)?.citation}
              </p>
            )}

            {index < messages.length - 1 && <Separator className="my-4" />}
          </div>
        )
      )}
      <div className="flex justify-start items-center gap-5 mt-5">
        <ThumbsUp
          className="cursor-pointer h-4 w-4"
          onClick={() => {
            handleChatReaction("like");
          }}
        />
        <ThumbsDown
          className="cursor-pointer h-4 w-4"
          onClick={() => {
            handleChatReaction("dislike");
          }}
        />

        {isLoadingReaction && <Loader2 className="animate-spin h-4 w-4" />}
      </div>
      {isLoading && (
        <div className="mt-5">
          <SpinnerMessage />
        </div>
      )}
    </div>
  );
}
