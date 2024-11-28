// import { UseChatHelpers } from "ai/react";

// import { ExternalLink } from "@/components/external-link";
// import { IconArrowRight } from "@/components/ui/icons";

export function EmptyScreen() {
  return (
    <div className="mx-auto max-w-2xl px-4">
      <div className="flex flex-col gap-2 rounded-lg border bg-background p-8">
        <h1 className="text-lg font-semibold">Welcome to IremboLLM Chatbot!</h1>
        <p className="leading-normal text-muted-foreground">
          This is the IremboLLM chatbot, designed to assist users with questions
          about Irembo services and guide them through applying for various
          services available on the platform.
        </p>
      </div>
    </div>
  );
}
