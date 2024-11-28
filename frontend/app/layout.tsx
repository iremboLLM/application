import type { Metadata } from "next";
import localFont from "next/font/local";
import { ClerkProvider } from "@clerk/nextjs";
import "./globals.css";
import { TooltipProvider } from "@/components/ui/tooltip";
import { ReactQueryProvider } from "@/context/ReactQuery.context";
import { ChatContextProvider } from "@/context/Chat.context";
import { Toaster } from "@/components/ui/toaster";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "IremboLLM",
  description:
    "This is the IremboLLM chatbot, designed to assist users with questions about Irembo services and guide them through applying for various services available on the platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider signInUrl="/sign-in" signUpUrl="/sign-up">
      <html lang="en" suppressHydrationWarning>
        <body
          className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        >
          <ReactQueryProvider>
            <ChatContextProvider>
              <TooltipProvider>{children}</TooltipProvider>
              <Toaster />
            </ChatContextProvider>
          </ReactQueryProvider>
        </body>
      </html>
    </ClerkProvider>
  );
}
