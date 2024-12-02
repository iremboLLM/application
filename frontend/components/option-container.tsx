"use client";
import React from "react";
import { Button } from "./ui/button";
import { useChatContext } from "@/context/Chat.context";
import { USERS } from "@/lib/types";

const OptionContainer = ({ options }: { options: string[] }) => {
  const { addMessage } = useChatContext();
  return (
    <div className="flex items-center justify-start gap-5 mt-5">
      {options.map((option, index) => (
        <Button
          variant={"outline"}
          key={index}
          onClick={() => addMessage(USERS.USER, option)}
        >
          {option}
        </Button>
      ))}
    </div>
  );
};

export default OptionContainer;
