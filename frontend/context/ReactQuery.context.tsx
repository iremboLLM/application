"use client";
import React, { createContext, useContext, useState } from "react";
import { QueryClient, QueryClientProvider } from "react-query";

// Create a context to provide the QueryClient
const ReactQueryContext = createContext<{
  queryClient: QueryClient | undefined;
}>({ queryClient: undefined });

export const ReactQueryProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  // Initialize QueryClient instance
  const [queryClient] = useState(() => new QueryClient());

  return (
    <ReactQueryContext.Provider value={{ queryClient }}>
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </ReactQueryContext.Provider>
  );
};

// Custom hook to use the QueryClient context
export const useReactQueryClient = () => {
  const context = useContext(ReactQueryContext);
  if (!context) {
    throw new Error(
      "useReactQueryClient must be used within a ReactQueryProvider"
    );
  }
  return context;
};
