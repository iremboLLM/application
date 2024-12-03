// src/context/ChatContext.tsx
"use client";

import { useLanguageModelApi } from "@/hooks/use-language-model-api";
import {
  Citation,
  Forms,
  Message,
  Options,
  TextResponse,
  USERS,
} from "@/lib/types";
import { nanoid } from "@/lib/utils";
import React, {
  createContext,
  useContext,
  useState,
  ReactNode,
  useCallback,
  useEffect,
} from "react";
import { useToast } from "@/hooks/use-toast";
import { useUser } from "@clerk/nextjs";

interface ChatContextType {
  messages: Message[];
  addMessage: (user: USERS, text: string, hidden?: boolean) => void;
  clearMessages: () => void;
  isLoading: boolean;
  tasksToComplete: { created_at: Date; tasks: [] }[];
  options: Options[];
  responses: { response: string; created_at: Date }[];
  forms: Forms[];
  citations: Citation[];
}

// Create the context with a default value (it can be undefined initially)
const ChatContext = createContext<ChatContextType | undefined>(undefined);

// Create the ChatContextProvider to manage chat state
export const ChatContextProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const { user } = useUser();
  const { toast } = useToast();
  const [messages, setMessages] = useState<Message[]>([]);
  const [tasksToComplete, setTasksToComplete] = useState<
    { created_at: Date; tasks: [] }[]
  >([]);
  const [options, setOptions] = useState<Options[]>([]);
  const [responses, setResponses] = useState<TextResponse[]>([]);
  const [citations, setCitations] = useState<Citation[]>([]);
  const [forms, setForms] = useState<Forms[]>([]);

  const { mutate, isLoading, isSuccess, data, error, isError } =
    useLanguageModelApi();

  useEffect(() => {
    if (isError) {
      toast({
        title: "Error occurred",
        description: "Something went wrong, please try again later",
        variant: "destructive",
      });
      console.error(error);
    }
  }, [isError, toast, error]);

  // Add a new message to the chat
  const addMessage = useCallback(
    (user: USERS, text: string, hidden: boolean = false) => {
      const newMessage: Message = {
        id: nanoid(),
        content: text,
        role: user,
        created_at: new Date(),
        hidden: hidden,
      };
      setMessages((prevMessages) => [...prevMessages, newMessage]);
    },
    []
  );

  useEffect(() => {
    if (messages.length > 0) {
      const message = messages[messages.length - 1];
      if (message.role === USERS.USER) {
        mutate({
          query: message.content,
          agent_mode: "assistant",
          thread_id: user?.id as string,
        });
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [messages]);

  useEffect(() => {
    if (isSuccess && data) {
      if (data.response) {
        setResponses([
          ...responses,
          {
            response: data.response,
            created_at: new Date(),
            role: USERS.RESPONSE,
          },
        ]);
      }

      if (data.form) {
        setForms([
          ...forms,
          { form: data.form, created_at: new Date(), role: USERS.FORM },
        ]);
      }

      if (data.tasks && data.tasks.length > 0) {
        setTasksToComplete([
          ...tasksToComplete,
          { tasks: data.tasks, created_at: new Date() },
        ]);
      }
      if (data.options) {
        setOptions([
          ...options,
          { options: data.options, created_at: new Date(), role: USERS.OPTION },
        ]);
      } else {
        addMessage(USERS.AI, data.text);
      }

      if (data.citation) {
        setCitations([
          ...citations,
          {
            citation: data.citation,
            created_at: new Date(),
            role: USERS.CITATION,
          },
        ]);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isSuccess, data, addMessage]);

  // Clear all messages from the chat
  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  return (
    <ChatContext.Provider
      value={{
        messages,
        addMessage,
        clearMessages,
        isLoading,
        tasksToComplete,
        options,
        responses,
        citations,
        forms,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

// Custom hook to use the chat context
export const useChatContext = (): ChatContextType => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error("useChatContext must be used within a ChatContextProvider");
  }
  return context;
};
